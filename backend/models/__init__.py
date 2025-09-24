"""
数据模型模块
定义ETF网格交易分析系统的所有数据模型
"""

from .base import (
    BaseETFModel, PaginatedResponse, ErrorResponse, SuccessResponse,
    ValidationErrorDetail, ValidationErrorResponse, HealthCheckResponse,
    PerformanceMetrics, CacheMetrics
)
from .etf import (
    ETFBasicInfo, ETFPriceData, ETFHistoricalData, ETFMarketData,
    ETFPortfolioHolding, ETFPortfolio, ETFAnalysisInput,
    ETFPerformanceMetrics, ETFComparisonResult, ETFSearchCriteria, ETFSearchResult
)
from .analysis import (
    EvaluationResult, AmplitudeEvaluation, VolatilityEvaluation,
    MarketCharacteristicsEvaluation, LiquidityEvaluation, DataQualityEvaluation,
    SuitabilityEvaluation, GridFundAllocation, GridFundAllocationResult,
    GridStrategyParameters, StrategyRationale, ETFAnalysisResult,
    AnalysisSummary, PerformanceAnalysis, BacktestResult
)
from .strategy import (
    GridType, RiskPreference, StrategyStatus, GridLevel, GridStrategyConfig,
    GridStrategyState, TradeRecord, StrategyPerformance,
    StrategyOptimizationResult, StrategyBacktestRequest, StrategyComparisonResult
)
from .validators import (
    ETFValidators, GridValidators, ATRValidators, DateValidators,
    CommonValidators, ValidatorFactory
)

__all__ = [
    # 基础模型
    'BaseETFModel',
    'PaginatedResponse',
    'ErrorResponse',
    'SuccessResponse',
    'ValidationErrorDetail',
    'ValidationErrorResponse',
    'HealthCheckResponse',
    'PerformanceMetrics',
    'CacheMetrics',
    
    # ETF模型
    'ETFBasicInfo',
    'ETFPriceData',
    'ETFHistoricalData',
    'ETFMarketData',
    'ETFPortfolioHolding',
    'ETFPortfolio',
    'ETFAnalysisInput',
    'ETFPerformanceMetrics',
    'ETFComparisonResult',
    'ETFSearchCriteria',
    'ETFSearchResult',
    
    # 分析模型
    'EvaluationResult',
    'AmplitudeEvaluation',
    'VolatilityEvaluation',
    'MarketCharacteristicsEvaluation',
    'LiquidityEvaluation',
    'DataQualityEvaluation',
    'SuitabilityEvaluation',
    'GridFundAllocation',
    'GridFundAllocationResult',
    'GridStrategyParameters',
    'StrategyRationale',
    'ETFAnalysisResult',
    'AnalysisSummary',
    'PerformanceAnalysis',
    'BacktestResult',
    
    # 策略模型
    'GridType',
    'RiskPreference',
    'StrategyStatus',
    'GridLevel',
    'GridStrategyConfig',
    'GridStrategyState',
    'TradeRecord',
    'StrategyPerformance',
    'StrategyOptimizationResult',
    'StrategyBacktestRequest',
    'StrategyComparisonResult',
    
    # 验证器
    'ETFValidators',
    'GridValidators',
    'ATRValidators',
    'DateValidators',
    'CommonValidators',
    'ValidatorFactory'
]
