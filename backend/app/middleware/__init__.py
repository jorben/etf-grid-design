"""
中间件模块初始化
"""

from .error_handler import register_error_handlers
from .cors_handler import setup_cors

__all__ = ['register_error_handlers', 'setup_cors']