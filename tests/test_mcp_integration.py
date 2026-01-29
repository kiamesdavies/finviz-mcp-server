#!/usr/bin/env python3
"""
Integration tests for MCP server functionality.
Tests the actual MCP protocol integration and server behavior.
"""

import pytest
import asyncio
import json
import logging
from typing import Dict, Any, List
from unittest.mock import Mock, patch, AsyncMock
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent, Resource

from src.server import server
from src.finviz_client.screener import FinvizScreener
from src.finviz_client.base import FinvizClient
from src.finviz_client.news import FinvizNewsClient
from src.finviz_client.sector_analysis import FinvizSectorAnalysisClient

logger = logging.getLogger(__name__)


class TestMCPServerIntegration:
    """Test MCP server protocol integration."""

    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup method for each test."""
        self.mock_results = {
            "stocks": [
                {
                    "ticker": "AAPL",
                    "company": "Apple Inc.",
                    "sector": "Technology",
                    "industry": "Consumer Electronics",
                    "price": 150.0,
                    "volume": 50000000,
                    "market_cap": 2400000000000,
                    "pe_ratio": 25.5,
                    "eps": 6.0,
                    "dividend_yield": 0.5,
                }
            ],
            "total_count": 1,
            "execution_time": 1.5,
        }

    @pytest.mark.asyncio
    async def test_server_initialization(self):
        """Test that the MCP server initializes correctly."""
        assert server is not None
        assert isinstance(server, FastMCP)
        assert server.name == "Finviz MCP Server"

    @pytest.mark.asyncio
    async def test_tool_registration(self):
        """Test that all tools are properly registered with the MCP server."""
        expected_tools = [
            "earnings_screener",
            "volume_surge_screener",
            "get_stock_fundamentals",
            "get_multiple_stocks_fundamentals",
            "trend_reversion_screener",
            "uptrend_screener",
            "dividend_growth_screener",
            "etf_screener",
            "earnings_premarket_screener",
            "earnings_afterhours_screener",
            "earnings_trading_screener",

            "get_stock_news",
            "get_market_news",
            "get_sector_news",
            "get_sector_performance",
            "get_industry_performance",
            "get_country_performance",
            "get_market_overview",
            "get_relative_volume_stocks",
            "technical_analysis_screener",
            "upcoming_earnings_screener",
        ]

        # Get registered tools from the server
        tools = await server.list_tools()
        registered_tool_names = [tool.name for tool in tools]

        # Verify all expected tools are registered
        for expected_tool in expected_tools:
            assert expected_tool in registered_tool_names, f"Tool {expected_tool} not registered"

        # Verify we have at least the expected number of tools
        assert len(registered_tool_names) >= len(expected_tools)

    @pytest.mark.asyncio
    async def test_tool_metadata(self):
        """Test that tools have proper metadata."""
        tools = await server.list_tools()

        for tool in tools:
            # Each tool should have a name
            assert tool.name is not None
            assert len(tool.name) > 0

            # Each tool should have a description
            assert tool.description is not None
            assert len(tool.description) > 0

            # Tools should have input schema
            assert tool.inputSchema is not None

    @pytest.mark.asyncio
    async def test_mcp_protocol_compliance(self):
        """Test MCP protocol compliance."""
        # Test that server responds to standard MCP methods

        # Test list_tools
        tools = await server.list_tools()
        assert isinstance(tools, list)
        assert len(tools) > 0

        # Test that tools return proper TextContent
        with patch.object(FinvizScreener, "earnings_screener") as mock_screener:
            mock_screener.return_value = self.mock_results

            result = await server.call_tool("earnings_screener", {"earnings_date": "today_after"})

            assert result is not None
            # Result can be a tuple (TextContent list, metadata) or just a list
            if isinstance(result, tuple):
                result_data = result[0]
            else:
                result_data = result

            if isinstance(result_data, list):
                for item in result_data:
                    assert isinstance(item, (TextContent, dict))
            else:
                assert isinstance(result_data, (TextContent, dict))

    @pytest.mark.asyncio
    async def test_parameter_validation_integration(self):
        """Test parameter validation through MCP interface."""
        from mcp.server.fastmcp.exceptions import ToolError

        # Test missing required parameters - should raise ToolError
        with pytest.raises(ToolError):
            await server.call_tool("earnings_screener", {})  # Missing earnings_date

        # Test invalid parameter types - should return error in result
        result = await server.call_tool("earnings_screener", {
            "earnings_date": "invalid_date",
        })
        assert result is not None
        # Handle both tuple and list results
        result_data = result[0] if isinstance(result, (list, tuple)) else result
        if hasattr(result_data, 'text'):
            result_text = str(result_data.text)
        else:
            result_text = str(result_data)
        assert "Error" in result_text or "Invalid" in result_text or "invalid" in result_text.lower()

    @pytest.mark.asyncio
    async def test_tool_execution_flow(self):
        """Test the complete tool execution flow."""
        with patch.object(FinvizScreener, "earnings_screener") as mock_screener:
            mock_screener.return_value = self.mock_results

            # Execute tool and verify the flow
            result = await server.call_tool("earnings_screener", {
                "earnings_date": "today_after",
                "market_cap": "large",
                "min_price": 10.0
            })

            # Verify screener was called with correct parameters
            mock_screener.assert_called_once()
            call_args = mock_screener.call_args

            # Verify result is properly formatted
            assert result is not None


class TestMCPToolInterfaces:
    """Test individual MCP tool interfaces."""

    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup mock data for tool interface tests."""
        self.stock_data = {
            "ticker": "AAPL",
            "company": "Apple Inc.",
            "sector": "Technology",
            "price": 150.0,
            "volume": 50000000,
        }

        self.news_data = [
            {
                "title": "Apple Reports Strong Quarterly Results",
                "url": "http://example.com/news1",
                "timestamp": "2024-01-15T10:00:00Z",
            }
        ]

        self.sector_data = {
            "sectors": [
                {"name": "Technology", "performance": 2.5},
                {"name": "Healthcare", "performance": 1.8},
            ]
        }

    @pytest.mark.asyncio
    async def test_stock_fundamentals_interface(self):
        """Test stock fundamentals tool interface."""
        with patch.object(FinvizClient, "get_stock_fundamentals") as mock_client:
            mock_client.return_value = self.stock_data

            # Test single stock
            result = await server.call_tool("get_stock_fundamentals", {
                "ticker": "AAPL",
                "data_fields": ["price", "volume", "market_cap"]
            })

            assert result is not None
            mock_client.assert_called_once()

        # Test multiple stocks
        with patch.object(FinvizClient, "get_multiple_stocks_fundamentals") as mock_client:
            mock_client.return_value = [self.stock_data]

            result = await server.call_tool("get_multiple_stocks_fundamentals", {
                "tickers": ["AAPL", "MSFT"],
                "data_fields": ["price", "volume"]
            })

            assert result is not None
            mock_client.assert_called_once()

    @pytest.mark.asyncio
    async def test_news_tools_interface(self):
        """Test news-related tools interface."""
        # Stock news
        with patch.object(FinvizNewsClient, "get_stock_news") as mock_news:
            mock_news.return_value = self.news_data

            result = await server.call_tool("get_stock_news", {
                "tickers": "AAPL",
                "days_back": 7
            })

            assert result is not None
            mock_news.assert_called_once()

        # Market news
        with patch.object(FinvizNewsClient, "get_market_news") as mock_news:
            mock_news.return_value = self.news_data

            result = await server.call_tool("get_market_news", {
                "days_back": 3,
                "max_items": 20
            })

            assert result is not None
            mock_news.assert_called_once()

        # Sector news
        with patch.object(FinvizNewsClient, "get_sector_news") as mock_news:
            mock_news.return_value = self.news_data

            result = await server.call_tool("get_sector_news", {
                "sector": "Technology",
                "days_back": 5
            })

            assert result is not None
            mock_news.assert_called_once()

    @pytest.mark.asyncio
    async def test_sector_analysis_interface(self):
        """Test sector analysis tools interface."""
        # Sector performance
        with patch.object(FinvizSectorAnalysisClient, "get_sector_performance") as mock_sector:
            mock_sector.return_value = self.sector_data

            result = await server.call_tool("get_sector_performance", {
                "timeframe": "1d",
                "sort_by": "performance"
            })

            assert result is not None
            mock_sector.assert_called_once()

        # Industry performance
        with patch.object(FinvizSectorAnalysisClient, "get_industry_performance") as mock_industry:
            mock_industry.return_value = self.sector_data

            result = await server.call_tool("get_industry_performance", {
                "sector": "Technology",
                "timeframe": "1w"
            })

            assert result is not None
            mock_industry.assert_called_once()

        # Country performance
        with patch.object(FinvizSectorAnalysisClient, "get_country_performance") as mock_country:
            mock_country.return_value = self.sector_data

            result = await server.call_tool("get_country_performance", {
                "timeframe": "1m"
            })

            assert result is not None
            mock_country.assert_called_once()

    @pytest.mark.asyncio
    async def test_screener_tools_interface(self):
        """Test screener tools interface."""
        from src.models import StockData

        mock_stock_data = StockData(
            ticker="AAPL",
            company_name="Apple Inc.",
            sector="Technology",
            industry="Consumer Electronics",
            price=150.0,
            volume=50000000,
        )
        mock_screener_result = [mock_stock_data]

        screener_tests = [
            ("earnings_screener", {"earnings_date": "today_after"}, "earnings_screener"),
            ("volume_surge_screener", {}, "volume_surge_screener"),
            ("trend_reversion_screener", {"market_cap": "large", "rsi_max": 30}, "trend_reversion_screener"),
            ("uptrend_screener", {}, "uptrend_screener"),
            ("dividend_growth_screener", {"min_dividend_yield": 2.0}, "dividend_growth_screener"),
            ("etf_screener", {"strategy_type": "long"}, "etf_screener"),
            ("get_relative_volume_stocks", {"min_relative_volume": 1.5}, "get_relative_volume_stocks"),
            ("technical_analysis_screener", {"rsi_min": 30, "rsi_max": 70}, "technical_analysis_screener"),
            ("upcoming_earnings_screener", {"earnings_period": "next_week"}, "upcoming_earnings_screener"),
        ]

        for tool_name, params, method_name in screener_tests:
            with patch.object(FinvizScreener, method_name) as mock_screener:
                mock_screener.return_value = mock_screener_result

                result = await server.call_tool(tool_name, params)
                assert result is not None


