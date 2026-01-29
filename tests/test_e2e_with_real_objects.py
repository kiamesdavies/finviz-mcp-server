#!/usr/bin/env python3
"""
E2E tests using real objects.
Create real StockData instances (not mocks) to test server.py behavior.
"""

import pytest
import asyncio
from unittest.mock import patch
from src.server import server
from src.models import StockData
from src.finviz_client.screener import FinvizScreener

class TestE2EWithRealObjects:
    """E2E tests using real objects."""

    def setup_method(self):
        """Create a fully populated StockData object."""
        self.real_stock_data = StockData(
            ticker="AAPL",
            company_name="Apple Inc.",
            sector="Technology",
            industry="Consumer Electronics",
            price=180.50,
            price_change=2.35,
            price_change_percent=1.32,
            volume=45000000,
            avg_volume=55000000,
            market_cap=2800000000000,
            pe_ratio=28.5,
            eps=6.12,
            eps_next_y=6.50,
            eps_surprise=0.12,
            revenue_surprise=0.08,
            dividend_yield=0.48,
            beta=1.23,
            volatility=0.25,
            # Performance attributes
            performance_1w=1.8,
            performance_1m=4.5,  # Substitute for performance_4w
            performance_3m=8.2,
            performance_6m=12.7,
            performance_ytd=18.9,
            performance_1y=22.1,
            # Technical analysis
            sma_20=175.80,
            sma_50=170.20,
            sma_200=165.10,
            rsi=58.5,
            # Growth metrics
            eps_qoq_growth=15.2,
            sales_qoq_growth=8.7,
            target_price=195.0,
            # Other financial metrics
            debt_to_equity=1.45,
            current_ratio=1.05,
            roe=28.5,
            roa=15.2,
            gross_margin=0.38,
            operating_margin=0.30,
            profit_margin=0.25,
            # Ownership info
            insider_ownership=0.07,
            institutional_ownership=0.59,
            shares_outstanding=15500000000,
            shares_float=15400000000,
            # Earnings-related
            earnings_date="2024-01-25",
            # Additional performance metrics
            performance_1min=0.05,
            performance_5min=0.12,
            performance_30min=0.35,
            performance_1h=0.58,
            performance_4h=1.25
        )

        # Test data for multiple tickers (format expected by server.py)
        self.mock_results_with_real_objects = [self.real_stock_data]

    @pytest.mark.asyncio
    async def test_earnings_trading_screener_with_real_stockdata(self):
        """Ensure earnings_trading_screener works with real StockData."""
        
        with patch.object(FinvizScreener, "earnings_trading_screener") as mock_screener:
            mock_screener.return_value = self.mock_results_with_real_objects
            
            # server.py is actually invoked
            result = await server.call_tool("earnings_trading_screener", {
                "earnings_window": "yesterday_after_today_before",
                "market_cap": "large",
                "min_price": 10.0,
                "min_avg_volume": 1000000,
                "earnings_revision": "eps_revenue_positive",
                "price_trend": "positive_change"
            })
            
            # Confirm a result is returned
            assert result is not None
            # Confirm server.py string formatting works
            assert "AAPL" in str(result)
            mock_screener.assert_called_once()

    @pytest.mark.asyncio 
    async def test_earnings_premarket_screener_real_data(self):
        """Test real data processing in earnings_premarket_screener."""
        
        with patch.object(FinvizScreener, "earnings_premarket_screener") as mock_screener:
            mock_screener.return_value = self.mock_results_with_real_objects
            
            result = await server.call_tool("earnings_premarket_screener", {
                "earnings_timing": "today_before",
                "market_cap": "large",
                "min_price": 50.0,
                "min_price_change": 2.0
            })
            
            assert result is not None
            # Confirm attribute access on real StockData succeeds
            mock_screener.assert_called_once()

    @pytest.mark.asyncio
    async def test_volume_surge_screener_comprehensive_attributes(self):
        """Comprehensive attribute test for volume_surge_screener."""
        
        # Test data with more attributes
        enhanced_stock = StockData(
            ticker="NVDA",
            company_name="NVIDIA Corporation",
            sector="Technology",
            industry="Semiconductors",
            price=450.75,
            price_change=15.25,
            price_change_percent=3.50,
            volume=85000000,
            avg_volume=45000000,
            relative_volume=1.89,
            market_cap=1100000000000,
            pe_ratio=65.2,
            eps=12.45,
            performance_1w=8.5,
            performance_1m=12.8,
            performance_3m=25.7,
            volatility=0.45,
            rsi=72.3,
            sma_20=435.80,
            sma_50=420.15,
            sma_200=385.90
        )
        
        enhanced_results = [enhanced_stock]
        
        with patch.object(FinvizScreener, "volume_surge_screener") as mock_screener:
            mock_screener.return_value = enhanced_results
            
            result = await server.call_tool("volume_surge_screener", {
                "market_cap": "large",
                "min_price": 100.0,
                "min_relative_volume": 1.5,
                "min_price_change": 3.0,
                "sma_filter": "above_sma200"
            })
            
            assert result is not None
            # Test richer attribute access
            assert enhanced_stock.relative_volume == 1.89
            assert enhanced_stock.sma_200 == 385.90
            mock_screener.assert_called_once()

    def test_stockdata_attribute_access_patterns(self):
        """Directly test attribute access patterns used by server.py."""
        
        stock = self.real_stock_data
        
        # Simulate the actual processing done in server.py
        try:
            # Basic info formatting
            basic_info = [
                f"Ticker: {stock.ticker}",
                f"Company: {stock.company_name}",
                f"Sector: {stock.sector}",
                f"Price: ${stock.price:.2f}" if stock.price else "Price: N/A"
            ]
            
            # Performance info formatting
            performance_info = [
                f"1W Performance: {stock.performance_1w:.2f}%" if stock.performance_1w else "1W Performance: N/A",
                f"1M Performance: {stock.performance_1m:.2f}%" if stock.performance_1m else "1M Performance: N/A",
                f"3M Performance: {stock.performance_3m:.2f}%" if stock.performance_3m else "3M Performance: N/A"
            ]
            
            # Earnings-related info formatting
            earnings_info = [
                f"EPS Surprise: {stock.eps_surprise:.2f}%" if stock.eps_surprise else "EPS Surprise: N/A",
                f"Revenue Surprise: {stock.revenue_surprise:.2f}%" if stock.revenue_surprise else "Revenue Surprise: N/A",
                f"EPS QoQ Growth: {stock.eps_qoq_growth:.2f}%" if stock.eps_qoq_growth else "EPS QoQ Growth: N/A"
            ]
            
            # Technical info formatting
            technical_info = [
                f"RSI: {stock.rsi:.1f}" if stock.rsi else "RSI: N/A",
                f"Volatility: {stock.volatility:.2f}" if stock.volatility else "Volatility: N/A",
                f"Beta: {stock.beta:.2f}" if stock.beta else "Beta: N/A"
            ]
            
            # Confirm all info is formatted correctly
            all_info = basic_info + performance_info + earnings_info + technical_info
            
            for info_line in all_info:
                assert isinstance(info_line, str)
                assert len(info_line) > 0
                assert "None" not in info_line  # Ensure None is not in the string
                
        except AttributeError as e:
            pytest.fail(f"AttributeError in server.py simulation: {e}")

    def test_all_performance_attributes_exist(self):
        """Ensure all performance attributes exist."""
        
        stock = self.real_stock_data
        
        # All performance attributes that server.py may reference
        performance_attrs = [
            'performance_1min', 'performance_5min', 'performance_30min', 'performance_1h',
            'performance_4h', 'performance_1w', 'performance_1m', 'performance_3m',
            'performance_6m', 'performance_ytd', 'performance_1y'
        ]
        
        missing_attrs = []
        for attr in performance_attrs:
            if not hasattr(stock, attr):
                missing_attrs.append(attr)
        
        if missing_attrs:
            pytest.fail(f"Missing performance attributes: {missing_attrs}")
        
        # Confirm each attribute value has a valid type
        for attr in performance_attrs:
            value = getattr(stock, attr)
            if value is not None:
                assert isinstance(value, (int, float)), f"{attr} has invalid type: {type(value)}"

    def test_error_prone_attribute_combinations(self):
        """Test attribute combinations that are error-prone."""
        
        # Test with some attributes set to None
        partial_stock = StockData(
            ticker="PARTIAL",
            company_name="Partial Data Corp",
            sector="Test",
            industry="Test",
            # Intentionally leave some attributes unset
            price=None,
            performance_1w=None,
            performance_1m=None,
            eps_surprise=None,
            revenue_surprise=None
        )
        
        # Test safe access patterns for None attributes
        try:
            price_text = f"Price: ${partial_stock.price:.2f}" if partial_stock.price else "Price: N/A"
            perf_1w_text = f"1W Performance: {partial_stock.performance_1w:.2f}%" if partial_stock.performance_1w else "1W Performance: N/A"
            perf_1m_text = f"1M Performance: {partial_stock.performance_1m:.2f}%" if partial_stock.performance_1m else "1M Performance: N/A"
            eps_text = f"EPS Surprise: {partial_stock.eps_surprise:.2f}%" if partial_stock.eps_surprise else "EPS Surprise: N/A"
            
            # Confirm "N/A" is set correctly
            assert price_text == "Price: N/A"
            assert perf_1w_text == "1W Performance: N/A"
            assert perf_1m_text == "1M Performance: N/A"
            assert eps_text == "EPS Surprise: N/A"
            
        except (AttributeError, TypeError) as e:
            pytest.fail(f"Error handling None attributes: {e}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 
