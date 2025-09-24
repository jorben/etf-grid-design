"""
策略配置相关数据模型
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum

class GridType(Enum):
    """网格类型枚举"""
    ARITHMETIC = "等差"
    GEOMETRIC = "等比"

class RiskPreference(Enum):
    """风险偏好枚举"""
    CONSERVATIVE = "保守"
    BALANCED = "稳健"
    AGGRESSIVE = "激进"

@dataclass
class StrategyConfig:
    """策略配置模型"""
    etf_code: str
    total_capital: float
    grid_type: str
    risk_preference: str
    trading_frequency: Optional[str] = "medium"
    max_position_ratio: Optional[float] = 0.8
    stop_loss_ratio: Optional[float] = None
    take_profit_ratio: Optional[float] = None
    
    def __post_init__(self):
        """数据验证"""
        if not self.etf_code or len(self.etf_code) != 6:
            raise ValueError("ETF代码必须是6位数字")
        if self.total_capital <= 0:
            raise ValueError("总资金必须大于0")
        if self.grid_type not in [gt.value for gt in GridType]:
            raise ValueError(f"网格类型必须是{[gt.value for gt in GridType]}之一")
        if self.risk_preference not in [rp.value for rp in RiskPreference]:
            raise ValueError(f"风险偏好必须是{[rp.value for rp in RiskPreference]}之一")

@dataclass
class GridLevel:
    """单个网格水平模型"""
    level: int
    price: float
    is_buy_level: bool
    quantity: int
    amount: float
    status: str = "pending"  # pending, filled, cancelled
    
    def __post_init__(self):
        """数据验证"""
        if self.price <= 0:
            raise ValueError("价格必须大于0")
        if self.quantity < 0:
            raise ValueError("数量不能为负数")

@dataclass
class GridStrategy:
    """完整网格策略模型"""
    config: StrategyConfig
    grid_levels: List[GridLevel]
    base_position: Dict[str, Any]
    expected_return: Optional[float] = None
    max_risk: Optional[float] = None
    
    def __post_init__(self):
        """数据验证"""
        if not self.grid_levels:
            raise ValueError("网格水平不能为空")
        if not self.base_position:
            raise ValueError("底仓配置不能为空")

@dataclass
class BacktestResult:
    """回测结果模型"""
    start_date: str
    end_date: str
    total_return: float
    annualized_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    total_trades: int
    profit_trades: int
    loss_trades: int
    
    def __post_init__(self):
        """数据验证"""
        if self.total_trades < 0:
            raise ValueError("交易次数不能为负数")
        if not 0 <= self.win_rate <= 1:
            raise ValueError("胜率必须在0-1之间")

@dataclass
class PerformanceMetrics:
    """性能指标模型"""
    total_return: float
    annualized_return: float
    volatility: float
    sharpe_ratio: float
    max_drawdown: float
    calmar_ratio: float
    win_rate: float
    profit_factor: float
    
    def __post_init__(self):
        """数据验证"""
        if not 0 <= self.win_rate <= 1:
            raise ValueError("胜率必须在0-1之间")
        if self.volatility < 0:
            raise ValueError("波动率不能为负数")

@dataclass
class TradingSignal:
    """交易信号模型"""
    timestamp: str
    signal_type: str  # 'buy', 'sell', 'hold'
    price: float
    quantity: int
    confidence: float
    reason: str
    
    def __post_init__(self):
        """数据验证"""
        if self.signal_type not in ['buy', 'sell', 'hold']:
            raise ValueError("信号类型必须是buy、sell或hold")
        if self.price <= 0:
            raise ValueError("价格必须大于0")
        if not 0 <= self.confidence <= 1:
            raise ValueError("置信度必须在0-1之间")

@dataclass
class PositionInfo:
    """持仓信息模型"""
    etf_code: str
    total_quantity: int
    average_cost: float
    current_price: float
    market_value: float
    unrealized_pnl: float
    unrealized_pnl_ratio: float
    
    def __post_init__(self):
        """数据验证"""
        if self.total_quantity < 0:
            raise ValueError("持仓数量不能为负数")
        if self.average_cost <= 0 or self.current_price <= 0:
            raise ValueError("成本价和当前价必须大于0")

@dataclass
class RiskControl:
    """风险控制模型"""
    max_position_ratio: float
    stop_loss_ratio: Optional[float] = None
    take_profit_ratio: Optional[float] = None
    max_drawdown_limit: Optional[float] = None
    position_size_limit: Optional[int] = None
    
    def __post_init__(self):
        """数据验证"""
        if not 0 < self.max_position_ratio <= 1:
            raise ValueError("最大仓位比例必须在0-1之间")
        if self.stop_loss_ratio and self.stop_loss_ratio >= 0:
            raise ValueError("止损比例应为负数")
        if self.take_profit_ratio and self.take_profit_ratio <= 0:
            raise ValueError("止盈比例应为正数")