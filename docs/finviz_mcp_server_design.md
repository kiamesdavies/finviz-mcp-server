# Finviz MCP Server Design

## 1. Overview

This document defines the design of a server that exposes Finviz functionality through MCP (Model Context Protocol), based on the existing Finviz scripts.

FinvizMCP (Model Context Protocol) Finviz

## 2. Current Usage Analysis

### 2. Current Usage Analysis1

1. **Short-term trading strategies** (10 files)
2. **Mid/long-term investment strategies** (2 files)
3. **Screening & analysis** (7 files)
4. **News & sentiment analysis** (1 file)
5. **Utility tools** (2 files)

### 2. Current Usage Analysis2

## 3. MCP Server Architecture

### 3.1 Project Layout

```
finviz-mcp-server/
├── src/
│ ├── server.py # MCP server entry
│ ├── tools/ # MCP tool definitions
│ │ ├── __init__.py
│ │ ├── screening.py # Screening tools
│ │ ├── fundamentals.py # Fundamentals tools
│ │ ├── news.py # News tools
│ │ ├── sector_analysis.py # Sector analysis tools
│ │ └── technical.py # Technical analysis tools
│ ├── finviz_client/ # Finviz API client
│ │ ├── __init__.py
│ │ ├── base.py # Base API client
│ │ ├── screener.py # Screening features
│ │ ├── fundamentals.py # Fundamentals features
│ │ └── news.py # News features
│ └── utils/
│ ├── __init__.py
│ ├── validators.py # Input validation
│ └── formatters.py # Output formatting
├── tests/
├── requirements.txt
└── README.md
```

### 3.2 MCP Tools Overview

Tools are grouped by screening, fundamentals, news, sector/industry analysis, and technical analysis.

## 4. MCP Tool Specifications

### 4.1 Screening Tools

#### 4.1 Screening Tools.1 earnings_screener
```json
{
 "name": "earnings_screener",
 "description": "",
 "inputSchema": {
 "type": "object",
 "properties": {
 "earnings_date": {
 "type": "string",
 "enum": ["today_after", "tomorrow_before", "this_week", "within_2_weeks"],
 "description": "Earnings date selection"
 },
 "market_cap": {
 "type": "string",
 "enum": ["small", "mid", "large", "mega"],
 "description": "Market cap filter"
 },
 "min_price": {"type": "number", "description": "Minimum price"},
 "max_price": {"type": "number", "description": "Maximum price"},
 "min_volume": {"type": "number", "description": "Minimum volume"},
 "sectors": {
 "type": "array",
 "items": {"type": "string"},
 "description": "Target sectors"
 },
 "premarket_price_change": {
 "type": "object",
 "properties": {
 "enabled": {"type": "boolean", "description": "Enable this filter"},
 "min_change_percent": {"type": "number", "description": "Minimum price change (%)"},
 "max_change_percent": {"type": "number", "description": "Maximum price change (%)"}
 },
 "description": "Maximum price change (%)"
 },
 "afterhours_price_change": {
 "type": "object",
 "properties": {
 "enabled": {"type": "boolean", "description": "Enable this filter"},
 "min_change_percent": {"type": "number", "description": "Minimum price change (%)"},
 "max_change_percent": {"type": "number", "description": "Maximum price change (%)"}
 },
 "description": "Maximum price change (%)"
 }
 },
 "required": ["earnings_date"]
 }
}
```

#### 4.1 Screening Tools.2 trend_reversion_screener
```json
{
 "name": "trend_reversion_screener",
 "description": "Maximum price change (%)",
 "inputSchema": {
 "type": "object",
 "properties": {
 "market_cap": {
 "type": "string",
 "enum": ["mid_large", "large", "mega"],
 "description": "Market cap filter"
 },
 "eps_growth_qoq": {"type": "number", "description": "EPS(QoQ) "},
 "revenue_growth_qoq": {"type": "number", "description": "(QoQ) "},
 "rsi_max": {"type": "number", "description": "RSI"},
 "sectors": {
 "type": "array",
 "items": {"type": "string"},
 "description": "Target sectors"
 },
 "exclude_sectors": {
 "type": "array",
 "items": {"type": "string"},
 "description": "Excluded sectors"
 }
 }
 }
}
```

#### 4.1 Screening Tools.3 uptrend_screener
```json
{
 "name": "uptrend_screener",
 "description": "Excluded sectors",
 "inputSchema": {
 "type": "object",
 "properties": {
 "trend_type": {
 "type": "string",
 "enum": ["strong_uptrend", "breakout", "momentum"],
 "description": "Trend type"
 },
 "sma_period": {
 "type": "string",
 "enum": ["20", "50", "200"],
 "description": "Moving average period"
 },
 "relative_volume": {"type": "number", "description": "Minimum relative volume"},
 "price_change": {"type": "number", "description": "Minimum price change (%)"}
 }
 }
}
```

#### 4.1 Screening Tools.4 dividend_growth_screener
```json
{
 "name": "dividend_growth_screener",
 "description": "Minimum price change (%)",
 "inputSchema": {
 "type": "object",
 "properties": {
 "min_dividend_yield": {"type": "number", "description": "Minimum dividend yield"},
 "max_dividend_yield": {"type": "number", "description": "Maximum dividend yield"},
 "min_dividend_growth": {"type": "number", "description": "Minimum dividend growth rate"},
 "min_payout_ratio": {"type": "number", "description": "Minimum payout ratio"},
 "max_payout_ratio": {"type": "number", "description": "Maximum payout ratio"},
 "min_roe": {"type": "number", "description": "ROE"},
 "max_debt_equity": {"type": "number", "description": "Maximum debt-to-equity ratio"}
 }
 }
}
```

#### 4.1 Screening Tools.5 etf_screener
```json
{
 "name": "etf_screener",
 "description": "ETF",
 "inputSchema": {
 "type": "object",
 "properties": {
 "strategy_type": {
 "type": "string",
 "enum": ["long", "short"],
 "description": "Strategy type"
 },
 "asset_class": {
 "type": "string",
 "enum": ["equity", "bond", "commodity", "currency"],
 "description": "Asset class"
 },
 "min_aum": {"type": "number", "description": "Minimum AUM"},
 "max_expense_ratio": {"type": "number", "description": "Maximum expense ratio"}
 }
 }
}
```

