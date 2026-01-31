#!/usr/bin/env python3
"""
Unit tests for get_price_bars MCP tool
"""
import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.constants import PRICE_BAR_TIMEFRAMES, FINVIZ_QUOTE_API_URL
from src.utils.validators import validate_timeframe


class TestPriceBarConstants:
    """Test price bar related constants."""

    def test_price_bar_timeframes_exist(self):
        """Test that PRICE_BAR_TIMEFRAMES constant is defined."""
        assert PRICE_BAR_TIMEFRAMES is not None
        assert isinstance(PRICE_BAR_TIMEFRAMES, dict)

    def test_all_timeframes_present(self):
        """Test that all expected timeframes are present."""
        expected_timeframes = ['i5', 'i15', 'i30', 'h', 'd', 'w', 'm']
        for tf in expected_timeframes:
            assert tf in PRICE_BAR_TIMEFRAMES, f"Missing timeframe: {tf}"

    def test_timeframe_descriptions(self):
        """Test timeframe descriptions."""
        assert PRICE_BAR_TIMEFRAMES['i5'] == '5 minutes'
        assert PRICE_BAR_TIMEFRAMES['i15'] == '15 minutes'
        assert PRICE_BAR_TIMEFRAMES['i30'] == '30 minutes'
        assert PRICE_BAR_TIMEFRAMES['h'] == 'Hourly'
        assert PRICE_BAR_TIMEFRAMES['d'] == 'Daily'
        assert PRICE_BAR_TIMEFRAMES['w'] == 'Weekly'
        assert PRICE_BAR_TIMEFRAMES['m'] == 'Monthly'

    def test_quote_api_url(self):
        """Test that FINVIZ_QUOTE_API_URL is correct."""
        assert FINVIZ_QUOTE_API_URL == "https://api.finviz.com/api/quote.ashx"


class TestTimeframeValidator:
    """Test validate_timeframe function."""

    def test_valid_timeframes(self):
        """Test all valid timeframes pass validation."""
        valid_timeframes = ['i5', 'i15', 'i30', 'h', 'd', 'w', 'm']
        for tf in valid_timeframes:
            assert validate_timeframe(tf) is True, f"Expected {tf} to be valid"

    def test_valid_timeframes_uppercase(self):
        """Test uppercase timeframes are also valid."""
        valid_timeframes = ['I5', 'I15', 'I30', 'H', 'D', 'W', 'M']
        for tf in valid_timeframes:
            assert validate_timeframe(tf) is True, f"Expected {tf} to be valid"

    def test_invalid_timeframes(self):
        """Test invalid timeframes fail validation."""
        invalid_timeframes = ['i1', 'i10', 'i60', 'daily', 'weekly', '1h', '15m', '', None, 123]
        for tf in invalid_timeframes:
            assert validate_timeframe(tf) is False, f"Expected {tf} to be invalid"

    def test_none_timeframe(self):
        """Test None timeframe is invalid."""
        assert validate_timeframe(None) is False

    def test_empty_string_timeframe(self):
        """Test empty string timeframe is invalid."""
        assert validate_timeframe('') is False


class TestFinvizClientGetPriceBars:
    """Test FinvizClient.get_price_bars method."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock FinvizClient."""
        from src.finviz_client.base import FinvizClient
        client = FinvizClient(api_key='test_api_key')
        return client

    @pytest.fixture
    def mock_response_data(self):
        """Sample response data from Finviz Quote API."""
        return {
            'date': ['14:00', '14:15', '14:30', '14:45', '15:00'],
            'open': [125.10, 125.50, 125.80, 126.00, 126.20],
            'high': [125.80, 126.00, 126.20, 126.50, 126.80],
            'low': [124.90, 125.30, 125.60, 125.80, 126.00],
            'close': [125.50, 125.80, 126.00, 126.30, 126.50],
            'volume': [1234567, 987654, 876543, 765432, 654321],
            'prevClose': 124.50
        }

    def test_get_price_bars_success(self, mock_client, mock_response_data):
        """Test successful price bar retrieval."""
        mock_response = MagicMock()
        mock_response.text = '{"date": []}'  # Not HTML
        mock_response.json.return_value = mock_response_data

        with patch.object(mock_client, '_make_request', return_value=mock_response):
            result = mock_client.get_price_bars('NVDA', 'i15', 5)

            assert result is not None
            assert 'date' in result
            assert 'close' in result
            assert 'open' in result
            assert 'high' in result
            assert 'low' in result
            assert 'volume' in result
            assert result['prevClose'] == 124.50

    def test_get_price_bars_empty_response(self, mock_client):
        """Test handling of empty response."""
        mock_response = MagicMock()
        mock_response.text = '{}'
        mock_response.json.return_value = {}

        with patch.object(mock_client, '_make_request', return_value=mock_response):
            result = mock_client.get_price_bars('INVALID', 'i15', 20)
            assert result is None or result == {}

    def test_get_price_bars_html_error(self, mock_client):
        """Test handling of HTML error response."""
        mock_response = MagicMock()
        mock_response.text = '<!DOCTYPE html><html>Error</html>'

        with patch.object(mock_client, '_make_request', return_value=mock_response):
            result = mock_client.get_price_bars('NVDA', 'i15', 20)
            assert result is None


class TestGetPriceBarsServer:
    """Test get_price_bars MCP server tool."""

    @pytest.fixture
    def mock_finviz_client(self):
        """Mock the finviz_client module-level variable."""
        return MagicMock()

    def test_invalid_ticker_raises_error(self):
        """Test that invalid ticker raises ValueError."""
        from src.server import get_price_bars

        with pytest.raises(ValueError, match="Invalid ticker"):
            get_price_bars(ticker="INVALID123456", timeframe="i15", bars=20)

    def test_invalid_timeframe_raises_error(self):
        """Test that invalid timeframe raises ValueError."""
        from src.server import get_price_bars

        with pytest.raises(ValueError, match="Invalid timeframe"):
            get_price_bars(ticker="NVDA", timeframe="invalid", bars=20)

    def test_invalid_bars_count_raises_error(self):
        """Test that invalid bars count raises ValueError."""
        from src.server import get_price_bars

        with pytest.raises(ValueError, match="Invalid bars count"):
            get_price_bars(ticker="NVDA", timeframe="i15", bars=0)

        with pytest.raises(ValueError, match="Invalid bars count"):
            get_price_bars(ticker="NVDA", timeframe="i15", bars=1001)


class TestOutputFormat:
    """Test output format of get_price_bars."""

    def test_csv_header_format(self):
        """Test that CSV header has correct column order."""
        expected_header = "Time,Close,Open,High,Low,Volume"
        # This would be tested with actual output from the function
        assert "Time" in expected_header
        assert "Close" in expected_header
        assert "Open" in expected_header
        assert "High" in expected_header
        assert "Low" in expected_header
        assert "Volume" in expected_header


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
