"""
自定义异常体系
定义ETF分析系统的异常类和错误处理机制
"""

from typing import Optional, Dict, Any, List
from ..config.constants import ErrorConstants


class ETFAnalysisException(Exception):
    """ETF分析系统基础异常"""
    
    def __init__(
        self, 
        message: str, 
        error_code: int = ErrorConstants.UNKNOWN_ERROR,
        detail: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.detail = detail
        self.context = context or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'error_code': self.error_code,
            'message': self.message,
            'detail': self.detail,
            'context': self.context
        }


class DataValidationError(ETFAnalysisException):
    """数据验证异常"""
    
    def __init__(
        self, 
        message: str, 
        validation_errors: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ):
        super().__init__(
            message, 
            error_code=ErrorConstants.DATA_VALIDATION_ERROR,
            **kwargs
        )
        self.validation_errors = validation_errors or []
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        result = super().to_dict()
        result['validation_errors'] = self.validation_errors
        return result


class DataFetchError(ETFAnalysisException):
    """数据获取异常"""
    
    def __init__(self, message: str, data_source: Optional[str] = None, **kwargs):
        super().__init__(
            message, 
            error_code=ErrorConstants.DATA_FETCH_ERROR,
            **kwargs
        )
        self.data_source = data_source


class DataProcessingError(ETFAnalysisException):
    """数据处理异常"""
    
    def __init__(self, message: str, processing_step: Optional[str] = None, **kwargs):
        super().__init__(
            message, 
            error_code=ErrorConstants.DATA_PROCESSING_ERROR,
            **kwargs
        )
        self.processing_step = processing_step


