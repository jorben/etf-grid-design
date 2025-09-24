"""
性能监控工具
提供系统性能监控和指标收集功能
"""

import time
import threading
import psutil
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import deque, defaultdict
from ..config.constants import PerformanceConstants


class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self, max_records: int = 1000):
        self.max_records = max_records
        self.metrics = defaultdict(lambda: deque(maxlen=max_records))
        self.lock = threading.Lock()
        self.start_time = time.time()
        
        # 系统性能指标
        self.system_metrics = {
            'cpu_usage': deque(maxlen=100),
            'memory_usage': deque(maxlen=100),
            'disk_io': deque(maxlen=100),
            'network_io': deque(maxlen=100)
        }
    
    def record_metric(self, metric_name: str, value: float, timestamp: Optional[float] = None):
        """记录性能指标"""
        if timestamp is None:
            timestamp = time.time()
        
        with self.lock:
            self.metrics[metric_name].append({
                'value': value,
                'timestamp': timestamp
            })
    
    def get_metric_stats(self, metric_name: str, window_seconds: int = 300) -> Dict[str, float]:
        """获取指标统计信息"""
        with self.lock:
            records = list(self.metrics[metric_name])
        
        if not records:
            return {}
        
        # 过滤时间窗口内的记录
        cutoff_time = time.time() - window_seconds
        recent_records = [
            r for r in records 
            if r['timestamp'] >= cutoff_time
        ]
        
        if not recent_records:
            return {}
        
        values = [r['value'] for r in recent_records]
        
        return {
            'count': len(values),
            'min': min(values),
            'max': max(values),
            'mean': sum(values) / len(values),
            'latest': values[-1]
        }
    
    def record_function_performance(self, func_name: str, execution_time: float):
        """记录函数性能"""
        self.record_metric(f"function_{func_name}_time", execution_time)
        self.record_metric("total_function_calls", 1)
    
    def record_api_performance(self, endpoint: str, response_time: float, status_code: int):
        """记录API性能"""
        self.record_metric(f"api_{endpoint}_response_time", response_time)
        self.record_metric(f"api_{endpoint}_status_{status_code}", 1)
    
    def record_cache_performance(self, cache_hits: int, cache_misses: int):
        """记录缓存性能"""
        total = cache_hits + cache_misses
        if total > 0:
            hit_rate = cache_hits / total
            self.record_metric("cache_hit_rate", hit_rate)
        
        self.record_metric("cache_hits", cache_hits)
        self.record_metric("cache_misses", cache_misses)
    
    def collect_system_metrics(self):
        """收集系统性能指标"""
        try:
            # CPU使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            self.system_metrics['cpu_usage'].append({
                'value': cpu_percent,
                'timestamp': time.time()
            })
            
            # 内存使用率
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            self.system_metrics['memory_usage'].append({
                'value': memory_percent,
                'timestamp': time.time()
            })
            
            # 磁盘IO
            disk_io = psutil.disk_io_counters()
            if disk_io:
                disk_usage = (disk_io.read_bytes + disk_io.write_bytes) / (1024 * 1024)  # MB
                self.system_metrics['disk_io'].append({
                    'value': disk_usage,
                    'timestamp': time.time()
                })
            
            # 网络IO
            net_io = psutil.net_io_counters()
            if net_io:
                net_usage = (net_io.bytes_sent + net_io.bytes_recv) / (1024 * 1024)  # MB
                self.system_metrics['network_io'].append({
                    'value': net_usage,
                    'timestamp': time.time()
                })
                
        except Exception as e:
            logging.warning(f"收集系统指标失败: {e}")
    
    def get_system_metrics_summary(self) -> Dict[str, Any]:
        """获取系统指标摘要"""
        summary = {}
        
        for metric_name, records in self.system_metrics.items():
            if records:
                values = [r['value'] for r in records]
                summary[metric_name] = {
                    'current': values[-1] if values else 0,
                    'average': sum(values) / len(values) if values else 0,
                    'max': max(values) if values else 0
                }
        
        return summary
    
    def get_performance_summary(self, window_seconds: int = 300) -> Dict[str, Any]:
        """获取性能摘要"""
        summary = {
            'uptime': time.time() - self.start_time,
            'timestamp': datetime.now().isoformat(),
            'system_metrics': self.get_system_metrics_summary(),
            'application_metrics': {}
        }
        
        # 应用性能指标
        metric_patterns = [
            ('function_.*_time', 'function_performance'),
            ('api_.*_response_time', 'api_performance'),
            ('cache_.*', 'cache_performance')
        ]
        
        for pattern, category in metric_patterns:
            category_metrics = {}
            for metric_name in self.metrics:
                if re.match(pattern, metric_name):
                    stats = self.get_metric_stats(metric_name, window_seconds)
                    if stats:
                        category_metrics[metric_name] = stats
            
            if category_metrics:
                summary['application_metrics'][category] = category_metrics
        
        return summary
    
    def is_system_healthy(self, thresholds: Optional[Dict[str, float]] = None) -> bool:
        """检查系统健康状态"""
        if thresholds is None:
            thresholds = {
                'cpu_usage': 90.0,  # CPU使用率阈值
                'memory_usage': 85.0,  # 内存使用率阈值
                'api_response_time': 5.0  # API响应时间阈值（秒）
            }
        
        system_metrics = self.get_system_metrics_summary()
        
        # 检查系统资源
        if (system_metrics.get('cpu_usage', {}).get('current', 0) > thresholds['cpu_usage'] or
            system_metrics.get('memory_usage', {}).get('current', 0) > thresholds['memory_usage']):
            return False
        
        # 检查API性能
        api_stats = self.get_metric_stats('api_.*_response_time', 60)  # 最近1分钟
        if api_stats.get('max', 0) > thresholds['api_response_time']:
            return False
        
        return True


