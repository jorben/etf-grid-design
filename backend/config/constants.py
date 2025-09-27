"""
系统常量定义
定义应用中使用的重要常量
"""

from enum import Enum
from typing import Dict, List, Tuple


class ETFConstants:
    """ETF相关常量"""
    
    # ETF代码前缀
    STOCK_ETF_PREFIX = ["51", "15", "58"]
    BOND_ETF_PREFIX = ["51", "15", "58"]
    COMMODITY_ETF_PREFIX = ["15", "51"]
    
    # ETF类型映射
    ETF_TYPE_MAPPING = {
        "51": "股票ETF",
        "15": "债券ETF", 
        "58": "商品ETF"
    }
    
    # 最小交易单位
    MIN_TRADE_UNIT = 100  # 最小交易单位（手）
    MIN_TRADE_QUANTITY = 100  # 最小交易数量（股）
    
    # 价格精度
    PRICE_PRECISION = 3  # 价格小数位数
    AMOUNT_PRECISION = 2  # 金额小数位数
    
    # 默认分析参数
    DEFAULT_ANALYSIS_DAYS = 365
    MIN_ANALYSIS_DAYS = 30
    MAX_ANALYSIS_DAYS = 1000


class GridConstants:
    """网格交易常量"""
    
    # 网格类型
    GRID_TYPES = ["等差", "等比"]
    
    # 风险偏好
    RISK_PREFERENCES = ["低频", "均衡", "高频"]
    
    # 网格数量限制
    MIN_GRID_COUNT = 5
    MAX_GRID_COUNT = 160
    DEFAULT_GRID_COUNT = 20
    
    # 资金分配比例
    BASE_POSITION_RATIO_RANGE = (0.1, 0.5)  # 底仓比例范围
    GRID_FUND_RATIO_RANGE = (0.3, 0.7)  # 网格资金比例范围
    RESERVE_FUND_RATIO_RANGE = (0.1, 0.3)  # 预留资金比例范围
    
    # 交易频率
    TRADING_FREQUENCIES = ["low", "medium", "high"]
    
    # 默认参数
    DEFAULT_COMMISSION_RATE = 0.0003  # 默认佣金费率
    DEFAULT_SLIPPAGE = 0.001  # 默认滑点


class ATRConstants:
    """ATR算法常量"""
    
    # ATR计算周期
    DEFAULT_ATR_PERIOD = 14
    MIN_ATR_PERIOD = 5
    MAX_ATR_PERIOD = 50
    
    # ATR乘数
    ATR_MULTIPLIERS = {
        "低频": 1.0,
        "均衡": 1.5, 
        "高频": 2.0
    }
    
    # 波动率等级阈值
    VOLATILITY_THRESHOLDS = {
        "低波动": 0.02,   # 2%
        "中等波动": 0.05,  # 5%
        "高波动": 0.10    # 10%
    }


class RiskConstants:
    """风险控制常量"""
    
    # 风险等级
    RISK_LEVELS = {
        "低风险": (80, 100),
        "中低风险": (60, 79),
        "中等风险": (40, 59), 
        "中高风险": (20, 39),
        "高风险": (0, 19)
    }
    
    # 适宜度评分权重
    SUITABILITY_WEIGHTS = {
        "amplitude": 0.25,      # 振幅权重
        "volatility": 0.20,     # 波动率权重
        "liquidity": 0.25,      # 流动性权重
        "market_characteristics": 0.15,  # 市场特征权重
        "data_quality": 0.15     # 数据质量权重
    }
    
    # 最大回撤限制
    MAX_DRAWDOWN_LIMITS = {
        "低频": 0.05,   # 5%
        "均衡": 0.10,   # 10%
        "高频": 0.15    # 15%
    }


