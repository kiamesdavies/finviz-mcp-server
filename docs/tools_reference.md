# Finviz MCP Server - Tools Reference

## 🔍 Screening Tools

### `earnings_screener`
Basic screening for upcoming earnings

**Parameters:**
- `earnings_date` (required): Earnings date (`today_after`, `tomorrow_before`, `this_week`, `within_2_weeks`)
- `market_cap`: Market cap filter (`small`, `mid`, `large`, `mega`)
- `min_price`: Minimum price
- `min_volume`: Minimum volume
- `sectors`: Target sectors

### `volume_surge_screener`
Screen for rising stocks with volume surges

**Parameters:**
- `market_cap`: Market cap filter (default: `smallover`)
- `min_price`: Minimum price (default: 10)
- `min_relative_volume`: Minimum relative volume (default: 1.5)
- `min_price_change`: Minimum price change percent (default: 2.0%)
- `sma_filter`: Moving average filter (default: `above_sma200`)

### `trend_reversion_screener`
Screen for trend reversal candidates

**Parameters:**
- `market_cap`: Market cap filter (default: `mid_large`)
- `eps_growth_qoq`: Minimum EPS growth (QoQ)
- `revenue_growth_qoq`: Minimum revenue growth (QoQ)
- `rsi_max`: Maximum RSI
- `sectors`, `exclude_sectors`: Sector filters

### `uptrend_screener`
Screen for uptrend stocks

**Parameters:**
- `trend_type`: Trend type (`strong_uptrend`, `breakout`, `momentum`)
- `sma_period`: Moving average period (`20`, `50`, `200`)
- `relative_volume`: Minimum relative volume
- `price_change`: Minimum price change percent

### `dividend_growth_screener`
Screen for dividend growth stocks

**Parameters:**
- `min_dividend_yield`, `max_dividend_yield`: Dividend yield range
- `min_dividend_growth`: Minimum dividend growth rate
- `min_roe`: Minimum ROE
- `max_debt_equity`: Maximum debt-to-equity ratio

### `etf_screener`
ETF strategy screening

**Parameters:**
- `strategy_type`: Strategy type (`long`, `short`)
- `asset_class`: Asset class (`equity`, `bond`, `commodity`, `currency`)
- `min_aum`: Minimum assets under management
- `max_expense_ratio`: Maximum expense ratio

## 📈 Earnings-Related Screening

### `earnings_premarket_screener`
Stocks rising on premarket earnings

**Parameters:**
- `earnings_timing`: Earnings timing (default: `today_before`)
- `min_price_change`: Minimum price change percent (default: 2.0%)
- `include_premarket_data`: Include premarket data
- `max_results`: Max results (default: 60)

### `earnings_afterhours_screener`
Stocks rising in after-hours on earnings

**Parameters:**
- `earnings_timing`: Earnings timing (default: `today_after`)
- `min_afterhours_change`: Minimum after-hours change percent (default: 2.0%)
- `include_afterhours_data`: Include after-hours data
- `max_results`: Max results (default: 60)

### `earnings_trading_screener`
Earnings trading candidates (focus on revisions and surprises)

**Parameters:**
- `earnings_window`: Earnings window (default: `yesterday_after_today_before`)
- `earnings_revision`: Earnings revision filter (default: `eps_revenue_positive`)
- `price_trend`: Price trend filter (default: `positive_change`)
- `sort_by`: Sort key (default: `eps_surprise`)

### `earnings_winners_screener`
Earnings winners screening (weekly performance, EPS/revenue surprise)

**Parameters:**
- `earnings_period`: Earnings period (default: `this_week`)
- `market_cap`: Market cap filter (default: `smallover`)
- `min_price`: Minimum price (default: $10)
- `min_avg_volume`: Minimum average volume (default: o500 = 500,000+)
- `min_eps_growth_qoq`: Minimum EPS QoQ growth (%) (default: 10%)
- `min_eps_revision`: Minimum EPS revision (%) (default: 5%)
- `min_sales_growth_qoq`: Minimum revenue QoQ growth (%) (default: 5%)
- `min_weekly_performance`: Weekly performance filter (default: 5to-1w)
- `sma200_filter`: Above 200-day SMA filter (default: True)
- `target_sectors`: Target sectors (default: top 6 sectors)
- `max_results`: Max results (default: 50)
- `sort_by`: Sort key (`performance_1w`, `eps_growth_qoq`, `eps_surprise`, `price_change`, `volume`)
- `sort_order`: Sort order (`asc`, `desc`)

### `upcoming_earnings_screener`
Upcoming earnings next week (preparation for earnings trends)

**Parameters:**
- `earnings_period`: Earnings period (default: `next_week`)
- `market_cap`: Market cap filter (default: `smallover`)
- `min_price`: Minimum price (default: $10)
- `min_avg_volume`: Minimum average volume (default: 500,000)
- `target_sectors`: Target sectors (8 sectors)
- `max_results`: Max results (default: 100)
- `sort_by`: Sort key (`earnings_date`, `market_cap`, `target_price_upside`, `volatility`)
- `include_chart_view`: Include weekly chart view (default: True)
- `earnings_calendar_format`: Output in earnings calendar format (default: False)

