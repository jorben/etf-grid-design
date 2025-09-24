"""
ETF数据模型
定义ETF相关的数据结构和领域模型
"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ETFBasicInfo(BaseModel):
    """ETF基础信息模型"""
    code: str = Field(..., description="ETF代码")
    name: str = Field(..., description="ETF名称")
    management_company: str = Field(..., description="基金管理公司")
    current_price: float = Field(..., description="当前价格")
    change_pct: float = Field(..., description="涨跌幅")
    volume: float = Field(..., description="成交量")
    amount: float = Field(..., description="成交额")
    setup_date: str = Field(..., description="成立日期")
    list_date: str = Field(..., description="上市日期")
    fund_type: str = Field(default="ETF", description="基金类型")
    status: str = Field(default="L", description="状态")
    trade_date: str = Field(..., description="交易日期")
    data_age_days: int = Field(..., description="数据时效性（天数）")


class ETFPriceData(BaseModel):
    """ETF价格数据模型"""
    date: str = Field(..., description="日期")
    open: float = Field(..., description="开盘价")
    high: float = Field(..., description="最高价")
    low: float = Field(..., description="最低价")
    close: float = Field(..., description="收盘价")
    volume: float = Field(..., description="成交量")
    amount: float = Field(..., description="成交额")


class ETFHistoricalData(BaseModel):
    """ETF历史数据模型"""
    etf_code: str = Field(..., description="ETF代码")
    data: List[ETFPriceData] = Field(..., description="价格数据列表")
    start_date: str = Field(..., description="开始日期")
    end_date: str = Field(..., description="结束日期")
    total_days: int = Field(..., description="总天数")


class ETFMarketData(BaseModel):
    """ETF市场数据模型"""
    etf_code: str = Field(..., description="ETF代码")
    timestamp: datetime = Field(default_factory=datetime.now, description="时间戳")
    price_data: ETFPriceData = Field(..., description="价格数据")
    market_cap: Optional[float] = Field(None, description="市值")
    pe_ratio: Optional[float] = Field(None, description="市盈率")
    pb_ratio: Optional[float] = Field(None, description="市净率")
    dividend_yield: Optional[float] = Field(None, description="股息率")


class ETFPortfolioHolding(BaseModel):
    """ETF持仓成分模型"""
    stock_code: str = Field(..., description="股票代码")
    stock_name: str = Field(..., description="股票名称")
    weight: float = Field(..., description="权重")
    shares: float = Field(..., description="持股数量")
    market_value: float = Field(..., description="市值")


class ETFPortfolio(BaseModel):
    """ETF投资组合模型"""
    etf_code: str = Field(..., description="ETF代码")
    report_date: str = Field(..., description="报告日期")
    total_assets: float = Field(..., description="总资产")
    total_shares: float = Field(..., description="总份额")
    holdings: List[ETFPortfolioHolding] = Field(..., description="持仓列表")
    top_10_weight: float = Field(..., description="前十大权重")
    industry_distribution: Dict[str, float] = Field(..., description="行业分布")


class ETFAnalysisInput(BaseModel):
    """ETF分析输入参数模型"""
    etf_code: str = Field(..., description="ETF代码")
    total_capital: float = Field(..., gt=0, description="总投资资金")
    grid_type: str = Field(..., regex="^(等差|等比)$", description="网格类型")
    risk_preference: str = Field(..., regex="^(保守|稳健|激进)$", description="风险偏好")
    analysis_days: int = Field(default=365, ge=30, le=1000, description="分析天数")


class ETFPerformanceMetrics(BaseModel):
    """ETF绩效指标模型"""
    etf_code: str = Field(..., description="ETF代码")
    period: str = Field(..., description="统计周期")
    total_return: float = Field(..., description="总收益率")
    annual_return: float = Field(..., description="年化收益率")
    volatility: float = Field(..., description="波动率")
    sharpe_ratio: Optional[float] = Field(None, description="夏普比率")
    max_drawdown: float = Field(..., description="最大回撤")
    calmar_ratio: Optional[float] = Field(None, description="卡玛比率")
    tracking_error: Optional[float] = Field(None, description="跟踪误差")
    information_ratio: Optional[float] = Field(None, description="信息比率")


class ETFComparisonResult(BaseModel):
    """ETF比较结果模型"""
    etf_codes: List[str] = Field(..., description="比较的ETF代码列表")
    comparison_date: str = Field(..., description="比较日期")
    metrics_comparison: Dict[str, Dict[str, float]] = Field(..., description="指标比较")
    ranking: Dict[str, int] = Field(..., description="排名结果")
    recommendations: List[str] = Field(..., description="推荐建议")


class ETFSearchCriteria(BaseModel):
    """ETF搜索条件模型"""
    keywords: Optional[str] = Field(None, description="关键词")
    fund_type: Optional[str] = Field(None, description="基金类型")
    management_company: Optional[str] = Field(None, description="管理公司")
    min_assets: Optional[float] = Field(None, description="最小资产规模")
    max_assets: Optional[float] = Field(None, description="最大资产规模")
    min_dividend_yield: Optional[float] = Field(None, description="最小股息率")
    max_dividend_yield: Optional[float] = Field(None, description="最大股息率")
    sort_by: str = Field(default="volume", description="排序字段")
    sort_order: str = Field(default="desc", regex="^(asc|desc)$", description="排序方向")


class ETFSearchResult(BaseModel):
    """ETF搜索结果模型"""
    criteria: ETFSearchCriteria = Field(..., description="搜索条件")
    total_count: int = Field(..., description="总数量")
    results: List[ETFBasicInfo] = Field(..., description="搜索结果")
    search_time: datetime = Field(default_factory=datetime.now, description="搜索时间")
