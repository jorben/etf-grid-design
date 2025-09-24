"""
分析结果模型
定义分析相关的数据结构和结果模型
"""

from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from pydantic import BaseModel, Field
from .etf import ETFBasicInfo


class EvaluationResult(BaseModel):
    """评估结果基类"""
    score: int = Field(..., ge=0, description="得分")
    max_score: int = Field(..., ge=0, description="满分")
    level: str = Field(..., description="等级")
    description: str = Field(..., description="描述")
    details: str = Field(..., description="详细说明")


class AmplitudeEvaluation(EvaluationResult):
    """振幅评估结果"""
    atr_ratio: float = Field(..., description="ATR比率")
    atr_pct: float = Field(..., description="ATR百分比")


class VolatilityEvaluation(EvaluationResult):
    """波动率评估结果"""
    volatility: float = Field(..., description="波动率")
    volatility_pct: float = Field(..., description="波动率百分比")


class MarketCharacteristicsEvaluation(EvaluationResult):
    """市场特征评估结果"""
    adx_value: float = Field(..., description="ADX指数")
    market_type: str = Field(..., description="市场类型")


class LiquidityEvaluation(EvaluationResult):
    """流动性评估结果"""
    avg_amount: float = Field(..., description="日均成交额")
    volume_stability: float = Field(..., description="成交量稳定性")


class DataQualityEvaluation(BaseModel):
    """数据质量评估结果"""
    freshness: str = Field(..., description="数据新鲜度")
    freshness_desc: str = Field(..., description="新鲜度描述")
    completeness: str = Field(..., description="数据完整性")
    completeness_desc: str = Field(..., description="完整性描述")
    latest_date: str = Field(..., description="最新日期")
    start_date: str = Field(..., description="开始日期")
    analysis_days: int = Field(..., description="分析天数")
    total_records: int = Field(..., description="总记录数")
    missing_rate: float = Field(..., description="缺失率")
    days_since_update: int = Field(..., description="距离更新天数")


class SuitabilityEvaluation(BaseModel):
    """适宜度综合评估结果"""
    total_score: int = Field(..., ge=0, le=100, description="总分")
    max_total_score: int = Field(default=100, description="总分满分")
    conclusion: str = Field(..., description="结论")
    recommendation: str = Field(..., description="建议")
    risk_level: str = Field(..., description="风险等级")
    has_fatal_flaw: bool = Field(..., description="是否存在致命缺陷")
    fatal_flaws: List[str] = Field(..., description="致命缺陷列表")
    
    evaluations: Dict[str, EvaluationResult] = Field(..., description="各维度评估结果")
    data_quality: DataQualityEvaluation = Field(..., description="数据质量评估")
    atr_analysis: Dict = Field(..., description="ATR分析结果")
    market_indicators: Dict = Field(..., description="市场指标")


class GridFundAllocation(BaseModel):
    """网格资金分配详情"""
    level: int = Field(..., ge=1, description="网格层级")
    price: float = Field(..., gt=0, description="价格")
    allocated_fund: float = Field(..., ge=0, description="分配资金")
    shares: int = Field(..., ge=0, description="股数")
    actual_fund: float = Field(..., ge=0, description="实际资金")
    is_buy_level: bool = Field(..., description="是否为买入层级")


class GridFundAllocationResult(BaseModel):
    """网格资金分配结果"""
    base_position_amount: float = Field(..., ge=0, description="底仓金额")
    grid_trading_amount: float = Field(..., ge=0, description="网格交易金额")
    reserve_amount: float = Field(..., ge=0, description="预留资金")
    grid_funds: List[GridFundAllocation] = Field(..., description="网格资金分配")
    total_buy_grid_fund: float = Field(..., ge=0, description="总买入网格资金")
    grid_fund_utilization_rate: float = Field(..., ge=0, le=1, description="网格资金利用率")
    expected_profit_per_trade: float = Field(..., description="预期单笔收益")
    grid_count: int = Field(..., ge=0, description="网格数量")
    base_position_ratio: float = Field(..., ge=0, le=1, description="底仓比例")
    single_trade_quantity: int = Field(..., ge=0, description="单笔交易数量")
    buy_grid_fund: float = Field(..., ge=0, description="买入网格资金")
    buy_grid_safety_ratio: float = Field(..., ge=0, description="买入网格安全比率")
    extreme_case_safe: bool = Field(..., description="极端情况是否安全")