#### 4.1 Screening Tools.6 volume_surge_screener
```json
{
 "name": "volume_surge_screener",
 "description": "Maximum expense ratio",
 "inputSchema": {
 "type": "object",
 "properties": {
 "market_cap": {
 "type": "string",
 "enum": ["small", "mid", "large", "mega", "smallover"],
 "default": "smallover",
 "description": "Market cap filter"
 },
 "min_price": {
 "type": "number",
 "default": 10,
 "description": "Minimum price"
 },
 "min_avg_volume": {
 "type": "number",
 "default": 100000,
 "description": "Minimum average volume"
 },
 "min_relative_volume": {
 "type": "number",
 "default": 1.5,
 "description": "Minimum relative volume"
 },
 "min_price_change": {
 "type": "number",
 "default": 2.0,
 "description": "Minimum price change (%)"
 },
 "sma_filter": {
 "type": "string",
 "enum": ["above_sma20", "above_sma50", "above_sma200", "none"],
 "default": "above_sma200",
 "description": "Sma filter"
 },
 "stocks_only": {
 "type": "boolean",
 "default": true,
 "description": "（ETF）"
 },
 "max_results": {
 "type": "number",
 "default": 50,
 "description": "Maximum number of results"
 },
 "sort_by": {
 "type": "string",
 "enum": ["price_change", "relative_volume", "volume", "price"],
 "default": "price_change",
 "description": "Sort key"
 },
 "sectors": {
 "type": "array",
 "items": {"type": "string"},
 "description": "Target sectors"
 },
 "exclude_sectors": {
 "type": "array",
 "items": {"type": "string"},
 "description": "Excluded sectors"
 }
 }
 }
}
```

#### 4.1 Screening Tools.7 earnings_premarket_screener
```json
{
 "name": "earnings_premarket_screener",
 "description": "Excluded sectors",
 "inputSchema": {
 "type": "object",
 "properties": {
 "earnings_timing": {
 "type": "string",
 "enum": ["today_before", "yesterday_before", "this_week_before"],
 "default": "today_before",
 "description": "Earnings timing"
 },
 "market_cap": {
 "type": "string",
 "enum": ["small", "mid", "large", "mega", "smallover"],
 "default": "smallover",
 "description": "Market cap filter"
 },
 "min_price": {
 "type": "number",
 "default": 10,
 "description": "Minimum price"
 },
 "min_avg_volume": {
 "type": "number",
 "default": 100000,
 "description": "Minimum average volume"
 },
 "min_price_change": {
 "type": "number",
 "default": 2.0,
 "description": "Minimum price change (%)"
 },
 "max_price_change": {
 "type": "number",
 "description": "Maximum price change"
 },
 "include_premarket_data": {
 "type": "boolean",
 "default": true,
 "description": "Include premarket data"
 },
 "data_fields": {
 "type": "array",
 "items": {
 "type": "string",
 "enum": [
 "ticker", "company", "sector", "industry", "country",
 "market_cap", "pe_ratio", "price", "change", "change_percent",
 "volume", "avg_volume", "relative_volume", "float", "outstanding",
 "insider_own", "institutional_own", "short_interest", "target_price",
 "52w_high", "52w_low", "rsi", "gap", "analyst_recom"
 ]
 },
 "default": [
 "ticker", "company", "sector", "price", "change", "change_percent",
 "volume", "relative_volume", "market_cap", "pe_ratio", "target_price"
 ],
 "description": "List of data fields"
 },
 "max_results": {
 "type": "number",
 "default": 60,
 "description": "Maximum number of results"
 },
 "sort_by": {
 "type": "string",
 "enum": ["change_percent", "change_abs", "volume", "relative_volume", "market_cap"],
 "default": "change_percent",
 "description": "Sort key"
 },
 "sort_order": {
 "type": "string",
 "enum": ["desc", "asc"],
 "default": "desc",
 "description": "Sort order"
 },
 "sectors": {
 "type": "array",
 "items": {"type": "string"},
 "description": "Target sectors"
 },
 "exclude_sectors": {
 "type": "array",
 "items": {"type": "string"},
 "description": "Excluded sectors"
 }
 }
 }
}
```

#### 4.1 Screening Tools.8 earnings_afterhours_screener
```json
{
 "name": "earnings_afterhours_screener",
 "description": "Excluded sectors",
 "inputSchema": {
 "type": "object",
 "properties": {
 "earnings_timing": {
 "type": "string",
 "enum": ["today_after", "yesterday_after", "this_week_after"],
 "default": "today_after",
 "description": "Earnings timing"
 },
 "market_cap": {
 "type": "string",
 "enum": ["small", "mid", "large", "mega", "smallover"],
 "default": "smallover",
 "description": "Market cap filter"
 },
 "min_price": {
 "type": "number",
 "default": 10,
 "description": "Minimum price"
 },
 "min_avg_volume": {
 "type": "number",
 "default": 100000,
 "description": "Minimum average volume"
 },
 "min_afterhours_change": {
 "type": "number",
 "default": 2.0,
 "description": "Minimum after-hours change (%)"
 },
 "max_afterhours_change": {
 "type": "number",
 "description": "Maximum afterhours change"
 },
 "include_afterhours_data": {
 "type": "boolean",
 "default": true,
 "description": "Include after-hours data"
 },
 "data_fields": {
 "type": "array",
 "items": {
 "type": "string",
 "enum": [
 "ticker", "company", "sector", "industry", "country",
 "market_cap", "pe_ratio", "price", "change", "change_percent",
 "afterhours_change", "afterhours_change_percent", "afterhours_price",
 "volume", "avg_volume", "relative_volume", "float", "outstanding",
 "insider_own", "institutional_own", "short_interest", "target_price",
 "52w_high", "52w_low", "rsi", "gap", "analyst_recom"
 ]
 },
 "default": [
 "ticker", "company", "sector", "price", "afterhours_change", "afterhours_change_percent",
 "volume", "relative_volume", "market_cap", "pe_ratio", "target_price"
 ],
 "description": "List of data fields"
 },
 "max_results": {
 "type": "number",
 "default": 60,
 "description": "Maximum number of results"
 },
 "sort_by": {
 "type": "string",
 "enum": ["afterhours_change_percent", "afterhours_change_abs", "change_percent", "volume", "relative_volume", "market_cap"],
 "default": "afterhours_change_percent",
 "description": "Sort key"
 },
 "sort_order": {
 "type": "string",
 "enum": ["desc", "asc"],
 "default": "desc",
 "description": "Sort order"
 },
 "sectors": {
 "type": "array",
 "items": {"type": "string"},
 "description": "Target sectors"
 },
 "exclude_sectors": {
 "type": "array",
 "items": {"type": "string"},
 "description": "Excluded sectors"
 }
 }
 }
}
```

