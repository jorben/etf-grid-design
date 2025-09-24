"""
测试模块
提供ETF网格交易分析系统的完整测试体系
"""

from .fixtures.etf_data import (
    ETF_BASIC_DATA, ETF_PRICE_HISTORY, ETF_PORTFOLIO_DATA,
    ANALYSIS_INPUT_DATA, ANALYSIS_RESULT_DATA, PERFORMANCE_METRICS_DATA,
    ERROR_SCENARIOS, get_etf_data, get_price_history, get_analysis_input,
    get_analysis_result, get_error_scenario
)

from .fixtures.market_data import (
    MARKET_INDEX_DATA, INDUSTRY_DATA, MACRO_ECONOMIC_DATA,
    MARKET_SENTIMENT_DATA, TECHNICAL_INDICATORS_DATA,
    MARKET_TREND_DATA, VOLATILITY_DATA, CORRELATION_MATRIX,
    RISK_METRICS_DATA, MARKET_STATE_DATA, MARKET_EVENTS_DATA,
    get_market_index, get_industry_data, get_macro_data,
    get_technical_indicators, get_market_trend, get_volatility_data,
    get_correlation_matrix, get_risk_metrics, get_market_state,
    get_recent_market_events
)

from .utils import (
    TestDataGenerator, TestFileHelper, MockHelper,
    PerformanceTestHelper, AsyncTestHelper,
    test_data_generator, test_file_helper, mock_helper,
    performance_test_helper, async_test_helper
)

__all__ = [
    # ETF测试数据
    'ETF_BASIC_DATA',
    'ETF_PRICE_HISTORY', 
    'ETF_PORTFOLIO_DATA',
    'ANALYSIS_INPUT_DATA',
    'ANALYSIS_RESULT_DATA',
    'PERFORMANCE_METRICS_DATA',
    'ERROR_SCENARIOS',
    'get_etf_data',
    'get_price_history', 
    'get_analysis_input',
    'get_analysis_result',
    'get_error_scenario',
    
    # 市场测试数据
    'MARKET_INDEX_DATA',
    'INDUSTRY_DATA',
    'MACRO_ECONOMIC_DATA',
    'MARKET_SENTIMENT_DATA',
    'TECHNICAL_INDICATORS_DATA',
    'MARKET_TREND_DATA',
    'VOLATILITY_DATA',
    'CORRELATION_MATRIX',
    'RISK_METRICS_DATA',
    'MARKET_STATE_DATA',
    'MARKET_EVENTS_DATA',
    'get_market_index',
    'get_industry_data',
    'get_macro_data',
    'get_technical_indicators',
    'get_market_trend',
    'get_volatility_data',
    'get_correlation_matrix',
    'get_risk_metrics',
    'get_market_state',
    'get_recent_market_events',
    
    # 测试工具
    'TestDataGenerator',
    'TestFileHelper',
    'MockHelper',
    'PerformanceTestHelper', 
    'AsyncTestHelper',
    'test_data_generator',
    'test_file_helper',
    'mock_helper',
    'performance_test_helper',
    'async_test_helper'
]
