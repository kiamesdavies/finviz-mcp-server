#!/usr/bin/env python3
"""
Comprehensive test suite for Finviz MCP Server.
Tests all MCP tools with both mocked and live API tests.

Run with: pytest tests/test_server.py -v
Run live tests: pytest tests/test_server.py -v -m live
"""

import os
import sys
import pytest
from typing import List
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import server and related modules
from src.server import (
    server,
    finviz_client,
    finviz_screener,
    finviz_news,
    finviz_sector,
    finviz_sec,
    earnings_screener,
    volume_surge_screener,
    get_stock_fundamentals,
    get_multiple_stocks_fundamentals,
    trend_reversion_screener,
    uptrend_screener,
    dividend_growth_screener,
    etf_screener,
    earnings_premarket_screener,
    earnings_afterhours_screener,
    earnings_trading_screener,
    earnings_winners_screener,
    upcoming_earnings_screener,
    get_stock_news,
    get_market_news,
    get_sector_news,
    get_sector_performance,
    get_industry_performance,
    get_country_performance,
    get_sector_specific_industry_performance,
    get_capitalization_performance,
    get_market_overview,
    get_relative_volume_stocks,
    technical_analysis_screener,
    get_sec_filings,
    get_major_sec_filings,
    get_insider_sec_filings,
    get_sec_filing_summary,
    get_edgar_filing_content,
    get_multiple_edgar_filing_contents,
    get_edgar_company_filings,
    get_edgar_company_facts,
    get_edgar_company_concept,
    get_moving_average_position,
)
from src.models import StockData, NewsData, SECFilingData
from mcp.types import TextContent


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def mock_stock_data():
    """Create mock StockData object for testing."""
    return StockData(
        ticker="AAPL",
        company_name="Apple Inc.",
        sector="Technology",
        industry="Consumer Electronics",
        price=185.50,
        price_change=2.35,
        volume=52000000,
        avg_volume=48000000,
        relative_volume=1.08,
        market_cap=2850000.0,  # In millions
        pe_ratio=28.5,
        forward_pe=24.2,
        peg=1.8,
        eps=6.51,
        dividend_yield=0.52,
        rsi=55.3,
        beta=1.25,
        volatility=22.5,
        performance_1w=3.2,
        performance_1m=8.5,
        sma_20=182.5,
        sma_50=178.3,
        sma_200=172.1,
        week_52_high=199.62,
        week_52_low=143.90,
        earnings_date="Jan 30",
        eps_surprise=5.2,
        revenue_surprise=3.1,
    )


@pytest.fixture
def mock_stock_data_list(mock_stock_data):
    """Create a list of mock StockData objects."""
    stocks = [mock_stock_data]
    # Add a few more mock stocks
    stocks.append(StockData(
        ticker="MSFT",
        company_name="Microsoft Corporation",
        sector="Technology",
        industry="Software - Infrastructure",
        price=405.25,
        volume=25000000,
        market_cap=3010000.0,
        pe_ratio=35.2,
        dividend_yield=0.75,
        performance_1w=2.1,
    ))
    stocks.append(StockData(
        ticker="GOOGL",
        company_name="Alphabet Inc.",
        sector="Communication Services",
        industry="Internet Content & Information",
        price=148.50,
        volume=18000000,
        market_cap=1850000.0,
        pe_ratio=24.8,
        performance_1w=1.8,
    ))
    return stocks


@pytest.fixture
def mock_news_data():
    """Create mock NewsData object for testing."""
    return NewsData(
        ticker="AAPL",
        title="Apple Reports Record Quarterly Revenue",
        source="Reuters",
        date=datetime.now(),
        url="https://example.com/news/apple-earnings",
        category="earnings"
    )


@pytest.fixture
def mock_sec_filing_data():
    """Create mock SECFilingData object for testing."""
    return SECFilingData(
        ticker="AAPL",
        filing_date="2024-01-15",
        report_date="2024-01-01",
        form="10-K",
        description="Annual Report",
        filing_url="https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=AAPL",
        document_url="https://www.sec.gov/Archives/edgar/data/320193/000032019324000001/aapl-20231230.htm"
    )