#### 4.1 Screening Tools.9 earnings_trading_screener
```json
{
 "name": "earnings_trading_screener",
 "description": "Excluded sectors",
 "inputSchema": {
 "type": "object",
 "properties": {
 "earnings_window": {
 "type": "string",
 "enum": ["yesterday_after_today_before", "today_before_after", "this_week", "custom"],
 "default": "yesterday_after_today_before",
 "description": "Earnings window"
 },
 "market_cap": {
 "type": "string",
 "enum": ["small", "mid", "large", "mega", "smallover"],
 "default": "smallover",
 "description": "Market cap filter"
 },
 "min_price": {
 "type": "number",
 "default": 10,
 "description": "Minimum price"
 },
 "min_avg_volume": {
 "type": "number",
 "default": 200000,
 "description": "Minimum average volume"
 },
 "earnings_revision": {
 "type": "string",
 "enum": ["eps_revenue_positive", "eps_positive", "revenue_positive", "any_positive"],
 "default": "eps_revenue_positive",
 "description": "Earnings revision filter"
 },
 "price_trend": {
 "type": "string",
 "enum": ["positive_change", "recovery_from_decline", "any_upward"],
 "default": "positive_change",
 "description": "Price trend filter"
 },
 "performance_filter": {
 "type": "object",
 "properties": {
 "recent_decline_recovery": {
 "type": "boolean",
 "default": true,
 "description": "Parameter: recent decline recovery"
 },
 "max_4week_decline": {
 "type": "number",
 "default": -4.0,
 "description": "4(%)"
 }
 },
 "description": "Maximum 4week decline"
 },
 "volatility_filter": {
 "type": "object",
 "properties": {
 "min_volatility": {
 "type": "number",
 "default": 1.0,
 "description": "Minimum volatility"
 },
 "max_volatility": {
 "type": "number",
 "description": "Maximum volatility"
 }
 },
 "description": "Maximum volatility"
 },
 "data_fields": {
 "type": "array",
 "items": {
 "type": "string",
 "enum": [
 "ticker", "company", "sector", "industry", "market_cap", "price",
 "change", "change_percent", "volume", "avg_volume", "relative_volume",
 "eps_surprise", "revenue_surprise", "eps_estimate", "revenue_estimate",
 "pe_ratio", "target_price", "analyst_recom", "volatility",
 "performance_4w", "performance_1m", "rsi", "beta",
 "float", "outstanding", "insider_own", "institutional_own"
 ]
 },
 "default": [
 "ticker", "company", "sector", "price", "change", "change_percent",
 "eps_surprise", "revenue_surprise", "volume", "relative_volume",
 "market_cap", "volatility", "performance_4w", "target_price"
 ],
 "description": "List of data fields"
 },
 "max_results": {
 "type": "number",
 "default": 60,
 "description": "Maximum number of results"
 },
 "sort_by": {
 "type": "string",
 "enum": ["eps_surprise", "revenue_surprise", "combined_surprise", "change_percent", "volatility", "volume"],
 "default": "eps_surprise",
 "description": "Sort key"
 },
 "sort_order": {
 "type": "string",
 "enum": ["desc", "asc"],
 "default": "desc",
 "description": "Sort order"
 },
 "sectors": {
 "type": "array",
 "items": {"type": "string"},
 "description": "Target sectors"
 },
 "exclude_sectors": {
 "type": "array",
 "items": {"type": "string"},
 "description": "Excluded sectors"
 }
 }
 }
}
```

