import re
from typing import Optional, List, Any, Dict, Union
from ..constants import ALL_PARAMETERS, SUBTHEME_VALUES

def validate_ticker(ticker: str) -> bool:
    """
    Validate a ticker symbol.

    Args:
        ticker: Ticker symbol

    Returns:
        True if the ticker is valid
    """
    if not ticker or not isinstance(ticker, str):
        return False
    
    # Basic pattern check (1-5 letters)
    pattern = r'^[A-Z]{1,5}$'
    return bool(re.match(pattern, ticker.upper()))

def validate_tickers(tickers: str) -> bool:
    """
    Validate multiple ticker symbols.

    Args:
        tickers: Comma-separated ticker symbols

    Returns:
        True if all tickers are valid
    """
    if not tickers or not isinstance(tickers, str):
        return False
    
    # Split by comma and validate each ticker
    ticker_list = [t.strip() for t in tickers.split(',') if t.strip()]
    
    if not ticker_list:
        return False
    
    # Check all tickers
    return all(validate_ticker(ticker) for ticker in ticker_list)

def parse_tickers(tickers: str) -> List[str]:
    """
    Convert comma-separated ticker string to a list.

    Args:
        tickers: Comma-separated ticker symbols

    Returns:
        List of ticker symbols
    """
    if not tickers or not isinstance(tickers, str):
        return []
    
    # Split by comma, trim whitespace, and uppercase
    return [t.strip().upper() for t in tickers.split(',') if t.strip()]

def validate_price_range(min_price: Optional[Union[int, float, str]], max_price: Optional[Union[int, float, str]]) -> bool:
    """
    Validate a price range.

    Args:
        min_price: Minimum price (number or Finviz preset like 'o5', 'u10')
        max_price: Maximum price (number or Finviz preset like 'o5', 'u10')

    Returns:
        True if the price range is valid
    """
    def _convert_to_float(value):
        """Convert price value to float (supports Finviz format)."""
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            # Finviz preset format (e.g., 'o5', 'u10')
            if value.startswith(('o', 'u')):
                try:
                    return float(value[1:])
                except ValueError:
                    return None
            # Numeric string
            try:
                return float(value)
            except ValueError:
                return None
        return None
    
    min_val = _convert_to_float(min_price)
    max_val = _convert_to_float(max_price)
    
    if min_val is not None and min_val < 0:
        return False
    
    if max_val is not None and max_val < 0:
        return False
    
    if min_val is not None and max_val is not None:
        return min_val <= max_val
    
    return True

def validate_market_cap(market_cap: str) -> bool:
    """
    Validate a market cap filter.

    Args:
        market_cap: Market cap filter

    Returns:
        True if the market cap filter is valid
    """
    return market_cap in ALL_PARAMETERS['cap']

def validate_earnings_date(earnings_date: str) -> bool:
    """
    Validate an earnings date filter.

    Args:
        earnings_date: Earnings date filter

    Returns:
        True if the earnings date filter is valid
    """
    # Valid earnings date values at API level
    valid_api_values = {
        'today_after',
        'today_before', 
        'tomorrow_after',
        'tomorrow_before',
        'yesterday_after',
        'yesterday_before',
        'this_week',
        'next_week',
        'within_2_weeks',
        'thisweek',
        'nextweek',
        'nextdays5'
    }
    
    return earnings_date in valid_api_values

def validate_subtheme(subtheme: str) -> bool:
    """
    Validate a subtheme filter value.

    Args:
        subtheme: Subtheme name (e.g., 'aicloud', 'semismemory')

    Returns:
        True if the subtheme is valid
    """
    if not subtheme or not isinstance(subtheme, str):
        return False
    return subtheme.lower() in SUBTHEME_VALUES


def validate_sector(sector: str) -> bool:
    """
    Validate a sector name.

    Args:
        sector: Sector name

    Returns:
        True if the sector name is valid
    """
    # Valid sector names at API level
    valid_api_sectors = {
        # User-friendly sector names
        'Basic Materials',
        'Communication Services', 
        'Consumer Cyclical',
        'Consumer Defensive',
        'Energy',
        'Financial',
        'Healthcare',
        'Industrials',
        'Real Estate',
        'Technology',
        'Utilities',
        # Also accept internal parameter values
        'basicmaterials',
        'communicationservices',
        'consumercyclical', 
        'consumerdefensive',
        'energy',
        'financial',
        'healthcare',
        'industrials',
        'realestate',
        'technology',
        'utilities'
    }
    
    return sector in valid_api_sectors

