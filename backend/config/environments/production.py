"""
生产环境配置
生产环境特定的配置设置
"""

from ..settings import Settings


class ProductionSettings(Settings):
    """生产环境配置"""
    
    # 应用配置
    debug: bool = False
    log_level: str = "INFO"
    
    # API配置
    api_host: str = "0.0.0.0"
    api_port: int = 5001
    api_workers: int = 4  # 生产环境使用更多工作进程
    api_timeout: int = 30
    
    # 缓存配置
    cache_ttl_seconds: int = 3600  # 1小时缓存
    cache_max_size: int = 1000
    
    # 算法配置
    atr_period: int = 14
    grid_max_count: int = 160
    analysis_days_default: int = 365
    
    # 性能监控
    enable_performance_monitoring: bool = True
    performance_log_interval: int = 300  # 5分钟记录一次性能日志
    
    # 安全配置
    cors_origins: str = "https://yourdomain.com"  # 替换为实际域名
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600
    
    # 外部服务配置
    tushare_timeout: int = 30
    
    # 文件路径配置
    log_dir: str = "logs/prod"
    data_dir: str = "data/prod"
    temp_dir: str = "temp/prod"
    
    # 生产环境特定的安全配置
    enable_health_check: bool = True
    
    class Config:
        env_prefix = "PROD_"
        env_file = ".env.production"
