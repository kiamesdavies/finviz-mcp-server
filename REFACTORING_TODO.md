# Finviz MCP Server Refactoring TODO

## 📋 Overview

This document outlines a comprehensive refactoring plan for Finviz MCP Server. The current codebase is functionally strong, but it needs a phased improvement plan to enhance maintainability, extensibility, and testability.

**Codebase size**: ~9,729 lines (source) + 4,149 lines (tests) + 8,155 lines (docs)

---

## 🚨 High Priority Issues

### 1. **Split the giant method**
**File**: `src/finviz_client/base.py`
**Target**: `_convert_filters_to_finviz` method (500+ lines)

#### Problem
- A single method handles all filter types (price, volume, P/E, RSI, etc.)
- Very high complexity and difficult to test
- Large impact when adding new filters

#### Solution
```python
# Split the current giant method into smaller parts:
class FinvizFilterBuilder:
    def _convert_price_filters(self, filters: Dict) -> str:
        """Convert price-related filters."""
        pass
    
    def _convert_volume_filters(self, filters: Dict) -> str:
        """Convert volume-related filters."""
        pass
    
    def _convert_financial_ratio_filters(self, filters: Dict) -> str:
        """Convert financial ratio filters (P/E, P/B, P/S, etc.)."""
        pass
    
    def _convert_technical_filters(self, filters: Dict) -> str:
        """Convert technical indicator filters (RSI, SMA, etc.)."""
        pass
    
    def _convert_sector_filters(self, filters: Dict) -> str:
        """Convert sector/industry filters."""
        pass
    
    def _convert_earnings_filters(self, filters: Dict) -> str:
        """Convert earnings-related filters."""
        pass
```

#### Tasks
- [ ] Design and implement the FilterBuilder class
- [ ] Split the existing method
- [ ] Add unit tests
- [ ] Verify existing functionality

---

### 2. **Eliminate duplicated code**
**File**: `src/finviz_client/base.py`
**Target**: Duplicate range filter logic

#### Problem
- The same pattern repeats for price, volume, P/E, dividend yield, etc. (~200 lines of duplication)
- Small logic differences can introduce bugs

#### Solution
```python
def _build_range_filter(self, 
                       filter_prefix: str, 
                       min_val: Optional[Union[int, float, str]], 
                       max_val: Optional[Union[int, float, str]],
                       safe_conversion_func: Callable) -> str:
    """
    Shared range filter construction logic.

    Args:
        filter_prefix: Filter prefix (e.g., 'sh_price_', 'fa_pe_')
        min_val: Minimum value
        max_val: Maximum value
        safe_conversion_func: Value conversion function

    Returns:
        Finviz-formatted filter string
    """
    if min_val is None and max_val is None:
        return ""

    min_converted = safe_conversion_func(min_val) if min_val is not None else None
    max_converted = safe_conversion_func(max_val) if max_val is not None else None

    # Handle Finviz preset format
    if min_converted and min_converted.startswith(('o', 'u')):
        return f'{filter_prefix}{min_converted},'
    elif max_converted and max_converted.startswith(('o', 'u')):
        return f'{filter_prefix}{max_converted},'

    # Handle range format
    if min_converted and max_converted:
        return f'{filter_prefix}{min_converted}to{max_converted},'
    elif min_converted:
        return f'{filter_prefix}{min_converted}to,'
    elif max_converted:
        return f'{filter_prefix}to{max_converted},'

    return ""
```

#### Tasks
- [ ] Implement shared range filter method
- [ ] Apply to each filter type
- [ ] Run regression tests
- [ ] Confirm code reduction (target: -200 lines)

---

### 3. **Centralize hardcoded settings**
**Files**: Scattered across multiple files
**Target**: Hardcoded Finviz parameters

#### Problem
- URL parameters, column indexes, etc. are hardcoded in multiple places
- Large blast radius for configuration changes
- Difficult to adapt to Finviz API changes

#### Solution
```python
# src/config/finviz_config.py
class FinvizConfig:
    """Centralized Finviz API configuration."""

    # API basics
    BASE_URL = "https://elite.finviz.com"
    EXPORT_URL = f"{BASE_URL}/export.ashx"
    QUOTE_EXPORT_URL = f"{BASE_URL}/quote_export.ashx"
    NEWS_EXPORT_URL = f"{BASE_URL}/news_export.ashx"

    # Default parameters
    DEFAULT_VIEW = '151'  # View that includes earnings data
    DEFAULT_SORT = '-ticker'

    # Column indexes by use case
    BASIC_COLUMNS = "0,1,2,3,4,5,6,7,8,9,10"
    EARNINGS_COLUMNS = "0,1,2,79,3,4,5,129,6,7,8,9,10,11,12,13"
    ALL_COLUMNS = "0,1,2,79,3,4,5,129,6,7,8,9,10,11,12,13,73,74,75,14..."

    # Rate limiting
    RATE_LIMIT_DELAY = 1.0
    MAX_RETRIES = 3
    REQUEST_TIMEOUT = 30

    # Batch size limits
    MAX_RESULTS_PER_REQUEST = 1000
    BATCH_SIZE = 5
```