def validate_percentage(value: float, min_val: float = -100, max_val: float = 1000) -> bool:
    """
    Validate a percentage value.

    Args:
        value: Percentage value
        min_val: Minimum value
        max_val: Maximum value

    Returns:
        True if the percentage is valid
    """
    return min_val <= value <= max_val

def validate_volume(volume: Union[int, float, str]) -> bool:
    """
    Validate volume (supports numeric and Finviz string formats).

    Args:
        volume: Volume (number or Finviz format: o100, u500, 500to2000, etc.)

    Returns:
        True if volume is valid
    """
    if isinstance(volume, (int, float)):
        return volume >= 0
    
    if isinstance(volume, str):
        # Also check numeric strings (int and float)
        try:
            return float(volume) >= 0
        except ValueError:
            pass  # If not numeric, continue to Finviz format check
            
        # Validate Finviz average volume format
        
        # Under/Over patterns (fixed values)
        fixed_patterns = {
            # Under patterns
            'u50', 'u100', 'u500', 'u750', 'u1000',
            # Over patterns  
            'o50', 'o100', 'o200', 'o300', 'o400', 'o500', 'o750', 'o1000', 'o2000',
            # Legacy range patterns (backward compatibility)
            '100to500', '100to1000', '500to1000', '500to10000',
            # Custom
            'frange'
        }
        
        if volume in fixed_patterns:
            return True
        
        # Validate custom range pattern (number to number)
        # Examples: 500to2000, 100to500, 1000to5000
        import re
        range_pattern = r'^\d+to\d*$'
        if re.match(range_pattern, volume):
            return True
        
        return False
    
    return False

