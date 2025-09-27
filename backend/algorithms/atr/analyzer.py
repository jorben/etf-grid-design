"""
ATR分析器 - 分析逻辑
从服务层抽离的ATR分析逻辑模块
"""

import pandas as pd
from typing import Dict, Tuple
import logging
from .calculator import ATRCalculator

logger = logging.getLogger(__name__)

class ATRAnalyzer:
    """ATR分析器 - 分析逻辑"""
    
    def __init__(self, calculator: ATRCalculator):
        """
        初始化ATR分析器
        
        Args:
            calculator: ATR计算器实例
        """
        self.calculator = calculator
    
    def get_atr_analysis(self, df: pd.DataFrame) -> Dict:
        """
        获取ATR分析结果
        
        Args:
            df: 包含ATR数据的DataFrame
            
        Returns:
            ATR分析结果字典
        """
        try:
            # 获取最新的ATR数据
            latest_data = df.iloc[-1]
            
            # 计算统计指标
            atr_stats = {
                'current_atr': float(latest_data['ATR']),
                'current_atr_ratio': float(latest_data['atr_ratio']),
                'current_atr_pct': float(latest_data['atr_pct']),
                'avg_atr_ratio': float(df['atr_ratio'].mean()),
                'max_atr_ratio': float(df['atr_ratio'].max()),
                'min_atr_ratio': float(df['atr_ratio'].min()),
                'atr_volatility': float(df['atr_ratio'].std()),
                'current_price': float(latest_data['close']),
                'period': self.calculator.period
            }
            
            # ATR趋势分析
            recent_atr = df['atr_ratio'].tail(30).mean()  # 最近30天平均
            historical_atr = df['atr_ratio'].head(-30).mean()  # 历史平均
            
            atr_stats['atr_trend'] = 'increasing' if recent_atr > historical_atr else 'decreasing'
            atr_stats['trend_strength'] = abs(recent_atr - historical_atr) / historical_atr
            
            logger.info(f"ATR分析完成，当前ATR比率: {atr_stats['current_atr_pct']:.2f}%")
            return atr_stats
            
        except Exception as e:
            logger.error(f"ATR分析失败: {str(e)}")
            raise
    
    def calculate_price_range(self, current_price: float, atr_ratio: float, 
                            risk_preference: str, adjustment_coefficient: float = 1.0) -> Tuple[float, float]:
        """
        基于ATR计算价格区间
        
        Args:
            current_price: 当前价格
            atr_ratio: ATR比率
            risk_preference: 频率偏好 ('低频', '均衡', '高频')
            adjustment_coefficient: 调节系数 (0-2)，默认1.0
                系数越大，频率系数越离散；系数越小，频率系数越聚拢
                
        Returns:
            (下边界, 上边界) 价格区间
        """
        try:
            # 默认风险系数映射
            default_risk_multipliers = {
                '低频': 7,
                '均衡': 5.5,
                '高频': 4,
            }
            
            # 应用调节系数
            risk_multipliers = {}
            for risk_level, default_value in default_risk_multipliers.items():
                # 计算与中间值(4)的差异
                diff_from_mid = default_value - 5
                # 应用调节系数：系数越大差异放大，系数越小差异缩小
                adjusted_diff = diff_from_mid * adjustment_coefficient
                # 计算调整后的风险系数
                risk_multipliers[risk_level] = 5 + adjusted_diff
            
            multiplier = risk_multipliers.get(risk_preference, 5)
            
            # 计算价格区间比例
            price_range_ratio = atr_ratio * multiplier
            
            # 计算上下边界
            price_lower = current_price * (1 - price_range_ratio)
            price_upper = current_price * (1 + price_range_ratio)
            
            logger.info(f"价格区间计算完成: [{price_lower:.3f}, {price_upper:.3f}]，AtrRatio：{atr_ratio}，risk：{risk_preference}，adjustment：{adjustment_coefficient:.1f}")
            return price_lower, price_upper
            
        except Exception as e:
            logger.error(f"价格区间计算失败: {str(e)}")
            raise
    
    def get_atr_score(self, atr_ratio: float) -> Tuple[int, str]:
        """
        基于ATR比率计算振幅评分
        
        Args:
            atr_ratio: ATR比率
            
        Returns:
            (评分, 评级说明)
        """
        try:
            atr_pct = atr_ratio * 100
            
            if atr_pct >= 2.0:
                return 35, "振幅充足，交易机会丰富"
            elif atr_pct >= 1.5:
                return 25, "振幅适中，基本适合"
            else:
                return 0, "振幅不足，不推荐"
                
        except Exception as e:
            logger.error(f"ATR评分计算失败: {str(e)}")
            return 0, "计算错误"
    
    def analyze_atr_characteristics(self, df: pd.DataFrame) -> Dict:
        """
        分析ATR特征
        
        Args:
            df: 包含ATR数据的DataFrame
            
        Returns:
            ATR特征分析结果
        """
        try:
            # 获取基础分析结果
            atr_analysis = self.get_atr_analysis(df)
            
            # 分析波动模式
            volatility_pattern = self._analyze_volatility_pattern(df)
            
            # 分析趋势特征
            trend_characteristics = self._analyze_trend_characteristics(df)
            
            # 分析周期性
            periodicity_analysis = self._analyze_periodicity(df)
            
            result = {
                'basic_analysis': atr_analysis,
                'volatility_pattern': volatility_pattern,
                'trend_characteristics': trend_characteristics,
                'periodicity_analysis': periodicity_analysis
            }
            
            logger.info("ATR特征分析完成")
            return result
            
        except Exception as e:
            logger.error(f"ATR特征分析失败: {str(e)}")
            raise
    
    def _analyze_volatility_pattern(self, df: pd.DataFrame) -> Dict:
        """分析波动模式"""
        try:
            atr_ratio = df['atr_ratio']
            
            # 计算波动率聚类特征
            volatility_clustering = atr_ratio.autocorr(lag=1)
            
            # 计算波动率水平
            volatility_level = '高' if atr_ratio.mean() > 0.02 else '中' if atr_ratio.mean() > 0.01 else '低'
            
            # 计算波动率稳定性
            volatility_stability = '稳定' if atr_ratio.std() < atr_ratio.mean() * 0.3 else '不稳定'
            
            return {
                'volatility_clustering': float(volatility_clustering),
                'volatility_level': volatility_level,
                'volatility_stability': volatility_stability,
                'avg_volatility': float(atr_ratio.mean()),
                'volatility_std': float(atr_ratio.std())
            }
            
        except Exception as e:
            logger.error(f"波动模式分析失败: {str(e)}")
            return {}
    
    def _analyze_trend_characteristics(self, df: pd.DataFrame) -> Dict:
        """分析趋势特征"""
        try:
            atr_ratio = df['atr_ratio']
            
            # 计算趋势强度
            trend_strength = atr_ratio.diff().abs().mean()
            
            # 判断趋势方向
            recent_trend = atr_ratio.tail(10).mean() - atr_ratio.head(10).mean()
            trend_direction = '上升' if recent_trend > 0 else '下降' if recent_trend < 0 else '平稳'
            
            # 计算趋势持续性
            trend_persistence = atr_ratio.rolling(window=5).apply(
                lambda x: (x.diff() > 0).sum() / len(x) if len(x) > 1 else 0
            ).mean()
            
            return {
                'trend_strength': float(trend_strength),
                'trend_direction': trend_direction,
                'trend_persistence': float(trend_persistence),
                'recent_trend': float(recent_trend)
            }
            
        except Exception as e:
            logger.error(f"趋势特征分析失败: {str(e)}")
            return {}
    
    def _analyze_periodicity(self, df: pd.DataFrame) -> Dict:
        """分析周期性"""
        try:
            atr_ratio = df['atr_ratio']
            
            # 简单的周期性分析（基于自相关）
            autocorrelations = []
            for lag in range(1, 11):  # 检查1-10天的自相关
                autocorr = atr_ratio.autocorr(lag=lag)
                autocorrelations.append({'lag': lag, 'autocorrelation': float(autocorr)})
            
            # 找出最强的周期性
            strongest_period = max(autocorrelations, key=lambda x: abs(x['autocorrelation']))
            
            return {
                'autocorrelations': autocorrelations,
                'strongest_period': strongest_period,
                'has_strong_periodicity': abs(strongest_period['autocorrelation']) > 0.3
            }
            
        except Exception as e:
            logger.error(f"周期性分析失败: {str(e)}")
            return {}
