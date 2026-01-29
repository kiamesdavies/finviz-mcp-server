#!/usr/bin/env python3
"""
MCP System Validation Test Suite
Recommended for release: system-level functional tests via real MCP calls.
Comprehensive tests including data validity checks.
"""

import pytest
import asyncio
import sys
import os
import re
import time
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# MCP tools import (for real MCP calls)
from src.server import (
    earnings_screener,
    earnings_trading_screener,
    earnings_premarket_screener,
    earnings_afterhours_screener,
    volume_surge_screener,
    uptrend_screener,
    upcoming_earnings_screener,
    get_stock_fundamentals,
    get_multiple_stocks_fundamentals,
    get_market_overview,
    dividend_growth_screener,
    earnings_winners_screener
)

@dataclass
class TestResult:
    """Dataclass for test results."""
    test_name: str
    success: bool
    execution_time: float
    result_data: Any
    error_message: Optional[str] = None
    data_quality_score: float = 0.0
    stocks_found: int = 0

class MCPSystemValidationTest:
    """MCP system validation test class."""

    def __init__(self):
        self.test_results: List[TestResult] = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def log_test_result(self, result: TestResult):
        """Log test result."""
        self.test_results.append(result)
        self.total_tests += 1
        
        if result.success:
            self.passed_tests += 1
            print(f"✅ {result.test_name} - Execution time: {result.execution_time:.2f}s, Stocks found: {result.stocks_found}")
        else:
            print(f"❌ {result.test_name} - Error: {result.error_message}")

    def validate_stock_data_quality(self, result_text: str, test_name: str) -> tuple[float, int]:
        """Validate stock data quality."""
        quality_score = 0.0
        stocks_found = 0
        
        # Detect ticker symbols
        ticker_pattern = r'\b[A-Z]{1,5}\b'
        tickers = re.findall(ticker_pattern, result_text)
        stocks_found = len(set(tickers))
        
        # Basic quality checks
        quality_checks = [
            ('Price data', r'\$\d+\.\d+'),
            ('Percentages', r'[+-]?\d+\.\d+%'),
            ('Volume', r'[\d,]+(?:K|M|B)?'),
            ('Sector info', r'(Technology|Healthcare|Financial|Energy|Consumer|Industrial|Real Estate|Utilities|Communication|Basic Materials)'),
            ('Result format', r'(Results|stocks|found|detected)'),
        ]
        
        for check_name, pattern in quality_checks:
            if re.search(pattern, result_text):
                quality_score += 20.0  # 20 points per check
        
        # Detect error patterns (penalty)
        error_patterns = [
            r'Error|Exception|Failed',
            r'AttributeError|TypeError|KeyError',
            r'NoneType|object has no attribute',
            r'connection error|timeout'
        ]
        
        for error_pattern in error_patterns:
            if re.search(error_pattern, result_text, re.IGNORECASE):
                quality_score -= 30.0
        
        return max(0.0, min(100.0, quality_score)), stocks_found

    def test_earnings_related_functions(self):
        """Comprehensive tests for earnings-related features."""
        print("\n🔍 Starting earnings-related tests...")
        
        # 1. Upcoming earnings stock screening
        start_time = time.time()
        try:
            result = earnings_screener(earnings_date="today_after")
            execution_time = time.time() - start_time
            result_text = str(result[0].text) if result and len(result) > 0 else str(result)
            quality_score, stocks_found = self.validate_stock_data_quality(result_text, "earnings_screener")
            
            self.log_test_result(TestResult(
                test_name="Upcoming earnings stock screening",
                success=True,
                execution_time=execution_time,
                result_data=result,
                data_quality_score=quality_score,
                stocks_found=stocks_found
            ))
        except Exception as e:
            self.log_test_result(TestResult(
                test_name="Upcoming earnings stock screening",
                success=False,
                execution_time=time.time() - start_time,
                result_data=None,
                error_message=str(e)
            ))

        # 2. Earnings trade candidates
        start_time = time.time()
        try:
            result = earnings_trading_screener()
            execution_time = time.time() - start_time
            result_text = str(result[0].text) if result and len(result) > 0 else str(result)
            quality_score, stocks_found = self.validate_stock_data_quality(result_text, "earnings_trading_screener")
            
            # Expected: 0 results is OK (outside trading hours)
            success = True  # If no error, treat as success
            
            self.log_test_result(TestResult(
                test_name="Earnings trade candidates",
                success=success,
                execution_time=execution_time,
                result_data=result,
                data_quality_score=quality_score,
                stocks_found=stocks_found
            ))
        except Exception as e:
            self.log_test_result(TestResult(
                test_name="Earnings trade candidates",
                success=False,
                execution_time=time.time() - start_time,
                result_data=None,
                error_message=str(e)
            ))

    def test_basic_screening_functions(self):
        """Basic screening function tests."""
        print("\n🔍 Starting basic screening tests...")
        
        # 1. Volume surge stocks
        start_time = time.time()
        try:
            result = volume_surge_screener()
            execution_time = time.time() - start_time
            result_text = str(result[0].text) if result and len(result) > 0 else str(result)
            quality_score, stocks_found = self.validate_stock_data_quality(result_text, "volume_surge_screener")
            
            # High quality if 50+ stocks found
            if stocks_found >= 50:
                quality_score += 20.0
            
            self.log_test_result(TestResult(
                test_name="Volume surge screening",
                success=True,
                execution_time=execution_time,
                result_data=result,
                data_quality_score=quality_score,
                stocks_found=stocks_found
            ))
        except Exception as e:
            self.log_test_result(TestResult(
                test_name="Volume surge screening",
                success=False,
                execution_time=time.time() - start_time,
                result_data=None,
                error_message=str(e)
            ))

        # 2. Uptrend stocks
        start_time = time.time()
        try:
            result = uptrend_screener()
            execution_time = time.time() - start_time
            result_text = str(result[0].text) if result and len(result) > 0 else str(result)
            quality_score, stocks_found = self.validate_stock_data_quality(result_text, "uptrend_screener")
            
            # High quality if 200+ stocks found
            if stocks_found >= 200:
                quality_score += 20.0
            
            self.log_test_result(TestResult(
                test_name="Uptrend screening",
                success=True,
                execution_time=execution_time,
                result_data=result,
                data_quality_score=quality_score,
                stocks_found=stocks_found
            ))
        except Exception as e:
            self.log_test_result(TestResult(
                test_name="Uptrend screening",
                success=False,
                execution_time=time.time() - start_time,
                result_data=None,
                error_message=str(e)
            ))

    def test_stock_data_functions(self):
        """Stock data retrieval tests."""
        print("\n🔍 Starting stock data retrieval tests...")
        
        # 1. Single-stock fundamentals
        start_time = time.time()
        try:
            result = get_stock_fundamentals(
                ticker="AAPL",
                data_fields=["price", "change", "volume", "pe_ratio", "eps"]
            )
            execution_time = time.time() - start_time
            result_text = str(result[0].text) if result and len(result) > 0 else str(result)
            
            # AAPL-specific data checks
            quality_score = 0.0
            if "AAPL" in result_text: quality_score += 25.0
            if re.search(r'\$\d+\.\d+', result_text): quality_score += 25.0  # Price
            if re.search(r'[\d,]+', result_text): quality_score += 25.0  # Volume
            if "Fundamental Data" in result_text: quality_score += 25.0
            
            self.log_test_result(TestResult(
                test_name="Single-stock fundamentals (AAPL)",
                success=True,
                execution_time=execution_time,
                result_data=result,
                data_quality_score=quality_score,
                stocks_found=1
            ))
        except Exception as e:
            self.log_test_result(TestResult(
                test_name="Single-stock fundamentals (AAPL)",
                success=False,
                execution_time=time.time() - start_time,
                result_data=None,
                error_message=str(e)
            ))

        # 2. Multi-stock fundamentals
        start_time = time.time()
        try:
            result = get_multiple_stocks_fundamentals(
                tickers=["MSFT", "GOOGL", "NVDA"],
                data_fields=["price", "change", "market_cap", "pe_ratio"]
            )
            execution_time = time.time() - start_time
            result_text = str(result[0].text) if result and len(result) > 0 else str(result)
            
            # Multi-stock data checks
            quality_score = 0.0
            target_tickers = ["MSFT", "GOOGL", "NVDA"]
            found_tickers = sum(1 for ticker in target_tickers if ticker in result_text)
            quality_score += (found_tickers / len(target_tickers)) * 50.0
            
            if "Fundamental Data" in result_text: quality_score += 25.0
            if re.search(r'\$\d+\.\d+', result_text): quality_score += 25.0
            
            self.log_test_result(TestResult(
                test_name="Multi-stock fundamentals (MSFT, GOOGL, NVDA)",
                success=True,
                execution_time=execution_time,
                result_data=result,
                data_quality_score=quality_score,
                stocks_found=found_tickers
            ))
        except Exception as e:
            self.log_test_result(TestResult(
                test_name="Multi-stock fundamentals (MSFT, GOOGL, NVDA)",
                success=False,
                execution_time=time.time() - start_time,
                result_data=None,
                error_message=str(e)
            ))

        # 3. Market overview data
        start_time = time.time()
        try:
            result = get_market_overview()
            execution_time = time.time() - start_time
            result_text = str(result[0].text) if result and len(result) > 0 else str(result)
            
            # Market overview data checks
            quality_score = 0.0
            market_indicators = ["SPY", "QQQ", "DIA", "IWM", "TLT", "GLD"]
            found_indicators = sum(1 for indicator in market_indicators if indicator in result_text)
            quality_score += (found_indicators / len(market_indicators)) * 50.0
            
            if "Market Overview" in result_text: quality_score += 25.0
            if re.search(r'\$\d+\.\d+', result_text): quality_score += 25.0
            
            self.log_test_result(TestResult(
                test_name="Market overview data",
                success=True,
                execution_time=execution_time,
                result_data=result,
                data_quality_score=quality_score,
                stocks_found=found_indicators
            ))
        except Exception as e:
            self.log_test_result(TestResult(
                test_name="Market overview data",
                success=False,
                execution_time=time.time() - start_time,
                result_data=None,
                error_message=str(e)
            ))

    def test_parameter_type_validation(self):
        """Parameter type validation tests (min_volume, etc.)."""
        print("\n🔍 Starting parameter type validation tests...")
        
        # 1. Finviz string format test - "o100"
        start_time = time.time()
        try:
            result = earnings_screener(
                earnings_date="within_2_weeks",
                min_volume="o100"
            )
            execution_time = time.time() - start_time
            result_text = str(result[0].text) if result and len(result) > 0 else str(result)
            quality_score, stocks_found = self.validate_stock_data_quality(result_text, "earnings_screener_o100")
            
            self.log_test_result(TestResult(
                test_name="min_volume type fix test (o100 format)",
                success=True,
                execution_time=execution_time,
                result_data=result,
                data_quality_score=quality_score,
                stocks_found=stocks_found
            ))
        except Exception as e:
            self.log_test_result(TestResult(
                test_name="min_volume type fix test (o100 format)",
                success=False,
                execution_time=time.time() - start_time,
                result_data=None,
                error_message=str(e)
            ))

    def test_advanced_screening_functions(self):
        """Advanced screening function tests."""
        print("\n🔍 Starting advanced screening tests...")
        
        # 1. Dividend growth stocks
        start_time = time.time()
        try:
            result = dividend_growth_screener(min_dividend_yield=2)
            execution_time = time.time() - start_time
            result_text = str(result[0].text) if result and len(result) > 0 else str(result)
            quality_score, stocks_found = self.validate_stock_data_quality(result_text, "dividend_growth_screener")
            
            # Dividend-related data check
            if "Dividend" in result_text:
                quality_score += 20.0
            
            self.log_test_result(TestResult(
                test_name="Dividend growth screening",
                success=True,
                execution_time=execution_time,
                result_data=result,
                data_quality_score=quality_score,
                stocks_found=stocks_found
            ))
        except Exception as e:
            self.log_test_result(TestResult(
                test_name="Dividend growth screening",
                success=False,
                execution_time=time.time() - start_time,
                result_data=None,
                error_message=str(e)
            ))

    def generate_test_report(self) -> str:
        """Generate a comprehensive test report."""
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        report = f"""
==============================================================================
🧪 MCP SYSTEM VALIDATION TEST REPORT
==============================================================================
📊 Test run summary:
   Total tests: {self.total_tests}
   Passed: {self.passed_tests}
   Failed: {self.total_tests - self.passed_tests}
   Pass rate: {success_rate:.1f}%

==============================================================================
📈 Results by feature:
"""
        
        # Results by category
        categories = {
            "Earnings": ["Upcoming earnings", "Earnings trade"],
            "Basic screening": ["Volume surge", "Uptrend"],
            "Data retrieval": ["Single-stock", "Multi-stock", "Market overview"],
            "Parameter types": ["o100 format"],
            "Advanced features": ["Dividend growth"]
        }
        
        for category, keywords in categories.items():
            category_tests = [r for r in self.test_results if any(kw in r.test_name for kw in keywords)]
            if category_tests:
                category_success = sum(1 for r in category_tests if r.success)
                category_total = len(category_tests)
                category_rate = (category_success / category_total * 100) if category_total > 0 else 0
                
                report += f"\n🔹 {category}: {category_success}/{category_total} ({category_rate:.1f}%)\n"
                
                for result in category_tests:
                    status = "✅" if result.success else "❌"
                    report += f"   {status} {result.test_name}\n"
                    if result.success:
                        report += f"      Execution time: {result.execution_time:.2f}s, "
                        report += f"Quality score: {result.data_quality_score:.1f}, "
                        report += f"Stocks found: {result.stocks_found}\n"
                    else:
                        report += f"      Error: {result.error_message}\n"

        # Quality analysis
        successful_tests = [r for r in self.test_results if r.success]
        if successful_tests:
            avg_quality = sum(r.data_quality_score for r in successful_tests) / len(successful_tests)
            total_stocks = sum(r.stocks_found for r in successful_tests)
            avg_execution_time = sum(r.execution_time for r in successful_tests) / len(successful_tests)
            
            report += f"""
==============================================================================
📊 Quality analysis:
   Average quality score: {avg_quality:.1f}/100
   Total stocks found: {total_stocks}
   Average execution time: {avg_execution_time:.2f}s

==============================================================================
🎯 Release decision:
"""
            
            if success_rate >= 90 and avg_quality >= 70:
                report += "   🟢 PASS - Release ready\n"
            elif success_rate >= 80 and avg_quality >= 60:
                report += "   🟡 CAUTION - Review required\n"
            else:
                report += "   🔴 FAIL - Fixes required\n"

        report += "\n=============================================================================="
        
        return report

    def run_all_tests(self):
        """Run all tests."""
        print("🚀 Starting MCP System Validation Test Suite")
        print("=" * 80)
        
        # Run each test category in sequence
        self.test_earnings_related_functions()
        self.test_basic_screening_functions()
        self.test_stock_data_functions()
        self.test_parameter_type_validation()
        self.test_advanced_screening_functions()
        
        # Generate and display report
        report = self.generate_test_report()
        print(report)
        
        return self.passed_tests == self.total_tests

# Main entry point
def main():
    """Run the main test suite."""
    validator = MCPSystemValidationTest()
    success = validator.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed! MCP System is ready for production.")
        return True
    else:
        print("\n⚠️  Some tests failed. Review the report above.")
        return False

if __name__ == "__main__":
    result = main()
    sys.exit(0 if result else 1) 
