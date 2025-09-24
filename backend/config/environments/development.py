"""
开发环境配置
开发环境特定的配置设置
"""

from ..settings import Settings


class DevelopmentSettings(Settings):
    """开发环境配置"""
    
    # 应用配置
    debug: bool = True
    log_level: str = "DEBUG"
    
    # API配置
    api_host: str = "127.0.0.1"
    api_port: int = 5001
    api_workers: int = 1
    api_timeout: int = 60  # 开发环境可以设置更长的超时时间
    
    # 缓存配置
    cache_ttl_seconds: int = 300  # 5分钟缓存，便于调试
    cache_max_size: int = 500
    
    # 算法配置
    atr_period: int = 14
    grid_max_count: int = 50  # 开发环境使用较少的网格数量
    analysis_days_default: int = 180  # 开发环境使用较短的分析周期
    
    # 性能监控
    enable_performance_monitoring: bool = True
    performance_log_interval: int = 60  # 1分钟记录一次性能日志
    
    # 安全配置
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    rate_limit_requests: int = 1000  # 开发环境放宽限制
    rate_limit_window: int = 3600
    
    # 外部服务配置
    tushare_timeout: int = 60  # 开发环境可以设置更长的超时时间
    
    # 文件路径配置
    log_dir: str = "logs/dev"
    data_dir: str = "data/dev"
    temp_dir: str = "temp/dev"
    
    class Config:
        env_prefix = "DEV_"
        env_file = ".env.development"