@pytest.fixture
def api_key():
    """Get API key from environment."""
    key = os.getenv('FINVIZ_API_KEY')
    return key


# ============================================================================
# Unit Tests - Earnings Screeners
# ============================================================================

class TestEarningsScreener:
    """Tests for earnings-related screeners."""

    def test_earnings_screener_basic(self, mock_stock_data_list):
        """Test basic earnings screener functionality."""
        with patch.object(finviz_screener, 'earnings_screener', return_value=mock_stock_data_list):
            result = earnings_screener(earnings_date="today_after")

            assert result is not None
            assert isinstance(result, list)
            assert len(result) > 0
            assert isinstance(result[0], TextContent)
            assert "AAPL" in result[0].text or "Earnings" in result[0].text

    def test_earnings_screener_with_filters(self, mock_stock_data_list):
        """Test earnings screener with various filters."""
        with patch.object(finviz_screener, 'earnings_screener', return_value=mock_stock_data_list):
            result = earnings_screener(
                earnings_date="this_week",
                market_cap="large",
                min_price=10,
                max_price=500,
                min_volume=1000000,
                sectors=["Technology", "Healthcare"]
            )

            assert result is not None
            assert isinstance(result, list)

    def test_earnings_screener_empty_results(self):
        """Test earnings screener with no results."""
        with patch.object(finviz_screener, 'earnings_screener', return_value=[]):
            result = earnings_screener(earnings_date="today_after")

            assert result is not None
            assert "No stocks found" in result[0].text

    def test_earnings_screener_invalid_date(self):
        """Test earnings screener with invalid earnings date."""
        result = earnings_screener(earnings_date="invalid_date")

        assert result is not None
        assert "Error" in result[0].text or "Invalid" in result[0].text

    def test_volume_surge_screener(self, mock_stock_data_list):
        """Test volume surge screener."""
        with patch.object(finviz_screener, 'volume_surge_screener', return_value=mock_stock_data_list):
            result = volume_surge_screener()

            assert result is not None
            assert isinstance(result, list)

    def test_earnings_premarket_screener(self, mock_stock_data_list):
        """Test earnings premarket screener."""
        with patch.object(finviz_screener, 'earnings_premarket_screener', return_value=mock_stock_data_list):
            result = earnings_premarket_screener()

            assert result is not None
            assert isinstance(result, list)

    def test_earnings_afterhours_screener(self, mock_stock_data_list):
        """Test earnings afterhours screener."""
        with patch.object(finviz_screener, 'earnings_afterhours_screener', return_value=mock_stock_data_list):
            result = earnings_afterhours_screener()

            assert result is not None
            assert isinstance(result, list)

    def test_earnings_trading_screener(self, mock_stock_data_list):
        """Test earnings trading screener."""
        with patch.object(finviz_screener, 'earnings_trading_screener', return_value=mock_stock_data_list):
            result = earnings_trading_screener()

            assert result is not None
            assert isinstance(result, list)

    def test_earnings_winners_screener(self, mock_stock_data_list):
        """Test earnings winners screener."""
        with patch.object(finviz_screener, 'earnings_winners_screener', return_value=mock_stock_data_list):
            result = earnings_winners_screener(
                earnings_period="this_week",
                market_cap="smallover"
            )

            assert result is not None
            assert isinstance(result, list)

    def test_upcoming_earnings_screener(self, mock_stock_data_list):
        """Test upcoming earnings screener."""
        with patch.object(finviz_screener, 'upcoming_earnings_screener', return_value=mock_stock_data_list):
            result = upcoming_earnings_screener(
                earnings_period="next_week",
                market_cap="smallover"
            )

            assert result is not None
            assert isinstance(result, list)


# ============================================================================
# Unit Tests - Fundamental Data
# ============================================================================

