# Finviz Custom Range Analysis (Detailed)

HTML file: `finviz_screen_page.html`

This document details URL patterns when specifying custom ranges (manual inputs) in Finviz.

## 🎯 Range-Capable Filters

Detected range-capable filters: **20**

### Analyst Recommendation - `an_recom`

### Market Cap - `cap`
#### 📊 Range Examples

| Range | URL Parameter | Description | Full URL Example |
|---|---|---|---|
| `1to10` | `cap_1to10` | Market Cap: $1B to $10B | `https://finviz.com/screener.ashx?v=111&f=cap_1to10` |
| `10to50` | `cap_10to50` | Market Cap: $10B to $50B | `https://finviz.com/screener.ashx?v=111&f=cap_10to50` |
| `2to20` | `cap_2to20` | Market Cap: $2B to $20B | `https://finviz.com/screener.ashx?v=111&f=cap_2to20` |

- **Data type**: currency
- **Unit**: USD (Billions)
- **Format**: Market Cap: ${min}B to ${max}B

### Earnings Date - `earningsdate`

### Exchange - `exch`

### Dividend Yield - `fa_div`
#### 📊 Range Examples

| Range | URL Parameter | Description | Full URL Example |
|---|---|---|---|
| `2to5` | `fa_div_2to5` | Dividend: 2% to 5% | `https://finviz.com/screener.ashx?v=111&f=fa_div_2to5` |
| `5to10` | `fa_div_5to10` | Dividend: 5% to 10% | `https://finviz.com/screener.ashx?v=111&f=fa_div_5to10` |
| `1to3` | `fa_div_1to3` | Dividend: 1% to 3% | `https://finviz.com/screener.ashx?v=111&f=fa_div_1to3` |

- **Data type**: percentage
- **Unit**: %
- **Format**: Dividend: {min}% to {max}%

### Country - `geo`

### Index - `idx`

### Industry - `ind`

### IPO Date - `ipodate`

### Sector - `sec`

### Average Volume - `sh_avgvol`
#### 📊 Range Examples

| Range | URL Parameter | Description | Full URL Example |
|---|---|---|---|
| `100to500` | `sh_avgvol_100to500` | Volume: 100K to 500K | `https://finviz.com/screener.ashx?v=111&f=sh_avgvol_100to500` |
| `500to1000` | `sh_avgvol_500to1000` | Volume: 500K to 1000K | `https://finviz.com/screener.ashx?v=111&f=sh_avgvol_500to1000` |
| `1000to5000` | `sh_avgvol_1000to5000` | Volume: 1000K to 5000K | `https://finviz.com/screener.ashx?v=111&f=sh_avgvol_1000to5000` |

- **Data type**: volume
- **Unit**: K shares
- **Format**: Volume: {min}K to {max}K

### Current Volume - `sh_curvol`

### Float - `sh_float`

### Option/Short - `sh_opt`

### Shares Outstanding - `sh_outstanding`

### Price - `sh_price`
#### 📊 Range Examples

| Range | URL Parameter | Description | Full URL Example |
|---|---|---|---|
| `10to50` | `sh_price_10to50` | Price: $10 to $50 | `https://finviz.com/screener.ashx?v=111&f=sh_price_10to50` |
| `5to20` | `sh_price_5to20` | Price: $5 to $20 | `https://finviz.com/screener.ashx?v=111&f=sh_price_5to20` |
| `1to10` | `sh_price_1to10` | Price: $1 to $10 | `https://finviz.com/screener.ashx?v=111&f=sh_price_1to10` |

- **Data type**: currency
- **Unit**: USD
- **Format**: Price: ${min} to ${max}

### Relative Volume - `sh_relvol`
#### 📊 Range Examples

| Range | URL Parameter | Description | Full URL Example |
|---|---|---|---|
| `1to3` | `sh_relvol_1to3` | Rel Volume: 1x to 3x | `https://finviz.com/screener.ashx?v=111&f=sh_relvol_1to3` |
| `2to5` | `sh_relvol_2to5` | Rel Volume: 2x to 5x | `https://finviz.com/screener.ashx?v=111&f=sh_relvol_2to5` |
| `0.5to2` | `sh_relvol_0.5to2` | Rel Volume: 0.5x to 2x | `https://finviz.com/screener.ashx?v=111&f=sh_relvol_0.5to2` |

