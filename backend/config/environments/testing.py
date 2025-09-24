"""
测试环境配置
测试环境特定的配置设置
"""

from ..settings import Settings


class TestingSettings(Settings):
    """测试环境配置"""
    
    # 应用配置
    debug: bool = True
    log_level: str = "DEBUG"
    
    # API配置
    api_host: str = "127.0.0.1"
    api_port: int = 5002  # 测试环境使用不同端口
    api_workers: int = 1
    api_timeout: int = 10  # 测试环境使用较短的超时时间
    
    # 缓存配置
    cache_ttl_seconds: int = 60  # 1分钟缓存，便于测试
    cache_max_size: int = 100
    
    # 算法配置
    atr_period: int = 14
    grid_max_count: int = 10  # 测试环境使用较少的网格数量
    analysis_days_default: int = 30  # 测试环境使用较短的分析周期
    
    # 性能监控
    enable_performance_monitoring: bool = False  # 测试环境关闭性能监控
    performance_log_interval: int = 0
    
    # 安全配置
    cors_origins: str = "*"
    rate_limit_requests: int = 10000  # 测试环境放宽限制
    rate_limit_window: int = 3600
    
    # 外部服务配置
    tushare_timeout: int = 5  # 测试环境使用较短的超时时间
    tushare_token: str = "test_token_12345678901234567890123456"  # 测试用token
    
    # 文件路径配置
    log_dir: str = "logs/test"
    data_dir: str = "data/test"
    temp_dir: str = "temp/test"
    
    # 测试环境特定的配置
    enable_health_check: bool = False  # 测试环境关闭健康检查
    
    class Config:
        env_prefix = "TEST_"
        env_file = ".env.testing"