class TestFundamentalsTools:
    """Tests for fundamental data tools."""

    def test_get_stock_fundamentals_single(self, mock_stock_data):
        """Test single stock fundamentals retrieval."""
        # Convert mock_stock_data to dict format as the client returns
        mock_data = mock_stock_data.to_dict()

        with patch.object(finviz_client, 'get_stock_fundamentals', return_value=mock_data):
            result = get_stock_fundamentals(ticker="AAPL")

            assert result is not None
            assert isinstance(result, list)
            assert len(result) > 0
            assert "AAPL" in result[0].text

    def test_get_stock_fundamentals_with_fields(self, mock_stock_data):
        """Test stock fundamentals with specific fields."""
        mock_data = mock_stock_data.to_dict()

        with patch.object(finviz_client, 'get_stock_fundamentals', return_value=mock_data):
            result = get_stock_fundamentals(
                ticker="AAPL",
                data_fields=["price", "pe_ratio", "dividend_yield"]
            )

            assert result is not None
            assert isinstance(result, list)

    def test_get_stock_fundamentals_invalid_ticker(self):
        """Test stock fundamentals with invalid ticker."""
        # Invalid ticker should raise ValueError
        with pytest.raises(ValueError):
            get_stock_fundamentals(ticker="invalid123")

    def test_get_stock_fundamentals_not_found(self):
        """Test stock fundamentals for non-existent ticker."""
        with patch.object(finviz_client, 'get_stock_fundamentals', return_value=None):
            result = get_stock_fundamentals(ticker="XXXXX")

            assert result is not None
            assert "No data found" in result[0].text

    def test_get_multiple_stocks_fundamentals(self, mock_stock_data_list):
        """Test multiple stocks fundamentals retrieval."""
        mock_data = [s.to_dict() for s in mock_stock_data_list]

        with patch.object(finviz_client, 'get_multiple_stocks_fundamentals', return_value=mock_data):
            result = get_multiple_stocks_fundamentals(
                tickers=["AAPL", "MSFT", "GOOGL"]
            )

            assert result is not None
            assert isinstance(result, list)

    def test_get_multiple_stocks_fundamentals_empty(self):
        """Test multiple stocks fundamentals with empty list."""
        with pytest.raises(ValueError):
            get_multiple_stocks_fundamentals(tickers=[])


# ============================================================================
# Unit Tests - Trend Analysis
# ============================================================================

class TestTrendAnalysisTools:
    """Tests for trend analysis tools."""

    def test_trend_reversion_screener(self, mock_stock_data_list):
        """Test trend reversion screener."""
        with patch.object(finviz_screener, 'trend_reversion_screener', return_value=mock_stock_data_list):
            result = trend_reversion_screener(
                market_cap="mid_large",
                rsi_max=30
            )

            assert result is not None
            assert isinstance(result, list)

    def test_uptrend_screener(self, mock_stock_data_list):
        """Test uptrend screener."""
        with patch.object(finviz_screener, 'uptrend_screener', return_value=mock_stock_data_list):
            result = uptrend_screener()

            assert result is not None
            assert isinstance(result, list)

    def test_technical_analysis_screener(self, mock_stock_data_list):
        """Test technical analysis screener."""
        with patch.object(finviz_screener, 'screen_stocks', return_value=mock_stock_data_list):
            result = technical_analysis_screener(
                rsi_min=30,
                rsi_max=70,
                price_vs_sma200="above",
                min_price=10
            )

            assert result is not None
            assert isinstance(result, list)


# ============================================================================
# Unit Tests - Dividend and ETF Screeners
# ============================================================================

class TestDividendAndETFScreeners:
    """Tests for dividend and ETF screeners."""

    def test_dividend_growth_screener(self, mock_stock_data_list):
        """Test dividend growth screener."""
        with patch.object(finviz_screener, 'dividend_growth_screener', return_value=mock_stock_data_list):
            result = dividend_growth_screener(
                min_dividend_yield=2.0,
                max_pe_ratio=30.0
            )

            assert result is not None
            assert isinstance(result, list)

    def test_dividend_growth_screener_default_params(self, mock_stock_data_list):
        """Test dividend growth screener with default parameters."""
        with patch.object(finviz_screener, 'dividend_growth_screener', return_value=mock_stock_data_list):
            result = dividend_growth_screener()

            assert result is not None
            assert isinstance(result, list)

    def test_etf_screener(self, mock_stock_data_list):
        """Test ETF screener."""
        with patch.object(finviz_screener, 'etf_screener', return_value=mock_stock_data_list):
            result = etf_screener(
                strategy_type="long",
                asset_class="equity"
            )

            assert result is not None
            assert isinstance(result, list)