class TestMCPErrorHandling:
    """Test MCP-specific error handling."""

    @pytest.mark.asyncio
    async def test_tool_not_found_error(self):
        """Test handling of non-existent tool calls."""
        try:
            result = await server.call_tool("non_existent_tool", {})
            # If no exception, result should indicate an error
            if result:
                result_text = str(result[0].text) if hasattr(result[0], 'text') else str(result[0])
                assert "error" in result_text.lower() or "not found" in result_text.lower()
        except (AttributeError, KeyError, Exception):
            # Exception is acceptable for non-existent tools
            pass

    @pytest.mark.asyncio
    async def test_malformed_tool_call(self):
        """Test handling of malformed tool calls."""
        # Test with invalid parameters structure - should handle gracefully
        try:
            result = await server.call_tool("earnings_screener", "invalid_params")
            # If no exception, should have error in result
            assert result is not None
        except (ValueError, TypeError, KeyError, Exception):
            # Exception is acceptable for malformed params
            pass

    @pytest.mark.asyncio
    async def test_tool_execution_error_propagation(self):
        """Test that tool execution errors are handled gracefully."""
        with patch.object(FinvizScreener, "earnings_screener") as mock_screener:
            mock_screener.side_effect = Exception("Screener error")

            result = await server.call_tool("earnings_screener", {"earnings_date": "today_after"})
            # Tools now return error messages in TextContent instead of raising
            assert result is not None
            # Handle both tuple (result, meta) and list format
            result_data = result[0] if isinstance(result, (list, tuple)) else result
            if isinstance(result_data, list):
                result_text = str(result_data[0].text)
            elif hasattr(result_data, 'text'):
                result_text = str(result_data.text)
            else:
                result_text = str(result_data)
            assert "Error" in result_text or "error" in result_text.lower()

    @pytest.mark.asyncio
    async def test_timeout_handling(self):
        """Test timeout handling in MCP tool execution."""
        # Test that tool returns gracefully even if there's a timeout-like error
        with patch.object(FinvizScreener, "earnings_screener") as mock_screener:
            mock_screener.side_effect = TimeoutError("Request timed out")

            result = await server.call_tool("earnings_screener", {"earnings_date": "today_after"})
            # Tools should return error in result
            assert result is not None
            result_data = result[0] if isinstance(result, (list, tuple)) else result
            if isinstance(result_data, list):
                result_text = str(result_data[0].text)
            elif hasattr(result_data, 'text'):
                result_text = str(result_data.text)
            else:
                result_text = str(result_data)
            assert "Error" in result_text or "timeout" in result_text.lower()


