# Finviz MCP Server Complete Guide (2025 Edition)

Meta description: Use finviz-mcp-server to streamline daily stock screening. Cover earnings trades, dividend ideas, sector analysis, and more with MCP-based workflows.

## Why finviz-mcp-server?

Common problems with manual screening:
- Switching between multiple sites
- 1-2 hours spent on daily market checks
- Subjective, inconsistent screening criteria
- Fragmented data sources

What finviz-mcp-server delivers:
- Time savings: daily market checks in about 5 minutes
- Higher precision: 20+ advanced screening tools
- Automation: MCP tools for structured workflows
- Consistency: unified data source and formats

Cost note: Finviz Elite is required (around $25/month). The workflow savings usually pay for the subscription quickly.

## Full Setup Guide (about 10 minutes)

### Prerequisites

| Item | Requirement | Check |
|------|-------------|-------|
| Python | 3.11+ | `python3 --version` |
| Finviz Elite | Required | https://finviz.com/elite.ashx |
| Claude Desktop | Latest | https://claude.ai/download |

Important: The current implementation requires a Finviz Elite API key. Free Finviz accounts do not work.

---

### Step 1: Project setup (about 3 minutes)

```bash
# Create a project directory
mkdir ~/finviz-trading && cd ~/finviz-trading

# Create a Python virtual environment
python3.11 -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Install finviz-mcp-server
git clone https://github.com/your-repo/finviz-mcp-server.git
cd finviz-mcp-server
pip install -e .
```

### Step 2: Get a Finviz Elite API key (about 2 minutes)

Required: Finviz Elite subscription and API key.

How to get the key:
1. Subscribe at https://finviz.com/elite.ashx
2. Go to Account Settings -> API Access
3. Click Generate New API Key
4. Copy the key for Step 3

Without the API key, most features will not work.

### Step 3: Configure Claude Desktop MCP (about 5 minutes)

Config file locations:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Example config:

```json
{
  "mcpServers": {
    "finviz": {
      "command": "/Users/your-username/finviz-trading/finviz-mcp-server/venv/bin/finviz-mcp-server",
      "args": [],
      "cwd": "/Users/your-username/finviz-trading/finviz-mcp-server",
      "env": {
        "FINVIZ_API_KEY": "your_actual_finviz_elite_api_key_here",
        "LOG_LEVEL": "INFO",
        "RATE_LIMIT_REQUESTS_PER_MINUTE": "100"
      }
    }
  }
}
```

Notes:
- Use the absolute path to your venv `finviz-mcp-server` executable
- Set `cwd` to the project root
- Ensure the API key is correct

### Step 4: Verify the setup

Start Claude Desktop, open a new chat, and run a basic check such as:
- Ask for a market overview
- Request a simple earnings screener

If it works, you should receive a structured response.

## Daily Workflow (5-minute routine)

### 1) Market overview (about 90 seconds)

Goal: get a quick sense of market direction and risk.

Example prompt:
"Get a market overview for today and summarize key indices, sectors, and risk indicators."

Look for:
- S&P 500 and NASDAQ direction
- Sector leadership/laggards
- Volatility (VIX) context

### 2) Earnings focus (about 2 minutes)

Goal: identify earnings-driven opportunities.

Example:
```python
earnings_screener(
    earnings_date="today_after",
    market_cap="large",
    min_price=10,
    min_volume=1000000,
    sectors=["Technology", "Healthcare"]
)
```

### 3) Volume surge scan (about 60 seconds)

Goal: capture unusual activity and momentum.

Example:
```python
volume_surge_screener(
    market_cap="smallover",
    min_price=10,
    min_relative_volume=1.5,
    min_price_change=2.0,
    sma_filter="above_sma200"
)
```

## Strategy Playbooks

### A) Earnings trading

Use earnings-focused tools for premarket and after-hours moves:
- `earnings_premarket_screener`
- `earnings_afterhours_screener`
- `earnings_trading_screener`

### B) Dividend growth screening

```python
dividend_growth_screener(
    min_dividend_yield=2.0,
    min_dividend_growth=5.0,
    min_roe=10.0,
    max_debt_equity=0.6
)
```

### C) ETF strategy screening

```python
etf_screener(
    strategy_type="long",
    asset_class="equity",
    min_aum=1000,
    max_expense_ratio=0.5
)
```

### D) Sector rotation

1) Check sector performance
2) Filter within strong sectors

```python
get_sector_performance(timeframe="1w")
```

Then:
```python
volume_surge_screener(
    sectors=["Technology", "Healthcare"],
    min_relative_volume=2.0,
    min_price_change=3.0
)
```

### E) Technical screening

```python
technical_analysis_screener(
    rsi_min=40,
    rsi_max=70,
    price_vs_sma200="above",
    min_price=10,
    min_volume=500000
)
```

## News and SEC Filings

### News
```python
get_stock_news(ticker="AAPL", days_back=7)
get_market_news(days_back=3, max_items=20)
```

### SEC filings
```python
get_major_sec_filings(ticker="AAPL", days_back=90)
get_insider_sec_filings(ticker="AAPL", days_back=30)
```

## Prompting Tips

Good prompts are specific and structured:
- Include market cap, price, volume, and sector constraints
- Ask for a fixed number of results
- Specify output format (ticker, price, RSI, rationale)

Example:
"Find up to 5 technology stocks with market cap > $1B, RSI between 30-70, dividend yield > 2%. Return ticker, company, price, RSI, dividend yield, and a short reason."

## Troubleshooting

Common issues:

1) API key errors
- Confirm `FINVIZ_API_KEY` is set in the MCP config
- Re-start Claude Desktop completely

2) No data returned
- Verify filters are not too strict
- Test a simple screener with minimal constraints

3) Slow responses
- Reduce `max_results`
- Limit filters and sectors

4) Code changes not reflected
- Fully restart Claude Desktop
- Ensure MCP server processes are stopped and restarted

## Maintenance Checklist (Monthly)

- Confirm Finviz Elite subscription is active
- Check for MCP server updates
- Update Claude Desktop if needed
- Review rate limits and performance

## Disclaimer

This guide is for educational purposes only. Investing involves risk, and you are responsible for your own decisions. Past performance does not guarantee future results.

## Author

Experience: US equities trading and automation
Focus: screening, quantitative analysis, risk management