#### 4.1 Screening Tools.11 upcoming_earnings_screener
```json
{
 "name": "upcoming_earnings_screener",
 "description": "Excluded sectors",
 "inputSchema": {
 "type": "object",
 "properties": {
 "earnings_period": {
 "type": "string",
 "enum": ["next_week", "next_2_weeks", "next_month", "custom_range"],
 "default": "next_week",
 "description": "Earnings period"
 },
 "market_cap": {
 "type": "string",
 "enum": ["small", "mid", "large", "mega", "smallover"],
 "default": "smallover",
 "description": "Market cap filter"
 },
 "min_price": {
 "type": "number",
 "default": 10,
 "description": "Minimum price"
 },
 "min_avg_volume": {
 "type": "number",
 "default": 500000,
 "description": "Minimum average volume"
 },
 "target_sectors": {
 "type": "array",
 "items": {
 "type": "string",
 "enum": [
 "technology", "industrials", "healthcare", "communication_services",
 "consumer_cyclical", "financial", "consumer_defensive", "basic_materials",
 "real_estate", "utilities", "energy"
 ]
 },
 "default": [
 "technology", "industrials", "healthcare", "communication_services",
 "consumer_cyclical", "financial", "consumer_defensive", "basic_materials"
 ],
 "description": "（8）"
 },
 "pre_earnings_analysis": {
 "type": "object",
 "properties": {
 "include_estimates": {
 "type": "boolean",
 "default": true,
 "description": "EPS"
 },
 "include_revisions": {
 "type": "boolean",
 "default": true,
 "description": "Include revisions"
 },
 "include_historical_surprise": {
 "type": "boolean",
 "default": true,
 "description": "Include historical surprise"
 },
 "include_options_activity": {
 "type": "boolean",
 "default": false,
 "description": "Include options activity"
 }
 },
 "description": "Include options activity"
 },
 "risk_assessment": {
 "type": "object",
 "properties": {
 "include_volatility": {
 "type": "boolean",
 "default": true,
 "description": "Include volatility"
 },
 "include_short_interest": {
 "type": "boolean",
 "default": true,
 "description": "Include short interest"
 },
 "include_analyst_changes": {
 "type": "boolean",
 "default": true,
 "description": "Include analyst changes"
 }
 },
 "description": "Include analyst changes"
 },
 "data_fields": {
 "type": "array",
 "items": {
 "type": "string",
 "enum": [
 "ticker", "company", "sector", "industry", "country", "market_cap",
 "price", "change", "change_percent", "volume", "avg_volume", "relative_volume",
 "earnings_date", "earnings_timing", "eps_estimate", "revenue_estimate",
 "eps_estimate_revision", "revenue_estimate_revision", "analyst_count",
 "pe_ratio", "forward_pe", "peg", "target_price", "analyst_recom",
 "performance_1w", "performance_1m", "performance_3m", "sma_200_relative",
 "rsi", "beta", "volatility", "short_interest", "short_ratio",
 "float", "outstanding", "insider_own", "institutional_own",
 "historical_eps_surprise", "historical_revenue_surprise"
 ]
 },
 "default": [
 "ticker", "company", "sector", "industry", "earnings_date", "earnings_timing",
 "eps_estimate", "revenue_estimate", "eps_estimate_revision", "analyst_count",
 "price", "market_cap", "pe_ratio", "target_price", "analyst_recom",
 "volatility", "short_interest", "avg_volume"
 ],
 "description": "List of data fields"
 },
 "max_results": {
 "type": "number",
 "default": 100,
 "description": "Maximum number of results"
 },
 "sort_by": {
 "type": "string",
 "enum": [
 "earnings_date", "market_cap", "eps_estimate_revision", "analyst_recom",
 "volatility", "short_interest", "target_price_upside", "ticker"
 ],
 "default": "earnings_date",
 "description": "Sort key"
 },
 "sort_order": {
 "type": "string",
 "enum": ["asc", "desc"],
 "default": "asc",
 "description": "Sort order"
 },
 "include_chart_view": {
 "type": "boolean",
 "default": true,
 "description": "Include weekly chart view"
 },
 "earnings_calendar_format": {
 "type": "boolean",
 "default": false,
 "description": "Output in earnings calendar format"
 }
 }
 }
}
```

### 4.2 Fundamental Data Tools

#### 4.2 Fundamental Data Tools.1 get_stock_fundamentals
```json
{
 "name": "get_stock_fundamentals",
 "description": "Output in earnings calendar format",
 "inputSchema": {
 "type": "object",
 "properties": {
 "ticker": {"type": "string", "description": "Stock ticker"},
 "data_fields": {
 "type": "array",
 "items": {"type": "string"},
 "description": "List of data fields"
 }
 },
 "required": ["ticker"]
 }
}
```

#### 4.2 Fundamental Data Tools.2 get_multiple_stocks_fundamentals
```json
{
 "name": "get_multiple_stocks_fundamentals",
 "description": "List of data fields",
 "inputSchema": {
 "type": "object",
 "properties": {
 "tickers": {
 "type": "array",
 "items": {"type": "string"},
 "description": "List of stock tickers"
 },
 "data_fields": {
 "type": "array",
 "items": {"type": "string"},
 "description": "List of data fields"
 }
 },
 "required": ["tickers"]
 }
}
```

### 4.3 News Tools

#### 4.3 News Tools.1 get_stock_news
```json
{
 "name": "get_stock_news",
 "description": "List of data fields",
 "inputSchema": {
 "type": "object",
 "properties": {
 "ticker": {"type": "string", "description": "Stock ticker"},
 "days_back": {"type": "number", "description": "Lookback window in days"},
 "news_type": {
 "type": "string",
 "enum": ["all", "earnings", "analyst", "insider", "general"],
 "description": "News type"
 }
 },
 "required": ["ticker"]
 }
}
```

### 4.4 Market & Sector Analysis Tools

#### 4.4 Market & Sector Analysis Tools.1 get_sector_performance
```json
{
 "name": "get_sector_performance",
 "description": "News type",
 "inputSchema": {
 "type": "object",
 "properties": {
 "timeframe": {
 "type": "string",
 "enum": ["1d", "1w", "1m", "3m", "6m", "1y"],
 "description": "Timeframe"
 },
 "sectors": {
 "type": "array",
 "items": {"type": "string"},
 "description": "Target sectors"
 }
 }
 }
}
```

#### 4.4 Market & Sector Analysis Tools.2 get_industry_performance
```json
{
 "name": "get_industry_performance",
 "description": "Target sectors",
 "inputSchema": {
 "type": "object",
 "properties": {
 "timeframe": {
 "type": "string",
 "enum": ["1d", "1w", "1m", "3m", "6m", "1y"],
 "description": "Timeframe"
 },
 "industries": {
 "type": "array",
 "items": {"type": "string"},
 "description": "Target industries"
 }
 }
 }
}
```

#### 4.4 Market & Sector Analysis Tools.3 get_country_performance
```json
{
 "name": "get_country_performance",
 "description": "Target industries",
 "inputSchema": {
 "type": "object",
 "properties": {
 "timeframe": {
 "type": "string",
 "enum": ["1d", "1w", "1m", "3m", "6m", "1y"],
 "description": "Timeframe"
 },
 "countries": {
 "type": "array",
 "items": {"type": "string"},
 "description": "Target countries"
 }
 }
 }
}
```

### 4.5 Technical Analysis Tools

#### 4.5 Technical Analysis Tools.1 get_relative_volume_stocks
```json
{
 "name": "get_relative_volume_stocks",
 "description": "Target countries",
 "inputSchema": {
 "type": "object",
 "properties": {
 "min_relative_volume": {"type": "number", "description": "Minimum relative volume"},
 "min_price": {"type": "number", "description": "Minimum price"},
 "sectors": {
 "type": "array",
 "items": {"type": "string"},
 "description": "Target sectors"
 }
 },
 "required": ["min_relative_volume"]
 }
}
```

### 4.6 SEC Filing Tools

