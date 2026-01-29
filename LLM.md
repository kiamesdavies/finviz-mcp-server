# Finviz MCP Server - AI Reference

## Parameter Values

**market_cap:** `small` | `mid` | `large` | `mega` | `smallover` | `midover`
**earnings_date:** `today_after` | `today_before` | `this_week` | `next_week` | `within_2_weeks`
**sectors:** `Technology` | `Healthcare` | `Financial Services` | `Industrials` | `Consumer Cyclical` | `Communication Services`

### Subthemes (Finviz Elite Thematic Filters)
Use format: `subtheme="themename"`. Examples:
- **AI:** `aicloud`, `aicompute`, `aimodels`, `aienterprise`, `airobotics`, `aisecurity`
- **Semis:** `semismemory`, `semisfoundries`, `semislithography`, `semispackaging`, `semisanalog`
- **Defense:** `defensedrones`, `defensespacetech`, `defensemissiles`, `defensecyberdefense`
- **Healthcare:** `healthcareoncology`, `healthcaremetabolic`, `healthcaregenomics`
- **Energy:** `energycleansolar`, `energycleanwind`, `energycleanhydrogen`, `commenergyuranium`
- **Space:** `spacesatellites`, `spaceinfrastructure`, `spacelaunch`
- **EVs:** `evsbatteries`, `evscharging`, `evsmanufacturers`
- **Fintech:** `fintechpayments`, `fintechblockchain`, `fintechneobanks`
- **Quantum:** `quantumhardware`, `quantumsoftware`, `quantumcloud`
- **Robotics:** `roboticsautomation`, `roboticslogistics`, `roboticsmedical`

Full list: 240+ themes covering AI, automation, blockchain, cloud, cybersecurity, defense, ecommerce, energy, EVs, fintech, hardware, healthcare, IoT, longevity, nanotech, quantum, robotics, semiconductors, software, space, telecom, transportation, VR, wearables.

---

## Screeners

### earnings_screener
```python
earnings_screener(
    earnings_date="today_after",  # REQUIRED
    market_cap="large",
    min_price=10,
    sectors=["Technology"],
    subtheme="aicloud"
)
```

### volume_surge_screener / uptrend_screener
**Fixed conditions - NO parameters**
```python
volume_surge_screener()  # $10+, 2%+ up, 1.5x rel vol, above SMA200
uptrend_screener()       # 4W up, above SMA20/200, SMA50>SMA200
```

### trend_reversion_screener
```python
trend_reversion_screener(
    market_cap="large",
    rsi_max=30,
    eps_growth_qoq=10.0,
    subtheme="semismemory"
)
```

### dividend_growth_screener
```python
dividend_growth_screener(
    min_dividend_yield=2.5,
    max_pe_ratio=25.0,
    min_roe=15.0,
    subtheme="energycleanutilities"
)
```

### technical_analysis_screener
```python
technical_analysis_screener(
    rsi_max=30,
    price_vs_sma200="below",
    min_price=10,
    subtheme="defensedrones"
)
```

### get_relative_volume_stocks
```python
get_relative_volume_stocks(
    min_relative_volume=2.0,  # REQUIRED
    min_price=10,
    subtheme="aicompute"
)
```

### etf_screener
```python
etf_screener(strategy_type="long", asset_class="equity")  # bond, commodity, currency
```

---

## Earnings Tools

### earnings_premarket_screener / earnings_afterhours_screener / earnings_trading_screener
**Fixed conditions - NO parameters**
```python
earnings_premarket_screener()   # Today premarket, 2%+ up
earnings_afterhours_screener()  # Today after hours, 2%+ up
earnings_trading_screener()     # Yesterday/today, EPS revision up
```

### earnings_winners_screener
```python
earnings_winners_screener(
    earnings_period="this_week",
    min_eps_growth_qoq=15.0,
    target_sectors=["Technology"],
    subtheme="aicloud"
)
```

### upcoming_earnings_screener
```python
upcoming_earnings_screener(
    earnings_period="next_week",
    market_cap="large",
    sort_by="market_cap",
    subtheme="healthcareoncology"
)
```

---

## Fundamentals

```python
get_stock_fundamentals(ticker="NVDA")
get_stock_fundamentals(ticker="AAPL", data_fields=["price", "p_e", "market_cap"])

get_multiple_stocks_fundamentals(tickers=["AAPL", "MSFT", "NVDA"])

get_moving_average_position(ticker="TSLA")
```

**Common fields:** `price`, `market_cap`, `p_e`, `forward_p_e`, `eps_ttm`, `dividend_yield`, `performance_week`, `performance_month`, `relative_strength_index_14`, `beta`, `eps_surprise`, `revenue_surprise`

---

## News

```python
get_stock_news(tickers="NVDA", days_back=7, news_type="earnings")
get_market_news(days_back=3, max_items=20)
get_sector_news(sector="Technology", days_back=5)
```

---

## Market Analysis

```python
get_market_overview()
get_sector_performance()
get_industry_performance()
get_sector_specific_industry_performance(sector="technology")
get_capitalization_performance()
get_country_performance(countries=["USA", "China"])
```

---

## SEC Filings

```python
get_sec_filings(ticker="AAPL", form_types=["10-K", "10-Q"], days_back=90)
get_major_sec_filings(ticker="AAPL")
get_insider_sec_filings(ticker="AAPL")
get_sec_filing_summary(ticker="AAPL")
```

---

## Field Discovery

```python
list_available_fields()
get_field_categories()
describe_field(field_name="eps_surprise")
search_fields(keyword="growth")
validate_fields(field_names=["price", "p_e", "invalid_field"])
```

---

## EDGAR API

```python
get_edgar_company_filings(ticker="AAPL", form_types=["10-K"], days_back=365)
get_edgar_company_facts(ticker="AAPL")
get_edgar_company_concept(ticker="AAPL", concept="Revenues", taxonomy="us-gaap")
get_edgar_filing_content(ticker="AAPL", accession_number="...", primary_document="...")
get_multiple_edgar_filing_contents(ticker="AAPL", filings_data=[{"accession_number": "...", "primary_document": "..."}])
```
