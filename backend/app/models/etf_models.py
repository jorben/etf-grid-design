"""
ETF相关数据模型
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class ETFBasicInfo:
    """ETF基础信息模型"""
    code: str
    name: str
    market: Optional[str] = None
    list_date: Optional[str] = None
    fund_type: Optional[str] = None
    management_fee: Optional[float] = None
    custodian_fee: Optional[float] = None
    benchmark: Optional[str] = None
    
    def __post_init__(self):
        """数据验证"""
        if not self.code or len(self.code) != 6:
            raise ValueError("ETF代码必须是6位数字")
        if not self.name:
            raise ValueError("ETF名称不能为空")

@dataclass
class ETFPriceData:
    """ETF价格数据模型"""
    trade_date: str
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int
    amount: float
    pct_change: Optional[float] = None
    
    def __post_init__(self):
        """数据验证"""
        if self.high_price < self.low_price:
            raise ValueError("最高价不能低于最低价")
        if self.open_price <= 0 or self.close_price <= 0:
            raise ValueError("价格必须大于0")
        if self.volume < 0 or self.amount < 0:
            raise ValueError("成交量和成交额不能为负数")

@dataclass
class PopularETF:
    """热门ETF模型"""
    code: str
    name: str
    category: Optional[str] = None
    is_popular: bool = True
    current_price: Optional[float] = None
    pct_change: Optional[float] = None
    
    def __post_init__(self):
        """数据验证"""
        if not self.code or len(self.code) != 6:
            raise ValueError("ETF代码必须是6位数字")
        if not self.name:
            raise ValueError("ETF名称不能为空")

@dataclass
class ETFLatestPrice:
    """ETF最新价格模型"""
    code: str
    trade_date: str
    close_price: float
    pct_change: Optional[float] = None
    volume: Optional[int] = None
    amount: Optional[float] = None
    
    def __post_init__(self):
        """数据验证"""
        if self.close_price <= 0:
            raise ValueError("价格必须大于0")

@dataclass
class ETFSearchResult:
    """ETF搜索结果模型"""
    code: str
    name: str
    market: str
    list_date: Optional[str] = None
    
    def __post_init__(self):
        """数据验证"""
        if not self.code or not self.name:
            raise ValueError("代码和名称不能为空")