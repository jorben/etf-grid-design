"""
装饰器工具
提供性能监控、缓存、重试等装饰器功能
"""

import time
import functools
import logging
from typing import Any, Callable, Optional, Dict, Type, Union
from functools import wraps
import threading
from ..config.constants import LogConstants


def performance_monitor(func: Callable) -> Callable:
    """
    性能监控装饰器
    记录函数执行时间和性能指标
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # 记录性能日志
            logger = logging.getLogger(func.__module__)
            logger.debug(
                f"性能监控 - {func.__name__}: "
                f"执行时间: {execution_time:.4f}s, "
                f"参数数量: {len(args) + len(kwargs)}"
            )
            
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger = logging.getLogger(func.__module__)
            logger.error(
                f"性能监控 - {func.__name__}: "
                f"执行失败, 耗时: {execution_time:.4f}s, "
                f"错误: {e}"
            )
            raise
    
    return wrapper


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: Union[Type[Exception], tuple] = Exception,
    logger: Optional[logging.Logger] = None
):
    """
    重试装饰器
    在遇到指定异常时自动重试函数
    
    Args:
        max_attempts: 最大重试次数
        delay: 初始延迟时间（秒）
        backoff_factor: 退避因子，每次重试延迟时间乘以该因子
        exceptions: 需要重试的异常类型
        logger: 日志记录器
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            current_delay = delay
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_attempts - 1:
                        # 最后一次重试失败，抛出异常
                        if logger:
                            logger.error(
                                f"重试失败 - {func.__name__}: "
                                f"第{attempt + 1}次尝试失败，不再重试: {e}"
                            )
                        raise
                    
                    if logger:
                        logger.warning(
                            f"重试中 - {func.__name__}: "
                            f"第{attempt + 1}次尝试失败，{current_delay}s后重试: {e}"
                        )
                    
                    time.sleep(current_delay)
                    current_delay *= backoff_factor
            
            # 理论上不会执行到这里
            raise last_exception  # type: ignore
        
        return wrapper
    return decorator


def cache_result(
    cache_key_func: Optional[Callable] = None,
    ttl: int = 3600,
    max_size: int = 1000
):
    """
    缓存结果装饰器
    缓存函数结果，避免重复计算
    
    Args:
        cache_key_func: 自定义缓存键生成函数
        ttl: 缓存生存时间（秒）
        max_size: 最大缓存条目数
    """
    # 简单的内存缓存实现
    cache: Dict[str, Dict[str, Any]] = {
        'data': {},
        'timestamps': {},
        'size': 0
    }
    cache_lock = threading.Lock()
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # 生成缓存键
            if cache_key_func:
                cache_key = cache_key_func(*args, **kwargs)
            else:
                cache_key = f"{func.__module__}.{func.__name__}:{args}:{kwargs}"
            
            current_time = time.time()
            
            with cache_lock:
                # 检查缓存是否有效
                if (cache_key in cache['data'] and 
                    current_time - cache['timestamps'].get(cache_key, 0) < ttl):
                    return cache['data'][cache_key]
                
                # 清理过期缓存
                expired_keys = [
                    key for key, timestamp in cache['timestamps'].items()
                    if current_time - timestamp >= ttl
                ]
                for key in expired_keys:
                    cache['data'].pop(key, None)
                    cache['timestamps'].pop(key, None)
                    cache['size'] -= 1
            
            # 执行函数获取结果
            result = func(*args, **kwargs)
            
            with cache_lock:
                # 检查缓存大小限制
                if cache['size'] >= max_size:
                    # 移除最旧的缓存项
                    oldest_key = min(cache['timestamps'].items(), key=lambda x: x[1])[0]
                    cache['data'].pop(oldest_key, None)
                    cache['timestamps'].pop(oldest_key, None)
                    cache['size'] -= 1
                
                # 缓存结果
                cache['data'][cache_key] = result
                cache['timestamps'][cache_key] = current_time
                cache['size'] += 1
            
            return result
        
        return wrapper
    return decorator


