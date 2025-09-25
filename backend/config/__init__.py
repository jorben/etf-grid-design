"""
配置管理模块
提供统一的配置管理和环境配置支持
"""

from .settings import Settings, DevelopmentSettings, ProductionSettings, TestingSettings, get_settings, settings
from .constants import (
    ETFConstants, GridConstants, ATRConstants, RiskConstants, 
    PerformanceConstants, TimeConstants, ErrorConstants, 
    LogConstants, APIResponseConstants, get_constants
)
from .validation import (
    ConfigValidator, ConfigurationSchema, EnvironmentValidator,
    validate_configuration, get_configuration_errors, is_configuration_valid
)
from .version import (
    PROJECT_VERSION, API_VERSION, FRONTEND_VERSION, BACKEND_VERSION,
    get_version_info
)

__all__ = [
    # 配置类
    'Settings',
    'DevelopmentSettings',
    'ProductionSettings', 
    'TestingSettings',
    'get_settings',
    'settings',
    
    # 常量类
    'ETFConstants',
    'GridConstants',
    'ATRConstants',
    'RiskConstants',
    'PerformanceConstants',
    'TimeConstants',
    'ErrorConstants',
    'LogConstants',
    'APIResponseConstants',
    'get_constants',
    
    # 验证类
    'ConfigValidator',
    'ConfigurationSchema',
    'EnvironmentValidator',
    'validate_configuration',
    'get_configuration_errors',
    'is_configuration_valid',
    
    # 版本信息
    'PROJECT_VERSION',
    'API_VERSION',
    'FRONTEND_VERSION',
    'BACKEND_VERSION',
    'get_version_info'
]
