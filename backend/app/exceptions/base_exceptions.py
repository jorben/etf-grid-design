"""
基础异常类定义
"""

class BaseAPIException(Exception):
    """API基础异常类"""
    status_code = 500
    error_code = "INTERNAL_ERROR"
    message = "内部服务器错误"
    
    def __init__(self, message: str = None, details: dict = None):
        if message:
            self.message = message
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        result = {
            'success': False,
            'error_code': self.error_code,
            'error': self.message
        }
        if self.details:
            result['details'] = self.details
        return result

class ValidationError(BaseAPIException):
    """数据验证异常"""
    status_code = 400
    error_code = "VALIDATION_ERROR"
    message = "数据验证失败"

class ConfigurationError(BaseAPIException):
    """配置错误异常"""
    status_code = 500
    error_code = "CONFIGURATION_ERROR"
    message = "配置错误"

class ServiceUnavailableError(BaseAPIException):
    """服务不可用异常"""
    status_code = 503
    error_code = "SERVICE_UNAVAILABLE"
    message = "服务暂时不可用"

class RateLimitError(BaseAPIException):
    """请求频率限制异常"""
    status_code = 429
    error_code = "RATE_LIMIT_EXCEEDED"
    message = "请求频率超限"

class AuthenticationError(BaseAPIException):
    """认证异常"""
    status_code = 401
    error_code = "AUTHENTICATION_ERROR"
    message = "认证失败"

class AuthorizationError(BaseAPIException):
    """授权异常"""
    status_code = 403
    error_code = "AUTHORIZATION_ERROR"
    message = "权限不足"