class GridStrategyParameters(BaseModel):
    """网格策略参数"""
    current_price: float = Field(..., gt=0, description="当前价格")
    
    price_range: Dict[str, float] = Field(..., description="价格区间")
    grid_config: Dict[str, Any] = Field(..., description="网格配置")
    price_levels: List[float] = Field(..., description="价格水平")
    fund_allocation: GridFundAllocationResult = Field(..., description="资金分配")
    
    risk_preference: str = Field(..., description="风险偏好")
    atr_based: bool = Field(..., description="是否基于ATR")
    atr_score: int = Field(..., ge=0, le=100, description="ATR评分")
    atr_description: str = Field(..., description="ATR描述")
    
    calculation_method: str = Field(..., description="计算方法")
    calculation_logic: Dict[str, str] = Field(..., description="计算逻辑")


class StrategyRationale(BaseModel):
    """策略逻辑说明"""
    rationale_type: str = Field(..., description="逻辑类型")
    title: str = Field(..., description="标题")
    description: str = Field(..., description="描述")
    supporting_data: Dict[str, Any] = Field(..., description="支持数据")
    confidence_level: str = Field(..., description="置信度")


class ETFAnalysisResult(BaseModel):
    """ETF分析结果"""
    etf_info: ETFBasicInfo = Field(..., description="ETF信息")
    analysis_input: Dict = Field(..., description="分析输入参数")
    suitability_evaluation: SuitabilityEvaluation = Field(..., description="适宜度评估")
    grid_strategy: GridStrategyParameters = Field(..., description="网格策略参数")
    strategy_rationales: List[StrategyRationale] = Field(..., description="策略逻辑说明")
    
    analysis_timestamp: datetime = Field(default_factory=datetime.now, description="分析时间")
    analysis_duration: float = Field(..., ge=0, description="分析耗时（秒）")
    data_source: str = Field(..., description="数据来源")
    version: str = Field(default="1.0", description="分析版本")


class AnalysisSummary(BaseModel):
    """分析摘要"""
    etf_code: str = Field(..., description="ETF代码")
    total_score: int = Field(..., description="总分")
    conclusion: str = Field(..., description="结论")
    recommendation: str = Field(..., description="建议")
    risk_level: str = Field(..., description="风险等级")
    grid_count: int = Field(..., description="网格数量")
    base_position_ratio: float = Field(..., description="底仓比例")
    expected_profit_per_trade: float = Field(..., description="预期单笔收益")
    analysis_date: str = Field(..., description="分析日期")


class PerformanceAnalysis(BaseModel):
    """性能分析结果"""
    analysis_id: str = Field(..., description="分析ID")
    etf_code: str = Field(..., description="ETF代码")
    performance_metrics: Dict[str, float] = Field(..., description="性能指标")
    benchmark_comparison: Dict[str, float] = Field(..., description="基准比较")
    risk_metrics: Dict[str, float] = Field(..., description="风险指标")
    optimization_suggestions: List[str] = Field(..., description="优化建议")


class BacktestResult(BaseModel):
    """回测结果"""
    strategy_name: str = Field(..., description="策略名称")
    etf_code: str = Field(..., description="ETF代码")
    backtest_period: Tuple[str, str] = Field(..., description="回测期间")
    total_return: float = Field(..., description="总收益率")
    annual_return: float = Field(..., description="年化收益率")
    max_drawdown: float = Field(..., description="最大回撤")
    sharpe_ratio: float = Field(..., description="夏普比率")
    win_rate: float = Field(..., description="胜率")
    profit_factor: float = Field(..., description="盈利因子")
    total_trades: int = Field(..., description="总交易次数")
    backtest_details: Dict[str, Any] = Field(..., description="回测详情")
