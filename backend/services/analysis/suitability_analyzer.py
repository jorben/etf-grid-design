"""
标的适宜度评估模块
实现4维度量化评分体系（总分100分）
重构后的服务层，使用算法模块进行计算
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import logging
from algorithms.atr.analyzer import ATRAnalyzer
from algorithms.atr.calculator import ATRCalculator, calculate_volatility, calculate_adx

logger = logging.getLogger(__name__)

class SuitabilityAnalyzer:
    """标的适宜度评估器"""
    
    def __init__(self, atr_analyzer: ATRAnalyzer = None):
        """
        初始化评估器
        
        Args:
            atr_analyzer: ATR分析器实例
        """
        self.atr_analyzer = atr_analyzer or ATRAnalyzer(ATRCalculator())
        
    def evaluate_amplitude(self, atr_ratio: float) -> Dict:
        """
        振幅评估（35分）- 基于ATR算法
        
        Args:
            atr_ratio: ATR比率
            
        Returns:
            振幅评估结果
        """
        try:
            atr_pct = atr_ratio * 100
            
            if atr_pct >= 2.0:
                score = 35
                level = "优秀"
                description = "振幅充足，交易机会丰富"
            elif atr_pct >= 1.5:
                score = 25
                level = "良好"
                description = "振幅适中，基本适合"
            else:
                score = 0
                level = "不足"
                description = "振幅不足，不推荐"
            
            return {
                'score': score,
                'max_score': 35,
                'level': level,
                'description': description,
                'atr_ratio': atr_ratio,
                'atr_pct': atr_pct,
                'details': f"ATR比率: {atr_pct:.2f}%"
            }
            
        except Exception as e:
            logger.error(f"振幅评估失败: {str(e)}")
            return self._get_error_result(35, "振幅评估")
    
    def evaluate_volatility(self, volatility: float) -> Dict:
        """
        波动率评估（30分）
        
        Args:
            volatility: 年化历史波动率
            
        Returns:
            波动率评估结果
        """
        try:
            vol_pct = volatility * 100
            
            if 15 <= vol_pct <= 45:
                score = 30
                level = "理想"
                description = "理想区间，风险收益平衡"
            elif vol_pct < 15:
                score = 18
                level = "偏低"
                description = "波动偏低，收益有限"
            else:  # vol_pct > 45
                score = 12
                level = "偏高"
                description = "剧烈波动，风险较高"
            
            return {
                'score': score,
                'max_score': 30,
                'level': level,
                'description': description,
                'volatility': volatility,
                'volatility_pct': vol_pct,
                'details': f"年化波动率: {vol_pct:.1f}%"
            }
            
        except Exception as e:
            logger.error(f"波动率评估失败: {str(e)}")
            return self._get_error_result(30, "波动率评估")
    
    def evaluate_market_characteristics(self, adx_value: float) -> Dict:
        """
        市场特征评估（25分）
        基于ADX指数判断趋势/震荡特征
        
        Args:
            adx_value: ADX指数值
            
        Returns:
            市场特征评估结果
        """
        try:
            if adx_value < 20:
                score = 25
                level = "震荡市"
                description = "非常适合网格交易"
                market_type = "震荡"
            elif adx_value < 40:
                score = 18
                level = "弱趋势"
                description = "可以进行，需注意风险"
                market_type = "弱趋势"
            else:
                score = 6
                level = "强趋势"
                description = "不推荐，风险较高"
                market_type = "强趋势"
            
            return {
                'score': score,
                'max_score': 25,
                'level': level,
                'description': description,
                'adx_value': adx_value,
                'market_type': market_type,
                'details': f"ADX指数: {adx_value:.1f}，当前处于{market_type}状态"
            }
            
        except Exception as e:
            logger.error(f"市场特征评估失败: {str(e)}")
            return self._get_error_result(25, "市场特征评估")
    
    def evaluate_liquidity(self, avg_amount: float, volume_stability: float) -> Dict:
        """
        流动性评估（10分）
        基于日均成交额和成交量稳定性
        
        Args:
            avg_amount: 日均成交额（万元）
            volume_stability: 成交量稳定性（变异系数）
            
        Returns:
            流动性评估结果
        """
        try:
            # 基础评分（基于成交额）
            if avg_amount >= 10000:  # 1亿元
                base_score = 10
                level = "充足"
                description = "流动性充足"
            elif avg_amount >= 5000:  # 5000万元
                base_score = 6
                level = "尚可"
                description = "流动性尚可"
            elif avg_amount >= 2000:  # 2000万元
                base_score = 3
                level = "一般"
                description = "流动性一般"
            else:
                base_score = 1
                level = "不足"
                description = "流动性不足，不推荐"
            
            # 稳定性调整（变异系数越小越好）
            if volume_stability < 0.3:  # 变异系数小于30%
                stability_bonus = 0
                stability_desc = "成交量稳定"
            elif volume_stability < 0.5:  # 变异系数30%-50%
                stability_bonus = -1
                stability_desc = "成交量较稳定"
            else:  # 变异系数大于50%
                stability_bonus = -2
                stability_desc = "成交量不稳定"
            
            final_score = max(1, base_score + stability_bonus)
            
            return {
                'score': final_score,
                'max_score': 10,
                'level': level,
                'description': f"{description}，{stability_desc}",
                'avg_amount': avg_amount,
                'volume_stability': volume_stability,
                'details': f"日均成交额: {avg_amount:.0f}万元，成交量变异系数: {volume_stability:.2f}"
            }
            
        except Exception as e:
            logger.error(f"流动性评估失败: {str(e)}")
            return self._get_error_result(10, "流动性评估")
    
    def evaluate_data_quality(self, df: pd.DataFrame) -> Dict:
        """
        数据质量评估
        
        Args:
            df: 历史数据DataFrame
            
        Returns:
            数据质量评估结果
        """
        try:
            # 数据时效性检查
            latest_date = pd.to_datetime(df['date'].max())
            current_date = pd.Timestamp.now()
            days_diff = (current_date - latest_date).days
            
            if days_diff <= 1:
                freshness = "优秀"
                freshness_desc = "数据非常新鲜"
            elif days_diff <= 3:
                freshness = "良好"
                freshness_desc = "数据较新"
            else:
                freshness = "需要更新"
                freshness_desc = f"数据已过时{days_diff}天"
            
            # 数据完整性检查
            total_days = len(df)
            missing_rate = df.isnull().sum().sum() / (len(df) * len(df.columns))
            
            if missing_rate < 0.01:
                completeness = "优秀"
                completeness_desc = "数据完整"
            elif missing_rate < 0.05:
                completeness = "良好"
                completeness_desc = "数据基本完整"
            else:
                completeness = "一般"
                completeness_desc = f"数据缺失率: {missing_rate:.2%}"
            
            # 分析时间范围
            start_date = pd.to_datetime(df['date'].min())
            analysis_days = (latest_date - start_date).days
            
            return {
                'freshness': freshness,
                'freshness_desc': freshness_desc,
                'completeness': completeness,
                'completeness_desc': completeness_desc,
                'latest_date': latest_date.strftime('%Y-%m-%d'),
                'start_date': start_date.strftime('%Y-%m-%d'),
                'analysis_days': analysis_days,
                'total_records': total_days,
                'missing_rate': missing_rate,
                'days_since_update': days_diff
            }
            
        except Exception as e:
            logger.error(f"数据质量评估失败: {str(e)}")
            return {
                'freshness': '未知',
                'freshness_desc': '数据质量检查失败',
                'completeness': '未知',
                'completeness_desc': '无法评估数据完整性'
            }
    
    def comprehensive_evaluation(self, df: pd.DataFrame, etf_info: Dict) -> Dict:
        """
        综合适宜度评估
        
        Args:
            df: 历史数据DataFrame
            etf_info: ETF基础信息
            
        Returns:
            综合评估结果
        """
        try:
            # 1. 处理ATR数据（使用算法模块）
            df_processed = self.atr_analyzer.calculator.process_data(df.copy())
            atr_analysis = self.atr_analyzer.get_atr_analysis(df_processed)
            
            # 2. 计算各项指标（使用算法模块）
            volatility = calculate_volatility(df_processed)
            adx_value = calculate_adx(df_processed)
            
            # 计算流动性指标
            # Tushare API返回的amount单位是千元，需要除以10转换为万元
            avg_amount = df['amount'].mean() / 10  # 千元转换为万元
            
            # 成交量稳定性（变异系数）
            volume_stability = df['vol'].std() / df['vol'].mean()  # 变异系数
            
            # 3. 各维度评估
            amplitude_eval = self.evaluate_amplitude(atr_analysis['current_atr_ratio'])
            volatility_eval = self.evaluate_volatility(volatility)
            market_eval = self.evaluate_market_characteristics(adx_value)
            liquidity_eval = self.evaluate_liquidity(avg_amount, volume_stability)
            
            # 4. 数据质量评估
            data_quality = self.evaluate_data_quality(df)
            
            # 5. 计算总分
            total_score = (amplitude_eval['score'] + volatility_eval['score'] + 
                          market_eval['score'] + liquidity_eval['score'])
            
            # 6. 综合结论
            if total_score >= 70:
                conclusion = "非常适合"
                recommendation = "该标的非常适合进行网格交易"
                risk_level = "低"
            elif total_score >= 60:
                conclusion = "基本适合"
                recommendation = "该标的可以进行网格交易，需注意风险控制"
                risk_level = "中"
            else:
                conclusion = "不适合"
                recommendation = "该标的不推荐进行网格交易"
                risk_level = "高"
            
            # 7. 检查致命缺陷
            fatal_flaws = []
            if amplitude_eval['score'] == 0:
                fatal_flaws.append("振幅不足")
            if liquidity_eval['score'] <= 1:
                fatal_flaws.append("流动性严重不足")
            
            has_fatal_flaw = len(fatal_flaws) > 0
            if has_fatal_flaw:
                conclusion = "存在严重缺陷"
                recommendation = f"不推荐：{', '.join(fatal_flaws)}"
                risk_level = "极高"
            
            return {
                'total_score': total_score,
                'max_total_score': 100,
                'conclusion': conclusion,
                'recommendation': recommendation,
                'risk_level': risk_level,
                'has_fatal_flaw': has_fatal_flaw,
                'fatal_flaws': fatal_flaws,
                'evaluations': {
                    'amplitude': amplitude_eval,
                    'volatility': volatility_eval,
                    'market_characteristics': market_eval,
                    'liquidity': liquidity_eval
                },
                'data_quality': data_quality,
                'atr_analysis': atr_analysis,
                'market_indicators': {
                    'volatility': volatility,
                    'adx_value': adx_value,
                    'avg_amount': avg_amount,
                    'volume_stability': volume_stability
                }
            }
            
        except Exception as e:
            logger.error(f"综合适宜度评估失败: {str(e)}")
            raise
    
    def _get_error_result(self, max_score: int, eval_type: str) -> Dict:
        """获取错误结果"""
        return {
            'score': 0,
            'max_score': max_score,
            'level': '错误',
            'description': f'{eval_type}计算失败',
            'details': '数据处理异常'
        }

def get_suitability_summary(evaluation: Dict) -> str:
    """
    获取适宜度评估摘要文本
    
    Args:
        evaluation: 评估结果
        
    Returns:
        摘要文本
    """
    try:
        total_score = evaluation['total_score']
        conclusion = evaluation['conclusion']
        
        # 各维度得分
        amp_score = evaluation['evaluations']['amplitude']['score']
        vol_score = evaluation['evaluations']['volatility']['score']
        market_score = evaluation['evaluations']['market_characteristics']['score']
        liq_score = evaluation['evaluations']['liquidity']['score']
        
        summary = f"""
标的适宜度评估结果 (总分{total_score}/100分)

• 振幅评估: {amp_score}/35分 - {evaluation['evaluations']['amplitude']['description']}
• 波动率评估: {vol_score}/30分 - {evaluation['evaluations']['volatility']['description']}
• 市场特征评估: {market_score}/25分 - {evaluation['evaluations']['market_characteristics']['description']}
• 流动性评估: {liq_score}/10分 - {evaluation['evaluations']['liquidity']['description']}

综合结论: 该标的{conclusion}执行网格交易策略
建议: {evaluation['recommendation']}
        """.strip()
        
        return summary
        
    except Exception as e:
        logger.error(f"生成适宜度摘要失败: {str(e)}")
        return "适宜度评估摘要生成失败"
