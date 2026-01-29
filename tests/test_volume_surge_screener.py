import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def test_volume_surge_screener():
    """Run and debug the volume_surge_screener test."""
    try:
        # Instantiate the screener directly for detailed inspection
        from src.finviz_client.screener import FinvizScreener
        screener = FinvizScreener()
        
        # Check filter conditions
        print("\n=== Filter Conditions ===")
        filters = screener._build_volume_surge_filters()
        print(f"Filters: {filters}")
        
        # Check Finviz parameter conversion
        print("\n=== Finviz Parameter Conversion ===")
        finviz_params = screener._convert_filters_to_finviz(filters)
        print(f"Finviz Parameters: {finviz_params}")
        
        # Run the actual screening
        print("\n=== Screening Run ===")
        results = screener.volume_surge_screener()
        print(f"Result count: {len(results)}")
        
        # Show result details (first 5)
        if results:
            print("\n=== Result Details (First 5) ===")
            for i, stock in enumerate(results[:5]):
                # Use correct StockData object attributes
                company_name = getattr(stock, 'company_name', 'N/A')
                price = getattr(stock, 'price', 'N/A')
                price_change = getattr(stock, 'price_change', 'N/A')
                volume = getattr(stock, 'volume', 'N/A')
                
                print(f"{i+1}. {stock.ticker} - {company_name}")
                print(f"   Price: ${price} | Change: {price_change}% | Volume: {volume}")
                print()
        else:
            print("No results found.")
            
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_volume_surge_screener() 