# ============================================================================
# Unit Tests - News Tools
# ============================================================================

class TestNewsTools:
    """Tests for news retrieval tools."""

    def test_get_stock_news(self, mock_news_data):
        """Test stock news retrieval."""
        with patch.object(finviz_news, 'get_stock_news', return_value=[mock_news_data]):
            result = get_stock_news(tickers="AAPL", days_back=7)

            assert result is not None
            assert isinstance(result, list)

    def test_get_stock_news_multiple_tickers(self, mock_news_data):
        """Test stock news for multiple tickers."""
        with patch.object(finviz_news, 'get_stock_news', return_value=[mock_news_data]):
            result = get_stock_news(tickers="AAPL,MSFT", days_back=7)

            assert result is not None
            assert isinstance(result, list)

    def test_get_stock_news_empty(self):
        """Test stock news with no results."""
        with patch.object(finviz_news, 'get_stock_news', return_value=[]):
            result = get_stock_news(tickers="AAPL", days_back=7)

            assert result is not None
            assert "No news found" in result[0].text

    def test_get_market_news(self, mock_news_data):
        """Test market news retrieval."""
        with patch.object(finviz_news, 'get_market_news', return_value=[mock_news_data]):
            result = get_market_news(days_back=3, max_items=20)

            assert result is not None
            assert isinstance(result, list)

    def test_get_sector_news(self, mock_news_data):
        """Test sector news retrieval."""
        with patch.object(finviz_news, 'get_sector_news', return_value=[mock_news_data]):
            result = get_sector_news(sector="Technology", days_back=5)

            assert result is not None
            assert isinstance(result, list)


# ============================================================================
# Unit Tests - Market Analysis Tools
# ============================================================================

class TestMarketAnalysisTools:
    """Tests for market analysis tools."""

    def test_get_sector_performance(self):
        """Test sector performance retrieval."""
        mock_data = [
            {"name": "Technology", "market_cap": "10.5T", "pe_ratio": "28.5", "dividend_yield": "0.8%", "change": "+2.5%", "stocks": "450"}
        ]

        with patch.object(finviz_sector, 'get_sector_performance', return_value=mock_data):
            result = get_sector_performance()

            assert result is not None
            assert isinstance(result, list)

    def test_get_industry_performance(self):
        """Test industry performance retrieval."""
        mock_data = [
            {"industry": "Software - Infrastructure", "market_cap": "3.5T", "pe_ratio": "35.2", "change": "+1.8%", "stocks": "120"}
        ]

        with patch.object(finviz_sector, 'get_industry_performance', return_value=mock_data):
            result = get_industry_performance()

            assert result is not None
            assert isinstance(result, list)

    def test_get_country_performance(self):
        """Test country performance retrieval."""
        mock_data = [
            {"country": "USA", "market_cap": "45.2T", "pe_ratio": "22.1", "change": "+1.2%", "stocks": "5800"}
        ]

        with patch.object(finviz_sector, 'get_country_performance', return_value=mock_data):
            result = get_country_performance()

            assert result is not None
            assert isinstance(result, list)

    def test_get_sector_specific_industry_performance(self):
        """Test sector-specific industry performance."""
        mock_data = [
            {"industry": "Semiconductors", "market_cap": "1.2T", "pe_ratio": "32.5", "change": "+3.2%", "stocks": "45"}
        ]

        with patch.object(finviz_sector, 'get_sector_specific_industry_performance', return_value=mock_data):
            result = get_sector_specific_industry_performance(sector="technology")

            assert result is not None
            assert isinstance(result, list)

    def test_get_capitalization_performance(self):
        """Test capitalization performance retrieval."""
        mock_data = [
            {"capitalization": "Mega Cap", "market_cap": "35.2T", "pe_ratio": "25.5", "change": "+1.5%", "stocks": "120"}
        ]

        with patch.object(finviz_sector, 'get_capitalization_performance', return_value=mock_data):
            result = get_capitalization_performance()

            assert result is not None
            assert isinstance(result, list)

    def test_get_market_overview(self, mock_stock_data_list):
        """Test market overview."""
        mock_etf_data = [{"ticker": "SPY", "price": 485.50, "change": 1.2}]

        with patch.object(finviz_client, 'get_multiple_stocks_fundamentals', return_value=mock_etf_data):
            with patch.object(finviz_screener, 'volume_surge_screener', return_value=mock_stock_data_list):
                with patch.object(finviz_screener, 'uptrend_screener', return_value=mock_stock_data_list):
                    with patch.object(finviz_screener, 'earnings_screener', return_value=mock_stock_data_list):
                        result = get_market_overview()

                        assert result is not None
                        assert isinstance(result, list)