class PerformanceProfiler:
    """性能分析器"""
    
    def __init__(self):
        self.profiles = {}
        self.active_profiles = {}
    
    def start_profile(self, profile_name: str):
        """开始性能分析"""
        self.active_profiles[profile_name] = {
            'start_time': time.time(),
            'memory_start': psutil.Process().memory_info().rss / 1024 / 1024  # MB
        }
    
    def end_profile(self, profile_name: str) -> Dict[str, Any]:
        """结束性能分析并返回结果"""
        if profile_name not in self.active_profiles:
            return {}
        
        profile_data = self.active_profiles.pop(profile_name)
        end_time = time.time()
        memory_end = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        result = {
            'execution_time': end_time - profile_data['start_time'],
            'memory_used': memory_end - profile_data['memory_start'],
            'timestamp': datetime.now().isoformat()
        }
        
        # 保存分析结果
        if profile_name not in self.profiles:
            self.profiles[profile_name] = []
        self.profiles[profile_name].append(result)
        
        return result
    
    def get_profile_stats(self, profile_name: str) -> Dict[str, Any]:
        """获取性能分析统计"""
        if profile_name not in self.profiles or not self.profiles[profile_name]:
            return {}
        
        profiles = self.profiles[profile_name]
        execution_times = [p['execution_time'] for p in profiles]
        memory_used = [p['memory_used'] for p in profiles]
        
        return {
            'total_runs': len(profiles),
            'execution_time': {
                'min': min(execution_times),
                'max': max(execution_times),
                'mean': sum(execution_times) / len(execution_times),
                'latest': execution_times[-1] if execution_times else 0
            },
            'memory_usage': {
                'min': min(memory_used),
                'max': max(memory_used),
                'mean': sum(memory_used) / len(memory_used),
                'latest': memory_used[-1] if memory_used else 0
            }
        }


class ResourceMonitor:
    """资源监控器"""
    
    def __init__(self):
        self.resource_usage = {}
    
    def monitor_resource(self, resource_name: str, usage_callback: callable):
        """监控资源使用情况"""
        self.resource_usage[resource_name] = {
            'callback': usage_callback,
            'history': deque(maxlen=100),
            'last_check': time.time()
        }
    
    def check_resources(self) -> Dict[str, Any]:
        """检查资源使用情况"""
        current_status = {}
        
        for resource_name, monitor_info in self.resource_usage.items():
            try:
                usage = monitor_info['callback']()
                monitor_info['history'].append({
                    'usage': usage,
                    'timestamp': time.time()
                })
                current_status[resource_name] = usage
            except Exception as e:
                logging.error(f"检查资源 {resource_name} 失败: {e}")
                current_status[resource_name] = None
        
        return current_status
    
    def get_resource_trend(self, resource_name: str, window_minutes: int = 60) -> Dict[str, Any]:
        """获取资源使用趋势"""
        if resource_name not in self.resource_usage:
            return {}
        
        monitor_info = self.resource_usage[resource_name]
        cutoff_time = time.time() - (window_minutes * 60)
        
        recent_usage = [
            entry for entry in monitor_info['history']
            if entry['timestamp'] >= cutoff_time
        ]
        
        if not recent_usage:
            return {}
        
        usage_values = [entry['usage'] for entry in recent_usage]
        
        return {
            'current': usage_values[-1],
            'average': sum(usage_values) / len(usage_values),
            'trend': 'increasing' if len(usage_values) > 1 and usage_values[-1] > usage_values[0] else 'decreasing',
            'data_points': len(usage_values)
        }


# 全局性能监控实例
performance_monitor = PerformanceMonitor()
performance_profiler = PerformanceProfiler()
resource_monitor = ResourceMonitor()


def start_performance_monitoring(interval_seconds: int = 60):
    """启动性能监控"""
    def monitoring_loop():
        while True:
            try:
                performance_monitor.collect_system_metrics()
                resource_monitor.check_resources()
            except Exception as e:
                logging.error(f"性能监控循环错误: {e}")
            
            time.sleep(interval_seconds)
    
    monitor_thread = threading.Thread(target=monitoring_loop, daemon=True)
    monitor_thread.start()
    return monitor_thread


def profile_function(func):
    """函数性能分析装饰器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        profile_name = f"{func.__module__}.{func.__name__}"
        performance_profiler.start_profile(profile_name)
        
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            performance_profiler.end_profile(profile_name)
    
    return wrapper


import re  # 添加缺失的导入


# 资源监控回调函数示例
def get_database_connections():
    """获取数据库连接数（示例）"""
    # 这里需要根据实际的数据库实现来获取连接数
    return 0

def get_cache_usage():
    """获取缓存使用情况（示例）"""
    # 这里需要根据实际的缓存实现来获取使用情况
    return 0

def get_active_requests():
    """获取活跃请求数（示例）"""
    # 这里需要根据实际的请求跟踪实现来获取活跃请求数
    return 0


# 初始化资源监控
resource_monitor.monitor_resource('database_connections', get_database_connections)
resource_monitor.monitor_resource('cache_usage', get_cache_usage)
resource_monitor.monitor_resource('active_requests', get_active_requests)