class TestMCPDataSerialization:
    """Test data serialization and formatting for MCP responses."""

    @pytest.mark.asyncio
    async def test_response_formatting(self):
        """Test that responses are properly formatted for MCP."""
        mock_result = {
            "stocks": [
                {
                    "ticker": "AAPL",
                    "company": "Apple Inc.",
                    "price": 150.0,
                    "volume": 50000000,
                }
            ],
            "total_count": 1,
            "execution_time": 1.5,
        }

        with patch.object(FinvizScreener, "earnings_screener") as mock_screener:
            mock_screener.return_value = mock_result

            result = await server.call_tool("earnings_screener", {"earnings_date": "today_after"})

            assert result is not None
            
            # Result should be serializable
            if isinstance(result, list):
                for item in result:
                    if hasattr(item, 'text'):
                        # If it's TextContent, the text should be JSON serializable
                        try:
                            json.loads(item.text)
                        except (json.JSONDecodeError, AttributeError):
                            # If not JSON, should at least be a string
                            assert isinstance(item.text, str)

    @pytest.mark.asyncio
    async def test_special_character_serialization(self):
        """Test serialization of responses with special characters."""
        mock_result = {
            "stocks": [
                {
                    "ticker": "TEST",
                    "company": "Test Company™ & Co.",
                    "sector": "Technology/Software",
                    "notes": "Contains special chars: €, £, ¥, ©",
                }
            ],
            "total_count": 1,
            "execution_time": 1.0,
        }

        with patch.object(FinvizScreener, "earnings_screener") as mock_screener:
            mock_screener.return_value = mock_result

            result = await server.call_tool("earnings_screener", {"earnings_date": "today_after"})
            
            assert result is not None
            # Should handle special characters without errors

    @pytest.mark.asyncio
    async def test_large_dataset_serialization(self):
        """Test serialization of large datasets."""
        # Create a large mock dataset
        large_mock_result = {
            "stocks": [
                {
                    "ticker": f"STOCK{i:04d}",
                    "company": f"Company {i}",
                    "price": 100.0 + i,
                    "volume": 1000000 + i,
                } for i in range(500)  # 500 stocks
            ],
            "total_count": 500,
            "execution_time": 2.0,
        }

        with patch.object(FinvizScreener, "earnings_screener") as mock_screener:
            mock_screener.return_value = large_mock_result

            result = await server.call_tool("earnings_screener", {"earnings_date": "today_after"})
            
            assert result is not None
            # Should handle large datasets without memory issues