# ============================================================================
# Unit Tests - Relative Volume
# ============================================================================

class TestRelativeVolumeTools:
    """Tests for relative volume tools."""

    def test_get_relative_volume_stocks(self, mock_stock_data_list):
        """Test relative volume stocks retrieval."""
        with patch.object(finviz_screener, 'screen_stocks', return_value=mock_stock_data_list):
            result = get_relative_volume_stocks(
                min_relative_volume=2.0,
                min_price=10,
                max_results=50
            )

            assert result is not None
            assert isinstance(result, list)


# ============================================================================
# Unit Tests - SEC Filing Tools
# ============================================================================

class TestSECFilingTools:
    """Tests for SEC filing tools."""

    def test_get_sec_filings(self, mock_sec_filing_data):
        """Test SEC filings retrieval."""
        with patch.object(finviz_sec, 'get_sec_filings', return_value=[mock_sec_filing_data]):
            result = get_sec_filings(ticker="AAPL", days_back=30)

            assert result is not None
            assert isinstance(result, list)

    def test_get_sec_filings_with_form_types(self, mock_sec_filing_data):
        """Test SEC filings with form type filter."""
        with patch.object(finviz_sec, 'get_sec_filings', return_value=[mock_sec_filing_data]):
            result = get_sec_filings(
                ticker="AAPL",
                form_types=["10-K", "10-Q"],
                days_back=90
            )

            assert result is not None
            assert isinstance(result, list)

    def test_get_major_sec_filings(self, mock_sec_filing_data):
        """Test major SEC filings retrieval."""
        with patch.object(finviz_sec, 'get_major_filings', return_value=[mock_sec_filing_data]):
            result = get_major_sec_filings(ticker="AAPL", days_back=90)

            assert result is not None
            assert isinstance(result, list)

    def test_get_insider_sec_filings(self, mock_sec_filing_data):
        """Test insider SEC filings retrieval."""
        with patch.object(finviz_sec, 'get_insider_filings', return_value=[mock_sec_filing_data]):
            result = get_insider_sec_filings(ticker="AAPL", days_back=30)

            assert result is not None
            assert isinstance(result, list)

    def test_get_sec_filing_summary(self):
        """Test SEC filing summary."""
        mock_summary = {
            "total_filings": 15,
            "period_days": 90,
            "latest_filing_date": "2024-01-15",
            "latest_filing_form": "10-K",
            "forms": {"10-K": 1, "10-Q": 3, "8-K": 5, "4": 6}
        }

        with patch.object(finviz_sec, 'get_filing_summary', return_value=mock_summary):
            result = get_sec_filing_summary(ticker="AAPL", days_back=90)

            assert result is not None
            assert isinstance(result, list)


# ============================================================================
# Unit Tests - Moving Average Position
# ============================================================================

