# A New Approach to Trading and Investing with AI

## Overview

This article introduces a practical workflow that combines Finviz screening with AI-driven analysis. The goal is to reduce manual effort and make daily screening faster, more consistent, and easier to scale.

## Why combine Finviz with AI?

Finviz provides powerful screening filters, but manual use still requires:
- Repeated, time-consuming searches
- Careful record-keeping of parameters
- Multiple passes to refine results

AI adds:
- A natural-language interface for complex screens
- Consistent parameter selection
- The ability to chain steps (screen -> summarize -> refine)

## The workflow

1) Define your screening objective
- Earnings movers
- Volume surge momentum
- Dividend growth candidates
- Sector rotation

2) Run a structured screen
- Use finviz-mcp-server tools to apply consistent filters
- Save results for comparison and iteration

3) Summarize and prioritize
- Ask the AI to group by sector, volatility, or market cap
- Request short rationale per ticker

4) Track and review
- Keep a simple log of screens and outcomes
- Adjust filters based on performance

## Example: volume surge workflow

Prompt:
"Find small-cap stocks above the 200-day SMA with relative volume > 2 and price change > 3%. Return the top 10 with sector and RSI."

Follow-up:
"Summarize which sectors dominate this list and flag any outliers."

## Practical tips

- Keep filters consistent across days to compare results
- Use minimum price and volume thresholds to reduce noise
- Combine technical filters with fundamental guardrails

## Results to expect

Most users will see:
- Faster daily screening
- More repeatable decision criteria
- Better focus on high-signal candidates

## Disclaimer

This article is for educational purposes only. Investing involves risk, and all decisions are your responsibility.
