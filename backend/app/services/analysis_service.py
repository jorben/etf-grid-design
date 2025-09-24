"""
分析服务模块

提供ETF分析、ATR计算、网格策略等综合分析功能
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta

from ..config.settings import Settings
from ..models.etf_models import ETFPriceData
from ..models.analysis_models import ATRAnalysis, SuitabilityEvaluation, AnalysisResult
from ..models.strategy_models import StrategyConfig, GridLevel
from ..services.etf_service import ETFService
from ..core.atr_engine import ATREngine
from ..core.grid_calculator import GridCalculator
from ..core.suitability_analyzer import SuitabilityAnalyzer
from ..exceptions.business_exceptions import AnalysisError, DataValidationError
from ..utils.validators import validate_etf_code, validate_positive_number
from ..utils.calculators import calculate_volatility, calculate_returns

logger = logging.getLogger(__name__)


class AnalysisService:
    """分析服务"""
    
    def __init__(self, settings: Settings, etf_service: ETFService):
        """
        初始化分析服务
        
        Args:
            settings: 应用配置
            etf_service: ETF服务
        """
        self.settings = settings
        self.etf_service = etf_service
        self.atr_engine = ATREngine()
        self.grid_calculator = GridCalculator()
        self.suitability_analyzer = SuitabilityAnalyzer()
    
    def analyze_etf_suitability(self, etf_code: str, 
                               investment_amount: float = 10000.0,
                               risk_tolerance: str = "medium") -> SuitabilityEvaluation:
        """
        分析ETF适合性
        
        Args:
            etf_code: ETF代码
            investment_amount: 投资金额
            risk_tolerance: 风险承受能力 (low/medium/high)
            
        Returns:
            SuitabilityEvaluation: 适合性分析结果
        """
        if not validate_etf_code(etf_code):
            raise DataValidationError(f"无效的ETF代码: {etf_code}")
        
        if not validate_positive_number(investment_amount):
            raise DataValidationError("投资金额必须为正数")
        
        try:
            # 获取ETF基本信息
            basic_info = self.etf_service.get_etf_basic_info(etf_code)
            if not basic_info:
                raise AnalysisError(f"无法获取ETF基本信息: {etf_code}")
            
            # 获取历史数据用于分析
            end_date = datetime.now().strftime('%Y%m%d')
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
            
            historical_data = self.etf_service.get_etf_historical_data(
                etf_code, start_date, end_date
            )
            
            if not historical_data:
                raise AnalysisError(f"无法获取ETF历史数据: {etf_code}")
            
            # 进行适合性分析
            suitability = self.suitability_analyzer.analyze(
                etf_code=etf_code,
                basic_info=basic_info,
                historical_data=historical_data,
                investment_amount=investment_amount,
                risk_tolerance=risk_tolerance
            )
            
            logger.info(f"ETF适合性分析完成: {etf_code}")
            return suitability
            
        except Exception as e:
            logger.error(f"ETF适合性分析失败 {etf_code}: {e}")
            raise AnalysisError(f"适合性分析失败: {e}")
    
    def calculate_atr_analysis(self, etf_code: str, 
                              period: int = 20) -> ATRAnalysis:
        """
        计算ATR分析
        
        Args:
            etf_code: ETF代码
            period: ATR计算周期
            
        Returns:
            ATRAnalysis: ATR分析结果
        """
        if not validate_etf_code(etf_code):
            raise DataValidationError(f"无效的ETF代码: {etf_code}")
        
        if period <= 0:
            raise DataValidationError("ATR周期必须为正数")
        
        try:
            # 获取足够的历史数据
            end_date = datetime.now().strftime('%Y%m%d')
            start_date = (datetime.now() - timedelta(days=period * 3)).strftime('%Y%m%d')
            
            historical_data = self.etf_service.get_etf_historical_data(
                etf_code, start_date, end_date
            )
            
            if not historical_data or len(historical_data) < period:
                raise AnalysisError(f"历史数据不足，需要至少{period}个交易日的数据")
            
            # 创建指定周期的ATR引擎
            atr_engine = ATREngine(period=period)
            
            # 将ETFPriceData列表转换为DataFrame
            import pandas as pd
            df_data = []
            for data in historical_data:
                df_data.append({
                    'date': data.trade_date,
                    'open': data.open_price,
                    'high': data.high_price,
                    'low': data.low_price,
                    'close': data.close_price,
                    'volume': data.volume
                })
            
            df = pd.DataFrame(df_data)
            
            # 计算ATR - 使用完整的数据处理流程
            processed_df, atr_analysis = atr_engine.process_data(df)
            
            logger.info(f"ATR分析完成: {etf_code}")
            return atr_analysis
            
        except Exception as e:
            logger.error(f"ATR分析失败 {etf_code}: {e}")
            raise AnalysisError(f"ATR分析失败: {e}")
    
    def generate_grid_strategy(self, etf_code: str, 
                              investment_amount: float,
                              grid_count: int = 10,
                              price_range_percent: float = 0.2) -> AnalysisResult:
        """
        生成网格策略
        
        Args:
            etf_code: ETF代码
            investment_amount: 投资金额
            grid_count: 网格数量
            price_range_percent: 价格范围百分比
            
        Returns:
            AnalysisResult: 网格策略分析结果
        """
        if not validate_etf_code(etf_code):
            raise DataValidationError(f"无效的ETF代码: {etf_code}")
        
        if not validate_positive_number(investment_amount):
            raise DataValidationError("投资金额必须为正数")
        
        if grid_count <= 0:
            raise DataValidationError("网格数量必须为正数")
        
        if price_range_percent <= 0 or price_range_percent > 1:
            raise DataValidationError("价格范围百分比必须在0-1之间")
        
        try:
            # 获取当前价格
            latest_data = self.etf_service.get_etf_latest_data(etf_code)
            if not latest_data:
                raise AnalysisError(f"无法获取ETF最新数据: {etf_code}")
            
            # 获取ATR分析结果
            atr_result = self.calculate_atr_analysis(etf_code)
            
            # 创建网格策略配置对象（临时解决方案）
            class GridConfig:
                def __init__(self):
                    self.etf_code = etf_code
                    self.investment_amount = investment_amount
                    self.grid_count = grid_count
                    self.price_range_percent = price_range_percent
                    self.current_price = latest_data.close_price
                    self.atr_value = atr_result['current_atr']
                    self.atr_percentage = atr_result['current_atr_pct'] / 100  # 转换为小数
            
            strategy_config = GridConfig()
            
            # 计算网格策略
            grid_result = self.grid_calculator.calculate_grid_strategy(
                strategy_config, latest_data, atr_result
            )
            
            logger.info(f"网格策略生成完成: {etf_code}")
            return grid_result
            
        except Exception as e:
            logger.error(f"网格策略生成失败 {etf_code}: {e}")
            raise AnalysisError(f"网格策略生成失败: {e}")
    
    def comprehensive_analysis(self, etf_code: str, 
                             investment_amount: float = 10000.0,
                             risk_tolerance: str = "medium",
                             grid_count: int = 10) -> Dict[str, Any]:
        """
        综合分析
        
        Args:
            etf_code: ETF代码
            investment_amount: 投资金额
            risk_tolerance: 风险承受能力
            grid_count: 网格数量
            
        Returns:
            dict: 综合分析结果
        """
        try:
            # 获取ETF基本信息
            etf_summary = self.etf_service.get_etf_summary(etf_code)
            
            # 适合性分析
            suitability = self.analyze_etf_suitability(
                etf_code, investment_amount, risk_tolerance
            )
            
            # ATR分析
            atr_analysis = self.calculate_atr_analysis(etf_code)
            
            # 网格策略分析 - 无论适合性如何都生成网格分析
            grid_analysis = None
            try:
                grid_analysis = self.generate_grid_strategy(
                    etf_code, investment_amount, grid_count
                )
                logger.info(f"网格策略生成成功: {etf_code}")
            except Exception as e:
                logger.warning(f"网格策略生成失败: {e}")
            
            # 组装综合结果
            comprehensive_result = {
                'etf_info': etf_summary,
                'suitability_analysis': suitability.__dict__ if hasattr(suitability, '__dict__') else suitability,
                'atr_analysis': atr_analysis.__dict__ if hasattr(atr_analysis, '__dict__') else atr_analysis,
                'grid_analysis': grid_analysis.__dict__ if grid_analysis and hasattr(grid_analysis, '__dict__') else grid_analysis,
                'analysis_timestamp': datetime.now().isoformat(),
                'parameters': {
                    'investment_amount': investment_amount,
                    'risk_tolerance': risk_tolerance,
                    'grid_count': grid_count
                }
            }
            
            logger.info(f"综合分析完成: {etf_code}")
            return comprehensive_result
            
        except Exception as e:
            logger.error(f"综合分析失败 {etf_code}: {e}")
            raise AnalysisError(f"综合分析失败: {e}")
    
    def batch_analyze_popular_etfs(self, investment_amount: float = 10000.0,
                                  risk_tolerance: str = "medium") -> List[Dict[str, Any]]:
        """
        批量分析热门ETF
        
        Args:
            investment_amount: 投资金额
            risk_tolerance: 风险承受能力
            
        Returns:
            List[dict]: 批量分析结果
        """
        try:
            # 获取热门ETF列表
            popular_etfs = self.etf_service.get_popular_etfs()
            
            results = []
            for etf in popular_etfs:
                try:
                    # 进行适合性分析
                    suitability = self.analyze_etf_suitability(
                        etf.code, investment_amount, risk_tolerance
                    )
                    
                    # 获取基本信息
                    latest_data = self.etf_service.get_etf_latest_data(etf.code)
                    
                    result = {
                        'etf_code': etf.code,
                        'etf_name': etf.name,
                        'category': etf.category,
                        'is_suitable': suitability.is_suitable,
                        'suitability_score': suitability.suitability_score,
                        'risk_level': suitability.risk_level,
                        'current_price': latest_data.close_price if latest_data else 0,
                        'change_percent': latest_data.pct_change if latest_data else 0,
                        'recommendation': suitability.recommendation
                    }
                    results.append(result)
                    
                except Exception as e:
                    logger.warning(f"分析ETF {etf.code} 失败: {e}")
                    # 添加错误记录
                    results.append({
                        'etf_code': etf.code,
                        'etf_name': etf.name,
                        'category': etf.category,
                        'error': str(e)
                    })
            
            # 按适合性评分排序
            results.sort(key=lambda x: x.get('suitability_score', 0), reverse=True)
            
            logger.info(f"批量分析完成: {len(results)}个ETF")
            return results
            
        except Exception as e:
            logger.error(f"批量分析失败: {e}")
            raise AnalysisError(f"批量分析失败: {e}")
    
    def get_market_overview(self) -> Dict[str, Any]:
        """
        获取市场概览
        
        Returns:
            dict: 市场概览数据
        """
        try:
            # 获取热门ETF的最新数据
            popular_etfs = self.etf_service.get_popular_etfs()
            
            market_data = []
            total_change = 0
            positive_count = 0
            
            for etf in popular_etfs[:10]:  # 取前10个
                try:
                    latest_data = self.etf_service.get_etf_latest_data(etf.code)
                    if latest_data:
                        market_data.append({
                            'code': etf.code,
                            'name': etf.name,
                            'price': latest_data.close_price,
                            'change': latest_data.pct_change,
                            'change_percent': latest_data.pct_change,
                            'volume': latest_data.volume
                        })
                        
                        total_change += latest_data.pct_change if latest_data.pct_change else 0
                        if latest_data.pct_change and latest_data.pct_change > 0:
                            positive_count += 1
                            
                except Exception as e:
                    logger.warning(f"获取ETF {etf.code} 数据失败: {e}")
            
            # 计算市场统计
            market_stats = {
                'total_etfs': len(market_data),
                'average_change': total_change / len(market_data) if market_data else 0,
                'positive_ratio': positive_count / len(market_data) if market_data else 0,
                'market_sentiment': self._get_market_sentiment(total_change / len(market_data) if market_data else 0)
            }
            
            overview = {
                'market_data': market_data,
                'market_stats': market_stats,
                'update_time': datetime.now().isoformat()
            }
            
            logger.info("市场概览获取完成")
            return overview
            
        except Exception as e:
            logger.error(f"获取市场概览失败: {e}")
            return {
                'market_data': [],
                'market_stats': {},
                'error': str(e),
                'update_time': datetime.now().isoformat()
            }
    
    def _get_market_sentiment(self, average_change: float) -> str:
        """
        根据平均涨跌幅判断市场情绪
        
        Args:
            average_change: 平均涨跌幅
            
        Returns:
            str: 市场情绪描述
        """
        if average_change > 2:
            return "强烈乐观"
        elif average_change > 1:
            return "乐观"
        elif average_change > 0:
            return "谨慎乐观"
        elif average_change > -1:
            return "谨慎悲观"
        elif average_change > -2:
            return "悲观"
        else:
            return "强烈悲观"
