"""
工具函数模块
提供ETF网格交易分析系统的各种工具函数和功能
"""

from .helpers import (
    format_currency, format_percentage, calculate_trading_days,
    validate_date_range, calculate_risk_level, calculate_suitability_level,
    generate_strategy_summary, calculate_position_size, detect_market_regime,
    calculate_correlation, generate_risk_warnings, optimize_grid_spacing,
    validate_parameters, safe_divide, round_to_tick
)

from .exceptions import (
    ETFAnalysisException, DataValidationError, DataFetchError, DataProcessingError,
    AlgorithmCalculationError, OptimizationError, ExternalServiceError,
    APITimeoutError, NetworkError, ConfigurationError, EnvironmentError,
    CacheError, PermissionError, RateLimitExceededError, ResourceNotFoundError,
    InvalidParameterError, BusinessLogicError, ExceptionHandler, exception_factory
)

from .decorators import (
    performance_monitor, retry, cache_result, validate_input,
    log_execution, timeout, rate_limit, singleton, deprecated
)

from .performance import (
    PerformanceMonitor, PerformanceProfiler, ResourceMonitor,
    performance_monitor, performance_profiler, resource_monitor,
    start_performance_monitoring, profile_function
)

from .logging_config import (
    LogManager, StructuredLogger, PerformanceLogger, AuditLogger, JSONFormatter,
    log_manager, performance_logger, audit_logger, get_logger, configure_logging,
    app_logger, api_logger, algorithm_logger, service_logger, data_logger, cache_logger
)

# 重新导出helpers模块中的函数
__all__ = [
    # 辅助函数
    'format_currency',
    'format_percentage',
    'calculate_trading_days',
    'validate_date_range',
    'calculate_risk_level',
    'calculate_suitability_level',
    'generate_strategy_summary',
    'calculate_position_size',
    'detect_market_regime',
    'calculate_correlation',
    'generate_risk_warnings',
    'optimize_grid_spacing',
    'validate_parameters',
    'safe_divide',
    'round_to_tick',
    
    # 异常处理
    'ETFAnalysisException',
    'DataValidationError',
    'DataFetchError',
    'DataProcessingError',
    'AlgorithmCalculationError',
    'OptimizationError',
    'ExternalServiceError',
    'APITimeoutError',
    'NetworkError',
    'ConfigurationError',
    'EnvironmentError',
    'CacheError',
    'PermissionError',
    'RateLimitExceededError',
    'ResourceNotFoundError',
    'InvalidParameterError',
    'BusinessLogicError',
    'ExceptionHandler',
    'exception_factory',
    
    # 装饰器
    'performance_monitor',
    'retry',
    'cache_result',
    'validate_input',
    'log_execution',
    'timeout',
    'rate_limit',
    'singleton',
    'deprecated',
    
    # 性能监控
    'PerformanceMonitor',
    'PerformanceProfiler',
    'ResourceMonitor',
    'performance_monitor',
    'performance_profiler',
    'resource_monitor',
    'start_performance_monitoring',
    'profile_function',
    
    # 日志配置
    'LogManager',
    'StructuredLogger',
    'PerformanceLogger',
    'AuditLogger',
    'JSONFormatter',
    'log_manager',
    'performance_logger',
    'audit_logger',
    'get_logger',
    'configure_logging',
    'app_logger',
    'api_logger',
    'algorithm_logger',
    'service_logger',
    'data_logger',
    'cache_logger'
]
