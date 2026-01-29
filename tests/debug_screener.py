#!/usr/bin/env python3
"""
Debug script for Finviz screener issues
Script for debugging Finviz screener issues
"""

import sys
import os
import logging

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Enable debug logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from src.finviz_client.screener import FinvizScreener
from src.finviz_client.base import FinvizClient

def test_direct_url_construction():
    """Test by constructing the URL directly."""
    print("=== URL Construction Test ===")
    
    screener = FinvizScreener()
    
    # Build filters for next week's earnings
    filters = {
        'earnings_date': 'next_week',
        'market_cap': 'smallover',
        'price_min': 10,
        'avg_volume_min': 500,
        'sectors': ['Technology', 'Industrials', 'Healthcare', 
                   'Communication Services', 'Consumer Cyclical', 
                   'Financial Services', 'Consumer Defensive', 'Basic Materials']
    }
    
    # Convert to Finviz parameters
    finviz_params = screener._convert_filters_to_finviz(filters)
    print(f"Constructed parameters: {finviz_params}")
    
    # Build URL
    from urllib.parse import urlencode
    base_url = "https://finviz.com/screener.ashx"
    full_url = f"{base_url}?{urlencode(finviz_params)}"
    print(f"Constructed URL: {full_url}")
    
    # Actual Finviz URL (reference)
    expected_url = "https://elite.finviz.com/screener.ashx?v=311&p=w&f=cap_smallover,earningsdate_nextweek,sec_technology|industrials|healthcare|communicationservices|consumercyclical|financial|consumerdefensive|basicmaterials,sh_avgvol_o500,sh_price_o10&ft=4&o=ticker&ar=10"
    print(f"Expected URL: {expected_url}")

def test_basic_request():
    """Basic HTTP request test."""
    print("\n=== Basic HTTP Request Test ===")
    
    client = FinvizClient()
    
    try:
        # Access a basic screener page
        response = client._make_request("https://finviz.com/screener.ashx", {'v': '111'})
        print(f"Response status: {response.status_code}")
        print(f"Response size: {len(response.text)} characters")
        
        # Check part of the HTML
        if "screener" in response.text.lower():
            print("✓ Screener page loaded successfully")
        else:
            print("✗ Problem loading screener page")
            
    except Exception as e:
        print(f"✗ HTTP request error: {e}")

def test_csv_export():
    """CSV export test."""
    print("\n=== CSV Export Test ===")
    
    client = FinvizClient()
    
    try:
        # Try CSV export with the simplest filter
        params = {'v': '111'}
        response = client._make_request("https://finviz.com/export.ashx", params)
        print(f"CSV response status: {response.status_code}")
        print(f"CSV response size: {len(response.text)} characters")
        print(f"First 200 CSV characters: {response.text[:200]}")
        
        if "ticker" in response.text.lower() or "symbol" in response.text.lower():
            print("✓ CSV data retrieved successfully")
        else:
            print("✗ Problem retrieving CSV data")
            
    except Exception as e:
        print(f"✗ CSV export error: {e}")

def test_html_parsing():
    """HTML parsing test."""
    print("\n=== HTML Parsing Test ===")
    
    client = FinvizClient()
    
    try:
        # Fetch and parse basic screener HTML
        params = {'v': '111', 'f': 'cap_smallover'}
        response = client._make_request("https://finviz.com/screener.ashx", params)
        
        # Parse HTML
        parsed_data = client._parse_finviz_table(response.text)
        print(f"Parsed rows: {len(parsed_data)}")
        
        if parsed_data:
            print("✓ HTML parsing succeeded")
            print(f"First row keys: {list(parsed_data[0].keys())}")
        else:
            print("✗ HTML parsing returned 0 rows")
            
    except Exception as e:
        print(f"✗ HTML parsing error: {e}")

def main():
    """Main entry point."""
    print("🔍 Finviz Screener Debug Tests Start")
    print("=" * 60)
    
    test_direct_url_construction()
    test_basic_request()
    test_csv_export()
    test_html_parsing()
    
    print("\n" + "=" * 60)
    print("📊 Debug tests complete")

if __name__ == "__main__":
    main() 