class TestMovingAveragePosition:
    """Tests for moving average position tool."""

    def test_get_moving_average_position(self, mock_stock_data):
        """Test moving average position retrieval."""
        mock_fundamentals = {
            "price": 185.50,
            "20_day_simple_moving_average": "-2.5%",
            "50_day_simple_moving_average": "-5.2%",
            "200_day_simple_moving_average": "+8.3%",
        }

        with patch.object(finviz_client, 'get_stock_fundamentals', return_value=mock_fundamentals):
            result = get_moving_average_position(ticker="AAPL")

            assert result is not None
            assert isinstance(result, list)
            assert "Moving Average Position" in result[0].text

    def test_get_moving_average_position_invalid_ticker(self):
        """Test moving average position with invalid ticker."""
        with pytest.raises(ValueError):
            get_moving_average_position(ticker="invalid123")


# ============================================================================
# Live Integration Tests (marked with 'live')
# ============================================================================

@pytest.mark.live
class TestLiveIntegration:
    """Live integration tests using real Finviz API.

    These tests require a valid FINVIZ_API_KEY in .env file.
    Run with: pytest tests/test_server.py -v -m live
    """

    @pytest.fixture(autouse=True)
    def check_api_key(self, api_key):
        """Skip live tests if no API key is available."""
        if not api_key:
            pytest.skip("FINVIZ_API_KEY not found in environment")

    def test_live_get_stock_fundamentals(self):
        """Live test for stock fundamentals."""
        result = get_stock_fundamentals(ticker="AAPL")

        assert result is not None
        assert isinstance(result, list)
        assert len(result) > 0
        # Should contain price data
        assert "Price" in result[0].text or "AAPL" in result[0].text

    def test_live_get_multiple_stocks_fundamentals(self):
        """Live test for multiple stocks fundamentals."""
        result = get_multiple_stocks_fundamentals(tickers=["AAPL", "MSFT"])

        assert result is not None
        assert isinstance(result, list)
        assert len(result) > 0

    def test_live_get_sector_performance(self):
        """Live test for sector performance."""
        result = get_sector_performance()

        assert result is not None
        assert isinstance(result, list)
        assert len(result) > 0

    def test_live_get_industry_performance(self):
        """Live test for industry performance."""
        result = get_industry_performance()

        assert result is not None
        assert isinstance(result, list)

    def test_live_get_country_performance(self):
        """Live test for country performance."""
        result = get_country_performance()

        assert result is not None
        assert isinstance(result, list)

    def test_live_get_capitalization_performance(self):
        """Live test for capitalization performance."""
        result = get_capitalization_performance()

        assert result is not None
        assert isinstance(result, list)

    def test_live_get_moving_average_position(self):
        """Live test for moving average position."""
        result = get_moving_average_position(ticker="AAPL")

        assert result is not None
        assert isinstance(result, list)
        assert "Moving Average Position" in result[0].text

    def test_live_uptrend_screener(self):
        """Live test for uptrend screener."""
        result = uptrend_screener()

        assert result is not None
        assert isinstance(result, list)

    def test_live_volume_surge_screener(self):
        """Live test for volume surge screener."""
        result = volume_surge_screener()

        assert result is not None
        assert isinstance(result, list)


# ============================================================================
# Error Handling Tests
# ============================================================================

class TestErrorHandling:
    """Tests for error handling."""

    def test_invalid_ticker_format(self):
        """Test handling of invalid ticker formats."""
        invalid_tickers = ["", "123", "TOOLONGTICKER", "invalid!"]

        for ticker in invalid_tickers:
            with pytest.raises(ValueError):
                get_stock_fundamentals(ticker=ticker)

    def test_invalid_market_cap(self, mock_stock_data_list):
        """Test handling of invalid market cap filter."""
        result = earnings_screener(
            earnings_date="today_after",
            market_cap="invalid_cap"
        )

        assert result is not None
        assert "Error" in result[0].text or "Invalid" in result[0].text

    def test_network_error_handling(self):
        """Test handling of network errors."""
        with patch.object(finviz_client, 'get_stock_fundamentals', side_effect=ConnectionError("Network error")):
            result = get_stock_fundamentals(ticker="AAPL")

            assert result is not None
            assert "Error" in result[0].text

    def test_timeout_error_handling(self):
        """Test handling of timeout errors."""
        with patch.object(finviz_client, 'get_stock_fundamentals', side_effect=TimeoutError("Request timed out")):
            result = get_stock_fundamentals(ticker="AAPL")

            assert result is not None
            assert "Error" in result[0].text