#### 4.6.1 get_sec_filings
```json
{
 "name": "get_sec_filings",
 "description": "SEC",
 "inputSchema": {
 "type": "object",
 "properties": {
 "ticker": {"type": "string", "description": "Stock ticker"},
 "form_types": {
 "type": "array",
 "items": {"type": "string"},
 "description": "Form type filter"
 },
 "days_back": {"type": "integer", "description": "Lookback window in days"},
 "max_results": {"type": "integer", "description": "Maximum number of results"},
 "sort_by": {"type": "string", "description": "Sort key"},
 "sort_order": {"type": "string", "description": "Sort order"}
 },
 "required": ["ticker"]
 }
}
```

## 5. Data Models

### 5. Data Models1

#### StockData
```python
@dataclass
class StockData:
 ticker: str
 company_name: str
 sector: str
 industry: str
 country: Optional[str] #
 market_cap: float
 price: float
 volume: int
 avg_volume: int
 relative_volume: Optional[float] #
 price_change: Optional[float] # (%)
 price_change_abs: Optional[float] #
 gap: Optional[float] # （）
 premarket_price: Optional[float] #
 premarket_change: Optional[float] #
 premarket_change_percent: Optional[float] # (%)
 afterhours_price: Optional[float] #
 afterhours_change: Optional[float] #
 afterhours_change_percent: Optional[float] # (%)
 earnings_date: Optional[str] #
 earnings_timing: Optional[str] # （before/after）
 eps_surprise: Optional[float] # EPS(%)
 revenue_surprise: Optional[float] # (%)
 eps_estimate: Optional[float] # EPS
 revenue_estimate: Optional[float] #
 eps_actual: Optional[float] # EPS
 revenue_actual: Optional[float] #
 eps_qoq_growth: Optional[float] # EPS(%)
 sales_qoq_growth: Optional[float] # (%)
 eps_revision: Optional[float] # EPS(%)
 revenue_revision: Optional[float] # (%)
 volatility: Optional[float] #
 beta: Optional[float] #
 performance_1w: Optional[float] # 1(%)
 performance_1m: Optional[float] # 1(%)
 performance_4w: Optional[float] # 4(%)
 performance_ytd: Optional[float] # (%)
 pe_ratio: Optional[float]
 forward_pe: Optional[float] # PER
 peg: Optional[float] # PEG
 eps: Optional[float]
 dividend_yield: Optional[float]
 rsi: Optional[float]
 sma_20: Optional[float]
 sma_50: Optional[float]
 sma_200: Optional[float]
 above_sma_20: Optional[bool] # SMA20
 above_sma_50: Optional[bool] # SMA50
 above_sma_200: Optional[bool] # SMA200
 sma_20_relative: Optional[float] # SMA20(%)
 sma_50_relative: Optional[float] # SMA50(%)
 sma_200_relative: Optional[float] # SMA200(%)
 target_price: Optional[float] #
 analyst_recommendation: Optional[str] #
 insider_ownership: Optional[float] #
 institutional_ownership: Optional[float] #
 short_interest: Optional[float] #
 float_shares: Optional[int] #
 outstanding_shares: Optional[int] #
 week_52_high: Optional[float] # 52
 week_52_low: Optional[float] # 52

 def to_dict(self) -> dict:
 return asdict(self)
```

#### NewsData
```python
@dataclass
class NewsData:
 ticker: str
 title: str
 source: str
 date: datetime
 url: str
 category: str

 def to_dict(self) -> dict:
 return asdict(self)
```

#### SectorPerformance
```python
@dataclass
class SectorPerformance:
 sector: str
 performance_1d: float
 performance_1w: float
 performance_1m: float
 performance_3m: float
 performance_6m: float
 performance_1y: float
 stock_count: int

 def to_dict(self) -> dict:
 return asdict(self)
```

#### SECFilingData
```python
@dataclass
class SECFilingData:
 ticker: str
 filing_date: str
 report_date: str
 form: str
 description: str
 filing_url: str
 document_url: str

 def to_dict(self) -> dict:
 return asdict(self)
```

#### EarningsData
```python
@dataclass
class EarningsData:
 ticker: str
 company_name: str
 earnings_date: str
 earnings_timing: str # "before" or "after"
 pre_earnings_price: Optional[float] #
 post_earnings_price: Optional[float] #
 premarket_price: Optional[float] #
 afterhours_price: Optional[float] #
 current_price: Optional[float] #
 price_change_percent: Optional[float] #
 gap_percent: Optional[float] #
 volume: Optional[int] #
 avg_volume: Optional[int] #
 relative_volume: Optional[float] #
 eps_surprise: Optional[float] # EPS(%)
 revenue_surprise: Optional[float] # (%)
 eps_estimate: Optional[float] # EPS
 eps_actual: Optional[float] # EPS
 revenue_estimate: Optional[float] #
 revenue_actual: Optional[float] #
 earnings_revision: Optional[str] #
 market_reaction: Optional[str] # "positive", "negative", "neutral"
 volatility: Optional[float] #
 beta: Optional[float] #
 performance_4w: Optional[float] # 4
 recovery_from_decline: Optional[bool] #
 trading_opportunity_score: Optional[float] # (1-10)

 def to_dict(self) -> dict:
 return asdict(self)
```

#### UpcomingEarningsData
```python
@dataclass
class UpcomingEarningsData:
 ticker: str
 company_name: str
 sector: str
 industry: str
 earnings_date: str
 earnings_timing: str # "before" or "after"
 current_price: Optional[float] #
 market_cap: Optional[float] #
 avg_volume: Optional[int] #
 eps_estimate: Optional[float] # EPS
 revenue_estimate: Optional[float] #
 eps_estimate_revision: Optional[float] # EPS(%)
 revenue_estimate_revision: Optional[float] # (%)
 analyst_count: Optional[int] #
 estimate_trend: Optional[str] # ("improving", "declining", "stable")
 historical_eps_surprise: Optional[List[float]] # 4EPS
 historical_revenue_surprise: Optional[List[float]] # 4
 avg_eps_surprise: Optional[float] # EPS
 avg_revenue_surprise: Optional[float] #
 pe_ratio: Optional[float] # PER
 forward_pe: Optional[float] # PER
 peg: Optional[float] # PEG
 target_price: Optional[float] #
 target_price_upside: Optional[float] # (%)
 analyst_recommendation: Optional[str] #
 recent_rating_changes: Optional[List[dict]] #
 volatility: Optional[float] #
 beta: Optional[float] #
 short_interest: Optional[float] # (%)
 short_ratio: Optional[float] # （）
 insider_ownership: Optional[float] #
 institutional_ownership: Optional[float] #
 performance_1w: Optional[float] # 1
 performance_1m: Optional[float] # 1
 performance_3m: Optional[float] # 3
 sma_200_relative: Optional[float] # 200
 rsi: Optional[float] # RSI
 options_volume: Optional[int] #
 put_call_ratio: Optional[float] #
 implied_volatility: Optional[float] #
 earnings_potential_score: Optional[float] # (1-10)
 risk_score: Optional[float] # (1-10)
 surprise_probability: Optional[float] # (%)

 def to_dict(self) -> dict:
 return asdict(self)
```

