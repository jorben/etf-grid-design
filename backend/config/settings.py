"""
应用配置管理
定义系统配置和设置
"""

import os
from typing import Optional, Dict, Any
from pydantic import validator, Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Settings(BaseSettings):
    """应用主配置类"""
    
    # 应用基础配置
    app_name: str = Field(default="ETF Grid Trading Analysis", description="应用名称")
    app_version: str = Field(default="1.0.0", description="应用版本")
    environment: str = Field(default="development", description="运行环境")
    debug: bool = Field(default=False, description="调试模式")
    log_level: str = Field(default="INFO", description="日志级别")
    
    # API配置
    api_host: str = Field(default="0.0.0.0", description="API主机地址")
    api_port: int = Field(default=5001, description="API端口")
    api_workers: int = Field(default=1, description="API工作进程数")
    api_timeout: int = Field(default=30, description="API超时时间(秒)")
    
    # 数据库和缓存配置
    tushare_token: str = Field(..., description="Tushare API Token")
    cache_dir: str = Field(default="cache", description="缓存目录")
    cache_ttl_seconds: int = Field(default=3600, description="缓存过期时间(秒)")
    cache_max_size: int = Field(default=1000, description="缓存最大条目数")
    
    # 算法配置
    atr_period: int = Field(default=14, description="ATR计算周期")
    grid_max_count: int = Field(default=160, description="最大网格数量")
    grid_min_count: int = Field(default=5, description="最小网格数量")
    analysis_days_default: int = Field(default=365, description="默认分析天数")
    
    # 风险控制配置
    max_drawdown_limit: float = Field(default=0.1, description="最大回撤限制")
    stop_loss_ratio: float = Field(default=0.2, description="止损比例")
    take_profit_ratio: float = Field(default=0.3, description="止盈比例")
    
    # 性能监控配置
    enable_performance_monitoring: bool = Field(default=True, description="启用性能监控")
    performance_log_interval: int = Field(default=300, description="性能日志间隔(秒)")
    enable_health_check: bool = Field(default=True, description="启用健康检查")
    
    # 安全配置
    cors_origins: str = Field(default="*", description="CORS允许的源")
    rate_limit_requests: int = Field(default=100, description="速率限制请求数")
    rate_limit_window: int = Field(default=3600, description="速率限制窗口(秒)")
    
    # 外部服务配置
    tushare_base_url: str = Field(default="http://api.tushare.pro", description="Tushare基础URL")
    tushare_timeout: int = Field(default=30, description="Tushare超时时间(秒)")
    
    # 文件路径配置
    log_dir: str = Field(default="logs", description="日志目录")
    data_dir: str = Field(default="data", description="数据目录")
    temp_dir: str = Field(default="temp", description="临时目录")
    
    # 验证配置
    @validator('tushare_token')
    def validate_tushare_token(cls, v):
        """验证Tushare Token"""
        if not v:
            raise ValueError('TUSHARE_TOKEN环境变量是必需的')
        # 放宽长度验证，实际Tushare Token可能不是32位
        if len(v) < 16:
            raise ValueError('TUSHARE_TOKEN长度至少16位')
        return v
    
    @validator('api_port')
    def validate_api_port(cls, v):
        """验证API端口"""
        if v < 1024 or v > 65535:
            raise ValueError('API端口必须在1024-65535之间')
        return v
    
    @validator('log_level')
    def validate_log_level(cls, v):
        """验证日志级别"""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'日志级别必须是: {", ".join(valid_levels)}')
        return v.upper()
    
    @validator('cors_origins')
    def parse_cors_origins(cls, v):
        """解析CORS源配置"""
        if v == "*":
            return ["*"]
        return [origin.strip() for origin in v.split(",")]
    
    class Config:
        """Pydantic配置"""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        validate_assignment = True
        extra = "ignore"  # 忽略额外的环境变量


class DevelopmentSettings(Settings):
    """开发环境配置"""
    
    debug: bool = True
    log_level: str = "DEBUG"
    api_workers: int = 1
    cache_ttl_seconds: int = 300  # 5分钟缓存
    enable_performance_monitoring: bool = True


class ProductionSettings(Settings):
    """生产环境配置"""
    
    debug: bool = False
    log_level: str = "INFO"
    api_workers: int = 4
    cache_ttl_seconds: int = 3600  # 1小时缓存
    enable_performance_monitoring: bool = True


class TestingSettings(Settings):
    """测试环境配置"""
    
    debug: bool = True
    log_level: str = "DEBUG"
    api_workers: int = 1
    cache_ttl_seconds: int = 60  # 1分钟缓存
    enable_performance_monitoring: bool = False
    tushare_token: str = "test_token_12345678901234567890123456"


def get_settings() -> Settings:
    """根据环境获取配置实例"""
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    if env == "production":
        return ProductionSettings()
    elif env == "testing":
        return TestingSettings()
    else:
        return DevelopmentSettings()


# 全局配置实例
settings = get_settings()
