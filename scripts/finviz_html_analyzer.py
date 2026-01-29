#!/usr/bin/env python3
"""
Finviz HTML file analysis script.

Parses a saved Finviz HTML file and extracts all available filter
parameters and their values in detail.

Usage:
    python finviz_html_analyzer.py [html_file_path]
"""

from bs4 import BeautifulSoup
import json
import re
from dataclasses import dataclass
from typing import List, Dict, Optional
import sys
import os
from pathlib import Path
import argparse
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class FilterOption:
    """Filter option data class."""
    value: str
    label: str
    group: Optional[str] = None

@dataclass
class FilterParameter:
    """Filter parameter data class."""
    name: str
    id: str
    data_filter: str
    options: List[FilterOption]
    selected_value: Optional[str] = None
    category: Optional[str] = None
    data_url: Optional[str] = None
    data_url_selected: Optional[str] = None

class FinvizHTMLAnalyzer:
    """Finviz HTML analyzer."""
    
    def __init__(self, html_file_path: str):
        self.html_file_path = Path(html_file_path)
        self.filters = []
        
        # Filters to exclude (presets/personal settings)
        self.excluded_filters = {
            'screenerpresetsselect',     # Screener preset selection
            'screenerpresets',           # Screener preset
            'fs_screenerpresetsselect',  # Full ID version
            'fs_screenerpresets',        # Full ID version
        }
        
        if not self.html_file_path.exists():
            raise FileNotFoundError(f"HTML file not found: {html_file_path}")
        
        logger.info(f"Excluded filters: {', '.join(self.excluded_filters)}")
    
    def load_html(self) -> BeautifulSoup:
        """Load HTML file."""
        try:
            with open(self.html_file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            soup = BeautifulSoup(html_content, 'html.parser')
            logger.info(f"Loaded HTML file: {self.html_file_path}")
            return soup
            
        except UnicodeDecodeError:
            # If UTF-8 fails, try another encoding
            try:
                with open(self.html_file_path, 'r', encoding='iso-8859-1') as f:
                    html_content = f.read()
                soup = BeautifulSoup(html_content, 'html.parser')
                logger.info(f"Loaded HTML file (iso-8859-1): {self.html_file_path}")
                return soup
            except Exception as e:
                logger.error(f"HTML file read error: {e}")
                raise
        except Exception as e:
            logger.error(f"HTML file read error: {e}")
            raise
    
    def extract_filter_parameters(self) -> List[FilterParameter]:
        """Extract filter parameters."""
        try:
            soup = self.load_html()
            filters = []
            
            # Find select-tag filters (support multiple class patterns)
            select_patterns = [
                {'class': re.compile(r'screener-combo')},
                {'class': re.compile(r'fv-select')},
                {'class': re.compile(r'screener.*combo')},
                {'id': re.compile(r'^fs_')},  # IDs starting with fs_
            ]
            
            found_selects = set()  # Avoid duplicates
            
            for pattern in select_patterns:
                selects = soup.find_all('select', pattern)
                for select in selects:
                    select_id = select.get('id', '')
                    if select_id and select_id not in found_selects:
                        found_selects.add(select_id)
                        try:
                            filter_param = self._parse_select_element(select)
                            if filter_param:
                                filters.append(filter_param)
                        except Exception as e:
                            logger.warning(f"Select element parse error ({select_id}): {e}")
                            continue
            
            # Also find select elements with data-filter
            data_filter_selects = soup.find_all('select', attrs={'data-filter': True})
            for select in data_filter_selects:
                select_id = select.get('id', '')
                if select_id and select_id not in found_selects:
                    found_selects.add(select_id)
                    try:
                        filter_param = self._parse_select_element(select)
                        if filter_param:
                            filters.append(filter_param)
                    except Exception as e:
                        logger.warning(f"data-filter select parse error ({select_id}): {e}")
                        continue
            
            logger.info(f"Detected {len(filters)} filter parameters")
            
            # Sort filters by data-filter
            filters.sort(key=lambda x: x.data_filter)
            
            return filters
            
        except Exception as e:
            logger.error(f"Filter parameter extraction error: {e}")
            return []
    
    def _parse_select_element(self, select) -> Optional[FilterParameter]:
        """Parse a select element into a FilterParameter."""
        try:
            # Basic attributes
            select_id = select.get('id', '')
            data_filter = select.get('data-filter', '')
            data_url = select.get('data-url', '')
            data_url_selected = select.get('data-url-selected', '')
            
            if not data_filter and not select_id:
                return None
            
            # If data-filter is missing, infer from ID
            if not data_filter and select_id.startswith('fs_'):
                data_filter = select_id[3:]  # Remove fs_
            
            # Check excluded filters
            if (select_id.lower() in self.excluded_filters or 
                data_filter.lower() in self.excluded_filters):
                logger.debug(f"Excluded filter: {select_id} (data-filter: {data_filter})")
                return None
            
            # Parse options
            options = []
            current_group = None
            
            for element in select.find_all(['option', 'optgroup']):
                if element.name == 'optgroup':
                    current_group = element.get('label', '')
                elif element.name == 'option':
                    value = element.get('value', '')
                    label = element.get_text(strip=True)
                    
                    # Skip empty labels
                    if not label:
                        continue
                    
                    option = FilterOption(
                        value=value,
                        label=label,
                        group=current_group
                    )
                    options.append(option)
            
            # Get selected value
            selected_option = select.find('option', selected=True)
            if not selected_option:
                # Also check data-selected attribute
                selected_value = select.get('data-selected', '')
            else:
                selected_value = selected_option.get('value', '')
            
            return FilterParameter(
                name=self._get_filter_name_from_id(select_id, data_filter),
                id=select_id,
                data_filter=data_filter,
                options=options,
                selected_value=selected_value,
                data_url=data_url,
                data_url_selected=data_url_selected
            )
            
        except Exception as e:
            logger.warning(f"Error parsing select element: {e}")
            return None
    
    def _get_filter_name_from_id(self, element_id: str, data_filter: str = '') -> str:
        """Infer a filter name from element ID or data-filter."""
        # ID -> name mapping (extended)
        id_to_name = {
            'fs_exch': 'Exchange',
            'fs_idx': 'Index',
            'fs_sec': 'Sector',
            'fs_ind': 'Industry',
            'fs_geo': 'Country',
            'fs_cap': 'Market Cap',
            'fs_sh_price': 'Price',
            'fs_fa_div': 'Dividend Yield',
            'fs_fa_epsrev': 'EPS/Revenue Revision',
            'fs_sh_short': 'Short Float',
            'fs_an_recom': 'Analyst Recommendation',
            'fs_sh_opt': 'Option/Short',
            'fs_earningsdate': 'Earnings Date',
            'fs_ipodate': 'IPO Date',
            'fs_sh_avgvol': 'Average Volume',
            'fs_sh_relvol': 'Relative Volume',
            'fs_sh_curvol': 'Current Volume',
            'fs_sh_trades': 'Trades',
            'fs_sh_outstanding': 'Shares Outstanding',
            'fs_sh_float': 'Float',
            'fs_ta_perf2': 'Performance 2',
            'fs_ta_perf': 'Performance',
            'fs_targetprice': 'Target Price',
            'fs_ta_highlow52w': '52W High/Low',
            'fs_ta_sma20': 'SMA20 (20-day moving average)',
            'fs_ta_sma50': 'SMA50 (50-day moving average)',
            'fs_ta_sma200': 'SMA200 (200-day moving average)',
            'fs_ta_change': 'Change',
            'fs_ta_volume': 'Volume',
            'fs_fa_pe': 'P/E Ratio',
            'fs_fa_peg': 'PEG Ratio',
            'fs_fa_ps': 'P/S Ratio',
            'fs_fa_pb': 'P/B Ratio',
            'fs_fa_pc': 'P/C Ratio',
            'fs_fa_pfcf': 'P/FCF Ratio',
            'fs_fa_epsyoy': 'EPS Growth YoY',
            'fs_fa_epsqoq': 'EPS Growth QoQ',
            'fs_fa_salesyoy': 'Sales Growth YoY',
            'fs_fa_salesqoq': 'Sales Growth QoQ',
            'fs_fa_eps5y': 'EPS Growth 5Y',
            'fs_fa_sales5y': 'Sales Growth 5Y',
            'fs_fa_roe': 'ROE',
            'fs_fa_roa': 'ROA',
            'fs_fa_roi': 'ROI',
            'fs_fa_curratio': 'Current Ratio',
            'fs_fa_quickratio': 'Quick Ratio',
            'fs_fa_ltdebt': 'LT Debt/Eq',
            'fs_fa_debt': 'Debt/Eq',
            'fs_fa_grossmargin': 'Gross Margin',
            'fs_fa_opermargin': 'Operating Margin',
            'fs_fa_profitmargin': 'Profit Margin',
            'fs_fa_payout': 'Payout Ratio',
            'fs_fa_insiderown': 'Insider Own',
            'fs_fa_insidertrans': 'Insider Trans',
            'fs_fa_insthold': 'Inst Hold',
            'fs_fa_insttrans': 'Inst Trans',
        }
        
        # data-filter -> name mapping
        filter_to_name = {
            'exch': 'Exchange',
            'idx': 'Index',
            'sec': 'Sector',
            'ind': 'Industry',
            'geo': 'Country',
            'cap': 'Market Cap',
            'sh_price': 'Price',
            'fa_div': 'Dividend Yield',
            'fa_epsrev': 'EPS/Revenue Revision',
            'sh_short': 'Short Float',
            'an_recom': 'Analyst Recommendation',
            'sh_opt': 'Option/Short',
            'earningsdate': 'Earnings Date',
            'ipodate': 'IPO Date',
            'sh_avgvol': 'Average Volume',
            'sh_relvol': 'Relative Volume',
            'sh_curvol': 'Current Volume',
            'sh_trades': 'Trades',
            'sh_outstanding': 'Shares Outstanding',
            'sh_float': 'Float',
            'ta_perf2': 'Performance 2',
            'ta_perf': 'Performance',
            'targetprice': 'Target Price',
        }
        
        # Resolve by ID
        if element_id in id_to_name:
            return id_to_name[element_id]
        
        # Resolve by data-filter
        if data_filter in filter_to_name:
            return filter_to_name[data_filter]
        
        # Fallback
        if element_id:
            return element_id.replace('fs_', '').replace('_', ' ').title()
        elif data_filter:
            return data_filter.replace('_', ' ').title()
        else:
            return 'Unknown Filter'
    
    def categorize_filters(self, filters: List[FilterParameter]) -> Dict[str, List[FilterParameter]]:
        """Categorize filters by category."""
        categories = {
            'Basic info parameters': [],
            'Price/Market Cap parameters': [],
            'Dividend/Financial parameters': [],
            'Analyst/Recommendation parameters': [],
            'Date parameters': [],
            'Volume/Trading parameters': [],
            'Share issuance parameters': [],
            'Technical analysis parameters': [],
            'Other parameters': []
        }
        
        category_keywords = {
            'Basic info parameters': ['exchange', 'index', 'sector', 'industry', 'country', 'exch', 'idx', 'sec', 'ind', 'geo'],
            'Price/Market Cap parameters': ['market cap', 'price', 'target price', 'cap', 'sh_price', 'targetprice'],
            'Dividend/Financial parameters': ['dividend', 'eps', 'revenue', 'short', 'pe', 'pb', 'ps', 'roe', 'roa', 'margin', 'debt', 'fa_'],
            'Analyst/Recommendation parameters': ['analyst', 'recommendation', 'an_recom'],
            'Date parameters': ['earnings date', 'ipo date', 'earningsdate', 'ipodate'],
            'Volume/Trading parameters': ['volume', 'trades', 'sh_avgvol', 'sh_relvol', 'sh_curvol', 'sh_trades'],
            'Share issuance parameters': ['shares', 'float', 'outstanding', 'sh_outstanding', 'sh_float'],
            'Technical analysis parameters': ['performance', 'sma', 'change', 'high', 'low', 'ta_'],
        }
        
        for filter_param in filters:
            assigned = False
            search_text = f"{filter_param.name.lower()} {filter_param.data_filter.lower()}"
            
            for category, keywords in category_keywords.items():
                if any(keyword in search_text for keyword in keywords):
                    categories[category].append(filter_param)
                    assigned = True
                    break
            
            if not assigned:
                categories['Other parameters'].append(filter_param)
        
        return categories
    
    def export_to_markdown(self, filters: List[FilterParameter], output_file: str = None):
        """Export filter information to Markdown."""
        if output_file is None:
            output_file = f"finviz_filters_analysis_{self.html_file_path.stem}.md"
        
        try:
            categorized_filters = self.categorize_filters(filters)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("# Finviz Filter Parameter Details\n\n")
                f.write(f"HTML file: `{self.html_file_path.name}`\n")
                f.write(f"Analyzed at: {os.path.getctime(self.html_file_path)}\n\n")
                f.write("This document lists all parameters available in Finviz screening, along with their possible values.\n\n")
                
                for category, category_filters in categorized_filters.items():
                    if not category_filters:
                        continue
                        
                    f.write(f"## {category}\n\n")
                    
                    for filter_param in category_filters:
                        f.write(f"### {filter_param.name} - `{filter_param.data_filter}`\n")
                        
                        if filter_param.selected_value:
                            f.write(f"**Current selected value**: `{filter_param.selected_value}`\n\n")
                        
                        if filter_param.options:
                            # Switch layout depending on whether groups exist
                            has_groups = any(option.group for option in filter_param.options)
                            
                            if has_groups:
                                f.write("| Value | Description | Group |\n")
                                f.write("|---|---|---|\n")
                                
                                for option in filter_param.options:
                                    group = option.group or "-"
                                    f.write(f"| `{option.value}` | {option.label} | {group} |\n")
                            else:
                                f.write("| Value | Description |\n")
                                f.write("|---|---|\n")
                                
                                for option in filter_param.options:
                                    f.write(f"| `{option.value}` | {option.label} |\n")
                            
                            f.write("\n")
                        
                        # Include data-url if present
                        if filter_param.data_url:
                            f.write(f"**Data URL**: `{filter_param.data_url}`\n\n")
                        
                        f.write("\n")
                
                # Usage section
                f.write("## Usage\n\n")
                f.write("These parameters are used as URL query parameters for Finviz screening.\n\n")
                f.write("### Example:\n")
                f.write("```\n")
                f.write("https://finviz.com/screener.ashx?v=111&f=cap_large,sec_technology,ta_perf_1w_o5\n")
                f.write("```\n\n")
                f.write("### Combining multiple conditions:\n")
                f.write("- You can specify multiple parameters separated by commas\n")
                f.write("- Parameters from different categories are combined with AND\n")
                f.write("- Multiple values within the same category are combined with OR (with a few exceptions)\n\n")
            
            logger.info(f"Wrote filter info to {output_file}")
            
        except Exception as e:
            logger.error(f"Markdown export error: {e}")
    
    def export_to_json(self, filters: List[FilterParameter], output_file: str = None):
        """Export filter information to JSON."""
        if output_file is None:
            output_file = f"finviz_filters_analysis_{self.html_file_path.stem}.json"
        
        try:
            filter_data = {
                'source_file': str(self.html_file_path),
                'total_filters': len(filters),
                'filters': []
            }
            
            for filter_param in filters:
                options_data = []
                for option in filter_param.options:
                    options_data.append({
                        'value': option.value,
                        'label': option.label,
                        'group': option.group
                    })
                
                filter_info = {
                    'name': filter_param.name,
                    'id': filter_param.id,
                    'data_filter': filter_param.data_filter,
                    'selected_value': filter_param.selected_value,
                    'options_count': len(options_data),
                    'options': options_data
                }
                
                # Include data-url if present
                if filter_param.data_url:
                    filter_info['data_url'] = filter_param.data_url
                if filter_param.data_url_selected:
                    filter_info['data_url_selected'] = filter_param.data_url_selected
                
                filter_data['filters'].append(filter_info)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(filter_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Wrote filter info to {output_file}")
            
        except Exception as e:
            logger.error(f"JSON export error: {e}")
    
    def print_summary(self, filters: List[FilterParameter]):
        """Print a summary of analysis results."""
        print("\n" + "="*60)
        print("📊 Finviz Filter Analysis Summary")
        print("="*60)
        
        categorized = self.categorize_filters(filters)
        
        print(f"📄 Source file: {self.html_file_path.name}")
        print(f"🔢 Total filters: {len(filters)}")
        print(f"📂 Category count: {len([c for c, f in categorized.items() if f])}")
        
        print("\n📋 Category breakdown:")
        for category, category_filters in categorized.items():
            if category_filters:
                print(f"  📊 {category}: {len(category_filters)} items")
        
        # Top 5 filters (by option count)
        top_filters = sorted(filters, key=lambda x: len(x.options), reverse=True)[:5]
        print("\n🔝 Top 5 filters by option count:")
        for i, filter_param in enumerate(top_filters, 1):
            print(f"  {i}. {filter_param.name}: {len(filter_param.options)} options")
        
        print("\n" + "="*60)
    
    def analyze(self, export_format: str = 'both'):
        """Run full analysis."""
        try:
            logger.info("Starting filter analysis...")
            
            # Extract filters
            filters = self.extract_filter_parameters()
            
            if not filters:
                logger.error("No filters detected")
                return False
            
            # Show summary
            self.print_summary(filters)
            
            # Output results
            if export_format in ['markdown', 'both']:
                self.export_to_markdown(filters)
            
            if export_format in ['json', 'both']:
                self.export_to_json(filters)
            
            return True
            
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            return False

def main():
    """Main entry function."""
    parser = argparse.ArgumentParser(
        description='Finviz HTML analysis tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python finviz_html_analyzer.py finviz_screen_page.html
  python finviz_html_analyzer.py finviz_screen_page.html --format json
  python finviz_html_analyzer.py finviz_screen_page.html --format markdown
        """
    )
    
    parser.add_argument(
        'html_file',
        nargs='?',
        default='finviz_screen_page.html',
        help='Path to the HTML file to analyze (default: finviz_screen_page.html)'
    )
    
    parser.add_argument(
        '--format', '-f',
        choices=['markdown', 'json', 'both'],
        default='both',
        help='Output format (default: both)'
    )
    
    args = parser.parse_args()
    
    print("🔍 Finviz HTML Filter Analysis Tool")
    print("="*50)
    
    try:
        # Initialize analyzer
        analyzer = FinvizHTMLAnalyzer(args.html_file)
        
        # Run analysis
        success = analyzer.analyze(export_format=args.format)
        
        if success:
            print("\n✅ Analysis complete!")
            
            # Check output files
            stem = Path(args.html_file).stem
            
            if args.format in ['markdown', 'both']:
                md_file = f"finviz_filters_analysis_{stem}.md"
                if os.path.exists(md_file):
                    size = os.path.getsize(md_file) / 1024
                    print(f"📄 {md_file} ({size:.1f} KB)")
            
            if args.format in ['json', 'both']:
                json_file = f"finviz_filters_analysis_{stem}.json"
                if os.path.exists(json_file):
                    size = os.path.getsize(json_file) / 1024
                    print(f"📊 {json_file} ({size:.1f} KB)")
        else:
            print("\n❌ Analysis failed")
            return 1
            
    except FileNotFoundError as e:
        print(f"❌ File error: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 