#### Tasks
- [ ] Create config class
- [ ] Identify and migrate hardcoded values
- [ ] Add environment variable support
- [ ] Support dynamic config loading

---

## 🔶 Medium Priority Issues

### 4. **Separate class responsibilities**
**File**: `src/finviz_client/base.py`
**Target**: Overgrown `FinvizClient` class

#### Problem
- One class handles HTTP, CSV parsing, data conversion, and filter conversion
- Violates the single-responsibility principle
- Hard to mock during tests

#### Solution
```python
# src/finviz_client/http_client.py
class FinvizHttpClient:
    """HTTP-only client."""
    def __init__(self, api_key: Optional[str] = None):
        pass

    def fetch_csv(self, params: Dict) -> requests.Response:
        """Fetch CSV data."""
        pass

    def fetch_with_retry(self, url: str, params: Dict) -> requests.Response:
        """HTTP request with retries."""
        pass

# src/finviz_client/data_parser.py
class FinvizDataParser:
    """Data parsing helper."""
    def parse_csv_to_stocks(self, csv_content: str) -> List[StockData]:
        """Convert CSV to StockData list."""
        pass

    def parse_single_stock(self, row: pd.Series) -> StockData:
        """Convert a single row to StockData."""
        pass

# src/finviz_client/filter_builder.py
class FinvizFilterBuilder:
    """Filter construction helper."""
    def build_filters(self, filters: Dict) -> Dict[str, str]:
        """Convert internal filters to Finviz parameters."""
        pass
```

#### Tasks
- [ ] Design responsibility separation
- [ ] Implement new classes
- [ ] Refactor existing code
- [ ] Normalize interfaces
- [ ] Add dependency injection

---

### 5. **Standardize error handling**
**File**: `src/server.py`
**Target**: Exception handling in each tool method

#### Problem
- 20+ tool methods duplicate the same error-handling pattern
- Inconsistent error messages
- Logging is not standardized

#### Solution
```python
# src/utils/decorators.py
def finviz_tool_error_handler(log_context: str = ""):
    """Error-handling decorator for Finviz tools."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                logger.info(f"Starting {func.__name__} {log_context}")
                result = func(*args, **kwargs)
                logger.info(f"Completed {func.__name__} successfully")
                return result
            except ValueError as e:
                error_msg = f"Validation error in {func.__name__}: {str(e)}"
                logger.error(error_msg)
                return [TextContent(type="text", text=f"Error: {str(e)}")]
            except Exception as e:
                error_msg = f"Unexpected error in {func.__name__}: {str(e)}"
                logger.error(error_msg, exc_info=True)
                return [TextContent(type="text", text=f"Error: {str(e)}")]
        return wrapper
    return decorator

# Example usage
@server.tool()
@finviz_tool_error_handler("earnings screening")
def earnings_screener(earnings_date: str, ...) -> List[TextContent]:
    # Focus on validation and business logic only
    pass
```

#### Tasks
- [ ] Implement error-handling decorator
- [ ] Apply to all tool methods
- [ ] Standardize log levels
- [ ] Create error message templates

---

### 6. **Improve type safety**
**Files**: Multiple
**Target**: Overuse of `Optional[Union[int, float, str]]`

#### Problem
- Excessive Union usage weakens type checking
- IDE assistance is limited
- Increased runtime error risk

#### Solution
```python
# src/types/finviz_types.py
from typing import Union, Literal, NewType
from dataclasses import dataclass

# More specific type definitions
FinvizPresetValue = Literal['o5', 'o10', 'o50', 'u5', 'u10', 'u50']
NumericValue = Union[int, float]
PriceValue = Union[NumericValue, FinvizPresetValue]
VolumeValue = Union[NumericValue, FinvizPresetValue, str]  # Range input supported

# Custom types
TickerSymbol = NewType('TickerSymbol', str)
FinvizFilter = NewType('FinvizFilter', str)

@dataclass
class PriceRange:
    """Type-safe representation of a price range."""
    min_price: Optional[PriceValue] = None
    max_price: Optional[PriceValue] = None

    def __post_init__(self):
        # Validation logic
        pass

@dataclass
class VolumeRange:
    """Type-safe representation of a volume range."""
    min_volume: Optional[VolumeValue] = None
    max_volume: Optional[VolumeValue] = None
```

#### Tasks
- [ ] Define custom types
- [ ] Gradually migrate existing code
- [ ] Integrate validation
- [ ] Adopt type checking tools

---

### 7. **Unify duplicate CSV parsing implementations**
**File**: `src/finviz_client/base.py`
**Target**: `get_stock_fundamentals` and `get_multiple_stocks_fundamentals`

#### Problem
- Duplicate CSV → StockData conversion logic
- ~300 lines of duplicated code
- Reduced maintainability

