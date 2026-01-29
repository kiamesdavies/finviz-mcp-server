# Finviz MCP Server - Test Suite

This directory contains a comprehensive test suite for the Finviz MCP Server. It covers all 22 MCP tool functions and provides tests for parameter combinations, error handling, and integration behavior.

## Test File Structure

### 1. `test_e2e_screeners.py`
**End-to-end (E2E) tests**
- Tests all 22 MCP tool functions
- Verifies baseline behavior
- Tests basic parameters for each screener

**Tools covered:**
- Earnings Screeners (4 types)
- Volume & Trend Screeners (4 types)
- Fundamental Data Tools (2 types)
- News Functions (3 types)
- Market Analysis Tools (5 types)
- Technical Analysis Tools (4 types)

### 2. `test_parameter_combinations.py`
**Parameter combination tests**
- Systematically tests many parameter combinations
- Boundary value tests
- Performance tests with large datasets
- Comprehensive sector combination coverage

**Key test cases:**
- Price range combinations (min price, max price)
- Volume filter combinations
- Market cap × sector combinations
- Composite technical indicator conditions
- Tests with large ticker lists

### 3. `test_error_handling.py`
**Error handling and edge case tests**
- Input validation tests
- Network error handling
- Data validation and sanitization
- Concurrency and performance
- Resource management

**Error scenarios:**
- Invalid ticker formats
- Invalid parameter values
- Network connection errors
- HTTP errors (400, 401, 403, 404, 429, 500, 503)
- Rate limit errors
- Invalid response formats

### 4. `test_mcp_integration.py`
**MCP integration tests**
- MCP protocol compliance tests
- Server initialization tests
- Tool registration and metadata validation
- Data serialization
- Concurrency tests

**Integration checks:**
- Verify all tools are registered
- Parameter validation integration
- Response format validation
- Special characters and Unicode handling
- Large payload serialization

### 5. `test_comprehensive_parameters.py`
**Comprehensive parameter tests**
- Tests every parameter value from the Finviz docs
- Exhaustive checks for exchanges, indices, countries, sectors, and industries
- Detailed categories for market cap, price ranges, and dividend yields
- All options for date parameters and analyst recommendations
- Custom ranges (frange) and modal parameters
- Technical analysis parameters (RSI, moving averages, performance)

### 6. `test_financial_parameters.py`
**Financial parameter tests**
- Detailed tests for P/E, PEG, P/B, D/E ratios
- ROE, ROA, margins (gross, operating, net)
- Ownership structure (insider, institutional, float)
- Short interest and options availability
- Target price deviation range tests

## Usage

### 1. Run basic tests

```bash
# Run all tests
python run_tests.py all

# Run specific test categories
python run_tests.py e2e           # E2E tests
python run_tests.py params        # Parameter combination tests
python run_tests.py errors        # Error handling tests
python run_tests.py integration   # MCP integration tests
python run_tests.py comprehensive # Comprehensive parameter tests
python run_tests.py financial     # Financial parameter tests

# Smoke tests (quick verification)
python run_tests.py smoke

# Performance tests
python run_tests.py performance
```

### 2. Use pytest directly

```bash
# Run all tests
pytest tests/ -v

# Run specific test files
pytest tests/test_e2e_screeners.py -v
pytest tests/test_parameter_combinations.py -v
pytest tests/test_error_handling.py -v
pytest tests/test_mcp_integration.py -v
pytest tests/test_comprehensive_parameters.py -v
pytest tests/test_financial_parameters.py -v

# Run a specific test class/method
pytest tests/test_e2e_screeners.py::TestFinvizScreenersE2E::test_earnings_screener_basic -v

# Show detailed tracebacks on failure
pytest tests/ -v --tb=long

# Stop on first failure
pytest tests/ -x
```

### 3. Tests with coverage

```bash
# Run tests with coverage report
python run_tests.py coverage

# Or run pytest directly
pytest tests/ --cov=src --cov-report=html --cov-report=term
```

### 4. Parallel execution

```bash
# Parallel execution (pytest-xdist)
pytest tests/ -n auto

# Parallel execution with 4 processes
pytest tests/ -n 4
```

## Test Environment Setup

### 1. Install dependencies

```bash
# Install development dependencies
pip install -e .[dev]

# Or install individually
pip install pytest pytest-asyncio pytest-cov
```

### 2. Set environment variables

```bash
# Environment variables for tests (optional)
export FINVIZ_API_KEY=your_test_api_key
export LOG_LEVEL=DEBUG
export RATE_LIMIT_REQUESTS_PER_MINUTE=50
```

## Test Data and Mocks

### Mock data structure

All tests use mock data without connecting to the real Finviz server:

```python
mock_stock_data = {
    "ticker": "AAPL",
    "company": "Apple Inc.",
    "sector": "Technology",
    "industry": "Consumer Electronics",
    "price": 150.0,
    "volume": 50000000,
    "market_cap": 2400000000000,
    "pe_ratio": 25.5,
    "eps": 6.0,
    "dividend_yield": 0.5,
}
```

### Test patterns

1. **Happy path tests**: Verify expected behavior with valid inputs
2. **Error path tests**: Verify error handling with invalid inputs
3. **Boundary tests**: Verify behavior at min/max values
4. **Combination tests**: Verify behavior for parameter combinations

## CI/CD Integration
