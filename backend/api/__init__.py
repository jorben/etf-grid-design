"""
API模块初始化文件
统一导出API相关功能
"""

from .routes import register_routes
from .middleware import register_middleware, setup_cors, setup_logging

__all__ = [
    'register_routes',
    'register_middleware',
    'setup_cors',
    'setup_logging'
]
