#!/usr/bin/env python3
"""
Pytest configuration and shared fixtures for Finviz MCP Server tests.
"""

import os
import sys
import pytest
from datetime import datetime
from typing import List

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "live: marks tests as live integration tests (require API key)"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow-running"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests (no external dependencies)"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on markers."""
    # Skip live tests if --run-live is not provided
    if not config.getoption("--run-live", default=False):
        skip_live = pytest.mark.skip(reason="need --run-live option to run live tests")
        for item in items:
            if "live" in item.keywords:
                item.add_marker(skip_live)


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--run-live",
        action="store_true",
        default=False,
        help="run live integration tests that require API key"
    )


# ============================================================================
# Shared Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def api_key():
    """Get API key from environment (session-scoped for efficiency)."""
    return os.getenv('FINVIZ_API_KEY')


@pytest.fixture(scope="session")
def has_api_key(api_key):
    """Check if API key is available."""
    return api_key is not None and len(api_key) > 0


@pytest.fixture
def mock_stock_data():
    """Create mock StockData object for testing."""
    from src.models import StockData

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
        market_cap=2850000.0,
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
    from src.models import StockData

    stocks = [mock_stock_data]

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

    stocks.append(StockData(
        ticker="NVDA",
        company_name="NVIDIA Corporation",
        sector="Technology",
        industry="Semiconductors",
        price=875.50,
        volume=35000000,
        market_cap=2150000.0,
        pe_ratio=68.5,
        performance_1w=5.8,
        eps_surprise=12.5,
    ))

    stocks.append(StockData(
        ticker="AMZN",
        company_name="Amazon.com Inc.",
        sector="Consumer Cyclical",
        industry="Internet Retail",
        price=178.25,
        volume=42000000,
        market_cap=1850000.0,
        pe_ratio=58.2,
        performance_1w=2.5,
    ))

    return stocks


@pytest.fixture
def mock_news_data():
    """Create mock NewsData object for testing."""
    from src.models import NewsData

    return NewsData(
        ticker="AAPL",
        title="Apple Reports Record Quarterly Revenue",
        source="Reuters",
        date=datetime.now(),
        url="https://example.com/news/apple-earnings",
        category="earnings"
    )


@pytest.fixture
def mock_news_data_list(mock_news_data):
    """Create a list of mock NewsData objects."""
    from src.models import NewsData

    news_list = [mock_news_data]

    news_list.append(NewsData(
        ticker="AAPL",
        title="Apple Announces New Product Line",
        source="CNBC",
        date=datetime.now(),
        url="https://example.com/news/apple-products",
        category="general"
    ))

    news_list.append(NewsData(
        ticker="AAPL",
        title="Apple Stock Rises on Strong Earnings",
        source="Bloomberg",
        date=datetime.now(),
        url="https://example.com/news/apple-stock",
        category="analyst"
    ))

    return news_list


@pytest.fixture
def mock_sec_filing_data():
    """Create mock SECFilingData object for testing."""
    from src.models import SECFilingData

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
def mock_sec_filing_data_list(mock_sec_filing_data):
    """Create a list of mock SECFilingData objects."""
    from src.models import SECFilingData

    filings = [mock_sec_filing_data]

    filings.append(SECFilingData(
        ticker="AAPL",
        filing_date="2023-11-03",
        report_date="2023-09-30",
        form="10-Q",
        description="Quarterly Report",
        filing_url="https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=AAPL",
        document_url="https://www.sec.gov/Archives/edgar/data/320193/000032019323000001/aapl-20230930.htm"
    ))

    filings.append(SECFilingData(
        ticker="AAPL",
        filing_date="2024-01-10",
        report_date="2024-01-10",
        form="8-K",
        description="Current Report",
        filing_url="https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=AAPL",
        document_url="https://www.sec.gov/Archives/edgar/data/320193/000032019324000002/aapl-20240110.htm"
    ))

    return filings


@pytest.fixture
def mock_sector_data():
    """Create mock sector performance data."""
    return [
        {
            "name": "Technology",
            "market_cap": "15.2T",
            "pe_ratio": "32.5",
            "dividend_yield": "0.8%",
            "change": "+2.5%",
            "stocks": "650"
        },
        {
            "name": "Healthcare",
            "market_cap": "8.5T",
            "pe_ratio": "22.1",
            "dividend_yield": "1.5%",
            "change": "+1.2%",
            "stocks": "520"
        },
        {
            "name": "Financial Services",
            "market_cap": "10.1T",
            "pe_ratio": "15.8",
            "dividend_yield": "2.8%",
            "change": "+0.8%",
            "stocks": "480"
        },
    ]


@pytest.fixture
def mock_industry_data():
    """Create mock industry performance data."""
    return [
        {
            "industry": "Software - Infrastructure",
            "market_cap": "3.5T",
            "pe_ratio": "35.2",
            "change": "+1.8%",
            "stocks": "120"
        },
        {
            "industry": "Semiconductors",
            "market_cap": "2.8T",
            "pe_ratio": "45.5",
            "change": "+3.5%",
            "stocks": "85"
        },
    ]


@pytest.fixture
def mock_capitalization_data():
    """Create mock capitalization performance data."""
    return [
        {
            "capitalization": "Mega Cap ($200B+)",
            "market_cap": "35.2T",
            "pe_ratio": "28.5",
            "change": "+1.5%",
            "stocks": "45"
        },
        {
            "capitalization": "Large Cap ($10B-$200B)",
            "market_cap": "18.5T",
            "pe_ratio": "22.8",
            "change": "+1.2%",
            "stocks": "350"
        },
        {
            "capitalization": "Mid Cap ($2B-$10B)",
            "market_cap": "8.2T",
            "pe_ratio": "18.5",
            "change": "+0.8%",
            "stocks": "680"
        },
    ]


# ============================================================================
# Helper Fixtures
# ============================================================================

@pytest.fixture
def sample_tickers():
    """Return sample ticker symbols for testing."""
    return ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]


@pytest.fixture
def sample_sectors():
    """Return sample sectors for testing."""
    return [
        "Technology",
        "Healthcare",
        "Financial Services",
        "Consumer Cyclical",
        "Communication Services"
    ]


@pytest.fixture
def sample_market_caps():
    """Return sample market cap filters for testing."""
    return ["mega", "large", "mid", "small", "smallover", "midover"]


@pytest.fixture
def sample_earnings_dates():
    """Return sample earnings date filters for testing."""
    return [
        "today_after",
        "today_before",
        "tomorrow_after",
        "tomorrow_before",
        "this_week",
        "next_week"
    ]
