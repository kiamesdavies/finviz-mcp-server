#!/usr/bin/env python3
"""
Finviz HTML Quick Analysis Script

A wrapper script for quickly analyzing saved Finviz HTML files.
"""

import sys
import os
from pathlib import Path

# Add script directory to the path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

try:
    from finviz_html_analyzer import FinvizHTMLAnalyzer
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install the required packages:")
    print("pip install beautifulsoup4 lxml")
    sys.exit(1)

def quick_html_analyze(html_file: str = None):
    """Run HTML analysis."""
    print("🔍 Finviz HTML Filter Quick Analysis")
    print("=" * 50)
    
    # Check HTML file path
    if html_file is None:
        # Default search order
        default_files = [
            'finviz_screen_page.html',
            '../docs/finviz_screen_page.html',
            'finviz_elite_page.html',
            '../finviz_screen_page.html'
        ]
        
        found_file = None
        for file_path in default_files:
            if os.path.exists(file_path):
                found_file = file_path
                break
        
        if found_file:
            html_file = found_file
        else:
            print("❌ HTML file not found.")
            print("\nPlease provide one of the following files:")
            for file_path in default_files:
                print(f"  - {file_path}")
            
            # Prompt user input
            custom_path = input("\nOr enter the HTML file path: ").strip()
            if custom_path and os.path.exists(custom_path):
                html_file = custom_path
            else:
                print("❌ Specified HTML file not found")
                return False
    
    print(f"📄 HTML file: {html_file}")
    
    try:
        # Initialize analyzer
        analyzer = FinvizHTMLAnalyzer(html_file)
        
        print("🔄 Analyzing...")
        
        # Run analysis
        success = analyzer.analyze(export_format='both')
        
        if success:
            print("\n✅ Analysis completed!")
            
            # Check output files
            stem = Path(html_file).stem
            
            md_file = f"finviz_filters_analysis_{stem}.md"
            json_file = f"finviz_filters_analysis_{stem}.json"
            
            if os.path.exists(md_file):
                size = os.path.getsize(md_file) / 1024
                print(f"📄 {md_file} ({size:.1f} KB)")
            
            if os.path.exists(json_file):
                size = os.path.getsize(json_file) / 1024
                print(f"📊 {json_file} ({size:.1f} KB)")
            
            print("\n💡 Usage:")
            print(f"  - Markdown: Open {md_file} to review the parameter list")
            print(f"  - JSON: Open {json_file} to review the structured data")
            
            return True
        else:
            print("\n❌ Analysis failed")
            return False
            
    except FileNotFoundError as e:
        print(f"❌ File error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Finviz HTML quick analysis tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python quick_html_analyze.py
  python quick_html_analyze.py finviz_screen_page.html
  python quick_html_analyze.py ../docs/finviz_screen_page.html
        """
    )
    
    parser.add_argument(
        'html_file',
        nargs='?',
        help='Path to the HTML file to analyze (auto-detect if omitted)'
    )
    
    args = parser.parse_args()
    
    success = quick_html_analyze(args.html_file)
    
    if not success:
        print("\n🔧 Troubleshooting:")
        print("1. Confirm the HTML file is in the correct path")
        print("2. Confirm required packages are installed:")
        print("   pip install beautifulsoup4 lxml")
        print("3. Confirm the HTML file is a Finviz screener page")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 
