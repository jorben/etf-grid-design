"""
业务异常类定义
"""

from .base_exceptions import BaseAPIException

class ETFNotFoundError(BaseAPIException):
    """ETF不存在异常"""
    status_code = 404
    error_code = "ETF_NOT_FOUND"
    message = "ETF不存在或代码错误"

class InvalidParameterError(BaseAPIException):
    """参数错误异常"""
    status_code = 400
    error_code = "INVALID_PARAMETER"
    message = "参数错误"

class DataSourceError(BaseAPIException):
    """数据源异常"""
    status_code = 502
    error_code = "DATA_SOURCE_ERROR"
    message = "数据源访问失败"

class AnalysisError(BaseAPIException):
    """分析计算异常"""
    status_code = 500
    error_code = "ANALYSIS_ERROR"
    message = "分析计算失败"

class CacheError(BaseAPIException):
    """缓存异常"""
    status_code = 500
    error_code = "CACHE_ERROR"
    message = "缓存操作失败"

class StrategyError(BaseAPIException):
    """策略计算异常"""
    status_code = 500
    error_code = "STRATEGY_ERROR"
    message = "策略计算失败"

class InsufficientDataError(BaseAPIException):
    """数据不足异常"""
    status_code = 400
    error_code = "INSUFFICIENT_DATA"
    message = "数据不足，无法进行分析"

class MarketClosedError(BaseAPIException):
    """市场休市异常"""
    status_code = 400
    error_code = "MARKET_CLOSED"
    message = "市场休市，无法获取实时数据"

class CalculationError(BaseAPIException):
    """计算异常"""
    status_code = 500
    error_code = "CALCULATION_ERROR"
    message = "计算过程中发生错误"

class DataQualityError(BaseAPIException):
    """数据质量异常"""
    status_code = 400
    error_code = "DATA_QUALITY_ERROR"
    message = "数据质量不符合要求"

class ExternalAPIError(BaseAPIException):
    """外部API异常"""
    status_code = 502
    error_code = "EXTERNAL_API_ERROR"
    message = "外部API调用失败"

class ConfigurationError(BaseAPIException):
    """配置异常"""
    status_code = 500
    error_code = "CONFIGURATION_ERROR"
    message = "配置错误"

class DataValidationError(BaseAPIException):
    """数据验证异常"""
    status_code = 400
    error_code = "DATA_VALIDATION_ERROR"
    message = "数据验证失败"