# ============================================================================
# Validation Tests
# ============================================================================

class TestValidation:
    """Tests for input validation."""

    def test_validate_ticker_valid(self):
        """Test valid ticker validation."""
        from src.utils.validators import validate_ticker

        assert validate_ticker("AAPL") == True
        assert validate_ticker("MSFT") == True
        assert validate_ticker("A") == True
        assert validate_ticker("GOOGL") == True

    def test_validate_ticker_invalid(self):
        """Test invalid ticker validation."""
        from src.utils.validators import validate_ticker

        assert validate_ticker("") == False
        assert validate_ticker("123") == False
        assert validate_ticker("TOOLONG") == False
        assert validate_ticker("invalid") == False

    def test_validate_market_cap(self):
        """Test market cap validation."""
        from src.utils.validators import validate_market_cap

        assert validate_market_cap("large") == True
        assert validate_market_cap("mid") == True
        assert validate_market_cap("small") == True
        assert validate_market_cap("mega") == True
        assert validate_market_cap("smallover") == True
        assert validate_market_cap("invalid") == False

    def test_validate_earnings_date(self):
        """Test earnings date validation."""
        from src.utils.validators import validate_earnings_date

        assert validate_earnings_date("today_after") == True
        assert validate_earnings_date("today_before") == True
        assert validate_earnings_date("this_week") == True
        assert validate_earnings_date("next_week") == True
        assert validate_earnings_date("invalid") == False

    def test_validate_price_range(self):
        """Test price range validation."""
        from src.utils.validators import validate_price_range

        assert validate_price_range(10, 100) == True
        assert validate_price_range(None, 100) == True
        assert validate_price_range(10, None) == True
        assert validate_price_range(100, 10) == False  # min > max
        assert validate_price_range(-10, 100) == False  # negative

    def test_validate_sector(self):
        """Test sector validation."""
        from src.utils.validators import validate_sector

        assert validate_sector("Technology") == True
        assert validate_sector("Healthcare") == True
        assert validate_sector("Financial") == True
        assert validate_sector("technology") == True
        assert validate_sector("InvalidSector") == False


# ============================================================================
# Data Model Tests
# ============================================================================

class TestDataModels:
    """Tests for data models."""

    def test_stock_data_to_dict(self, mock_stock_data):
        """Test StockData to_dict conversion."""
        data_dict = mock_stock_data.to_dict()

        assert isinstance(data_dict, dict)
        assert data_dict['ticker'] == "AAPL"
        assert data_dict['price'] == 185.50
        assert data_dict['sector'] == "Technology"

    def test_stock_data_from_dict(self):
        """Test StockData from_dict creation."""
        data = {
            "ticker": "MSFT",
            "company_name": "Microsoft",
            "sector": "Technology",
            "industry": "Software",
            "price": 405.25
        }

        stock = StockData.from_dict(data)

        assert stock.ticker == "MSFT"
        assert stock.price == 405.25

    def test_news_data_to_dict(self, mock_news_data):
        """Test NewsData to_dict conversion."""
        data_dict = mock_news_data.to_dict()

        assert isinstance(data_dict, dict)
        assert data_dict['ticker'] == "AAPL"
        assert data_dict['source'] == "Reuters"

    def test_sec_filing_data_to_dict(self, mock_sec_filing_data):
        """Test SECFilingData to_dict conversion."""
        data_dict = mock_sec_filing_data.to_dict()

        assert isinstance(data_dict, dict)
        assert data_dict['ticker'] == "AAPL"
        assert data_dict['form'] == "10-K"


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    # Run all tests except live tests by default
    pytest.main([__file__, "-v", "-m", "not live"])