def validate_screening_params(params: Dict[str, Any]) -> List[str]:
    """
    Validate screening parameters (full version).

    Args:
        params: Screening parameters

    Returns:
        List of error messages (empty means valid)
    """
    errors = []
    
    # Validate basic parameters
    basic_params = {
        'exchange': 'exch',
        'index': 'idx', 
        'sector': 'sec',
        'industry': 'ind',
        'country': 'geo',
        'market_cap': 'cap',
        'price': 'sh_price',
        'target_price': 'targetprice',
        'dividend_yield': 'fa_div',
        'short_float': 'sh_short',
        'analyst_recommendation': 'an_recom',
        'option_short': 'sh_opt',
        'earnings_date': 'earningsdate',
        'ipo_date': 'ipodate',
        'average_volume': 'sh_avgvol',
        'relative_volume': 'sh_relvol',
        'current_volume': 'sh_curvol',
        'trades': 'sh_trades',
        'shares_outstanding': 'sh_outstanding',
        'float': 'sh_float'
    }
    
    for param_name, param_key in basic_params.items():
        if param_name in params and params[param_name] is not None:
            if params[param_name] not in ALL_PARAMETERS[param_key]:
                errors.append(f"Invalid {param_name}: {params[param_name]}")
    
    # Price range check
    min_price = params.get('min_price')
    max_price = params.get('max_price')
    if not validate_price_range(min_price, max_price):
        errors.append("Invalid price range")
    
    # Numeric range checks
    numeric_range_params = [
        'pe_min', 'pe_max', 'forward_pe_min', 'forward_pe_max',
        'peg_min', 'peg_max', 'ps_min', 'ps_max', 'pb_min', 'pb_max',
        'debt_equity_min', 'debt_equity_max', 'roe_min', 'roe_max',
        'roi_min', 'roi_max', 'roa_min', 'roa_max',
        'gross_margin_min', 'gross_margin_max',
        'operating_margin_min', 'operating_margin_max',
        'net_margin_min', 'net_margin_max',
        'rsi_min', 'rsi_max', 'beta_min', 'beta_max',
        'dividend_yield_min', 'dividend_yield_max',
        'volume_min', 'avg_volume_min', 'relative_volume_min',
        'price_change_min', 'price_change_max',
        'performance_week_min', 'performance_month_min',
        'performance_quarter_min', 'performance_halfyear_min',
        'performance_year_min', 'performance_ytd_min',
        'volatility_week_min', 'volatility_month_min',
        'week52_high_distance_min', 'week52_low_distance_min',
        'eps_growth_this_year_min', 'eps_growth_next_year_min',
        'eps_growth_past_5_years_min', 'eps_growth_next_5_years_min',
        'sales_growth_quarter_min', 'sales_growth_past_5_years_min',
        'insider_ownership_min', 'insider_ownership_max',
        'institutional_ownership_min', 'institutional_ownership_max'
    ]
    
    for param in numeric_range_params:
        if param in params and params[param] is not None:
            if not isinstance(params[param], (int, float)):
                errors.append(f"Invalid {param}: must be numeric")
    
    # Multiple sector check
    if 'sectors' in params and params['sectors']:
        for sector in params['sectors']:
            if not validate_sector(sector):
                errors.append(f"Invalid sector: {sector}")
    
    # Excluded sector check
    if 'exclude_sectors' in params and params['exclude_sectors']:
        for sector in params['exclude_sectors']:
            if not validate_sector(sector):
                errors.append(f"Invalid exclude_sector: {sector}")
    
    # SMA filter check
    if 'sma_filter' in params and params['sma_filter'] is not None:
        valid_sma_filters = ['above_sma20', 'above_sma50', 'above_sma200', 
                            'below_sma20', 'below_sma50', 'below_sma200', 'none']
        if params['sma_filter'] not in valid_sma_filters:
            errors.append(f"Invalid sma_filter: {params['sma_filter']}")
    
    # Sort-by check
    if 'sort_by' in params and params['sort_by'] is not None:
        valid_sort_options = [
            'ticker', 'company', 'sector', 'industry', 'country',
            'market_cap', 'pe', 'price', 'change', 'volume',
            'price_change', 'relative_volume', 'performance_week',
            'performance_month', 'performance_quarter', 'performance_year',
            'analyst_recom', 'avg_volume', 'dividend_yield',
            'eps', 'sales', 'float', 'insider_own', 'inst_own',
            'rsi', 'volatility', 'earnings_date', 'ipo_date'
        ]
        if params['sort_by'] not in valid_sort_options:
            errors.append(f"Invalid sort_by: {params['sort_by']}")
    
    # Sort order check
    if 'sort_order' in params and params['sort_order'] is not None:
        if params['sort_order'] not in ['asc', 'desc']:
            errors.append(f"Invalid sort_order: {params['sort_order']}")
    
    # Max results check
    if 'max_results' in params and params['max_results'] is not None:
        max_results = params['max_results']
        if not isinstance(max_results, int) or max_results <= 0 or max_results > 10000:
            errors.append(f"Invalid max_results: {max_results} (must be 1-10000)")
    
    # View check
    if 'view' in params and params['view'] is not None:
        valid_views = ['111', '121', '131', '141', '151', '161', '171']
        if params['view'] not in valid_views:
            errors.append(f"Invalid view: {params['view']}")
    
    return errors

