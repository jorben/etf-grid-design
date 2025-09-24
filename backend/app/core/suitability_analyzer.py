"""
适合性分析器模块

基于ETF特征、历史表现和用户风险偏好进行适合性分析
"""

import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta

from ..models.etf_models import ETFBasicInfo, ETFPriceData
from ..models.analysis_models import SuitabilityEvaluation
from ..utils.calculators import calculate_volatility, calculate_returns, calculate_max_drawdown
from ..utils.formatters import format_percentage

logger = logging.getLogger(__name__)


class SuitabilityAnalyzer:
    """适合性分析器"""
    
    def __init__(self):
        """初始化适合性分析器"""
        # 风险等级权重配置
        self.risk_weights = {
            'low': {'volatility': 0.4, 'drawdown': 0.3, 'returns': 0.2, 'liquidity': 0.1},
            'medium': {'volatility': 0.3, 'drawdown': 0.25, 'returns': 0.3, 'liquidity': 0.15},
            'high': {'volatility': 0.2, 'drawdown': 0.2, 'returns': 0.4, 'liquidity': 0.2}
        }
        
        # 评分标准
        self.scoring_criteria = {
            'volatility': {
                'excellent': (0, 0.1),      # 年化波动率 < 10%
                'good': (0.1, 0.2),         # 10% - 20%
                'fair': (0.2, 0.3),         # 20% - 30%
                'poor': (0.3, float('inf')) # > 30%
            },
            'returns': {
                'excellent': (0.15, float('inf')),  # 年化收益率 > 15%
                'good': (0.08, 0.15),               # 8% - 15%
                'fair': (0.03, 0.08),               # 3% - 8%
                'poor': (float('-inf'), 0.03)      # < 3%
            },
            'drawdown': {
                'excellent': (0, 0.05),     # 最大回撤 < 5%
                'good': (0.05, 0.15),       # 5% - 15%
                'fair': (0.15, 0.25),       # 15% - 25%
                'poor': (0.25, float('inf')) # > 25%
            },
            'liquidity': {
                'excellent': (100000000, float('inf')),  # 日均成交额 > 1亿
                'good': (50000000, 100000000),           # 5000万 - 1亿
                'fair': (10000000, 50000000),            # 1000万 - 5000万
                'poor': (0, 10000000)                    # < 1000万
            }
        }
        
        # 评分映射
        self.score_mapping = {
            'excellent': 100,
            'good': 80,
            'fair': 60,
            'poor': 40
        }
    
    def analyze(self, etf_code: str, basic_info: ETFBasicInfo, 
                historical_data: List[ETFPriceData], investment_amount: float,
                risk_tolerance: str) -> SuitabilityEvaluation:
        """
        进行适合性分析
        
        Args:
            etf_code: ETF代码
            basic_info: ETF基本信息
            historical_data: 历史价格数据
            investment_amount: 投资金额
            risk_tolerance: 风险承受能力
            
        Returns:
            SuitabilityEvaluation: 适合性分析结果
        """
        try:
            # 计算各项指标
            metrics = self._calculate_metrics(historical_data)
            
            # 计算各项评分
            scores = self._calculate_scores(metrics)
            
            # 计算综合适合性评分
            suitability_score = self._calculate_suitability_score(scores, risk_tolerance)
            
            # 判断是否适合
            is_suitable = suitability_score >= 60
            
            # 生成风险等级
            risk_level = self._determine_risk_level(metrics)
            
            # 生成投资建议
            recommendation = self._generate_recommendation(
                scores, metrics, risk_tolerance, investment_amount, is_suitable
            )
            
            # 生成详细分析
            detailed_analysis = self._generate_detailed_analysis(
                basic_info, metrics, scores, risk_tolerance
            )
            
            # 根据适合性评分确定等级和颜色
            if suitability_score >= 80:
                level = "非常适合"
                color = "green"
            elif suitability_score >= 60:
                level = "基本适合"
                color = "yellow"
            else:
                level = "不适合"
                color = "red"
            
            return SuitabilityEvaluation(
                total_score=round(suitability_score, 2),
                amplitude_score=scores.get('returns', 0),
                volatility_score=scores.get('volatility', 0),
                market_score=scores.get('drawdown', 0),
                liquidity_score=scores.get('liquidity', 0),
                data_quality_score=min(100, metrics.get('data_points', 0) * 2),  # 数据质量评分
                level=level,
                color=color,
                description=f"综合评分{suitability_score:.1f}分，{level}网格交易",
                recommendation=recommendation,
                details=detailed_analysis
            )
            
        except Exception as e:
            logger.error(f"适合性分析失败 {etf_code}: {e}")
            # 返回默认的分析结果
            return SuitabilityEvaluation(
                total_score=0,
                amplitude_score=0,
                volatility_score=0,
                market_score=0,
                liquidity_score=0,
                data_quality_score=0,
                level="不适合",
                color="red",
                description="分析失败",
                recommendation="分析失败，请稍后重试",
                details={"error": str(e)}
            )
    
    def _calculate_metrics(self, historical_data: List[ETFPriceData]) -> Dict[str, float]:
        """
        计算各项指标
        
        Args:
            historical_data: 历史价格数据
            
        Returns:
            dict: 各项指标
        """
        if not historical_data:
            return {}
        
        # 提取价格数据并转换为pandas Series
        import pandas as pd
        prices = [data.close_price for data in historical_data]
        volumes = [data.volume for data in historical_data]
        amounts = [data.amount for data in historical_data]
        
        # 转换为pandas Series
        price_series = pd.Series(prices)
        
        # 计算收益率
        returns = calculate_returns(price_series)
        
        # 计算年化收益率
        if len(returns) > 0:
            total_return = (prices[-1] / prices[0]) - 1
            days = len(historical_data)
            annualized_return = (1 + total_return) ** (252 / days) - 1
        else:
            annualized_return = 0
        
        # 计算年化波动率
        volatility = calculate_volatility(price_series)
        
        # 计算最大回撤
        max_drawdown = calculate_max_drawdown(price_series)
        
        # 计算平均流动性
        avg_amount = sum(amounts) / len(amounts) if amounts else 0
        
        # 计算夏普比率（假设无风险利率为3%）
        risk_free_rate = 0.03
        if volatility > 0:
            sharpe_ratio = (annualized_return - risk_free_rate) / volatility
        else:
            sharpe_ratio = 0
        
        return {
            'annualized_return': annualized_return,
            'volatility': volatility,
            'max_drawdown': abs(max_drawdown),
            'avg_daily_amount': avg_amount,
            'sharpe_ratio': sharpe_ratio,
            'data_points': len(historical_data)
        }
    
    def _calculate_scores(self, metrics: Dict[str, float]) -> Dict[str, int]:
        """
        计算各项评分
        
        Args:
            metrics: 各项指标
            
        Returns:
            dict: 各项评分
        """
        scores = {}
        
        for metric_name, value in metrics.items():
            if metric_name in self.scoring_criteria:
                criteria = self.scoring_criteria[metric_name]
                
                for level, (min_val, max_val) in criteria.items():
                    if min_val <= value < max_val:
                        scores[metric_name] = self.score_mapping[level]
                        break
                else:
                    scores[metric_name] = self.score_mapping['poor']
        
        return scores
    
    def _calculate_suitability_score(self, scores: Dict[str, int], 
                                   risk_tolerance: str) -> float:
        """
        计算综合适合性评分
        
        Args:
            scores: 各项评分
            risk_tolerance: 风险承受能力
            
        Returns:
            float: 综合适合性评分
        """
        if risk_tolerance not in self.risk_weights:
            risk_tolerance = 'medium'
        
        weights = self.risk_weights[risk_tolerance]
        weighted_score = 0
        total_weight = 0
        
        for metric, weight in weights.items():
            if metric in scores:
                weighted_score += scores[metric] * weight
                total_weight += weight
        
        if total_weight > 0:
            return weighted_score / total_weight
        else:
            return 0
    
    def _determine_risk_level(self, metrics: Dict[str, float]) -> str:
        """
        确定风险等级
        
        Args:
            metrics: 各项指标
            
        Returns:
            str: 风险等级
        """
        volatility = metrics.get('volatility', 0)
        max_drawdown = metrics.get('max_drawdown', 0)
        
        # 基于波动率和最大回撤确定风险等级
        if volatility < 0.15 and max_drawdown < 0.1:
            return "低风险"
        elif volatility < 0.25 and max_drawdown < 0.2:
            return "中等风险"
        elif volatility < 0.35 and max_drawdown < 0.3:
            return "中高风险"
        else:
            return "高风险"
    
    def _generate_recommendation(self, scores: Dict[str, int], metrics: Dict[str, float],
                               risk_tolerance: str, investment_amount: float,
                               is_suitable: bool) -> str:
        """
        生成投资建议
        
        Args:
            scores: 各项评分
            metrics: 各项指标
            risk_tolerance: 风险承受能力
            investment_amount: 投资金额
            is_suitable: 是否适合
            
        Returns:
            str: 投资建议
        """
        if not is_suitable:
            return "根据您的风险偏好和该ETF的特征，暂不建议投资此ETF。建议寻找风险收益特征更匹配的产品。"
        
        recommendations = []
        
        # 基于收益率的建议
        returns_score = scores.get('returns', 0)
        if returns_score >= 80:
            recommendations.append("该ETF历史收益表现优秀")
        elif returns_score >= 60:
            recommendations.append("该ETF历史收益表现良好")
        else:
            recommendations.append("该ETF历史收益表现一般，建议关注未来趋势")
        
        # 基于风险的建议
        volatility_score = scores.get('volatility', 0)
        if volatility_score >= 80:
            recommendations.append("波动率较低，适合稳健投资")
        elif volatility_score >= 60:
            recommendations.append("波动率适中，风险可控")
        else:
            recommendations.append("波动率较高，需要较强的风险承受能力")
        
        # 基于流动性的建议
        liquidity_score = scores.get('liquidity', 0)
        if liquidity_score < 60:
            recommendations.append("流动性一般，建议适量配置")
        
        # 基于投资金额的建议
        if investment_amount < 5000:
            recommendations.append("投资金额较小，建议定投方式分批建仓")
        elif investment_amount > 100000:
            recommendations.append("投资金额较大，建议分散投资降低风险")
        
        return "；".join(recommendations) + "。"
    
    def _generate_detailed_analysis(self, basic_info, 
                                  metrics: Dict[str, float], scores: Dict[str, int],
                                  risk_tolerance: str) -> Dict[str, Any]:
        """
        生成详细分析
        
        Args:
            basic_info: ETF基本信息 (可能是对象或字典)
            metrics: 各项指标
            scores: 各项评分
            risk_tolerance: 风险承受能力
            
        Returns:
            dict: 详细分析结果
        """
        # 处理basic_info可能是字典或对象的情况
        if isinstance(basic_info, dict):
            name = basic_info.get('name', '')
            fund_type = basic_info.get('fund_type', '')
            management = basic_info.get('management', '')
            m_fee = basic_info.get('management_fee', 0)
            c_fee = basic_info.get('custodian_fee', 0)
        else:
            name = getattr(basic_info, 'name', '')
            fund_type = getattr(basic_info, 'fund_type', '')
            management = getattr(basic_info, 'management', '')
            m_fee = getattr(basic_info, 'm_fee', 0)
            c_fee = getattr(basic_info, 'c_fee', 0)
        
        return {
            'basic_info': {
                'name': name,
                'fund_type': fund_type,
                'management': management,
                'management_fee': f"{m_fee}%" if m_fee else "N/A",
                'custodian_fee': f"{c_fee}%" if c_fee else "N/A"
            },
            'performance_metrics': {
                'annualized_return': format_percentage(metrics.get('annualized_return', 0)),
                'volatility': format_percentage(metrics.get('volatility', 0)),
                'max_drawdown': format_percentage(metrics.get('max_drawdown', 0)),
                'sharpe_ratio': round(metrics.get('sharpe_ratio', 0), 2),
                'avg_daily_amount': f"{metrics.get('avg_daily_amount', 0):,.0f}万元"
            },
            'score_breakdown': {
                'returns_score': scores.get('returns', 0),
                'volatility_score': scores.get('volatility', 0),
                'drawdown_score': scores.get('drawdown', 0),
                'liquidity_score': scores.get('liquidity', 0)
            },
            'risk_assessment': {
                'user_risk_tolerance': risk_tolerance,
                'etf_risk_level': self._determine_risk_level(metrics),
                'risk_match': self._assess_risk_match(risk_tolerance, metrics)
            },
            'data_quality': {
                'data_points': metrics.get('data_points', 0),
                'data_sufficiency': "充足" if metrics.get('data_points', 0) >= 60 else "不足"
            }
        }
    
    def _assess_risk_match(self, risk_tolerance: str, metrics: Dict[str, float]) -> str:
        """
        评估风险匹配度
        
        Args:
            risk_tolerance: 用户风险承受能力
            metrics: ETF指标
            
        Returns:
            str: 风险匹配度评估
        """
        volatility = metrics.get('volatility', 0)
        
        if risk_tolerance == 'low':
            if volatility < 0.15:
                return "高度匹配"
            elif volatility < 0.25:
                return "基本匹配"
            else:
                return "不匹配"
        elif risk_tolerance == 'medium':
            if volatility < 0.3:
                return "高度匹配"
            elif volatility < 0.4:
                return "基本匹配"
            else:
                return "不匹配"
        else:  # high
            if volatility > 0.2:
                return "高度匹配"
            elif volatility > 0.15:
                return "基本匹配"
            else:
                return "保守匹配"
