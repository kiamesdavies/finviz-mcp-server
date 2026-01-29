import sys
import os
from collections import defaultdict, Counter

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def analyze_volume_surge_stocks():
    """Detailed analysis of volume surge stocks."""
    try:
        from src.finviz_client.screener import FinvizScreener
        screener = FinvizScreener()
        
        print("=== Detailed Analysis of Volume Surge Stocks ===")
        
        # Run screening
        results = screener.volume_surge_screener()
        print(f"Total stocks: {len(results)}")
        
        # Sector analysis
        sector_analysis = defaultdict(list)
        industry_analysis = defaultdict(list)
        
        # Price change analysis
        price_change_ranges = {
            "10%+": [],
            "5-10%": [],
            "2-5%": []
        }
        
        # Market cap analysis
        market_cap_ranges = {
            "Large (50B+)": [],
            "Mid (2B-50B)": [],
            "Small (300M-2B)": []
        }
        
        # Top performers
        top_performers = []
        
        for i, stock in enumerate(results[:20]):  # Analyze top 20 stocks
            # Sector info
            sector = getattr(stock, 'sector', 'Unknown')
            industry = getattr(stock, 'industry', 'Unknown')
            
            # Basic info
            ticker = stock.ticker
            price = getattr(stock, 'price', 0)
            price_change = getattr(stock, 'price_change', 0)
            volume = getattr(stock, 'volume', 0)
            market_cap = getattr(stock, 'market_cap', 0)
            
            # Accumulate data
            sector_analysis[sector].append({
                'ticker': ticker,
                'price_change': price_change,
                'volume': volume
            })
            
            industry_analysis[industry].append(ticker)
            
            # Price change classification
            if price_change >= 10:
                price_change_ranges["10%+"].append(ticker)
            elif price_change >= 5:
                price_change_ranges["5-10%"].append(ticker)
            else:
                price_change_ranges["2-5%"].append(ticker)
            
            # Market cap classification (rough)
            if market_cap and market_cap > 50000:  # 50B+
                market_cap_ranges["Large (50B+)"].append(ticker)
            elif market_cap and market_cap > 2000:  # 2B-50B
                market_cap_ranges["Mid (2B-50B)"].append(ticker)
            else:
                market_cap_ranges["Small (300M-2B)"].append(ticker)
            
            # Top performers
            if i < 10:
                top_performers.append({
                    'rank': i + 1,
                    'ticker': ticker,
                    'price': price,
                    'price_change': price_change,
                    'volume': volume,
                    'sector': sector
                })
        
        # Output results
        print("\n=== TOP 10 Performers ===")
        for performer in top_performers:
            print(f"{performer['rank']:2d}. {performer['ticker']:6s} | "
                  f"{performer['price_change']:+6.2f}% | "
                  f"${performer['price']:7.2f} | "
                  f"{performer['volume']/1000000:6.1f}M vol | "
                  f"{performer['sector']}")
        
        print("\n=== Sector Distribution ===")
        sector_summary = {}
        for sector, stocks in sector_analysis.items():
            count = len(stocks)
            avg_change = sum(s['price_change'] for s in stocks) / count if count > 0 else 0
            sector_summary[sector] = {'count': count, 'avg_change': avg_change}
            print(f"{sector:25s}: {count:3d} stocks (avg change: {avg_change:+5.2f}%)")
        
        print("\n=== Price Change Distribution ===")
        for range_name, tickers in price_change_ranges.items():
            print(f"{range_name:10s}: {len(tickers):3d} stocks ({len(tickers)/len(results)*100:4.1f}%)")
            if tickers:
                print(f"  Example tickers: {', '.join(tickers[:5])}")
        
        print("\n=== Market Cap Distribution ===")
        for cap_range, tickers in market_cap_ranges.items():
            print(f"{cap_range:15s}: {len(tickers):3d} stocks")
        
        # Return analysis results as a dict
        return {
            'total_stocks': len(results),
            'top_performers': top_performers,
            'sector_summary': sector_summary,
            'price_change_distribution': {k: len(v) for k, v in price_change_ranges.items()},
            'market_cap_distribution': {k: len(v) for k, v in market_cap_ranges.items()},
            'top_sectors': sorted(sector_summary.items(), key=lambda x: x[1]['count'], reverse=True)[:5]
        }
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    analyze_volume_surge_stocks() 