#### Solution
```python
# src/finviz_client/csv_processor.py
class FinvizCSVProcessor:
    """Unified CSV processing class."""

    def __init__(self, field_mapping: Dict[str, str]):
        self.field_mapping = field_mapping

    def process_csv_response(self, 
                           csv_content: str, 
                           data_fields: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Unified CSV response handling."""
        df = pd.read_csv(StringIO(csv_content))
        return [self._process_row(row, data_fields) for _, row in df.iterrows()]

    def _process_row(self, row: pd.Series, data_fields: Optional[List[str]]) -> Dict[str, Any]:
        """Process a single row."""
        result = {}
        for col in row.index:
            if pd.notna(row[col]) and row[col] != '-':
                field_name = self._normalize_field_name(col)
                converted_value = self._convert_field_value(col, row[col])
                result[field_name] = converted_value

        if data_fields:
            return self._filter_fields(result, data_fields)
        return result
```

#### Tasks
- [ ] Implement CSV processor class
- [ ] Refactor existing methods
- [ ] Standardize field mapping
- [ ] Run performance tests

---

## 🔷 Low Priority Issues

### 8. **Unify naming conventions**
**Files**: Multiple
**Target**: Mixed Japanese/English naming

#### Problem
- Some comments and method names include Japanese
- Incomplete internationalization

#### Solution
- Standardize on English or adopt a multilingual pattern
- Internationalize docstrings

#### Tasks
- [ ] Create naming guidelines
- [ ] Gradual renaming
- [ ] Evaluate multilingual support

---

### 9. **Improve settings management**
**Files**: Multiple
**Target**: Scattered environment variable usage

#### Problem
- API key retrieval is duplicated in multiple places
- Configuration is not centralized

#### Solution
```python
# src/config/settings.py
class Settings:
    """Centralized application settings."""

    def __init__(self):
        self.api_key = self._get_api_key()
        self.rate_limit = self._get_rate_limit()
        self.log_level = self._get_log_level()

    def _get_api_key(self) -> Optional[str]:
        return os.getenv('FINVIZ_API_KEY')

    @lru_cache()
    def get_instance() -> 'Settings':
        return Settings()
```

#### Tasks
- [ ] Implement settings manager class
- [ ] Standardize environment variables
- [ ] Add settings validation

---

### 10. **Increase test coverage**
**Files**: `tests/`
**Target**: Tests for complex filter logic

#### Problem
- `_convert_filters_to_finviz` has too many branches to test easily
- Edge cases are under-tested

#### Solution
- Unit tests for small methods after refactoring
- Automated parameter combination tests

#### Tasks
- [ ] Measure test coverage
- [ ] Identify missing test cases
- [ ] Evaluate automated test generation

---

## 📅 Implementation Schedule

### Phase 1: Foundation (2-3 weeks)
1. **Week 1**: Implement settings management and FilterBuilder
2. **Week 2**: Implement shared range filter method
3. **Week 3**: Standardize error handling

### Phase 2: Architecture Improvements (2-3 weeks)
1. **Week 4-5**: Separate class responsibilities
2. **Week 6**: Unify CSV parsing

### Phase 3: Quality Improvements (1-2 weeks)
1. **Week 7**: Improve type safety
2. **Week 8**: Increase test coverage

### Phase 4: Final polish (1 week)
1. **Week 9**: Unify naming and documentation

---

## 🎯 Expected Outcomes

### Better maintainability
- **Method complexity**: 500 lines → under 50 lines
- **Code duplication**: remove ~200 lines
- **Time to add new features**: 50% reduction

### Better testability
- **Unit test coverage**: 70% → 90%
- **Integration test efficiency**: 3x faster via mocking
- **Bug detection time**: 80% reduction due to earlier detection

### Better readability
- **New developer ramp-up time**: 50% reduction
- **Code review time**: 30% reduction
- **Documentation maintenance effort**: 40% reduction

### Better extensibility
- **Add new filters**: more efficient via standardization
- **API change handling**: localized impact scope
- **New data sources**: easier to add via loose coupling

---

## 📊 Progress Tracking

### Checklist
- [ ] Phase 1: Foundation complete
- [ ] Phase 2: Architecture improvements complete
- [ ] Phase 3: Quality improvements complete
- [ ] Phase 4: Final polish complete

### Success metrics
- [ ] 90% test coverage achieved
- [ ] 50% code complexity reduction
- [ ] 50% reduction in time to add new features
- [ ] 80% reduction in bug reports

---

## 🤝 Contribution Guidelines

If you participate in this refactoring, follow these principles:

1. **Incremental changes**: Avoid large changes at once; accumulate small improvements
2. **Backward compatibility**: Preserve existing API interfaces as much as possible
3. **Test-driven**: Run tests before and after refactoring to verify correctness
4. **Documentation updates**: Update docs alongside code changes

---

*This document will be updated as work progresses. Check the latest version before starting.*

## 📝 Changelog

- **2025-01-01**: Initial draft
- **Author**: Claude Code Assistant
- **Review**: Not yet performed