class AlgorithmCalculationError(ETFAnalysisException):
    """算法计算异常"""
    
    def __init__(
        self, 
        message: str, 
        algorithm_name: Optional[str] = None,
        input_data: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        super().__init__(
            message, 
            error_code=ErrorConstants.CALCULATION_ERROR,
            **kwargs
        )
        self.algorithm_name = algorithm_name
        self.input_data = input_data or {}


class OptimizationError(ETFAnalysisException):
    """优化算法异常"""
    
    def __init__(
        self, 
        message: str, 
        optimization_type: Optional[str] = None,
        constraints: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        super().__init__(
            message, 
            error_code=ErrorConstants.OPTIMIZATION_ERROR,
            **kwargs
        )
        self.optimization_type = optimization_type
        self.constraints = constraints or {}


class ExternalServiceError(ETFAnalysisException):
    """外部服务异常"""
    
    def __init__(
        self, 
        message: str, 
        service_name: Optional[str] = None,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        super().__init__(
            message, 
            error_code=ErrorConstants.EXTERNAL_SERVICE_ERROR,
            **kwargs
        )
        self.service_name = service_name
        self.status_code = status_code
        self.response_data = response_data or {}


class APITimeoutError(ExternalServiceError):
    """API超时异常"""
    
    def __init__(self, message: str, timeout_seconds: Optional[float] = None, **kwargs):
        super().__init__(
            message, 
            error_code=ErrorConstants.API_TIMEOUT,
            **kwargs
        )
        self.timeout_seconds = timeout_seconds


class NetworkError(ExternalServiceError):
    """网络异常"""
    
    def __init__(self, message: str, url: Optional[str] = None, **kwargs):
        super().__init__(
            message, 
            error_code=ErrorConstants.NETWORK_ERROR,
            **kwargs
        )
        self.url = url


class ConfigurationError(ETFAnalysisException):
    """配置异常"""
    
    def __init__(
        self, 
        message: str, 
        config_key: Optional[str] = None,
        config_value: Optional[Any] = None,
        **kwargs
    ):
        super().__init__(
            message, 
            error_code=ErrorConstants.CONFIGURATION_ERROR,
            **kwargs
        )
        self.config_key = config_key
        self.config_value = config_value


class EnvironmentError(ETFAnalysisException):
    """环境异常"""
    
    def __init__(
        self, 
        message: str, 
        environment_vars: Optional[List[str]] = None,
        **kwargs
    ):
        super().__init__(
            message, 
            error_code=ErrorConstants.ENVIRONMENT_ERROR,
            **kwargs
        )
        self.environment_vars = environment_vars or []


class CacheError(ETFAnalysisException):
    """缓存异常"""
    
    def __init__(
        self, 
        message: str, 
        cache_key: Optional[str] = None,
        cache_operation: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            message, 
            error_code=ErrorConstants.CACHE_ERROR,
            **kwargs
        )
        self.cache_key = cache_key
        self.cache_operation = cache_operation


class PermissionError(ETFAnalysisException):
    """权限异常"""
    
    def __init__(self, message: str, required_permissions: Optional[List[str]] = None, **kwargs):
        super().__init__(
            message, 
            error_code=ErrorConstants.PERMISSION_DENIED,
            **kwargs
        )
        self.required_permissions = required_permissions or []


class RateLimitExceededError(ETFAnalysisException):
    """速率限制异常"""
    
    def __init__(
        self, 
        message: str, 
        limit: Optional[int] = None,
        window: Optional[int] = None,
        **kwargs
    ):
        super().__init__(
            message, 
            error_code=ErrorConstants.RATE_LIMIT_EXCEEDED,
            **kwargs
        )
        self.limit = limit
        self.window = window


class ResourceNotFoundError(ETFAnalysisException):
    """资源未找到异常"""
    
    def __init__(self, message: str, resource_type: Optional[str] = None, **kwargs):
        super().__init__(
            message, 
            error_code=ErrorConstants.DATA_NOT_FOUND,
            **kwargs
        )
        self.resource_type = resource_type


class InvalidParameterError(ETFAnalysisException):
    """参数无效异常"""
    
    def __init__(self, message: str, parameter_name: Optional[str] = None, **kwargs):
        super().__init__(
            message, 
            error_code=ErrorConstants.INVALID_PARAMETER,
            **kwargs
        )
        self.parameter_name = parameter_name


class BusinessLogicError(ETFAnalysisException):
    """业务逻辑异常"""
    
    def __init__(
        self, 
        message: str, 
        business_rule: Optional[str] = None,
        constraint_violations: Optional[List[str]] = None,
        **kwargs
    ):
        super().__init__(
            message, 
            error_code=ErrorConstants.UNKNOWN_ERROR,
            **kwargs
        )
        self.business_rule = business_rule
        self.constraint_violations = constraint_violations or []


class ExceptionHandler:
    """异常处理器"""
    
    @staticmethod
    def handle_exception(exception: Exception) -> Dict[str, Any]:
        """处理异常并返回标准格式"""
        if isinstance(exception, ETFAnalysisException):
            return exception.to_dict()
        else:
            return {
                'error_code': ErrorConstants.UNKNOWN_ERROR,
                'message': str(exception),
                'detail': '系统内部错误',
                'context': {
                    'exception_type': type(exception).__name__
                }
            }
    
    @staticmethod
    def create_error_response(exception: Exception) -> Dict[str, Any]:
        """创建错误响应"""
        error_info = ExceptionHandler.handle_exception(exception)
        return {
            'success': False,
            'error': error_info,
            'timestamp': None  # 将在上层添加
        }


def create_exception_factory():
    """创建异常工厂"""
    
    class ExceptionFactory:
        """异常工厂类"""
        
        @staticmethod
        def validation_error(
            message: str, 
            validation_errors: Optional[List[Dict[str, Any]]] = None
        ) -> DataValidationError:
            """创建数据验证异常"""
            return DataValidationError(message, validation_errors)
        
        @staticmethod
        def external_service_error(
            message: str, 
            service_name: str,
            status_code: Optional[int] = None
        ) -> ExternalServiceError:
            """创建外部服务异常"""
            return ExternalServiceError(message, service_name, status_code)
        
        @staticmethod
        def configuration_error(
            message: str, 
            config_key: str,
            config_value: Optional[Any] = None
        ) -> ConfigurationError:
            """创建配置异常"""
            return ConfigurationError(message, config_key, config_value)
        
        @staticmethod
        def algorithm_error(
            message: str, 
            algorithm_name: str,
            input_data: Optional[Dict[str, Any]] = None
        ) -> AlgorithmCalculationError:
            """创建算法计算异常"""
            return AlgorithmCalculationError(message, algorithm_name, input_data)
        
        @staticmethod
        def resource_not_found(
            message: str, 
            resource_type: str
        ) -> ResourceNotFoundError:
            """创建资源未找到异常"""
            return ResourceNotFoundError(message, resource_type)
        
        @staticmethod
        def invalid_parameter(
            message: str, 
            parameter_name: str
        ) -> InvalidParameterError:
            """创建参数无效异常"""
            return InvalidParameterError(message, parameter_name)
    
    return ExceptionFactory()


# 全局异常工厂实例
exception_factory = create_exception_factory()