## 6. Validation & Formatting

### 6. Validation & Formatting1

- ****: Finviz API
- ****: API

### 6. Validation & Formatting2

```json
{
 "error": {
 "code": "AUTHENTICATION_ERROR",
 "message": "Invalid API key provided",
 "details": {
 "suggestion": "Please check your FINVIZ_API_KEY environment variable"
 }
 }
}
```

## 7. Error Handling

### 7. Error Handling1

```bash
FINVIZ_API_KEY=your_finviz_api_key_here
MCP_SERVER_PORT=8080
LOG_LEVEL=INFO
RATE_LIMIT_REQUESTS_PER_MINUTE=100
```

### 7. Error Handling2

```txt
mcp>=0.1.0
requests>=2.31.0
pandas>=2.0.0
python-dotenv>=1.0.0
pydantic>=2.0.0
```

## 8. Operations

### 8. Operations1

```python
# MCP Client

result = await mcp_client.call_tool(
 "earnings_screener",
 {
 "earnings_date": "today_after",
 "market_cap": "large",
 "min_price": 10,
 "min_volume": 1000000,
 "sectors": ["Technology", "Healthcare"]
 }
)

result = await mcp_client.call_tool(
 "earnings_screener",
 {
 "earnings_date": "today_after",
 "market_cap": "large",
 "min_price": 10,
 "min_volume": 1000000,
 "sectors": ["Technology", "Healthcare"],
 "afterhours_price_change": {
 "enabled": True,
 "min_change_percent": 2.0,
 "max_change_percent": 15.0
 }
 }
)

result = await mcp_client.call_tool(
 "earnings_screener",
 {
 "earnings_date": "tomorrow_before",
 "market_cap": "mid",
 "min_price": 5,
 "min_volume": 500000,
 "premarket_price_change": {
 "enabled": True,
 "min_change_percent": 1.0,
 "max_change_percent": 10.0
 }
 }
)
```

### 8. Operations2

```python
# （URL）
result = await mcp_client.call_tool(
 "volume_surge_screener",
 {
 "market_cap": "smallover",
 "min_price": 10,
 "min_avg_volume": 100000,
 "min_relative_volume": 1.5,
 "min_price_change": 2.0,
 "sma_filter": "above_sma200",
 "stocks_only": True,
 "sort_by": "price_change",
 "max_results": 50
 }
)

result = await mcp_client.call_tool(
 "volume_surge_screener",
 {
 "market_cap": "large",
 "min_price": 20,
 "min_relative_volume": 2.0,
 "min_price_change": 3.0,
 "sma_filter": "above_sma50",
 "sectors": ["Technology"],
 "sort_by": "relative_volume",
 "max_results": 25
 }
)

result = await mcp_client.call_tool(
 "volume_surge_screener",
 {
 "market_cap": "mid",
 "min_price": 15,
 "min_avg_volume": 500000,
 "min_relative_volume": 3.0,
 "min_price_change": 5.0,
 "sma_filter": "above_sma20",
 "exclude_sectors": ["Financial", "Real Estate"],
 "sort_by": "price_change",
 "max_results": 20
 }
)
```

### 8. Operations3

```python
# （URL）
result = await mcp_client.call_tool(
 "earnings_premarket_screener",
 {
 "earnings_timing": "today_before",
 "market_cap": "smallover",
 "min_price": 10,
 "min_avg_volume": 100000,
 "min_price_change": 2.0,
 "include_premarket_data": True,
 "max_results": 60,
 "sort_by": "change_percent",
 "sort_order": "desc"
 }
)

result = await mcp_client.call_tool(
 "earnings_premarket_screener",
 {
 "earnings_timing": "today_before",
 "market_cap": "large",
 "min_price": 25,
 "min_avg_volume": 1000000,
 "min_price_change": 1.5,
 "max_price_change": 20.0,
 "sectors": ["Technology", "Healthcare", "Consumer Discretionary"],
 "data_fields": [
 "ticker", "company", "sector", "price", "change", "change_percent",
 "volume", "relative_volume", "market_cap", "pe_ratio", "target_price",
 "analyst_recom", "gap", "52w_high", "52w_low"
 ],
 "max_results": 30,
 "sort_by": "change_percent"
 }
)

result = await mcp_client.call_tool(
 "earnings_premarket_screener",
 {
 "earnings_timing": "today_before",
 "market_cap": "mid",
 "min_price": 15,
 "min_avg_volume": 500000,
 "min_price_change": 3.0,
 "exclude_sectors": ["Financial", "Real Estate"],
 "data_fields": [
 "ticker", "company", "sector", "industry", "country",
 "market_cap", "pe_ratio", "price", "change", "change_percent",
 "volume", "avg_volume", "relative_volume", "float", "outstanding",
 "insider_own", "institutional_own", "short_interest", "target_price",
 "52w_high", "52w_low", "rsi", "gap", "analyst_recom"
 ],
 "max_results": 40,
 "sort_by": "relative_volume",
 "sort_order": "desc"
 }
)
```

### 8. Operations4

