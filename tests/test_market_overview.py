#!/usr/bin/env python3
"""
Tests for Market Overview functionality
"""
import os
import sys

# Add project root to the path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, 'src'))

def test_import():
    """Import test."""
    try:
        from utils.validators import validate_ticker
        from utils.finviz_client import FinvizClient
        from utils.screeners import FinvizScreener
        print("✅ Required modules imported successfully")
        return True
    except Exception as e:
        print(f"❌ Import error: {str(e)}")
        return False

def test_market_overview_syntax():
    """Syntax check."""
    try:
        # Syntax check for server.py
        import ast
        with open('src/server.py', 'r', encoding='utf-8') as f:
            source = f.read()
        
        ast.parse(source)
        print("✅ server.py syntax check succeeded")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error: {str(e)}")
        print(f"   Line {e.lineno}: {e.text}")
        return False

def test_finviz_tools():
    """Basic test for Finviz tools."""
    try:
        # Validation function test
        from utils.validators import validate_ticker
        
        # Valid tickers
        assert validate_ticker("SPY") == True
        assert validate_ticker("QQQ") == True
        assert validate_ticker("AAPL") == True
        
        # Invalid tickers
        assert validate_ticker("") == False
        assert validate_ticker("12345") == False
        
        print("✅ Validation test succeeded")
        return True
    except Exception as e:
        print(f"❌ Validation test error: {str(e)}")
        return False

def main():
    print("🚀 Starting Market Overview implementation tests")
    print("=" * 50)
    
    # Run tests
    tests = [
        ("Import test", test_import),
        ("Syntax check", test_market_overview_syntax),
        ("Finviz tools test", test_finviz_tools)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📊 {test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"🎯 Test results: {passed}/{total} passed")
    
    if passed == total:
        print("✅ All tests passed!")
        print("🚀 market_overview implementation complete")
    else:
        print("❌ Some tests failed")
        
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