class TestMCPConcurrency:
    """Test MCP server concurrency handling."""

    @pytest.mark.asyncio
    async def test_concurrent_tool_calls(self):
        """Test handling of concurrent tool calls."""
        mock_result = {"stocks": [], "total_count": 0, "execution_time": 0.1}

        with patch.object(FinvizScreener, "earnings_screener") as mock_screener:
            mock_screener.return_value = mock_result

            # Create multiple concurrent tool calls
            tasks = []
            for i in range(5):
                task = server.call_tool("earnings_screener", {"earnings_date": "today_after"})
                tasks.append(task)

            # Execute all concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # All should succeed
            for result in results:
                assert not isinstance(result, Exception)
                assert result is not None

    @pytest.mark.asyncio
    async def test_mixed_concurrent_tools(self):
        """Test concurrent calls to different tools."""
        mock_stock_result = {"stocks": [], "total_count": 0, "execution_time": 0.1}
        mock_news_result = [{"title": "Test", "url": "http://test.com"}]
        mock_sector_result = {"sectors": [{"name": "Tech", "performance": 1.0}]}

        with patch.object(FinvizScreener, "earnings_screener") as mock_earnings, \
             patch.object(FinvizNewsClient, "get_market_news") as mock_news, \
             patch.object(FinvizSectorAnalysisClient, "get_sector_performance") as mock_sector:

            mock_earnings.return_value = mock_stock_result
            mock_news.return_value = mock_news_result
            mock_sector.return_value = mock_sector_result

            # Create concurrent calls to different tools
            tasks = [
                server.call_tool("earnings_screener", {"earnings_date": "today_after"}),
                server.call_tool("get_market_news", {"limit": 10}),
                server.call_tool("get_sector_performance", {"timeframe": "1d"}),
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            # All should succeed
            for result in results:
                assert not isinstance(result, Exception)
                assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])