def validate_data_fields(fields: List[str]) -> List[str]:
    """
    Validate data fields (full version).

    Args:
        fields: List of data fields

    Returns:
        List of invalid fields
    """
    # Load valid fields dynamically from FINVIZ_COMPREHENSIVE_FIELD_MAPPING in constants.py
    try:
        from ..constants import FINVIZ_COMPREHENSIVE_FIELD_MAPPING
    except ImportError:
        # When running directly
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        from constants import FINVIZ_COMPREHENSIVE_FIELD_MAPPING
    
    valid_fields = set(FINVIZ_COMPREHENSIVE_FIELD_MAPPING.keys())
    
    # Additional valid fields (for backward compatibility)
    additional_valid_fields = {
        # Alternative names for fields reported as errors
        'eps_growth_this_y', 'eps_growth_next_y', 'eps_growth_next_5y',
        'eps_growth_past_5y', 'sales_growth_qtr', 'eps_growth_qtr', 
        'sales_growth_qoq', 'performance_1w', 'performance_1m',
        'recommendation', 'analyst_recommendation',
        'insider_own', 'institutional_own', 'insider_ownership', 'institutional_ownership',
        
        # Correct alternatives for invalid field names reported in errors
        'roi',  # Alternative for roic (Return on Invested Capital)
        'debt_equity',  # Alternative for debt_to_equity
        'book_value',  # Alternative for book_value_per_share
        'performance_week',  # Alternative for performance_1w
        'performance_month',  # Alternative for performance_1m
        'short_float',  # Alternative for float_short
        
        # Other alternative field names
        'profit_margin',  # Alias for profit_margin
        'all',  # Special key for all fields
        
        # Actual Finviz field names (104 fields)
        '200_day_simple_moving_average', '20_day_simple_moving_average', '50_day_high', 
        '50_day_low', '50_day_simple_moving_average', '52_week_high', '52_week_low', 
        'after_hours_change', 'after_hours_close', 'all_time_high', 'all_time_low', 
        'analyst_recom', 'average_true_range', 'average_volume', 'beta', 'book_sh', 
        'cash_sh', 'change', 'change_from_open', 'company', 'country', 'current_ratio', 
        'dividend', 'dividend_yield', 'earnings_date', 'employees', 'eps_growth_next_5_years', 
        'eps_growth_next_year', 'eps_growth_past_5_years', 'eps_growth_quarter_over_quarter', 
        'eps_growth_this_year', 'eps_next_q', 'eps_surprise', 'eps_ttm', 'float_percent', 
        'forward_p_e', 'gap', 'gross_margin', 'high', 'income', 'index', 'industry', 
        'insider_ownership', 'insider_transactions', 'institutional_ownership', 
        'institutional_transactions', 'ipo_date', 'low', 'lt_debt_equity', 'market_cap', 
        'no', 'open', 'operating_margin', 'optionable', 'p_b', 'p_cash', 'p_e', 
        'p_free_cash_flow', 'p_s', 'payout_ratio', 'peg', 'performance_10_minutes', 
        'performance_15_minutes', 'performance_1_hour', 'performance_1_minute', 
        'performance_2_hours', 'performance_2_minutes', 'performance_30_minutes', 
        'performance_3_minutes', 'performance_4_hours', 'performance_5_minutes', 
        'performance_half_year', 'performance_month', 'performance_quarter', 
        'performance_week', 'performance_year', 'performance_ytd', 'prev_close', 
        'price', 'profit_margin', 'quick_ratio', 'relative_strength_index_14', 
        'relative_volume', 'return_on_assets', 'return_on_equity', 'return_on_invested_capital', 
        'revenue_surprise', 'sales', 'sales_growth_past_5_years', 'sales_growth_quarter_over_quarter', 
        'sector', 'shares_float', 'shares_outstanding', 'short_float', 'short_interest', 
        'short_ratio', 'shortable', 'target_price', 'ticker', 'total_debt_equity', 
        'trades', 'volatility_month', 'volatility_week', 'volume'
    }
    
    valid_fields.update(additional_valid_fields)
    
    return [field for field in fields if field not in valid_fields]

def validate_exchange(exchange: str) -> bool:
    """
    Validate an exchange filter.

    Args:
        exchange: Exchange code

    Returns:
        True if the exchange code is valid
    """
    return exchange in ALL_PARAMETERS['exch']

def validate_index(index: str) -> bool:
    """
    Validate an index filter.

    Args:
        index: Index code

    Returns:
        True if the index code is valid
    """
    return index in ALL_PARAMETERS['idx']

def validate_industry(industry: str) -> bool:
    """
    Validate an industry filter.

    Args:
        industry: Industry code

    Returns:
        True if the industry code is valid
    """
    return industry in ALL_PARAMETERS['ind']

def validate_country(country: str) -> bool:
    """
    Validate a country filter.

    Args:
        country: Country code

    Returns:
        True if the country code is valid
    """
    return country in ALL_PARAMETERS['geo']

def validate_price_filter(price: str) -> bool:
    """
    Validate a price filter.

    Args:
        price: Price filter

    Returns:
        True if the price filter is valid
    """
    return price in ALL_PARAMETERS['sh_price']

def validate_target_price(target_price: str) -> bool:
    """
    Validate a target price filter.

    Args:
        target_price: Target price filter

    Returns:
        True if the target price filter is valid
    """
    return target_price in ALL_PARAMETERS['targetprice']

def validate_dividend_yield_filter(dividend_yield: str) -> bool:
    """
    Validate a dividend yield filter.

    Args:
        dividend_yield: Dividend yield filter

    Returns:
        True if the dividend yield filter is valid
    """
    return dividend_yield in ALL_PARAMETERS['fa_div']

def validate_short_float(short_float: str) -> bool:
    """
    Validate a short float filter.

    Args:
        short_float: Short float filter

    Returns:
        True if the short float filter is valid
    """
    return short_float in ALL_PARAMETERS['sh_short']

