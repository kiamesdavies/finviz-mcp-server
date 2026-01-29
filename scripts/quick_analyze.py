#!/usr/bin/env python3
"""
Finviz Elite Quick Analysis Script

A wrapper script to quickly run Finviz Elite filter analysis.
"""

import sys
import os
from pathlib import Path

# Add script directory to the path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

try:
    from finviz_elite_analyzer import FinvizEliteAnalyzer
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install the required packages:")
    print("pip install -r requirements.txt")
    sys.exit(1)

def quick_analyze():
    """Run quick analysis."""
    print("🔍 Finviz Elite Filter Quick Analysis")
    print("=" * 50)
    
    # Collect login credentials
    import getpass
    
    username = input("📧 Elite username: ").strip()
    if not username:
        print("❌ Username not provided")
        return False
    
    password = getpass.getpass("🔐 Elite password: ")
    if not password:
        print("❌ Password not provided")
        return False
    
    # Run analysis
    print("\n🚀 Starting analysis...")
    print("📝 Logging in...")
    
    analyzer = FinvizEliteAnalyzer()
    
    try:
        success = analyzer.run_full_analysis(
            username=username,
            password=password,
            export_format='both'
        )
        
        if success:
            print("\n✅ Analysis complete!")
            print("\n📄 Generated files:")
            
            # Check file existence
            md_file = "finviz_elite_filters.md"
            json_file = "finviz_elite_filters.json"
            
            if os.path.exists(md_file):
                file_size = os.path.getsize(md_file) / 1024  # KB
                print(f"  📋 {md_file} ({file_size:.1f} KB)")
            
            if os.path.exists(json_file):
                file_size = os.path.getsize(json_file) / 1024  # KB
                print(f"  📊 {json_file} ({file_size:.1f} KB)")
            
            print("\n🎉 Analysis finished successfully!")
            return True
        else:
            print("\n❌ Analysis failed")
            print("💡 Please check:")
            print("  - Login credentials are correct")
            print("  - Elite subscription is active")
            print("  - Internet connection is stable")
            return False
            
    except KeyboardInterrupt:
        print("\n⏹️  Interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

def main():
    """Main entry point."""
    try:
        success = quick_analyze()
        
        if success:
            # Show quick stats from the result file
            try:
                import json
                
                with open('finviz_elite_filters.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                print("\n📈 Stats:")
                print(f"  🔢 Filters detected: {len(data)}")
                
                # Category stats
                categories = {}
                for item in data:
                    category = "Other"  # Default
                    # Simple category classification
                    name = item.get('name', '')
                    if 'Exchange' in name or 'Index' in name or 'Sector' in name:
                        category = "Basic Info"
                    elif 'Price' in name or 'Cap' in name:
                        category = "Price & Market Cap"
                    elif 'Volume' in name:
                        category = "Volume & Trading"
                    elif 'Performance' in name:
                        category = "Technical Analysis"
                    
                    categories[category] = categories.get(category, 0) + 1
                
                for cat, count in categories.items():
                    if count > 0:
                        print(f"  📊 {cat}: {count}")
                        
            except Exception as e:
                print(f"  📊 Stats error: {e}")
        
        print("\n👋 Analysis complete")
        
    except KeyboardInterrupt:
        print("\n👋 Analysis interrupted")
    except Exception as e:
        print(f"❌ Execution error: {e}")

if __name__ == "__main__":
    main() 