class PerformanceConstants:
    """性能指标常量"""
    
    # 性能阈值
    PERFORMANCE_THRESHOLDS = {
        "优秀": 0.15,    # 15%
        "良好": 0.08,    # 8%
        "一般": 0.03,    # 3%
        "较差": -0.05    # -5%
    }
    
    # 夏普比率等级
    SHARPE_RATIO_LEVELS = {
        "优秀": 2.0,
        "良好": 1.0,
        "一般": 0.5,
        "较差": 0.0
    }
    
    # 胜率等级
    WIN_RATE_LEVELS = {
        "优秀": 0.7,     # 70%
        "良好": 0.6,     # 60%
        "一般": 0.5,     # 50%
        "较差": 0.4      # 40%
    }


class TimeConstants:
    """时间相关常量"""
    
    # 时间格式
    DATE_FORMAT = "%Y-%m-%d"
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    TIME_FORMAT = "%H:%M:%S"
    
    # 交易时间
    TRADING_HOURS = {
        "morning_start": "09:30:00",
        "morning_end": "11:30:00", 
        "afternoon_start": "13:00:00",
        "afternoon_end": "15:00:00"
    }
    
    # 节假日（示例，实际需要根据每年更新）
    HOLIDAYS_2024 = [
        "2024-01-01",  # 元旦
        "2024-02-10", "2024-02-11", "2024-02-12",  # 春节
        "2024-04-04", "2024-04-05", "2024-04-06",  # 清明节
        "2024-05-01", "2024-05-02", "2024-05-03",  # 劳动节
        "2024-06-10",  # 端午节
        "2024-09-15", "2024-09-16", "2024-09-17",  # 中秋节
        "2024-10-01", "2024-10-02", "2024-10-03", "2024-10-04", "2024-10-05", "2024-10-06", "2024-10-07"  # 国庆节
    ]


class ErrorConstants:
    """错误码常量"""
    
    # 成功
    SUCCESS = 0
    
    # 通用错误
    UNKNOWN_ERROR = 1000
    INVALID_PARAMETER = 1001
    DATA_NOT_FOUND = 1002
    PERMISSION_DENIED = 1003
    RATE_LIMIT_EXCEEDED = 1004
    
    # 数据相关错误
    DATA_VALIDATION_ERROR = 2001
    DATA_FETCH_ERROR = 2002
    DATA_PROCESSING_ERROR = 2003
    CACHE_ERROR = 2004
    
    # 算法相关错误
    CALCULATION_ERROR = 3001
    ALGORITHM_ERROR = 3002
    OPTIMIZATION_ERROR = 3003
    
    # 外部服务错误
    EXTERNAL_SERVICE_ERROR = 4001
    API_TIMEOUT = 4002
    NETWORK_ERROR = 4003
    
    # 配置错误
    CONFIGURATION_ERROR = 5001
    ENVIRONMENT_ERROR = 5002


class LogConstants:
    """日志相关常量"""
    
    # 日志级别
    LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    
    # 日志格式
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    JSON_LOG_FORMAT = {
        "timestamp": "%(asctime)s",
        "logger": "%(name)s", 
        "level": "%(levelname)s",
        "message": "%(message)s",
        "module": "%(module)s",
        "function": "%(funcName)s",
        "line": "%(lineno)d"
    }
    
    # 日志文件配置
    MAX_LOG_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    BACKUP_COUNT = 5  # 备份文件数量


class APIResponseConstants:
    """API响应常量"""
    
    # 响应状态
    STATUS_SUCCESS = "success"
    STATUS_ERROR = "error"
    
    # 响应消息
    MESSAGES = {
        "SUCCESS": "操作成功",
        "INVALID_PARAMETER": "参数错误",
        "DATA_NOT_FOUND": "数据不存在",
        "PERMISSION_DENIED": "权限不足",
        "RATE_LIMIT_EXCEEDED": "请求频率过高",
        "INTERNAL_ERROR": "内部错误"
    }


# 全局常量映射
CONSTANTS_MAPPING = {
    "etf": ETFConstants,
    "grid": GridConstants, 
    "atr": ATRConstants,
    "risk": RiskConstants,
    "performance": PerformanceConstants,
    "time": TimeConstants,
    "error": ErrorConstants,
    "log": LogConstants,
    "api": APIResponseConstants
}


def get_constants(category: str):
    """获取指定类别的常量"""
    return CONSTANTS_MAPPING.get(category)