- **Data type**: numeric
- **Unit**: multiplier
- **Format**: Rel Volume: {min}x to {max}x

### Short Float - `sh_short`

### Trades - `sh_trades`

### Target Price - `targetprice`

## 🔗 URL Pattern Structure Analysis

### Basic Structure
```
https://finviz.com/screener.ashx?v=111&f=[filter1],[filter2],[filter3]
```

### Custom Range Patterns
| Filter | Pattern | Example |
|---|---|---|
| `sh_price` | `sh_price_{min}to{max}` | `sh_price_10to50` |
| `cap` | `cap_{min}to{max}` | `cap_1to10` |
| `sh_avgvol` | `sh_avgvol_{min}to{max}` | `sh_avgvol_100to500` |
| `fa_pe` | `fa_pe_{min}to{max}` | `fa_pe_5to20` |
| `fa_div` | `fa_div_{min}to{max}` | `fa_div_2to5` |
| `sh_relvol` | `sh_relvol_{min}to{max}` | `sh_relvol_1to3` |
| `ta_perf` | `ta_perf_{min}to{max}` | `ta_perf_5to20` |
| `fa_pb` | `fa_pb_{min}to{max}` | `fa_pb_1to5` |
| `fa_ps` | `fa_ps_{min}to{max}` | `fa_ps_1to10` |
| `fa_roe` | `fa_roe_{min}to{max}` | `fa_roe_10to30` |
| `fa_roa` | `fa_roa_{min}to{max}` | `fa_roa_5to20` |
| `fa_roi` | `fa_roi_{min}to{max}` | `fa_roi_10to30` |
| `fa_curratio` | `fa_curratio_{min}to{max}` | `fa_curratio_1to5` |
| `fa_quickratio` | `fa_quickratio_{min}to{max}` | `fa_quickratio_0.5to3` |
| `fa_debteq` | `fa_debteq_{min}to{max}` | `fa_debteq_0to1` |
| `fa_ltdebteq` | `fa_ltdebteq_{min}to{max}` | `fa_ltdebteq_0to0.5` |
| `fa_grossmargin` | `fa_grossmargin_{min}to{max}` | `fa_grossmargin_20to60` |
| `fa_opermargin` | `fa_opermargin_{min}to{max}` | `fa_opermargin_5to30` |
| `fa_profitmargin` | `fa_profitmargin_{min}to{max}` | `fa_profitmargin_5to30` |
| `ta_beta` | `ta_beta_{min}to{max}` | `ta_beta_0.5to1.5` |
| `ta_volatility` | `ta_volatility_{min}to{max}` | `ta_volatility_5to15` |

## 💡 Practical Examples

### 1. Stocks priced $10-$50
**URL**: `https://finviz.com/screener.ashx?v=111&f=sh_price_10to50`

**Description**: $10$50

### 2. Mid-cap stocks with $1B-$10B market cap
**URL**: `https://finviz.com/screener.ashx?v=111&f=cap_1to10`

**Description**: $1B$10B

### 3. Value stocks with P/E 10-20
**URL**: `https://finviz.com/screener.ashx?v=111&f=fa_pe_10to20`

**Description**: PER1020

### 4. High-dividend stocks with 3-7% yield
**URL**: `https://finviz.com/screener.ashx?v=111&f=fa_div_3to7`

**Description**: 3%7%

### 5. Combined: Technology × mid-cap × reasonable P/E
**URL**: `https://finviz.com/screener.ashx?v=111&f=sec_technology,cap_1to10,fa_pe_10to25`

**Description**: PER10-25

## 🎯 Range Input Best Practices

### 📈 Numeric formats
- **Integers**: `10to50` (10 to 50)
- **Decimals**: `1.5to3.5` (1.5 to 3.5)
- **Negative values**: `-10to10` (-10% to +10%)

### 💰 Currency and unit considerations
- **Price**: USD `sh_price_10to50` ($10-$50)
- **Market cap**: billions USD `cap_1to10` ($1B-$10B)
- **Volume**: thousands of shares `sh_avgvol_100to500` (100K-500K)

### ⚠️ Notes
- Ensure min is less than max
- Extreme values may return zero results
- Some filters only support specific ranges

