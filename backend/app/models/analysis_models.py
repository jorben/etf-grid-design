"""
分析结果相关数据模型
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime

@dataclass
class ATRAnalysis:
    """ATR分析结果模型"""
    current_atr: float
    atr_ratio: float
    atr_score: int
    atr_level: str
    price_range: Dict[str, float]  # {'lower': float, 'upper': float}
    volatility: float
    adx_value: Optional[float] = None
    
    def __post_init__(self):
        """数据验证"""
        if self.atr_ratio < 0:
            raise ValueError("ATR比率不能为负数")
        if not 0 <= self.atr_score <= 100:
            raise ValueError("ATR评分必须在0-100之间")

@dataclass
class SuitabilityEvaluation:
    """适宜性评估结果模型"""
    total_score: float
    amplitude_score: int
    volatility_score: int
    market_score: int
    liquidity_score: int
    data_quality_score: int
    level: str  # '非常适合', '基本适合', '不适合'
    color: str  # 'green', 'yellow', 'red'
    description: str
    recommendation: str
    details: Dict[str, Any]
    
    @property
    def is_suitable(self) -> bool:
        """是否适合投资"""
        return self.level in ['非常适合', '基本适合']
    
    @property
    def suitability_score(self) -> float:
        """适合性评分（兼容性属性）"""
        return self.total_score
    
    @property
    def risk_level(self) -> str:
        """风险等级（基于评分计算）"""
        if self.total_score >= 80:
            return "低风险"
        elif self.total_score >= 60:
            return "中等风险"
        else:
            return "高风险"
    
    def __post_init__(self):
        """数据验证"""
        if not 0 <= self.total_score <= 100:
            raise ValueError("总评分必须在0-100之间")
        if self.level not in ['非常适合', '基本适合', '不适合']:
            raise ValueError("适宜性等级不正确")

@dataclass
class GridParameters:
    """网格参数模型"""
    grid_count: int
    grid_type: str  # '等差', '等比'
    step_size: float
    step_ratio: float
    price_lower: float
    price_upper: float
    price_levels: List[float]
    base_position_ratio: float
    single_trade_quantity: int
    
    def __post_init__(self):
        """数据验证"""
        if self.grid_count <= 0:
            raise ValueError("网格数量必须大于0")
        if self.grid_type not in ['等差', '等比']:
            raise ValueError("网格类型必须是'等差'或'等比'")
        if self.price_lower >= self.price_upper:
            raise ValueError("价格下限必须小于价格上限")

@dataclass
class FundAllocation:
    """资金分配模型"""
    total_capital: float
    base_position_amount: float
    grid_amount: float
    single_trade_amount: float
    buy_grid_count: int
    buy_grid_amount: float
    grid_utilization_rate: float
    
    def __post_init__(self):
        """数据验证"""
        if self.total_capital <= 0:
            raise ValueError("总资金必须大于0")
        if self.base_position_amount + self.grid_amount > self.total_capital * 1.01:  # 允许1%误差
            raise ValueError("资金分配总额不能超过总资金")

@dataclass
class AnalysisResult:
    """完整分析结果模型"""
    etf_info: Dict[str, Any]
    atr_analysis: ATRAnalysis
    suitability_evaluation: SuitabilityEvaluation
    grid_parameters: GridParameters
    fund_allocation: FundAllocation
    strategy_rationale: str
    adjustment_suggestions: List[str]
    risk_warnings: List[str]
    analysis_timestamp: str
    
    def __post_init__(self):
        """数据验证"""
        if not self.etf_info:
            raise ValueError("ETF信息不能为空")
        if not self.strategy_rationale:
            raise ValueError("策略说明不能为空")

@dataclass
class MarketRegime:
    """市场状态模型"""
    regime: str  # '上升趋势', '下降趋势', '震荡市场'
    confidence: float  # 置信度 0-1
    trend_strength: Optional[float] = None
    volatility_level: Optional[str] = None
    
    def __post_init__(self):
        """数据验证"""
        if self.regime not in ['上升趋势', '下降趋势', '震荡市场']:
            raise ValueError("市场状态不正确")
        if not 0 <= self.confidence <= 1:
            raise ValueError("置信度必须在0-1之间")

@dataclass
class RiskMetrics:
    """风险指标模型"""
    max_drawdown: float
    volatility: float
    sharpe_ratio: Optional[float] = None
    var_95: Optional[float] = None  # 95% VaR
    risk_level: str = "中等风险"
    
    def __post_init__(self):
        """数据验证"""
        if self.volatility < 0:
            raise ValueError("波动率不能为负数")
        if self.max_drawdown > 0:
            raise ValueError("最大回撤应为负数或0")
