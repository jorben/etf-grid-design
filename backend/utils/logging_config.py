"""
日志配置模块
提供统一的日志配置和管理功能
"""

import logging
import logging.config
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import json

from ..config import get_settings


class JSONFormatter(logging.Formatter):
    """JSON日志格式化器"""
    
    def format(self, record: logging.LogRecord) -> str:
        """格式化日志记录为JSON"""
        log_entry = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'message': record.getMessage(),
            'process': record.process,
            'thread': record.threadName
        }
        
        # 添加异常信息
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        # 添加额外字段
        if hasattr(record, 'extra_fields'):
            log_entry.update(record.extra_fields)
        
        return json.dumps(log_entry, ensure_ascii=False)


class StructuredLogger:
    """结构化日志记录器"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.extra_fields = {}
    
    def add_field(self, key: str, value: Any):
        """添加额外字段"""
        self.extra_fields[key] = value
        return self
    
    def _log_with_extra(self, level: int, msg: str, *args, **kwargs):
        """带额外字段的日志记录"""
        if self.extra_fields:
            if 'extra' not in kwargs:
                kwargs['extra'] = {}
            kwargs['extra']['extra_fields'] = self.extra_fields.copy()
        
        self.logger.log(level, msg, *args, **kwargs)
        self.extra_fields.clear()  # 清除临时字段
    
    def debug(self, msg: str, *args, **kwargs):
        """调试级别日志"""
        self._log_with_extra(logging.DEBUG, msg, *args, **kwargs)
    
    def info(self, msg: str, *args, **kwargs):
        """信息级别日志"""
        self._log_with_extra(logging.INFO, msg, *args, **kwargs)
    
    def warning(self, msg: str, *args, **kwargs):
        """警告级别日志"""
        self._log_with_extra(logging.WARNING, msg, *args, **kwargs)
    
    def error(self, msg: str, *args, **kwargs):
        """错误级别日志"""
        self._log_with_extra(logging.ERROR, msg, *args, **kwargs)
    
    def critical(self, msg: str, *args, **kwargs):
        """严重级别日志"""
        self._log_with_extra(logging.CRITICAL, msg, *args, **kwargs)
    
    def exception(self, msg: str, *args, **kwargs):
        """异常日志"""
        kwargs['exc_info'] = True
        self._log_with_extra(logging.ERROR, msg, *args, **kwargs)


class LogManager:
    """日志管理器"""
    
    def __init__(self):
        self.settings = get_settings()
        self._configured = False
    
    def configure_logging(self):
        """配置日志系统"""
        if self._configured:
            return
        
        # 创建日志目录
        log_dir = Path(self.settings.log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # 基础日志配置
        log_config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                },
                'json': {
                    '()': JSONFormatter
                },
                'detailed': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s'
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'DEBUG' if self.settings.debug else 'INFO',
                    'formatter': 'standard',
                    'stream': sys.stdout
                },
                'file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'INFO',
                    'formatter': 'detailed',
                    'filename': log_dir / 'app.log',
                    'maxBytes': 10 * 1024 * 1024,  # 10MB
                    'backupCount': 5,
                    'encoding': 'utf-8'
                },
                'error_file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'ERROR',
                    'formatter': 'detailed',
                    'filename': log_dir / 'error.log',
                    'maxBytes': 10 * 1024 * 1024,  # 10MB
                    'backupCount': 5,
                    'encoding': 'utf-8'
                },
                'json_file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'INFO',
                    'formatter': 'json',
                    'filename': log_dir / 'structured.log',
                    'maxBytes': 10 * 1024 * 1024,  # 10MB
                    'backupCount': 5,
                    'encoding': 'utf-8'
                }
            },
            'loggers': {
                '': {  # 根日志记录器
                    'level': 'DEBUG' if self.settings.debug else 'INFO',
                    'handlers': ['console', 'file', 'error_file', 'json_file'],
                    'propagate': True
                },
                'backend': {
                    'level': 'DEBUG' if self.settings.debug else 'INFO',
                    'handlers': ['console', 'file', 'error_file', 'json_file'],
                    'propagate': False
                },
                'algorithms': {
                    'level': 'INFO',
                    'handlers': ['file', 'json_file'],
                    'propagate': False
                },
                'services': {
                    'level': 'INFO',
                    'handlers': ['file', 'json_file'],
                    'propagate': False
                },
                'api': {
                    'level': 'INFO',
                    'handlers': ['console', 'file', 'json_file'],
                    'propagate': False
                },
                'uvicorn': {
                    'level': 'WARNING',
                    'handlers': ['file'],
                    'propagate': False
                },
                'fastapi': {
                    'level': 'WARNING',
                    'handlers': ['file'],
                    'propagate': False
                }
            }
        }
        
        # 应用日志配置
        logging.config.dictConfig(log_config)
        self._configured = True
        
        # 设置默认日志级别
        logging.getLogger().setLevel(
            logging.DEBUG if self.settings.debug else logging.INFO
        )
    
    def get_logger(self, name: str) -> StructuredLogger:
        """获取结构化日志记录器"""
        if not self._configured:
            self.configure_logging()
        
        return StructuredLogger(name)
    
    def set_log_level(self, logger_name: str, level: str):
        """设置日志级别"""
        if not self._configured:
            self.configure_logging()
        
        logger = logging.getLogger(logger_name)
        logger.setLevel(getattr(logging, level.upper()))
    
    def add_log_handler(self, handler: logging.Handler):
        """添加日志处理器"""
        if not self._configured:
            self.configure_logging()
        
        logging.getLogger().addHandler(handler)


class PerformanceLogger:
    """性能日志记录器"""
    
    def __init__(self):
        self.logger = logging.getLogger('performance')
        self.metrics = {}
    
    def log_performance(self, operation: str, duration: float, **kwargs):
        """记录性能指标"""
        log_data = {
            'operation': operation,
            'duration': duration,
            'timestamp': datetime.now().isoformat()
        }
        log_data.update(kwargs)
        
        if duration > 1.0:  # 超过1秒的操作记录为警告
            self.logger.warning(
                f"性能警告: {operation} 耗时 {duration:.3f}s",
                extra={'extra_fields': log_data}
            )
        else:
            self.logger.info(
                f"性能指标: {operation} 耗时 {duration:.3f}s",
                extra={'extra_fields': log_data}
            )
    
    def log_api_performance(self, endpoint: str, method: str, duration: float, 
                           status_code: int, **kwargs):
        """记录API性能"""
        log_data = {
            'endpoint': endpoint,
            'method': method,
            'duration': duration,
            'status_code': status_code,
            'timestamp': datetime.now().isoformat()
        }
        log_data.update(kwargs)
        
        self.logger.info(
            f"API性能: {method} {endpoint} - {status_code} - {duration:.3f}s",
            extra={'extra_fields': log_data}
        )
    
    def log_cache_performance(self, operation: str, hit: bool, duration: float, **kwargs):
        """记录缓存性能"""
        cache_type = "命中" if hit else "未命中"
        log_data = {
            'operation': operation,
            'cache_hit': hit,
            'duration': duration,
            'timestamp': datetime.now().isoformat()
        }
        log_data.update(kwargs)
        
        self.logger.info(
            f"缓存性能: {operation} - {cache_type} - {duration:.3f}s",
            extra={'extra_fields': log_data}
        )


class AuditLogger:
    """审计日志记录器"""
    
    def __init__(self):
        self.logger = logging.getLogger('audit')
    
    def log_user_action(self, user_id: str, action: str, resource: str, 
                       details: Dict[str, Any] = None):
        """记录用户操作"""
        log_data = {
            'user_id': user_id,
            'action': action,
            'resource': resource,
            'timestamp': datetime.now().isoformat()
        }
        
        if details:
            log_data['details'] = details
        
        self.logger.info(
            f"用户操作: {user_id} - {action} - {resource}",
            extra={'extra_fields': log_data}
        )
    
    def log_system_event(self, event_type: str, severity: str, 
                        description: str, details: Dict[str, Any] = None):
        """记录系统事件"""
        log_data = {
            'event_type': event_type,
            'severity': severity,
            'description': description,
            'timestamp': datetime.now().isoformat()
        }
        
        if details:
            log_data['details'] = details
        
        log_method = getattr(self.logger, severity.lower(), self.logger.info)
        log_method(
            f"系统事件: {event_type} - {severity} - {description}",
            extra={'extra_fields': log_data}
        )


# 全局日志管理器实例
log_manager = LogManager()
performance_logger = PerformanceLogger()
audit_logger = AuditLogger()


def get_logger(name: str) -> StructuredLogger:
    """获取日志记录器（快捷函数）"""
    return log_manager.get_logger(name)


def configure_logging():
    """配置日志系统（快捷函数）"""
    log_manager.configure_logging()


# 常用日志记录器
app_logger = get_logger('app')
api_logger = get_logger('api')
algorithm_logger = get_logger('algorithms')
service_logger = get_logger('services')
data_logger = get_logger('data')
cache_logger = get_logger('cache')


__all__ = [
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