def validate_analyst_recommendation(analyst_rec: str) -> bool:
    """
    Validate an analyst recommendation filter.

    Args:
        analyst_rec: Analyst recommendation filter

    Returns:
        True if the analyst recommendation filter is valid
    """
    return analyst_rec in ALL_PARAMETERS['an_recom']

def validate_option_short(option_short: str) -> bool:
    """
    Validate an option/short filter.

    Args:
        option_short: Option/short filter

    Returns:
        True if the option/short filter is valid
    """
    return option_short in ALL_PARAMETERS['sh_opt']

def validate_ipo_date(ipo_date: str) -> bool:
    """
    Validate an IPO date filter.

    Args:
        ipo_date: IPO date filter

    Returns:
        True if the IPO date filter is valid
    """
    return ipo_date in ALL_PARAMETERS['ipodate']

def validate_volume_filter(volume_type: str, volume_filter: str) -> bool:
    """
    Validate volume-related filters.

    Args:
        volume_type: Volume type ('sh_avgvol', 'sh_relvol', 'sh_curvol', 'sh_trades')
        volume_filter: Volume filter

    Returns:
        True if the volume filter is valid
    """
    if volume_type in ALL_PARAMETERS:
        return volume_filter in ALL_PARAMETERS[volume_type]
    return False

def validate_shares_filter(shares_type: str, shares_filter: str) -> bool:
    """
    Validate shares-related filters.

    Args:
        shares_type: Shares type ('sh_outstanding', 'sh_float')
        shares_filter: Shares filter

    Returns:
        True if the shares filter is valid
    """
    if shares_type in ALL_PARAMETERS:
        return shares_filter in ALL_PARAMETERS[shares_type]
    return False

def validate_custom_range(param_name: str, min_val: Optional[float], max_val: Optional[float]) -> bool:
    """
    Validate custom range parameters.

    Args:
        param_name: Parameter name
        min_val: Minimum value
        max_val: Maximum value

    Returns:
        True if the custom range is valid
    """
    # Only validate numeric parameters
    numeric_params = {
        'price', 'market_cap', 'pe', 'forward_pe', 'peg', 'ps', 'pb',
        'debt_equity', 'roe', 'roi', 'roa', 'dividend_yield',
        'volume', 'avg_volume', 'relative_volume', 'rsi', 'beta'
    }
    
    if param_name not in numeric_params:
        return False
    
    if min_val is not None and max_val is not None:
        return min_val <= max_val
    
    return True

def get_all_valid_values() -> Dict[str, List[str]]:
    """
    Get all valid parameter values.

    Returns:
        Dict of parameter names to valid values
    """
    return {param: list(values.keys()) for param, values in ALL_PARAMETERS.items()}

def validate_parameter_combination(params: Dict[str, Any]) -> List[str]:
    """
    Validate parameter combinations.

    Args:
        params: Parameter dict

    Returns:
        List of combination errors
    """
    errors = []
    
    # Exclusive ETF/stock combination check
    if params.get('exclude_etfs') and params.get('only_etfs'):
        errors.append("Cannot exclude and include ETFs simultaneously")
    
    # Price range combination check
    price_filters = ['price', 'price_min', 'price_max']
    price_count = sum(1 for p in price_filters if p in params and params[p] is not None)
    if price_count > 1:
        errors.append("Use either price filter OR price_min/max, not both")
    
    # Volume range combination check
    volume_filters = ['average_volume', 'avg_volume_min', 'volume_min']
    volume_count = sum(1 for v in volume_filters if v in params and params[v] is not None)
    if volume_count > 1:
        errors.append("Use either volume filter OR volume_min, not both")
    
    # Relative volume range combination check
    rel_volume_filters = ['relative_volume', 'relative_volume_min']
    rel_volume_count = sum(1 for rv in rel_volume_filters if rv in params and params[rv] is not None)
    if rel_volume_count > 1:
        errors.append("Use either relative_volume filter OR relative_volume_min, not both")
    
    return errors

def sanitize_input(value: Any) -> Any:
    """
    Sanitize input values.

    Args:
        value: Input value

    Returns:
        Sanitized value
    """
    if isinstance(value, str):
        # Basic sanitization to prevent SQL injection or XSS
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '|', '`']
        for char in dangerous_chars:
            value = value.replace(char, '')
        return value.strip()
    
    return value
