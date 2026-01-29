#!/usr/bin/env python3
"""
Finviz Custom Range Analysis - Quick Start

Easiest way to run:
  python quick_range_analyze.py

Or:
  cd scripts && python quick_range_analyze.py
"""

import os
import sys
from pathlib import Path

def main():
    print("🎯 Finviz Custom Range Analysis - Quick Start")
    print("="*60)
    
    # Auto-detect HTML file
    possible_paths = [
        '../docs/finviz_screen_page.html',
        'docs/finviz_screen_page.html',
        'finviz_screen_page.html'
    ]
    
    html_file = None
    for path in possible_paths:
        if os.path.exists(path):
            html_file = path
            print(f"✅ Found HTML file: {path}")
            break
    
    if not html_file:
        print("❌ finviz_screen_page.html not found")
        print("Check the following locations:")
        for path in possible_paths:
            print(f"  - {path}")
        return 1
    
    try:
        # Import finviz_range_analyzer.py
        from finviz_range_analyzer import FinvizRangeAnalyzer
        
        print("📊 Starting custom range analysis...")
        
        # Initialize and run analyzer
        analyzer = FinvizRangeAnalyzer(html_file)
        success = analyzer.analyze_with_ranges(export_format='both')
        
        if success:
            print("\n🎉 Custom range analysis completed!")
            
            # Check output files
            stem = Path(html_file).stem
            output_files = [
                f"finviz_range_analysis_{stem}.md",
                f"finviz_range_analysis_{stem}.json"
            ]
            
            print("\n📁 Output files:")
            for file in output_files:
                if os.path.exists(file):
                    size = os.path.getsize(file) / 1024
                    print(f"  ✅ {file} ({size:.1f} KB)")
                else:
                    print(f"  ❌ {file} (not created)")
            
            print("\n💡 Custom range URL examples:")
            print("  🔗 sh_price_10to50 → Price $10-$50")
            print("  🔗 cap_1to10 → Market cap $1B-$10B")
            print("  🔗 fa_pe_10to20 → P/E 10-20")
            print("  🔗 fa_div_3to7 → Dividend yield 3-7%")
            
            return 0
        else:
            print("\n❌ Custom range analysis failed")
            return 1
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Ensure finviz_range_analyzer.py is in the same directory")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 
