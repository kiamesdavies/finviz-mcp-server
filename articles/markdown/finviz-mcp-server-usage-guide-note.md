# Claude AI + Finviz: A Practical Upgrade for Stock Screening

## Cut hours to minutes

Finding good stocks is the hardest part of investing, but screening thousands of tickers manually is slow and error-prone. finviz-mcp-server turns Finviz screening into a natural-language workflow with Claude AI, so you can move from idea to shortlist in minutes.

What this note covers:
- How AI automates stock screening
- Why a $25/month Finviz Elite subscription can be worth it
- The core strategies you can run daily

## What is finviz-mcp-server?

finviz-mcp-server connects Claude AI to Finviz via MCP (Model Context Protocol). It exposes structured tools for:
- Earnings screening
- Volume surge detection
- Dividend growth and fundamentals
- Sector and industry analysis
- News and SEC filings

The key difference: you can express screens in plain English while keeping precise, repeatable filters under the hood.

## Why Finviz Elite is required

Finviz Elite unlocks:
- Full screening filters and advanced fields
- Faster data access
- More complete news and filings
- Larger, more reliable exports

Cost comparison (approximate):
- Bloomberg Terminal: $2,000/month
- FactSet: $1,500/month
- Refinitiv Eikon: $1,800/month
- Finviz Elite: $24.96/month

For most individual workflows, Finviz Elite covers the majority of what you need at a tiny fraction of the price.

## Five practical strategies

### 1) Earnings trade candidates
Use premarket and after-hours screeners to capture earnings-driven moves.

Example prompt:
"Find large-cap stocks reporting after the close with strong recent volume and positive revisions."

### 2) Volume surge momentum
Identify unusual volume + price strength early.

Example prompt:
"Show me small-cap stocks above the 200-day SMA with relative volume > 2."

### 3) Dividend growth focus
Filter for sustainable yield + quality.

Example prompt:
"Find dividend stocks with yield > 2%, ROE > 10%, and low debt."

### 4) Sector rotation
Track leadership and screen within the strongest sectors.

Example prompt:
"Summarize sector performance this week and list the top 5 tickers in the strongest sector."

### 5) Risk management
Use technical filters (RSI, SMA) to avoid weak setups.

Example prompt:
"Show stocks with RSI between 40 and 70 and price above the 200-day SMA."

## Setup in 3 steps (summary)

1) Install and run finviz-mcp-server in a Python 3.11 venv
2) Get your Finviz Elite API key
3) Add the MCP server config to Claude Desktop

If you have trouble, restart Claude Desktop fully after changes.

## Final note

This is an educational tool. Use it to build disciplined, repeatable screening workflows, not to replace judgment. Your risk is your own.
