#!/usr/bin/env python3
"""
Finviz Custom Range Analysis Script

Analyzes URL patterns used when specifying custom ranges (manual range inputs) in Finviz.
In addition to standard filter analysis, it extracts dynamic URL patterns for range inputs.

Usage:
    python finviz_range_analyzer.py [html_file_path]
"""

from bs4 import BeautifulSoup
import json
import re
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import sys
import os
from pathlib import Path
import argparse
import logging

# Import the existing HTML analyzer
try:
    from finviz_html_analyzer import FinvizHTMLAnalyzer, FilterParameter, FilterOption
except ImportError:
    print("❌ finviz_html_analyzer.py not found")
    sys.exit(1)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class RangePattern:
    """Data class for a custom range pattern."""
    filter_name: str
    parameter_name: str
    range_type: str  # 'numeric', 'percentage', 'currency', 'volume', 'date'
    min_value: Optional[str] = None
    max_value: Optional[str] = None
    unit: Optional[str] = None
    url_pattern: Optional[str] = None
    example_values: List[str] = None

@dataclass
class CustomInputField:
    """Data class for a custom input field."""
    field_id: str
    field_type: str
    associated_filter: str
    placeholder: Optional[str] = None
    validation_pattern: Optional[str] = None

class FinvizRangeAnalyzer(FinvizHTMLAnalyzer):
    """Finviz custom range analysis class (extends the HTML analyzer)."""
    
    def __init__(self, html_file_path: str):
        super().__init__(html_file_path)
        self.range_patterns = []
        self.custom_inputs = []
        
        # Known range parameter patterns
        self.known_range_patterns = {
            'sh_price': {
                'type': 'currency',
                'unit': 'USD',
                'examples': ['10to50', '5to20', '1to10', '20to100'],
                'format': 'Price: ${min} to ${max}'
            },
            'cap': {
                'type': 'currency',
                'unit': 'USD (Billions)',
                'examples': ['1to10', '10to50', '2to20'],
                'format': 'Market Cap: ${min}B to ${max}B'
            },
            'sh_avgvol': {
                'type': 'volume',
                'unit': 'K shares',
                'examples': ['100to500', '500to1000', '1000to5000'],
                'format': 'Volume: {min}K to {max}K'
            },
            'fa_pe': {
                'type': 'numeric',
                'unit': 'ratio',
                'examples': ['5to20', '10to30', '15to25'],
                'format': 'P/E: {min} to {max}'
            },
            'fa_div': {
                'type': 'percentage',
                'unit': '%',
                'examples': ['2to5', '5to10', '1to3'],
                'format': 'Dividend: {min}% to {max}%'
            },
            'sh_relvol': {
                'type': 'numeric',
                'unit': 'multiplier',
                'examples': ['1to3', '2to5', '0.5to2'],
                'format': 'Rel Volume: {min}x to {max}x'
            },
            'ta_perf': {
                'type': 'percentage',
                'unit': '%',
                'examples': ['5to20', '-10to10', '10to50'],
                'format': 'Performance: {min}% to {max}%'
            },
            'fa_pb': {
                'type': 'numeric',
                'unit': 'ratio',
                'examples': ['1to5', '0.5to3', '2to10'],
                'format': 'P/B: {min} to {max}'
            },
            'fa_ps': {
                'type': 'numeric',
                'unit': 'ratio',
                'examples': ['1to10', '0.5to5', '2to20'],
                'format': 'P/S: {min} to {max}'
            },
            'fa_roe': {
                'type': 'percentage',
                'unit': '%',
                'examples': ['10to30', '15to50', '5to25'],
                'format': 'ROE: {min}% to {max}%'
            },
            'fa_roa': {
                'type': 'percentage',
                'unit': '%',
                'examples': ['5to20', '10to30', '2to15'],
                'format': 'ROA: {min}% to {max}%'
            },
            'fa_roi': {
                'type': 'percentage',
                'unit': '%',
                'examples': ['10to30', '15to40', '5to25'],
                'format': 'ROI: {min}% to {max}%'
            },
            'fa_curratio': {
                'type': 'numeric',
                'unit': 'ratio',
                'examples': ['1to5', '2to10', '0.5to3'],
                'format': 'Current Ratio: {min} to {max}'
            },
            'fa_quickratio': {
                'type': 'numeric',
                'unit': 'ratio',
                'examples': ['0.5to3', '1to5', '0.2to2'],
                'format': 'Quick Ratio: {min} to {max}'
            },
            'fa_debteq': {
                'type': 'numeric',
                'unit': 'ratio',
                'examples': ['0to1', '0.5to2', '1to5'],
                'format': 'Debt/Eq: {min} to {max}'
            },
            'fa_ltdebteq': {
                'type': 'numeric',
                'unit': 'ratio',
                'examples': ['0to0.5', '0.5to2', '1to3'],
                'format': 'LT Debt/Eq: {min} to {max}'
            },
            'fa_grossmargin': {
                'type': 'percentage',
                'unit': '%',
                'examples': ['20to60', '30to80', '10to40'],
                'format': 'Gross Margin: {min}% to {max}%'
            },
            'fa_opermargin': {
                'type': 'percentage',
                'unit': '%',
                'examples': ['5to30', '10to50', '0to20'],
                'format': 'Oper Margin: {min}% to {max}%'
            },
            'fa_profitmargin': {
                'type': 'percentage',
                'unit': '%',
                'examples': ['5to30', '10to40', '0to20'],
                'format': 'Profit Margin: {min}% to {max}%'
            },
            'ta_beta': {
                'type': 'numeric',
                'unit': 'coefficient',
                'examples': ['0.5to1.5', '1to2', '0to1'],
                'format': 'Beta: {min} to {max}'
            },
            'ta_volatility': {
                'type': 'percentage',
                'unit': '%',
                'examples': ['5to15', '10to30', '2to10'],
                'format': 'Volatility: {min}% to {max}%'
            }
        }
    
    def extract_custom_input_fields(self) -> List[CustomInputField]:
        """Extract custom input fields."""
        try:
            soup = self.load_html()
            custom_inputs = []
            
            # Search input elements related to filters
            input_patterns = [
                {'type': 'text', 'class': re.compile(r'.*range.*|.*custom.*')},
                {'type': 'number'},
                {'id': re.compile(r'.*_min|.*_max|.*_from|.*_to')},
                {'name': re.compile(r'.*_min|.*_max|.*_from|.*_to')},
            ]
            
            for pattern in input_patterns:
                inputs = soup.find_all('input', pattern)
                for input_elem in inputs:
                    input_id = input_elem.get('id', '')
                    input_type = input_elem.get('type', '')
                    placeholder = input_elem.get('placeholder', '')
                    pattern_attr = input_elem.get('pattern', '')
                    
                    # Guess the associated filter
                    associated_filter = self._guess_associated_filter(input_id, placeholder)
                    
                    if associated_filter or input_id:
                        custom_input = CustomInputField(
                            field_id=input_id,
                            field_type=input_type,
                            associated_filter=associated_filter,
                            placeholder=placeholder,
                            validation_pattern=pattern_attr
                        )
                        custom_inputs.append(custom_input)
            
            logger.info(f"Detected {len(custom_inputs)} custom input fields")
            return custom_inputs
            
        except Exception as e:
            logger.error(f"Custom input field extraction error: {e}")
            return []
    
    def _guess_associated_filter(self, input_id: str, placeholder: str) -> str:
        """Infer the filter associated with an input field."""
        search_text = f"{input_id} {placeholder}".lower()
        
        filter_keywords = {
            'sh_price': ['price', 'dollar', '$'],
            'cap': ['market cap', 'capitalization', 'cap'],
            'sh_avgvol': ['volume', 'vol'],
            'fa_pe': ['p/e', 'pe ratio', 'price earnings'],
            'fa_div': ['dividend', 'yield'],
            'sh_relvol': ['relative volume', 'rel vol'],
            'ta_perf': ['performance', 'perf'],
            'fa_pb': ['p/b', 'pb ratio', 'price book'],
            'fa_ps': ['p/s', 'ps ratio', 'price sales'],
            'fa_roe': ['roe', 'return on equity'],
        }
        
        for filter_name, keywords in filter_keywords.items():
            if any(keyword in search_text for keyword in keywords):
                return filter_name
        
        return ''
    
    def analyze_data_url_patterns(self, filters: List[FilterParameter]) -> List[RangePattern]:
        """Analyze custom range patterns from data-url attributes."""
        range_patterns = []
        
        for filter_param in filters:
            if not filter_param.data_url and not filter_param.data_url_selected:
                continue
            
            # Extract range patterns from data-url
            urls_to_analyze = []
            if filter_param.data_url:
                urls_to_analyze.append(filter_param.data_url)
            if filter_param.data_url_selected:
                urls_to_analyze.append(filter_param.data_url_selected)
            
            for url in urls_to_analyze:
                patterns = self._extract_range_patterns_from_url(url, filter_param.data_filter)
                range_patterns.extend(patterns)
        
        return range_patterns
    
    def _extract_range_patterns_from_url(self, url: str, filter_name: str) -> List[RangePattern]:
        """Extract range patterns from a URL."""
        patterns = []
        
        # Parse the filter portion of the URL
        if 'f=' in url:
            filter_part = url.split('f=')[1].split('&')[0]
            filter_items = filter_part.split(',')
            
            for item in filter_items:
                if filter_name in item:
                    # Look for a range pattern
                    range_match = re.search(r'(\d+(?:\.\d+)?)to(\d+(?:\.\d+)?)', item)
                    if range_match:
                        min_val, max_val = range_match.groups()
                        
                        # Get detailed info from known patterns
                        pattern_info = self.known_range_patterns.get(filter_name, {})
                        
                        pattern = RangePattern(
                            filter_name=filter_name,
                            parameter_name=item,
                            range_type=pattern_info.get('type', 'numeric'),
                            min_value=min_val,
                            max_value=max_val,
                            unit=pattern_info.get('unit'),
                            url_pattern=item,
                            example_values=pattern_info.get('examples', [])
                        )
                        patterns.append(pattern)
        
        return patterns
    
    def generate_range_examples(self, filter_name: str) -> List[Dict[str, str]]:
        """Generate range examples for the given filter."""
        if filter_name not in self.known_range_patterns:
            return []
        
        pattern_info = self.known_range_patterns[filter_name]
        examples = []
        
        for example in pattern_info.get('examples', []):
            if 'to' in example:
                min_val, max_val = example.split('to')
                url_param = f"{filter_name}_{example}"
                description = pattern_info['format'].format(min=min_val, max=max_val)
                
                examples.append({
                    'range': example,
                    'url_parameter': url_param,
                    'description': description,
                    'full_url_example': f"https://finviz.com/screener.ashx?v=111&f={url_param}"
                })
        
        return examples
    
    def export_range_analysis_to_markdown(self, filters: List[FilterParameter], output_file: str = None):
        """Export custom range analysis results to Markdown."""
        if output_file is None:
            output_file = f"finviz_range_analysis_{self.html_file_path.stem}.md"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("# Finviz Custom Range / Range Input Detailed Analysis\n\n")
                f.write(f"HTML file: `{self.html_file_path.name}`\n\n")
                f.write("This document details URL patterns when specifying custom ranges (manual inputs) in Finviz.\n\n")
                
                # List of range-capable filters
                f.write("## 🎯 Range-Capable Filters\n\n")
                
                range_capable_filters = []
                for filter_param in filters:
                    has_custom = any(opt.value in ['frange', 'modal', 'custom'] for opt in filter_param.options)
                    if has_custom:
                        range_capable_filters.append(filter_param)
                
                f.write(f"Detected range-capable filters: **{len(range_capable_filters)}**\n\n")
                
                for filter_param in range_capable_filters:
                    f.write(f"### {filter_param.name} - `{filter_param.data_filter}`\n")
                    
                    # Generate custom range examples
                    examples = self.generate_range_examples(filter_param.data_filter)
                    
                    if examples:
                        f.write("#### 📊 Range Examples\n\n")
                        f.write("| Range | URL Parameter | Description | Full URL Example |\n")
                        f.write("|---|---|---|---|\n")
                        
                        for example in examples[:3]:  # Show top 3 examples
                            f.write(f"| `{example['range']}` | `{example['url_parameter']}` | {example['description']} | `{example['full_url_example']}` |\n")
                        
                        f.write("\n")
                    
                    # Known pattern info
                    if filter_param.data_filter in self.known_range_patterns:
                        pattern_info = self.known_range_patterns[filter_param.data_filter]
                        f.write(f"- **Data type**: {pattern_info['type']}\n")
                        f.write(f"- **Unit**: {pattern_info['unit']}\n")
                        f.write(f"- **Format**: {pattern_info['format']}\n")
                    
                    f.write("\n")
                
                # URL pattern structure analysis
                f.write("## 🔗 URL Pattern Structure Analysis\n\n")
                f.write("### Basic Structure\n")
                f.write("```\n")
                f.write("https://finviz.com/screener.ashx?v=111&f=[filter1],[filter2],[filter3]\n")
                f.write("```\n\n")
                
                f.write("### Custom Range Patterns\n")
                f.write("| Filter | Pattern | Example |\n")
                f.write("|---|---|---|\n")
                
                for filter_name, pattern_info in self.known_range_patterns.items():
                    example = pattern_info['examples'][0] if pattern_info['examples'] else 'XtoY'
                    f.write(f"| `{filter_name}` | `{filter_name}_{{min}}to{{max}}` | `{filter_name}_{example}` |\n")
                
                f.write("\n")
                
                # Practical usage examples
                f.write("## 💡 Practical Examples\n\n")
                
                practical_examples = [
                    {
                        'title': 'Stocks priced $10-$50',
                        'url': 'https://finviz.com/screener.ashx?v=111&f=sh_price_10to50',
                        'description': 'Stocks with prices between $10 and $50'
                    },
                    {
                        'title': 'Mid-cap stocks with $1B-$10B market cap',
                        'url': 'https://finviz.com/screener.ashx?v=111&f=cap_1to10',
                        'description': 'Stocks with market caps between $1B and $10B'
                    },
                    {
                        'title': 'Value stocks with P/E 10-20',
                        'url': 'https://finviz.com/screener.ashx?v=111&f=fa_pe_10to20',
                        'description': 'Stocks with P/E between 10 and 20'
                    },
                    {
                        'title': 'High-dividend stocks with 3-7% yield',
                        'url': 'https://finviz.com/screener.ashx?v=111&f=fa_div_3to7',
                        'description': 'Stocks with dividend yields between 3% and 7%'
                    },
                    {
                        'title': 'Combined: Technology × mid-cap × reasonable P/E',
                        'url': 'https://finviz.com/screener.ashx?v=111&f=sec_technology,cap_1to10,fa_pe_10to25',
                        'description': 'Technology sector mid-caps with P/E 10-25'
                    }
                ]
                
                for i, example in enumerate(practical_examples, 1):
                    f.write(f"### {i}. {example['title']}\n")
                    f.write(f"**URL**: `{example['url']}`\n\n")
                    f.write(f"**Description**: {example['description']}\n\n")
                
                # Range input best practices
                f.write("## 🎯 Range Input Best Practices\n\n")
                f.write("### 📈 Numeric formats\n")
                f.write("- **Integers**: `10to50` (10 to 50)\n")
                f.write("- **Decimals**: `1.5to3.5` (1.5 to 3.5)\n")
                f.write("- **Negative values**: `-10to10` (-10% to +10%)\n\n")
                
                f.write("### 💰 Currency and unit considerations\n")
                f.write("- **Price**: USD `sh_price_10to50` ($10-$50)\n")
                f.write("- **Market cap**: billions USD `cap_1to10` ($1B-$10B)\n")
                f.write("- **Volume**: thousands of shares `sh_avgvol_100to500` (100K-500K)\n\n")
                
                f.write("### ⚠️ Notes\n")
                f.write("- Ensure min is less than max\n")
                f.write("- Extreme values may return zero results\n")
                f.write("- Some filters only support specific ranges\n\n")
            
            logger.info(f"Exported custom range analysis to {output_file}")
            
        except Exception as e:
            logger.error(f"Range analysis Markdown export error: {e}")
    
    def analyze_with_ranges(self, export_format: str = 'both'):
        """Run full analysis (including range patterns)."""
        try:
            logger.info("Starting filter and range analysis...")
            
            # Extract base filters
            filters = self.extract_filter_parameters()
            
            if not filters:
                logger.error("No filters were detected")
                return False
            
            # Print summary
            self.print_range_summary(filters)
            
            # Output results
            if export_format in ['markdown', 'both']:
                self.export_to_markdown(filters)
                self.export_range_analysis_to_markdown(filters)
            
            if export_format in ['json', 'both']:
                self.export_to_json(filters)
                self.export_range_analysis_to_json(filters)
            
            return True
            
        except Exception as e:
            logger.error(f"Range analysis execution error: {e}")
            return False
    
    def export_range_analysis_to_json(self, filters: List[FilterParameter], output_file: str = None):
        """Export range analysis results to JSON."""
        if output_file is None:
            output_file = f"finviz_range_analysis_{self.html_file_path.stem}.json"
        
        try:
            range_data = {
                'source_file': str(self.html_file_path),
                'analysis_type': 'custom_range_patterns',
                'range_capable_filters': [],
                'url_patterns': {},
                'practical_examples': []
            }
            
            # Range-capable filters
            for filter_param in filters:
                has_custom = any(opt.value in ['frange', 'modal', 'custom'] for opt in filter_param.options)
                if has_custom:
                    examples = self.generate_range_examples(filter_param.data_filter)
                    
                    filter_info = {
                        'name': filter_param.name,
                        'data_filter': filter_param.data_filter,
                        'range_examples': examples,
                        'known_pattern': filter_param.data_filter in self.known_range_patterns
                    }
                    
                    if filter_param.data_filter in self.known_range_patterns:
                        pattern_info = self.known_range_patterns[filter_param.data_filter]
                        filter_info.update({
                            'data_type': pattern_info['type'],
                            'unit': pattern_info['unit'],
                            'format': pattern_info['format']
                        })
                    
                    range_data['range_capable_filters'].append(filter_info)
            
            # URL patterns
            for filter_name, pattern_info in self.known_range_patterns.items():
                range_data['url_patterns'][filter_name] = {
                    'pattern': f"{filter_name}_{{min}}to{{max}}",
                    'examples': pattern_info['examples'],
                    'type': pattern_info['type'],
                    'unit': pattern_info['unit']
                }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(range_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Exported range analysis results to {output_file}")
            
        except Exception as e:
            logger.error(f"Range analysis JSON export error: {e}")
    
    def print_range_summary(self, filters: List[FilterParameter]):
        """Print a summary of range analysis results."""
        print("\n" + "="*70)
        print("📊 Finviz Custom Range Analysis Summary")
        print("="*70)
        
        range_capable = [f for f in filters if any(opt.value in ['frange', 'modal', 'custom'] for opt in f.options)]
        
        print(f"📄 Source file: {self.html_file_path.name}")
        print(f"🔢 Total filters: {len(filters)}")
        print(f"🎯 Range-capable filters: {len(range_capable)}")
        print(f"🔗 Known range patterns: {len(self.known_range_patterns)}")
        
        if range_capable:
            print("\n🎯 Range-capable filters:")
            for filter_param in range_capable[:10]:  # Show top 10
                examples_count = len(self.generate_range_examples(filter_param.data_filter))
                print(f"  📈 {filter_param.name}: {examples_count} examples")
        
        print("\n💡 Range URL examples:")
        example_urls = [
            "sh_price_10to50 → Price $10-$50",
            "cap_1to10 → Market cap $1B-$10B",
            "fa_pe_10to20 → P/E 10-20",
            "fa_div_3to7 → Dividend yield 3-7%"
        ]
        for example in example_urls:
            print(f"  🔗 {example}")
        
        print("\n" + "="*70)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Finviz custom range analysis tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python finviz_range_analyzer.py
  python finviz_range_analyzer.py ../docs/finviz_screen_page.html
  python finviz_range_analyzer.py --format json
        """
    )
    
    parser.add_argument(
        'html_file',
        nargs='?',
        default='../docs/finviz_screen_page.html',
        help='Path to the HTML file to analyze'
    )
    
    parser.add_argument(
        '--format', '-f',
        choices=['markdown', 'json', 'both'],
        default='both',
        help='Specify output format (default: both)'
    )
    
    args = parser.parse_args()
    
    print("🎯 Finviz Custom Range Analysis Tool")
    print("="*60)
    
    try:
        # Initialize analyzer
        analyzer = FinvizRangeAnalyzer(args.html_file)
        
        # Run analysis
        success = analyzer.analyze_with_ranges(export_format=args.format)
        
        if success:
            print("\n✅ Range analysis completed!")
            
            # Check output files
            stem = Path(args.html_file).stem
            
            if args.format in ['markdown', 'both']:
                range_md_file = f"finviz_range_analysis_{stem}.md"
                if os.path.exists(range_md_file):
                    size = os.path.getsize(range_md_file) / 1024
                    print(f"📄 {range_md_file} ({size:.1f} KB)")
            
            if args.format in ['json', 'both']:
                range_json_file = f"finviz_range_analysis_{stem}.json"
                if os.path.exists(range_json_file):
                    size = os.path.getsize(range_json_file) / 1024
                    print(f"📊 {range_json_file} ({size:.1f} KB)")
        else:
            print("\n❌ Range analysis failed")
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
