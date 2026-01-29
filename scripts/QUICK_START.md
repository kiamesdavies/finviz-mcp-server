# Finviz HTML Analysis Quick Start Guide

## 🚀 Start the Analysis Fast

### Step 1: Obtain the HTML File
1. Open [Finviz Elite Screener](https://elite.finviz.com/screener.ashx) in your browser
2. Save the full page as `finviz_screen_page.html`
   - **Chrome**: Ctrl+S → select "Webpage, Complete" → Save
   - **Firefox**: Ctrl+S → select "Webpage, Complete" → Save
   - **Safari**: Cmd+S → select "Web Archive" or "Page Source" → Save

### Step 2: Run the Analysis
```bash
# Move to the scripts directory
cd scripts

# Install dependencies (first time only)
pip install beautifulsoup4 lxml

# Run the analysis
python quick_html_analyze.py
```

### Step 3: Check the Results
After the analysis finishes, the following files are generated:
- `finviz_filters_analysis_finviz_screen_page.md` - Readable Markdown format
- `finviz_filters_analysis_finviz_screen_page.json` - Structured data

## 📊 Using the Results

### Markdown File
- Detailed explanation for each filter item
- Category-organized list
- Examples of usage in actual URLs

### JSON File
- Machine-readable data format
- Useful for API development and scripting
- Can be used for filter value auto-completion

## 🔧 Troubleshooting

### Common Issues

#### 1. "HTML file not found"
**Solution:**
- Confirm the filename is `finviz_screen_page.html`
- Confirm it is placed in the `scripts` directory or its parent directory
- Specify the file path directly: `python quick_html_analyze.py /path/to/your/file.html`

#### 2. "Import error"
**Solution:**
```bash
pip install beautifulsoup4 lxml requests
```

#### 3. "No filters were detected"
**Solution:**
- Confirm the HTML file was saved completely
- Confirm the Finviz screener page (including the filter section) was saved
- Check the file size is not unusually small (typically 100KB+)

### Manual Runs

If you need more detailed control:
```bash
# Markdown only
python finviz_html_analyzer.py finviz_screen_page.html --format markdown

# JSON only
python finviz_html_analyzer.py finviz_screen_page.html --format json

# Analyze a different HTML file
python finviz_html_analyzer.py my_custom_finviz_page.html
```

## 💡 Tips

### 1. Update Docs
Use the generated Markdown file to update the project's parameter list

### 2. API Development
Use the JSON data to implement a Finviz-style screening API

### 3. Automation
Fetch and analyze HTML regularly to monitor new parameter additions

### 4. Filter Validation
Verify that the implemented screening parameters have correct values

## 📈 Next Steps

1. **Parameter implementation**: Expand screening features based on the analysis results
2. **Documentation updates**: Add newly discovered parameters to the docs
3. **Automation**: Integrate into a CI/CD pipeline to run analysis regularly