def validate_input(validation_rules: Dict[str, Callable]):
    """
    输入验证装饰器
    根据验证规则验证函数输入参数
    
    Args:
        validation_rules: 验证规则字典，键为参数名，值为验证函数
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # 获取函数参数信息
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # 验证参数
            for param_name, validator_func in validation_rules.items():
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    is_valid, message = validator_func(value)
                    if not is_valid:
                        from .exceptions import DataValidationError
                        raise DataValidationError(
                            f"参数验证失败: {param_name} - {message}",
                            validation_errors=[{
                                'field': param_name,
                                'message': message,
                                'value': value
                            }]
                        )
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


def log_execution(level: str = "INFO", include_args: bool = True):
    """
    执行日志装饰器
    记录函数执行日志
    
    Args:
        level: 日志级别
        include_args: 是否包含参数信息
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logger = logging.getLogger(func.__module__)
            
            # 记录开始执行
            if include_args:
                logger.log(
                    getattr(logging, level.upper()),
                    f"开始执行 - {func.__name__}: args={args}, kwargs={kwargs}"
                )
            else:
                logger.log(
                    getattr(logging, level.upper()),
                    f"开始执行 - {func.__name__}"
                )
            
            try:
                result = func(*args, **kwargs)
                logger.log(
                    getattr(logging, level.upper()),
                    f"执行完成 - {func.__name__}"
                )
                return result
            except Exception as e:
                logger.error(
                    f"执行失败 - {func.__name__}: {e}"
                )
                raise
        
        return wrapper
    return decorator


def timeout(seconds: float):
    """
    超时装饰器
    限制函数执行时间
    
    Args:
        seconds: 超时时间（秒）
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            import signal
            
            def timeout_handler(signum, frame):
                raise TimeoutError(f"函数 {func.__name__} 执行超时 ({seconds}s)")
            
            # 设置信号处理器
            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(int(seconds))
            
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                # 恢复原来的信号处理器
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)
        
        return wrapper
    return decorator


def rate_limit(requests_per_minute: int):
    """
    速率限制装饰器
    限制函数调用频率
    
    Args:
        requests_per_minute: 每分钟最大请求数
    """
    import threading
    from collections import deque
    
    # 线程安全的速率限制器
    class RateLimiter:
        def __init__(self, requests_per_minute: int):
            self.requests_per_minute = requests_per_minute
            self.requests = deque()
            self.lock = threading.Lock()
        
        def acquire(self):
            with self.lock:
                current_time = time.time()
                
                # 移除超过1分钟的请求记录
                while self.requests and current_time - self.requests[0] > 60:
                    self.requests.popleft()
                
                # 检查是否超过限制
                if len(self.requests) >= self.requests_per_minute:
                    wait_time = 60 - (current_time - self.requests[0])
                    time.sleep(wait_time)
                    # 重新计算
                    return self.acquire()
                
                # 记录当前请求
                self.requests.append(current_time)
    
    limiter = RateLimiter(requests_per_minute)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            limiter.acquire()
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


def singleton(cls):
    """
    单例装饰器
    确保类只有一个实例
    """
    instances = {}
    
    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return wrapper


def deprecated(replacement: Optional[str] = None):
    """
    弃用警告装饰器
    标记函数或类已弃用
    
    Args:
        replacement: 替代的函数或类名
    """
    def decorator(obj):
        if isinstance(obj, type):
            # 类装饰器
            class DeprecatedClass(obj):
                def __init__(self, *args, **kwargs):
                    warning_msg = f"类 {obj.__name__} 已弃用"
                    if replacement:
                        warning_msg += f"，请使用 {replacement} 替代"
                    logging.warning(warning_msg)
                    super().__init__(*args, **kwargs)
            
            return DeprecatedClass
        else:
            # 函数装饰器
            @wraps(obj)
            def wrapper(*args, **kwargs):
                warning_msg = f"函数 {obj.__name__} 已弃用"
                if replacement:
                    warning_msg += f"，请使用 {replacement} 替代"
                logging.warning(warning_msg)
                return obj(*args, **kwargs)
            
            return wrapper
    
    return decorator