## 📊 Fundamental Analysis

### `get_stock_fundamentals`
Get fundamentals for a single stock

**Parameters:**
- `ticker` (required): Stock ticker
- `data_fields`: List of data fields to fetch

### `get_multiple_stocks_fundamentals`
Batch fundamentals for multiple stocks

**Parameters:**
- `tickers` (required): List of stock tickers
- `data_fields`: List of data fields to fetch

## 📄 SEC Filing Analysis

### `get_sec_filings`
Get SEC filing list for a ticker

**Parameters:**
- `ticker` (required): Stock ticker
- `form_types`: Form type filter (e.g., `['10-K', '10-Q', '8-K']`)
- `days_back`: Lookback window in days (default: 30)
- `max_results`: Max results (default: 50)
- `sort_by`: Sort key (`filing_date`, `report_date`, `form`)
- `sort_order`: Sort order (`asc`, `desc`)

### `get_major_sec_filings`
Get major SEC filings (10-K, 10-Q, 8-K, etc.)

**Parameters:**
- `ticker` (required): Stock ticker
- `days_back`: Lookback window in days (default: 90)

### `get_insider_sec_filings`
Get insider-related SEC filings (Forms 3, 4, 5, etc.)

**Parameters:**
- `ticker` (required): Stock ticker
- `days_back`: Lookback window in days (default: 30)

### `get_sec_filing_summary`
Get SEC filing summary for a time window

**Parameters:**
- `ticker` (required): Stock ticker
- `days_back`: Lookback window in days (default: 90)

## 📰 News Analysis

### `get_stock_news`
Get stock-related news

**Parameters:**
- `ticker` (required): Stock ticker
- `days_back`: Lookback window in days (default: 7)
- `news_type`: News type (`all`, `earnings`, `analyst`, `insider`, `general`)

### `get_market_news`
Get market-wide news

**Parameters:**
- `days_back`: Lookback window in days (default: 3)
- `max_items`: Max items (default: 20)

### `get_sector_news`
Get sector-specific news

**Parameters:**
- `sector` (required): Sector name
- `days_back`: Lookback window in days (default: 5)
- `max_items`: Max items (default: 15)

## 🏭 Sector & Industry Analysis

### `get_sector_performance`
Sector performance analysis

**Parameters:**
- `timeframe`: Timeframe (`1d`, `1w`, `1m`, `3m`, `6m`, `1y`)
- `sectors`: Target sectors

### `get_industry_performance`
Industry performance analysis

**Parameters:**
- `timeframe`: Timeframe (`1d`, `1w`, `1m`, `3m`, `6m`, `1y`)
- `industries`: Target industries

### `get_country_performance`
Country-level market performance analysis

**Parameters:**
- `timeframe`: Timeframe (`1d`, `1w`, `1m`, `3m`, `6m`, `1y`)
- `countries`: Target countries

### `get_market_overview`
Get overall market overview

**Parameters:** none

## 📉 Technical Analysis

### `get_relative_volume_stocks`
Detect unusual relative volume stocks

**Parameters:**
- `min_relative_volume` (required): Minimum relative volume
- `min_price`: Minimum price
- `sectors`: Target sectors
- `max_results`: Max results (default: 50)

### `technical_analysis_screener`
Technical-analysis-based screening

**Parameters:**
- `rsi_min`, `rsi_max`: RSI range
- `price_vs_sma20`, `price_vs_sma50`, `price_vs_sma200`: Price vs. SMA (`above`, `below`)
- `min_price`: Minimum price
- `min_volume`: Minimum volume
- `sectors`: Target sectors
- `max_results`: Max results (default: 50)

## 🔧 Utilities

### `get_capitalization_performance`
Market-cap performance analysis

**Parameters:** none

### `get_sector_specific_industry_performance`
Industry performance within a sector

**Parameters:**
- `sector` (required): Sector name
- `timeframe`: Timeframe (`1d`, `1w`, `1m`, `3m`, `6m`, `1y`)

## 📋 Examples

### Basic screening
```python
# Find stocks with upcoming earnings
earnings_screener(
    earnings_date="today_after",
    market_cap="large",
    min_price=50
)

# Find volume surge stocks
volume_surge_screener(
    min_relative_volume=3.0,
    min_price_change=5.0
)
```

### Earnings analysis
```python
# Analyze earnings winners
earnings_winners_screener(
    earnings_period="this_week",
    sort_by="eps_surprise"
)

# Check next week's earnings
upcoming_earnings_screener(
    earnings_period="next_week",
    include_chart_view=True
)
```

### Fundamental analysis
```python
# Detailed data for a single stock
get_stock_fundamentals(ticker="AAPL")

# Compare multiple stocks
get_multiple_stocks_fundamentals(
    tickers=["AAPL", "MSFT", "GOOGL"]
)
```
