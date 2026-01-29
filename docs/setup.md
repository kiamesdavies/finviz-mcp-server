# Finviz MCP Server Setup Guide

## 1. Environment Check

Confirm Python is installed:
```bash
python3 --version
```

## 2. Install Dependencies

```bash
pip3 install -r requirements.txt
```

## 3. Environment Setup (Optional)

If you have a Finviz Elite API key:
```bash
cp .env.example .env
# Edit the .env file and add your API key
```

## 4. Run Basic Tests

```bash
python3 test_basic.py
```

## 5. Start the Server

### Method 1: Direct Run
```bash
python3 run_server.py
```

### Method 2: Run as a Module
```bash
python3 -m src.server
```

## 6. Connect with an MCP Client

Once the server is running, you can connect from an MCP-compatible client (such as Claude Desktop).

### Example Configuration for Claude Desktop

Add the following to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "finviz": {
      "command": "python3",
      "args": ["/path/to/finviz-mcp-server/run_server.py"],
      "env": {}
    }
  }
}
```

## 7. Available Tools

### Basic Screening
- `earnings_screener`: Upcoming earnings
- `volume_surge_screener`: Volume surge stocks
- `get_stock_fundamentals`: Single-stock fundamentals
- `get_multiple_stocks_fundamentals`: Batch fundamentals for multiple stocks

### Advanced Screening (Based on the design doc)
- `earnings_premarket_screener`: Premarket earnings
- `earnings_afterhours_screener`: After-hours earnings
- `earnings_trading_screener`: Earnings-trading candidates

## 8. Examples

### Earnings Screening
```
earnings_screener(
    earnings_date="today_after",
    market_cap="large", 
    min_price=10,
    sectors=["Technology"]
)
```

### Volume Surge Stocks
```
volume_surge_screener(
    min_relative_volume=2.0,
    min_price_change=5.0,
    market_cap="mid"
)
```

### Single Stock Fundamentals
```
get_stock_fundamentals(ticker="AAPL")
```

## 9. Troubleshooting

### Dependency Errors
```bash
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

### Environment Variable Issues
Confirm the `.env` file is in the correct location

### Rate Limit Errors
Set a Finviz Elite API key or adjust request intervals

## 10. Logs and Debugging

To change the log level, set an environment variable:
```bash
export LOG_LEVEL=DEBUG
python3 run_server.py
```

## Notes

1. This tool is for educational and research purposes only
2. Investment decisions are your own responsibility
3. Follow Finviz's terms of service
4. Avoid excessive requests and use appropriate intervals for the API
