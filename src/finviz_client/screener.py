import logging
from typing import Dict, List, Optional, Any
from urllib.parse import urlencode

from .base import FinvizClient
from ..models import StockData, ScreeningResult, UpcomingEarningsData, MARKET_CAP_FILTERS

logger = logging.getLogger(__name__)

class FinvizScreener(FinvizClient):
    """TODO: English documentation."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)
    
    def earnings_screener(self, **kwargs) -> List[StockData]:
        """TODO: English documentation."""
        filters = self._build_earnings_filters(**kwargs)
        return self.screen_stocks(filters)
    
    def volume_surge_screener(self) -> List[StockData]:
        """TODO: English documentation."""
        filters = self._build_volume_surge_filters()
        results = self.screen_stocks(filters)
        
        results.sort(key=lambda x: x.price_change or 0, reverse=True)
        
        return results
    
    def uptrend_screener(self) -> List[StockData]:
        """TODO: English documentation."""
        filters = self._build_uptrend_filters()
        results = self.screen_stocks(filters)
        
        return results
    
    def dividend_growth_screener(self, **kwargs) -> List[StockData]:
        """TODO: English documentation."""
        filters = self._build_dividend_growth_filters(**kwargs)
        results = self.screen_stocks(filters)
        
        max_results = kwargs.get('max_results', 100)
        sort_by = kwargs.get('sort_by', 'dividend_yield')
        sort_order = kwargs.get('sort_order', 'desc')
        
        if sort_by == 'dividend_yield':
            results.sort(key=lambda x: x.dividend_yield or 0, reverse=(sort_order == 'desc'))
        elif sort_by == 'market_cap':
            results.sort(key=lambda x: x.market_cap or 0, reverse=(sort_order == 'desc'))
        
        return results[:max_results]
    
    def etf_screener(self, **kwargs) -> List[StockData]:
        """TODO: English documentation."""
        filters = self._build_etf_filters(**kwargs)
        results = self.screen_stocks(filters)
        
        max_results = kwargs.get('max_results', 50)
        sort_by = kwargs.get('sort_by', 'aum')
        sort_order = kwargs.get('sort_order', 'desc')
        
        if sort_by == 'aum':
            results.sort(key=lambda x: x.aum or 0, reverse=(sort_order == 'desc'))
        elif sort_by == 'expense_ratio':
            results.sort(key=lambda x: x.net_expense_ratio or 0, reverse=(sort_order == 'asc'))
        
        return results[:max_results]
    
    def earnings_premarket_screener(self) -> List[StockData]:
        """TODO: English documentation."""
        filters = self._build_earnings_premarket_filters()
        results = self.screen_stocks(filters)
        
        results.sort(key=lambda x: x.price_change or 0, reverse=True)
        
        return results
    
    def earnings_afterhours_screener(self) -> List[StockData]:
        """TODO: English documentation."""
        filters = self._build_earnings_afterhours_filters()
        results = self.screen_stocks(filters)
        
        results.sort(key=lambda x: x.afterhours_change_percent or 0, reverse=True)
        
        return results[:60]
    
    def earnings_trading_screener(self) -> List[StockData]:
        """TODO: English documentation."""
        filters = self._build_earnings_trading_filters()
        results = self.screen_stocks(filters)
        
        results.sort(key=lambda x: x.eps_surprise or 0, reverse=True)
        
        return results[:60]
    
    def earnings_positive_surprise_screener(self, **kwargs) -> List[StockData]:
        """TODO: English documentation."""
        filters = self._build_earnings_positive_surprise_filters(**kwargs)
        results = self.screen_stocks(filters)
        
        max_results = kwargs.get('max_results', 50)
        sort_by = kwargs.get('sort_by', 'eps_qoq_growth')
        
        if sort_by == 'eps_qoq_growth':
            results.sort(key=lambda x: x.eps_growth_qtr or 0, reverse=True)
        elif sort_by == 'performance_1w':
            results.sort(key=lambda x: x.performance_1w or 0, reverse=True)
        
        return results[:max_results]
    
    def trend_reversion_screener(self, **kwargs) -> List[StockData]:
        """TODO: English documentation."""
        filters = self._build_trend_reversion_filters(**kwargs)
        results = self.screen_stocks(filters)
        
        max_results = kwargs.get('max_results', 50)
        sort_by = kwargs.get('sort_by', 'rsi')
        sort_order = kwargs.get('sort_order', 'asc')
        
        if sort_by == 'rsi':
            results.sort(key=lambda x: x.rsi or 0, reverse=(sort_order == 'desc'))
        elif sort_by == 'eps_growth_qoq':
            results.sort(key=lambda x: x.eps_growth_qtr or 0, reverse=(sort_order == 'desc'))
        
        return results[:max_results]
    
    def get_relative_volume_stocks(self, **kwargs) -> List[StockData]:
        """TODO: English documentation."""
        filters = self._build_relative_volume_filters(**kwargs)
        results = self.screen_stocks(filters)
        
        results.sort(key=lambda x: x.relative_volume or 0, reverse=True)
        
        max_results = kwargs.get('max_results', 50)
        return results[:max_results]
    
    def technical_analysis_screener(self, **kwargs) -> List[StockData]:
        """TODO: English documentation."""
        filters = self._build_technical_analysis_filters(**kwargs)
        results = self.screen_stocks(filters)
        
        max_results = kwargs.get('max_results', 50)
        return results[:max_results]
    
    def _build_earnings_filters(self, **kwargs) -> Dict[str, Any]:
        """TODO: English documentation."""
        filters = {}
        
        if 'earnings_date' in kwargs:
            filters['earnings_date'] = kwargs['earnings_date']
        
        if 'market_cap' in kwargs:
            filters['market_cap'] = kwargs['market_cap']
        
        if 'min_price' in kwargs:
            filters['price_min'] = kwargs['min_price']
        if 'max_price' in kwargs:
            filters['price_max'] = kwargs['max_price']
        
        if 'min_volume' in kwargs:
            filters['volume_min'] = kwargs['min_volume']
        
        if 'sectors' in kwargs and kwargs['sectors']:
            filters['sectors'] = kwargs['sectors']
        
        return filters
    
    def _build_volume_surge_filters(self) -> Dict[str, Any]:
        """TODO: English documentation."""
        filters = {}
        
        filters['market_cap'] = 'smallover'
        
        filters['avg_volume_min'] = 100000
        
        filters['price_min'] = 10.0
        
        filters['relative_volume_min'] = 1.5
        
        filters['price_change_min'] = 2.0
        
        filters['sma200_above'] = True
        
        filters['sort_by'] = 'price_change'
        filters['sort_order'] = 'desc'
        
        filters['stocks_only'] = True
        
        
        return filters
    
    def _build_uptrend_filters(self) -> Dict[str, Any]:
        """TODO: English documentation."""
        filters = {}
        
        filters['market_cap'] = 'microover'
        
        filters['avg_volume_min'] = 100
        
        filters['price_min'] = 10
        
        filters['near_52w_high'] = 30
        
        filters['performance_4w_positive'] = True
        
        filters['sma20_above'] = True
        filters['sma200_above'] = True
        filters['sma50_above_sma200'] = True
        
        filters['sort_by'] = 'eps_growth_yoy'
        filters['sort_order'] = 'desc'
        
        filters['stocks_only'] = True
        
        return filters
    
    def _build_dividend_growth_filters(self, **kwargs) -> Dict[str, Any]:
        """TODO: English documentation."""
        filters = {}
        
        filters['market_cap'] = kwargs.get('market_cap', 'midover')
        
        filters['dividend_yield_min'] = kwargs.get('min_dividend_yield', 2.0)
        
        filters['eps_growth_5y_positive'] = kwargs.get('eps_growth_5y_positive', True)
        filters['eps_growth_qoq_positive'] = kwargs.get('eps_growth_qoq_positive', True)
        filters['eps_growth_yoy_positive'] = kwargs.get('eps_growth_yoy_positive', True)
        
        filters['pb_ratio_max'] = kwargs.get('max_pb_ratio', 5.0)
        filters['pe_ratio_max'] = kwargs.get('max_pe_ratio', 30.0)
        
        filters['sales_growth_5y_positive'] = kwargs.get('sales_growth_5y_positive', True)
        filters['sales_growth_qoq_positive'] = kwargs.get('sales_growth_qoq_positive', True)
        
        filters['country'] = kwargs.get('country', 'USA')
        
        filters['stocks_only'] = kwargs.get('stocks_only', True)
        
        filters['sort_by'] = kwargs.get('sort_by', 'sma200')
        filters['sort_order'] = kwargs.get('sort_order', 'asc')
        
        if 'max_dividend_yield' in kwargs:
            filters['dividend_yield_max'] = kwargs['max_dividend_yield']
        
        if 'min_dividend_growth' in kwargs:
            filters['dividend_growth_min'] = kwargs['min_dividend_growth']
        
        if 'min_payout_ratio' in kwargs:
            filters['payout_ratio_min'] = kwargs['min_payout_ratio']
        
        if 'max_payout_ratio' in kwargs:
            filters['payout_ratio_max'] = kwargs['max_payout_ratio']
        
        if 'min_roe' in kwargs:
            filters['roe_min'] = kwargs['min_roe']
        
        if 'max_debt_equity' in kwargs:
            filters['debt_equity_max'] = kwargs['max_debt_equity']
        
        return filters
    
    def _build_etf_filters(self, **kwargs) -> Dict[str, Any]:
        """TODO: English documentation."""
        filters = {}
        
        strategy_type = kwargs.get('strategy_type', 'long')
        asset_class = kwargs.get('asset_class', 'equity')
        
        filters['instrument_type'] = 'etf'
        
        if 'min_aum' in kwargs:
            filters['aum_min'] = kwargs['min_aum']
        if 'max_expense_ratio' in kwargs:
            filters['expense_ratio_max'] = kwargs['max_expense_ratio']
        
        return filters
    
    def _build_earnings_premarket_filters(self) -> Dict[str, Any]:
        """TODO: English documentation."""
        filters = {}
        
        filters['earnings_date'] = 'today_before'
        
        filters['market_cap'] = 'smallover'
        
        filters['avg_volume_min'] = 100000
        
        filters['price_min'] = 10.0
        
        filters['price_change_min'] = 2.0
        
        filters['stocks_only'] = True
        
        filters['sort_by'] = 'price_change'
        filters['sort_order'] = 'desc'
        
        filters['max_results'] = 60
        
        return filters
    
    def _build_earnings_afterhours_filters(self) -> Dict[str, Any]:
        """TODO: English documentation."""
        filters = {}
        
        filters['earnings_date'] = 'today_after'
        
        filters['market_cap'] = 'smallover'
        
        filters['avg_volume_min'] = 100000
        
        filters['price_min'] = 10.0
        
        filters['afterhours_change_min'] = 2.0
        
        filters['stocks_only'] = True
        
        filters['sort_by'] = 'afterhours_change'
        filters['sort_order'] = 'desc'
        
        filters['max_results'] = 60
        
        return filters
    
    def _build_earnings_trading_filters(self) -> Dict[str, Any]:
        """TODO: English documentation."""
        filters = {
            'earnings_recent': True,
            
            'market_cap': 'midover',
            
            'earnings_revision_positive': True,
            
            'net_margin_min': 3.0,
            
            'avg_volume_min': 200000,
            
            'price_min': 30.0,
            
            'price_change_positive': True,
            
            'performance_4w_range': '0_to_negative_4w',
            
            'stocks_only': True,
            
            'sort_by': 'eps_surprise',
            'sort_order': 'desc',
            
            'max_results': 60,
            
            'screener_type': 'earnings_trading'
        }
        
        return filters
    
    def _build_earnings_positive_surprise_filters(self, **kwargs) -> Dict[str, Any]:
        """TODO: English documentation."""
        filters = {}
        
        filters['earnings_date'] = 'this_week'
        
        filters['market_cap'] = 'smallover'
        
        if 'min_price' in kwargs:
            filters['price_min'] = kwargs['min_price']
        
        growth_criteria = kwargs.get('growth_criteria', {})
        if growth_criteria.get('min_eps_qoq_growth'):
            filters['eps_growth_min'] = growth_criteria['min_eps_qoq_growth']
        
        performance_criteria = kwargs.get('performance_criteria', {})
        if performance_criteria.get('above_sma200'):
            filters['sma200_above'] = True
        
        return filters
    
    def upcoming_earnings_screener(self, **kwargs) -> List[UpcomingEarningsData]:
        """TODO: English documentation."""
        try:
            filters = self._build_upcoming_earnings_filters(**kwargs)
            
            raw_results = self.screen_stocks(filters)
            
            results = []
            for stock in raw_results:
                upcoming_data = self._convert_to_upcoming_earnings_data(stock, **kwargs)
                if upcoming_data:
                    results.append(upcoming_data)
            
            sort_by = kwargs.get('sort_by', 'earnings_date')
            sort_order = kwargs.get('sort_order', 'asc')
            results = self._sort_upcoming_earnings_results(results, sort_by, sort_order)
            
            max_results = kwargs.get('max_results', 100)
            return results[:max_results]
            
        except Exception as e:
            logger.error(f"Error in upcoming_earnings_screen: {e}")
            return []
    
    def earnings_winners_screener(self, **kwargs) -> List[StockData]:
        """TODO: English documentation."""
        try:
            filters = self._build_earnings_winners_filters(**kwargs)
            
            results = self.screen_stocks(filters)
            
            sort_by = kwargs.get('sort_by', 'performance_1w')
            sort_order = kwargs.get('sort_order', 'desc')
            
            if sort_by == 'performance_1w':
                results.sort(key=lambda x: x.performance_1w or -999, reverse=(sort_order == 'desc'))
            elif sort_by == 'eps_growth_qoq':
                results.sort(key=lambda x: x.eps_growth_qtr or -999, reverse=(sort_order == 'desc'))
            elif sort_by == 'price_change':
                results.sort(key=lambda x: x.price_change or -999, reverse=(sort_order == 'desc'))
            elif sort_by == 'volume':
                results.sort(key=lambda x: x.volume or 0, reverse=(sort_order == 'desc'))
            
            max_results = kwargs.get('max_results', 50)
            return results[:max_results]
            
        except Exception as e:
            logger.error(f"Error in earnings_winners_screener: {e}")
            return []
    
    def _build_earnings_winners_filters(self, **kwargs) -> Dict[str, Any]:
        """TODO: English documentation."""
        filters = {}
        
        if 'earnings_date' in kwargs:
            filters['earnings_date'] = kwargs['earnings_date']
        else:
            earnings_period = kwargs.get('earnings_period', 'this_week')
            if earnings_period == 'this_week':
                filters['earnings_date'] = 'thisweek'
            elif earnings_period == 'yesterday':
                filters['earnings_date'] = 'yesterday'
            elif earnings_period == 'today':
                filters['earnings_date'] = 'today'
            else:
                filters['earnings_date'] = 'thisweek'
        
        market_cap = kwargs.get('market_cap', 'smallover')
        if market_cap in MARKET_CAP_FILTERS:
            filters['market_cap'] = market_cap
        
        min_price = kwargs.get('min_price', 10.0)
        if min_price:
            filters['price_min'] = min_price
        
        min_avg_volume = kwargs.get('min_avg_volume', 500000)
        if min_avg_volume:
            finviz_volume = self._convert_volume_to_finviz_format(min_avg_volume)
            filters['avg_volume_min'] = finviz_volume
        
        min_eps_growth_qoq = kwargs.get('min_eps_growth_qoq', 10.0)
        if min_eps_growth_qoq:
            filters['eps_growth_qoq_min'] = min_eps_growth_qoq
        
        min_eps_revision = kwargs.get('min_eps_revision', 5.0)
        if min_eps_revision:
            filters['eps_revision_min'] = min_eps_revision
        
        min_sales_growth_qoq = kwargs.get('min_sales_growth_qoq', 5.0)
        if min_sales_growth_qoq:
            filters['sales_growth_qoq_min'] = min_sales_growth_qoq
        
        min_weekly_performance = kwargs.get('min_weekly_performance', '5to-1w')
        if min_weekly_performance:
            filters['weekly_performance'] = min_weekly_performance
        
        sma200_filter = kwargs.get('sma200_filter', True)
        if sma200_filter:
            filters['sma200_above'] = True
        
        target_sectors = kwargs.get('target_sectors', [
            'Technology', 'Industrials', 'Healthcare', 
            'Communication Services', 'Consumer Cyclical', 'Financial Services'
        ])
        if target_sectors:
            filters['sectors'] = target_sectors
        
        max_results = kwargs.get('max_results', 50)
        if max_results:
            filters['max_results'] = max_results
        
        return filters
    
    def _build_upcoming_earnings_filters(self, **kwargs) -> Dict[str, Any]:
        """TODO: English documentation."""
        filters = {}
        
        if 'earnings_date' in kwargs:
            filters['earnings_date'] = kwargs['earnings_date']
        else:
            earnings_period = kwargs.get('earnings_period', 'next_week')
            if earnings_period == 'next_week':
                filters['earnings_date'] = 'next_week'
            elif earnings_period == 'next_2_weeks':
                filters['earnings_date'] = 'within_2_weeks'
            elif earnings_period == 'next_month':
                filters['earnings_date'] = 'next_month'
        
        market_cap = kwargs.get('market_cap', 'smallover')
        if market_cap in MARKET_CAP_FILTERS:
            filters['market_cap'] = market_cap
        
        min_price = kwargs.get('min_price', 10)
        if min_price:
            filters['price_min'] = min_price
        
        min_avg_volume = kwargs.get('min_avg_volume', 500000)
        if min_avg_volume:
            finviz_volume = self._convert_volume_to_finviz_format(min_avg_volume)
            filters['avg_volume_min'] = finviz_volume
        
        max_results = kwargs.get('max_results')
        if max_results:
            filters['max_results'] = max_results
        
        target_sectors = kwargs.get('target_sectors', [
            'Technology', 'Industrials', 'Healthcare', 
            'Communication Services', 'Consumer Cyclical', 
            'Financial Services', 'Consumer Defensive', 'Basic Materials'
        ])
        if target_sectors:
            filters['sectors'] = target_sectors
        
        return filters
    
    def _convert_to_upcoming_earnings_data(self, stock: StockData, **kwargs) -> Optional[UpcomingEarningsData]:
        """TODO: English documentation."""
        try:
            upcoming_data = UpcomingEarningsData(
                ticker=stock.ticker,
                company_name=stock.company_name or "",
                sector=stock.sector or "",
                industry=stock.industry or "",
                earnings_date=stock.earnings_date or "",
                earnings_timing="unknown"
            )
            
            upcoming_data.current_price = stock.price
            upcoming_data.market_cap = stock.market_cap
            upcoming_data.avg_volume = stock.avg_volume
            
            upcoming_data.pe_ratio = stock.pe_ratio
            upcoming_data.target_price = stock.target_price
            upcoming_data.analyst_recommendation = stock.analyst_recommendation
            
            if stock.target_price and stock.price and stock.price > 0:
                upcoming_data.target_price_upside = ((stock.target_price - stock.price) / stock.price) * 100
            
            upcoming_data.volatility = stock.volatility
            upcoming_data.beta = stock.beta
            upcoming_data.short_interest = stock.short_interest
            upcoming_data.insider_ownership = stock.insider_ownership
            upcoming_data.institutional_ownership = stock.institutional_ownership
            
            upcoming_data.performance_1w = stock.performance_1w
            upcoming_data.performance_1m = stock.performance_1m
            upcoming_data.rsi = stock.rsi
            

            
            return upcoming_data
            
        except Exception as e:
            logger.warning(f"Failed to convert stock data to upcoming earnings data: {e}")
            return None
    

    

    
    def _sort_upcoming_earnings_results(self, results: List[UpcomingEarningsData], 
                                      sort_by: str, sort_order: str) -> List[UpcomingEarningsData]:
        """TODO: English documentation."""
        reverse = sort_order.lower() == 'desc'
        
        if sort_by == 'earnings_date':
            results.sort(key=lambda x: x.earnings_date or '', reverse=reverse)
        elif sort_by == 'market_cap':
            results.sort(key=lambda x: x.market_cap or 0, reverse=reverse)
        elif sort_by == 'target_price_upside':
            results.sort(key=lambda x: x.target_price_upside or 0, reverse=reverse)
        elif sort_by == 'volatility':
            results.sort(key=lambda x: x.volatility or 0, reverse=reverse)

        elif sort_by == 'ticker':
            results.sort(key=lambda x: x.ticker, reverse=reverse)
        
        return results
    
    def _build_trend_reversion_filters(self, **kwargs) -> Dict[str, Any]:
        """TODO: English documentation."""
        filters = {}
        
        market_cap = kwargs.get('market_cap', 'mid_large')
        filters['market_cap'] = market_cap
        
        if 'eps_growth_qoq' in kwargs:
            filters['eps_growth_qoq_min'] = kwargs['eps_growth_qoq']
        
        if 'revenue_growth_qoq' in kwargs:
            filters['revenue_growth_qoq_min'] = kwargs['revenue_growth_qoq']
        
        if 'rsi_max' in kwargs:
            filters['rsi_max'] = kwargs['rsi_max']
        
        if 'sectors' in kwargs and kwargs['sectors']:
            filters['sectors'] = kwargs['sectors']
        
        if 'exclude_sectors' in kwargs and kwargs['exclude_sectors']:
            filters['exclude_sectors'] = kwargs['exclude_sectors']
        
        return filters
    
    def _build_relative_volume_filters(self, **kwargs) -> Dict[str, Any]:
        """TODO: English documentation."""
        filters = {}
        
        filters['relative_volume_min'] = kwargs['min_relative_volume']
        
        if 'min_price' in kwargs:
            filters['price_min'] = kwargs['min_price']
        
        if 'sectors' in kwargs and kwargs['sectors']:
            filters['sectors'] = kwargs['sectors']
        
        return filters
    
    def _build_technical_analysis_filters(self, **kwargs) -> Dict[str, Any]:
        """TODO: English documentation."""
        filters = {}
        
        if 'rsi_min' in kwargs:
            filters['rsi_min'] = kwargs['rsi_min']
        
        if 'rsi_max' in kwargs:
            filters['rsi_max'] = kwargs['rsi_max']
        
        if 'price_vs_sma20' in kwargs:
            if kwargs['price_vs_sma20'] == 'above':
                filters['sma20_above'] = True
            elif kwargs['price_vs_sma20'] == 'below':
                filters['sma20_below'] = True
        
        if 'price_vs_sma50' in kwargs:
            if kwargs['price_vs_sma50'] == 'above':
                filters['sma50_above'] = True
            elif kwargs['price_vs_sma50'] == 'below':
                filters['sma50_below'] = True
        
        if 'price_vs_sma200' in kwargs:
            if kwargs['price_vs_sma200'] == 'above':
                filters['sma200_above'] = True
            elif kwargs['price_vs_sma200'] == 'below':
                filters['sma200_below'] = True
        
        if 'min_price' in kwargs:
            filters['price_min'] = kwargs['min_price']
        
        if 'min_volume' in kwargs:
            filters['volume_min'] = kwargs['min_volume']
        
        if 'sectors' in kwargs and kwargs['sectors']:
            filters['sectors'] = kwargs['sectors']
        
        return filters