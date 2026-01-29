# 🔍 Finviz Elite Filter Analysis Tools

A set of Python tools to comprehensively analyze Finviz filter options. These tools explore Elite-grade screening features in depth and generate documentation.

## 📋 Table of Contents

- [🚀 Quick Start](#-quick-start)
- [🛠️ Tool List](#️-tool-list)
- [💡 Examples](#-examples)
- [📊 Analysis Results](#-analysis-results)
- [⚙️ Configuration and Customization](#️-configuration-and-customization)
- [🔧 Troubleshooting](#-troubleshooting)

## 🚀 Quick Start

### Easiest method (recommended)

```bash
# Move to the scripts directory
cd scripts

# HTML file analysis (fast, recommended)
python quick_html_analyze.py

# Custom range analysis (range-based URLs)
python quick_range_analyze.py
```

### Manually specify a file

```bash
# Analyze a specific HTML file
python finviz_html_analyzer.py ../docs/finviz_screen_page.html

# Analyze custom range patterns
python finviz_range_analyzer.py ../docs/finviz_screen_page.html
```

## 🛠️ Tool List

### 📄 HTML File Analysis (recommended)

| Tool | Description | Highlights |
|------|-------------|------------|
| `finviz_html_analyzer.py` | Engine for parsing saved HTML files | ⚡ Fast, 🔒 No login required |
| `quick_html_analyze.py` | Simple wrapper for HTML analysis | 🎯 One-command run |

### 🎯 Custom Range Analysis (NEW!)

| Tool | Description | Highlights |
|------|-------------|------------|
| `finviz_range_analyzer.py` | Analyze URL patterns for custom ranges | 📈 Range syntax, 🔗 URL generation |
| `quick_range_analyze.py` | Simple wrapper for custom range analysis | 💡 Practical examples |

### 🌐 Elite Live Analysis (advanced)

| Tool | Description | Highlights |
|------|-------------|------------|
| `finviz_elite_analyzer.py` | Live analysis via Selenium | 🔄 Real-time, 🔐 Login required |
| `quick_analyze.py` | Simple wrapper for Elite analysis | 🚀 Automation-ready |

## 💡 Examples

### Basic filter analysis

```bash
# Parse all filters from an HTML file
python quick_html_analyze.py

# Output: finviz_filters_analysis_finviz_screen_page.md (75+ filters)
# Output: finviz_filters_analysis_finviz_screen_page.json (detailed data)
```

### Custom range analysis

```bash
# Analyze range-based URL patterns
python quick_range_analyze.py

# Example outputs:
# - sh_price_10to50 → Price $10-$50
# - cap_1to10 → Market cap $1B-$10B
# - fa_pe_10to20 → P/E 10-20
# - fa_div_3to7 → Dividend yield 3-7%
```

### Specific output formats

```bash
# Markdown only
python finviz_html_analyzer.py --format markdown

# JSON only
python finviz_range_analyzer.py --format json
```

## 📊 Analysis Results

### 📋 Base Filter Analysis

- Automatically detects **75+ filter items**
- Extracts **thousands of option values** in detail
- Auto-classifies into **8 major categories**:
  - 📈 Basic info (exchanges, indices, sectors, etc.)
  - 💰 Price & market cap
  - 📊 Financial & profitability
  - 🔄 Volume & trading
  - 📅 Dates & events
  - 🎯 Technical analysis
  - 👥 Analysts & recommendations
  - ⚙️ Other & special

### 🎯 Custom Range Analysis (NEW!)

- Identifies **range-capable filters**
- Detailed analysis of **URL pattern structures**
- **Practical examples** and best practices
- **20+ known patterns** such as:
  - 💵 Price range: `sh_price_10to50`
  - 📊 Market cap: `cap_1to10`
  - 📈 P/E range: `fa_pe_10to20`
  - 💎 Dividend yield: `fa_div_3to7`
  - 📉 Beta range: `ta_beta_0.5to1.5`

### 📁 Output Formats

#### Markdown (docs)
- `finviz_filters_analysis_*.md` - Base filter analysis
- `finviz_range_analysis_*.md` - Custom range analysis

#### JSON (programmatic)
- `finviz_filters_analysis_*.json` - Structured data
- `finviz_range_analysis_*.json` - Range pattern data

## ⚙️ Configuration and Customization

### 🎛️ Analysis parameters

```python
# Exclude filters
EXCLUDE_FILTERS = ['generic_filter', 'test_*']

# Output limit
MAX_OPTIONS_PER_FILTER = 1000

# Add known range patterns
CUSTOM_RANGE_PATTERNS = {
    'my_filter': {
        'type': 'percentage',
        'unit': '%',
        'examples': ['5to20', '10to30']
    }
}
```

### 🔧 Output customization

```bash
# Analyze specific categories only
python finviz_html_analyzer.py --categories "basic,financial"

# Choose detail level
python finviz_range_analyzer.py --detail-level high
```

## 🔧 Troubleshooting

### Common issues and solutions

#### 1. HTML file not found

```bash
❌ finviz_screen_page.html not found

✅ Solution:
- Confirm docs/finviz_screen_page.html exists
- Provide an explicit path: python quick_html_analyze.py ../docs/finviz_screen_page.html
```

#### 2. Empty analysis results

```bash
❌ No filters were detected

✅ Solution:
- Confirm the HTML file is a valid Finviz page
- Confirm the file size is reasonable (typically 100KB+)
- Possible encoding issue → re-save as UTF-8
```

#### 3. ImportError

```bash
❌ ImportError: No module named 'bs4'

✅ Solution:
pip install -r requirements.txt
```

### 📞 Support