```python
# （URL）
result = await mcp_client.call_tool(
 "earnings_afterhours_screener",
 {
 "earnings_timing": "today_after",
 "market_cap": "smallover",
 "min_price": 10,
 "min_avg_volume": 100000,
 "min_afterhours_change": 2.0,
 "include_afterhours_data": True,
 "max_results": 60,
 "sort_by": "afterhours_change_percent",
 "sort_order": "desc"
 }
)

result = await mcp_client.call_tool(
 "earnings_afterhours_screener",
 {
 "earnings_timing": "today_after",
 "market_cap": "large",
 "min_price": 20,
 "min_avg_volume": 1000000,
 "min_afterhours_change": 1.5,
 "max_afterhours_change": 25.0,
 "sectors": ["Technology", "Healthcare", "Consumer Discretionary"],
 "data_fields": [
 "ticker", "company", "sector", "price", "afterhours_change", "afterhours_change_percent",
 "afterhours_price", "volume", "relative_volume", "market_cap", "pe_ratio",
 "target_price", "analyst_recom", "52w_high", "52w_low"
 ],
 "max_results": 30,
 "sort_by": "afterhours_change_percent"
 }
)

result = await mcp_client.call_tool(
 "earnings_afterhours_screener",
 {
 "earnings_timing": "today_after",
 "market_cap": "mid",
 "min_price": 15,
 "min_avg_volume": 250000,
 "min_afterhours_change": 5.0,
 "max_afterhours_change": 50.0,
 "exclude_sectors": ["Financial", "Real Estate", "Utilities"],
 "data_fields": [
 "ticker", "company", "sector", "industry", "country",
 "market_cap", "pe_ratio", "price", "change", "change_percent",
 "afterhours_change", "afterhours_change_percent", "afterhours_price",
 "volume", "avg_volume", "relative_volume", "float", "outstanding",
 "insider_own", "institutional_own", "short_interest", "target_price",
 "52w_high", "52w_low", "rsi", "gap", "analyst_recom"
 ],
 "max_results": 25,
 "sort_by": "afterhours_change_percent",
 "sort_order": "desc"
 }
)
```

### 8. Operations5

```python
# （URL）
result = await mcp_client.call_tool(
 "earnings_trading_screener",
 {
 "earnings_window": "yesterday_after_today_before",
 "market_cap": "smallover",
 "min_price": 10,
 "min_avg_volume": 200000,
 "earnings_revision": "eps_revenue_positive",
 "price_trend": "positive_change",
 "performance_filter": {
 "recent_decline_recovery": True,
 "max_4week_decline": -4.0
 },
 "volatility_filter": {
 "min_volatility": 1.0
 },
 "max_results": 60,
 "sort_by": "eps_surprise",
 "sort_order": "desc"
 }
)

result = await mcp_client.call_tool(
 "earnings_trading_screener",
 {
 "earnings_window": "yesterday_after_today_before",
 "market_cap": "large",
 "min_price": 25,
 "min_avg_volume": 1000000,
 "earnings_revision": "eps_revenue_positive",
 "price_trend": "recovery_from_decline",
 "performance_filter": {
 "recent_decline_recovery": True,
 "max_4week_decline": -8.0
 },
 "volatility_filter": {
 "min_volatility": 0.8,
 "max_volatility": 3.0
 },
 "sectors": ["Technology", "Healthcare", "Consumer Discretionary"],
 "data_fields": [
 "ticker", "company", "sector", "price", "change", "change_percent",
 "eps_surprise", "revenue_surprise", "eps_estimate", "revenue_estimate",
 "volume", "relative_volume", "market_cap", "pe_ratio", "volatility",
 "performance_4w", "performance_1m", "target_price", "analyst_recom"
 ],
 "max_results": 30,
 "sort_by": "combined_surprise"
 }
)

result = await mcp_client.call_tool(
 "earnings_trading_screener",
 {
 "earnings_window": "today_before_after",
 "market_cap": "mid",
 "min_price": 15,
 "min_avg_volume": 500000,
 "earnings_revision": "any_positive",
 "price_trend": "any_upward",
 "performance_filter": {
 "recent_decline_recovery": True,
 "max_4week_decline": -10.0
 },
 "volatility_filter": {
 "min_volatility": 2.0,
 "max_volatility": 8.0
 },
 "exclude_sectors": ["Financial", "Real Estate", "Utilities"],
 "data_fields": [
 "ticker", "company", "sector", "industry", "market_cap", "price",
 "change", "change_percent", "volume", "avg_volume", "relative_volume",
 "eps_surprise", "revenue_surprise", "eps_estimate", "revenue_estimate",
 "pe_ratio", "target_price", "analyst_recom", "volatility", "beta",
 "performance_4w", "performance_1m", "rsi", "float", "outstanding"
 ],
 "max_results": 40,
 "sort_by": "volatility",
 "sort_order": "desc"
 }
)
```

### 8. Operations6

```python

```

### 8. Operations6.1

URL：

```python
example_results = [
 {
 "ticker": "AVAV",
 "company": "AeroVironment Inc",
 "sector": "Industrials",
 "industry": "Aerospace & Defense",
 "eps_qoq_growth": 173.98, # 173.98%EPS
 "sales_qoq_growth": 39.63, # 39.63%
 "market_cap": "12.71B",
 "pe_ratio": 180.17,
 "forward_pe": 65.56,
 "target_price": 249.29,
 "performance_analysis": "EPS"
 },
 {
 "ticker": "CCL",
 "company": "Carnival Corp",
 "sector": "Consumer Cyclical",
 "industry": "Travel Services",
 "eps_qoq_growth": 474.17, # 474.17%EPS
 "sales_qoq_growth": 9.46, # 9.46%
 "market_cap": "35.36B",
 "pe_ratio": 14.78,
 "forward_pe": 12.01,
 "target_price": 29.49,
 "performance_analysis": "EPS"
 },
 {
 "ticker": "SNX",
 "company": "TD Synnex Corp",
 "sector": "Technology",
 "industry": "Electronics & Computer Distribution",
 "eps_qoq_growth": 33.37, # 33.37%EPS
 "sales_qoq_growth": 7.16, # 7.16%
 "market_cap": "11.31B",
 "pe_ratio": 15.75,
 "forward_pe": 9.93,
 "target_price": 149.00,
 "performance_analysis": ""
 }
]
```

### 8. Operations7

