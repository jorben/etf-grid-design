"""
策略模型
定义网格策略相关的数据结构和配置模型
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class GridType(str, Enum):
    """网格类型枚举"""
    ARITHMETIC = "等差"
    GEOMETRIC = "等比"


class RiskPreference(str, Enum):
    """风险偏好枚举"""
    CONSERVATIVE = "低频"
    MODERATE = "均衡"
    AGGRESSIVE = "高频"


class StrategyStatus(str, Enum):
    """策略状态枚举"""
    ACTIVE = "active"
    PAUSED = "paused"
    STOPPED = "stopped"
    COMPLETED = "completed"


class GridLevel(BaseModel):
    """网格层级模型"""
    level: int = Field(..., ge=1, description="层级编号")
    price: float = Field(..., gt=0, description="价格")
    action: str = Field(..., description="操作类型")
    quantity: int = Field(..., ge=0, description="数量")
    allocated_fund: float = Field(..., ge=0, description="分配资金")
    executed: bool = Field(default=False, description="是否已执行")
    execution_time: Optional[datetime] = Field(None, description="执行时间")
    execution_price: Optional[float] = Field(None, description="执行价格")


class GridStrategyConfig(BaseModel):
    """网格策略配置"""
    etf_code: str = Field(..., description="ETF代码")
    strategy_name: str = Field(..., description="策略名称")
    grid_type: GridType = Field(..., description="网格类型")
    risk_preference: RiskPreference = Field(..., description="风险偏好")
    
    # 价格参数
    current_price: float = Field(..., gt=0, description="当前价格")
    price_lower: float = Field(..., gt=0, description="价格下限")
    price_upper: float = Field(..., gt=0, description="价格上限")
    
    # 资金参数
    total_capital: float = Field(..., gt=0, description="总资金")
    base_position_ratio: float = Field(..., ge=0, le=1, description="底仓比例")
    grid_trading_amount: float = Field(..., ge=0, description="网格交易金额")
    
    # 网格参数
    grid_count: int = Field(..., ge=2, le=200, description="网格数量")
    step_size: float = Field(..., gt=0, description="步长")
    step_ratio: float = Field(..., gt=0, description="步长比例")
    
    # 交易参数
    single_trade_quantity: int = Field(..., ge=0, description="单笔交易数量")
    commission_rate: float = Field(default=0.0003, ge=0, description="佣金费率")
    
    # 风险控制
    max_drawdown_limit: float = Field(default=0.1, ge=0, le=1, description="最大回撤限制")
    stop_loss_ratio: float = Field(default=0.2, ge=0, le=1, description="止损比例")
    take_profit_ratio: float = Field(default=0.3, ge=0, le=1, description="止盈比例")
    
    # 时间参数
    start_date: str = Field(..., description="开始日期")
    end_date: Optional[str] = Field(None, description="结束日期")
    rebalance_frequency: str = Field(default="daily", description="再平衡频率")
    
    # 高级配置
    enable_atr_adjustment: bool = Field(default=True, description="启用ATR调整")
    enable_dynamic_rebalancing: bool = Field(default=True, description="启用动态再平衡")
    enable_risk_control: bool = Field(default=True, description="启用风险控制")


class GridStrategyState(BaseModel):
    """网格策略状态"""
    strategy_id: str = Field(..., description="策略ID")
    current_status: StrategyStatus = Field(..., description="当前状态")
    current_price: float = Field(..., description="当前价格")
    current_position: int = Field(..., ge=0, description="当前持仓")
    current_value: float = Field(..., ge=0, description="当前市值")
    unrealized_pnl: float = Field(..., description="未实现盈亏")
    realized_pnl: float = Field(..., description="已实现盈亏")
    
    # 网格执行状态
    executed_levels: List[int] = Field(..., description="已执行层级")
    pending_levels: List[int] = Field(..., description="待执行层级")
    active_buy_levels: List[int] = Field(..., description="活跃买入层级")
    active_sell_levels: List[int] = Field(..., description="活跃卖出层级")
    
    # 资金状态
    available_cash: float = Field(..., ge=0, description="可用现金")
    total_invested: float = Field(..., ge=0, description="总投资")
    total_withdrawn: float = Field(..., ge=0, description="总提取")
    
    # 性能指标
    total_return: float = Field(..., description="总收益率")
    annual_return: float = Field(..., description="年化收益率")
    sharpe_ratio: Optional[float] = Field(None, description="夏普比率")
    max_drawdown: float = Field(..., description="最大回撤")
    
    # 交易统计
    total_trades: int = Field(..., ge=0, description="总交易次数")
    win_trades: int = Field(..., ge=0, description="盈利交易次数")
    loss_trades: int = Field(..., ge=0, description="亏损交易次数")
    win_rate: float = Field(..., ge=0, le=1, description="胜率")
    
    # 时间信息
    created_time: datetime = Field(..., description="创建时间")
    last_updated: datetime = Field(..., description="最后更新时间")
    last_trade_time: Optional[datetime] = Field(None, description="最后交易时间")


class TradeRecord(BaseModel):
    """交易记录"""
    trade_id: str = Field(..., description="交易ID")
    strategy_id: str = Field(..., description="策略ID")
    trade_time: datetime = Field(..., description="交易时间")
    trade_type: str = Field(..., description="交易类型")
    etf_code: str = Field(..., description="ETF代码")
    price: float = Field(..., gt=0, description="交易价格")
    quantity: int = Field(..., ge=0, description="交易数量")
    amount: float = Field(..., ge=0, description="交易金额")
    commission: float = Field(..., ge=0, description="佣金")
    net_amount: float = Field(..., description="净金额")
    
    # 网格相关信息
    grid_level: int = Field(..., ge=1, description="网格层级")
    grid_price: float = Field(..., gt=0, description="网格价格")
    grid_action: str = Field(..., description="网格操作")
    
    # 状态信息
    status: str = Field(..., description="交易状态")
    remarks: Optional[str] = Field(None, description="备注")


class StrategyPerformance(BaseModel):
    """策略性能统计"""
    strategy_id: str = Field(..., description="策略ID")
    period: str = Field(..., description="统计周期")
    
    # 收益指标
    total_return: float = Field(..., description="总收益率")
    annual_return: float = Field(..., description="年化收益率")
    cumulative_return: float = Field(..., description="累计收益率")
    monthly_return: float = Field(..., description="月收益率")
    daily_return: float = Field(..., description="日收益率")
    
    # 风险指标
    volatility: float = Field(..., description="波动率")
    sharpe_ratio: float = Field(..., description="夏普比率")
    sortino_ratio: Optional[float] = Field(None, description="索提诺比率")
    max_drawdown: float = Field(..., description="最大回撤")
    calmar_ratio: Optional[float] = Field(None, description="卡玛比率")
    
    # 交易指标
    total_trades: int = Field(..., description="总交易次数")
    win_rate: float = Field(..., description="胜率")
    profit_factor: float = Field(..., description="盈利因子")
    average_win: float = Field(..., description="平均盈利")
    average_loss: float = Field(..., description="平均亏损")
    
    # 资金指标
    total_invested: float = Field(..., description="总投资")
    current_value: float = Field(..., description="当前价值")
    cash_balance: float = Field(..., description="现金余额")
    margin_usage: float = Field(..., description="保证金使用率")
    
    # 时间信息
    start_date: str = Field(..., description="开始日期")
    end_date: str = Field(..., description="结束日期")
    calculation_date: datetime = Field(default_factory=datetime.now, description="计算日期")


class StrategyOptimizationResult(BaseModel):
    """策略优化结果"""
    original_config: GridStrategyConfig = Field(..., description="原始配置")
    optimized_config: GridStrategyConfig = Field(..., description="优化后配置")
    optimization_metrics: Dict[str, float] = Field(..., description="优化指标")
    improvement_details: Dict[str, Any] = Field(..., description="改进详情")
    optimization_date: datetime = Field(default_factory=datetime.now, description="优化日期")


class StrategyBacktestRequest(BaseModel):
    """策略回测请求"""
    strategy_config: GridStrategyConfig = Field(..., description="策略配置")
    backtest_period: Dict[str, str] = Field(..., description="回测期间")
    benchmark: Optional[str] = Field(None, description="基准指数")
    commission_rate: float = Field(default=0.0003, description="佣金费率")
    slippage: float = Field(default=0.001, description="滑点")
    initial_capital: float = Field(..., description="初始资金")


class StrategyComparisonResult(BaseModel):
    """策略比较结果"""
    compared_strategies: List[str] = Field(..., description="比较的策略")
    comparison_metrics: Dict[str, Dict[str, float]] = Field(..., description="比较指标")
    ranking: Dict[str, int] = Field(..., description="排名")
    recommendations: List[str] = Field(..., description="推荐建议")
    comparison_date: datetime = Field(default_factory=datetime.now, description="比较日期")