```python
# （URL）
result = await mcp_client.call_tool(
 "upcoming_earnings_screener",
 {
 "earnings_period": "next_week",
 "market_cap": "smallover",
 "min_price": 10,
 "min_avg_volume": 500000,
 "target_sectors": [
 "technology", "industrials", "healthcare", "communication_services",
 "consumer_cyclical", "financial", "consumer_defensive", "basic_materials"
 ],
 "pre_earnings_analysis": {
 "include_estimates": True,
 "include_revisions": True,
 "include_historical_surprise": True,
 "include_options_activity": False
 },
 "risk_assessment": {
 "include_volatility": True,
 "include_short_interest": True,
 "include_analyst_changes": True
 },
 "sort_by": "earnings_date",
 "sort_order": "asc",
 "max_results": 100
 }
)

result = await mcp_client.call_tool(
 "upcoming_earnings_screener",
 {
 "earnings_period": "next_week",
 "market_cap": "large",
 "min_price": 25,
 "min_avg_volume": 1000000,
 "target_sectors": ["technology", "healthcare", "financial"],
 "pre_earnings_analysis": {
 "include_estimates": True,
 "include_revisions": True,
 "include_historical_surprise": True,
 "include_options_activity": True
 },
 "risk_assessment": {
 "include_volatility": True,
 "include_short_interest": True,
 "include_analyst_changes": True
 },
 "data_fields": [
 "ticker", "company", "sector", "industry", "earnings_date", "earnings_timing",
 "eps_estimate", "revenue_estimate", "eps_estimate_revision", "analyst_count",
 "target_price", "target_price_upside", "analyst_recom", "pe_ratio", "forward_pe",
 "volatility", "short_interest", "avg_volume", "market_cap",
 "historical_eps_surprise", "historical_revenue_surprise"
 ],
 "sort_by": "target_price_upside",
 "sort_order": "desc",
 "max_results": 50
 }
)

result = await mcp_client.call_tool(
 "upcoming_earnings_screener",
 {
 "earnings_period": "next_week",
 "market_cap": "mid",
 "min_price": 15,
 "min_avg_volume": 250000,
 "target_sectors": [
 "technology", "industrials", "healthcare", "consumer_cyclical"
 ],
 "pre_earnings_analysis": {
 "include_estimates": True,
 "include_revisions": True,
 "include_historical_surprise": True,
 "include_options_activity": True
 },
 "risk_assessment": {
 "include_volatility": True,
 "include_short_interest": True,
 "include_analyst_changes": True
 },
 "data_fields": [
 "ticker", "company", "sector", "industry", "earnings_date", "earnings_timing",
 "eps_estimate", "revenue_estimate", "eps_estimate_revision", "revenue_estimate_revision",
 "analyst_count", "pe_ratio", "forward_pe", "peg", "target_price", "target_price_upside",
 "analyst_recom", "volatility", "beta", "short_interest", "short_ratio",
 "performance_1w", "performance_1m", "performance_3m", "sma_200_relative", "rsi",
 "historical_eps_surprise", "historical_revenue_surprise"
 ],
 "earnings_calendar_format": True,
 "include_chart_view": True,
 "sort_by": "earnings_date",
 "sort_order": "asc",
 "max_results": 75
 }
)
```

### 8. Operations7.1

URL：

```python
upcoming_earnings_examples = [
 {
 "ticker": "MSM",
 "company": "MSC Industrial Direct Co., Inc",
 "sector": "Industrials",
 "industry": "Industrial Distribution",
 "earnings_date": "2025-07-01",
 "earnings_timing": "before",
 "market_cap": "4.76B",
 "current_price": 85.50,
 "pe_ratio": 22.50,
 "forward_pe": 21.77,
 "target_price": 82.33,
 "analyst_recom": "2.55", # Buy=1, Hold=2, Sell=3
 "avg_volume": "528.55K",
 "dividend_yield": 4.05,
 "week_52_range": "68.10 - 90.81",
 "earnings_analysis": ""
 },
 {
 "ticker": "PRGS",
 "company": "Progress Software Corp",
 "sector": "Technology",
 "industry": "Software - Infrastructure",
 "earnings_date": "2025-06-30",
 "earnings_timing": "after",
 "market_cap": "2.74B",
 "current_price": 63.82,
 "pe_ratio": 49.48,
 "forward_pe": 11.17,
 "peg": 7.58,
 "target_price": 71.71,
 "target_price_upside": 12.4, # 12.4%
 "analyst_recom": "1.75", #
 "avg_volume": "568.99K",
 "week_52_range": "50.68 - 70.56",
 "earnings_analysis": "PE"
 },
 {
 "ticker": "STZ",
 "company": "Constellation Brands Inc",
 "sector": "Consumer Defensive",
 "industry": "Beverages - Brewers",
 "earnings_date": "2025-07-01",
 "earnings_timing": "after",
 "market_cap": "28.54B",
 "current_price": 166.50,
 "pe_ratio": None, # EPS
 "forward_pe": 11.71,
 "target_price": 201.00,
 "target_price_upside": 20.7, # 20.7%
 "analyst_recom": "1.96",
 "avg_volume": "2.12M",
 "dividend_yield": 2.57,
 "week_52_range": "159.35 - 264.45",
 "earnings_analysis": "S&P500"
 }
]
```

### 8. Operations8

```python
result = await mcp_client.call_tool(
 "get_stock_fundamentals",
 {
 "ticker": "AAPL",
 "data_fields": ["pe_ratio", "eps", "revenue_growth", "roe"]
 }
)
```

## 9.

### 9.1

- **TTL**:

### 9.2

- ****: API

## 10.

### 10.1

- MCP
- API

### 10.2

- Finviz API

## 11.

### 11.1

```python
logging.config.dictConfig({
 'version': 1,
 'disable_existing_loggers': False,
 'formatters': {
 'standard': {
 'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
 },
 },
 'handlers': {
 'default': {
 'level': 'INFO',
 'formatter': 'standard',
 'class': 'logging.StreamHandler',
 },
 },
 'loggers': {
 '': {
 'handlers': ['default'],
 'level': 'INFO',
 'propagate': False
 }
 }
})
```

### 11.2

- API

## 12.

### 12.1 Phase 1:

### 12.2 Phase 2:

### 12.3 Phase 3:

## 13.

MCP ServerFinvizMCPAPI