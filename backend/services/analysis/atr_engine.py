"""
ATR（平均真实波幅）算法引擎
核心算法模块，实现ATR计算和相关分析功能
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class ATREngine:
    """ATR算法引擎"""
    
    def __init__(self, period: int = 14):
        """
        初始化ATR引擎
        
        Args:
            period: ATR计算周期，默认14天
        """
        self.period = period
    
    def calculate_true_range(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        计算真实波幅（True Range）
        考虑跳空因素，比传统日振幅更准确
        
        Args:
            df: 包含OHLC数据的DataFrame
            
        Returns:
            添加了TR列的DataFrame
        """
        try:
            # 确保数据按日期排序
            df = df.sort_values('date')
            
            # 计算前一日收盘价
            df['prev_close'] = df['close'].shift(1)
            
            # 计算三种波幅
            df['hl'] = df['high'] - df['low']  # 当日最高最低价差
            df['hc'] = abs(df['high'] - df['prev_close'])  # 最高价与前日收盘价差
            df['lc'] = abs(df['low'] - df['prev_close'])   # 最低价与前日收盘价差
            
            # 真实波幅 = max(hl, hc, lc)
            df['tr'] = df[['hl', 'hc', 'lc']].max(axis=1)
            
            # 清理临时列
            df = df.drop(['hl', 'hc', 'lc'], axis=1)
            
            logger.info(f"计算真实波幅完成，数据量: {len(df)}")
            return df
            
        except Exception as e:
            logger.error(f"计算真实波幅失败: {str(e)}")
            raise
    
    def calculate_atr(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        计算ATR（平均真实波幅）
        
        Args:
            df: 包含TR数据的DataFrame
            
        Returns:
            添加了ATR相关指标的DataFrame
        """
        try:
            # 计算ATR（真实波幅的移动平均）
            df['atr'] = df['tr'].rolling(window=self.period, min_periods=1).mean()
            
            # 计算ATR比率（标准化处理）
            df['close_avg'] = df['close'].rolling(window=self.period, min_periods=1).mean()
            df['atr_ratio'] = df['atr'] / df['close_avg']
            
            # 计算ATR百分比（更直观的表示）
            df['atr_pct'] = df['atr_ratio'] * 100
            
            logger.info(f"计算ATR完成，周期: {self.period}天")
            return df
            
        except Exception as e:
            logger.error(f"计算ATR失败: {str(e)}")
            raise
    
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
                'current_atr': float(latest_data['atr']),
                'current_atr_ratio': float(latest_data['atr_ratio']),
                'current_atr_pct': float(latest_data['atr_pct']),
                'avg_atr_ratio': float(df['atr_ratio'].mean()),
                'max_atr_ratio': float(df['atr_ratio'].max()),
                'min_atr_ratio': float(df['atr_ratio'].min()),
                'atr_volatility': float(df['atr_ratio'].std()),
                'current_price': float(latest_data['close']),
                'period': self.period
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
                            risk_preference: str) -> Tuple[float, float]:
        """
        基于ATR计算价格区间
        
        Args:
            current_price: 当前价格
            atr_ratio: ATR比率
            risk_preference: 风险偏好 ('保守', '稳健', '激进')
            
        Returns:
            (下边界, 上边界) 价格区间
        """
        try:
            # 风险系数映射
            risk_multipliers = {
                '保守': 3,
                '稳健': 4,
                '激进': 5,
            }
            
            multiplier = risk_multipliers.get(risk_preference, 4)
            
            # 计算价格区间比例
            price_range_ratio = atr_ratio * multiplier
            
            # 计算上下边界
            price_lower = current_price * (1 - price_range_ratio)
            price_upper = current_price * (1 + price_range_ratio)
            
            logger.info(f"价格区间计算完成: [{price_lower:.3f}, {price_upper:.3f}]")
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
    
    def process_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """
        完整的ATR数据处理流程
        
        Args:
            df: 原始OHLC数据
            
        Returns:
            (处理后的DataFrame, ATR分析结果)
        """
        try:
            # 1. 计算真实波幅
            df = self.calculate_true_range(df)
            
            # 2. 计算ATR
            df = self.calculate_atr(df)
            
            # 3. 获取分析结果
            analysis = self.get_atr_analysis(df)
            
            logger.info("ATR数据处理完成")
            return df, analysis
            
        except Exception as e:
            logger.error(f"ATR数据处理失败: {str(e)}")
            raise

def calculate_volatility(df: pd.DataFrame) -> float:
    """
    计算年化历史波动率
    
    Args:
        df: 包含收盘价的DataFrame
        
    Returns:
        年化波动率
    """
    try:
        # 计算日收益率
        df['returns'] = np.log(df['close'] / df['close'].shift(1))
        
        # 计算年化波动率
        daily_volatility = df['returns'].std()
        annual_volatility = daily_volatility * np.sqrt(252)  # 252个交易日
        
        return float(annual_volatility)
        
    except Exception as e:
        logger.error(f"波动率计算失败: {str(e)}")
        return 0.0

def calculate_adx(df: pd.DataFrame, period: int = 14) -> float:
    """
    计算ADX指数（平均动向指数）
    用于判断趋势强度
    
    Args:
        df: 包含OHLC数据的DataFrame
        period: 计算周期
        
    Returns:
        ADX值
    """
    try:
        # 计算方向性移动
        df['high_diff'] = df['high'].diff()
        df['low_diff'] = df['low'].diff()
        
        # 计算+DM和-DM
        df['plus_dm'] = np.where(
            (df['high_diff'] > df['low_diff']) & (df['high_diff'] > 0),
            df['high_diff'], 0
        )
        df['minus_dm'] = np.where(
            (df['low_diff'] > df['high_diff']) & (df['low_diff'] > 0),
            df['low_diff'], 0
        )
        
        # 计算真实波幅
        df['tr'] = np.maximum(
            df['high'] - df['low'],
            np.maximum(
                abs(df['high'] - df['close'].shift(1)),
                abs(df['low'] - df['close'].shift(1))
            )
        )
        
        # 计算平滑的DM和TR
        df['plus_dm_smooth'] = df['plus_dm'].rolling(period).mean()
        df['minus_dm_smooth'] = df['minus_dm'].rolling(period).mean()
        df['tr_smooth'] = df['tr'].rolling(period).mean()
        
        # 计算+DI和-DI
        df['plus_di'] = 100 * df['plus_dm_smooth'] / df['tr_smooth']
        df['minus_di'] = 100 * df['minus_dm_smooth'] / df['tr_smooth']
        
        # 计算DX
        df['dx'] = 100 * abs(df['plus_di'] - df['minus_di']) / (df['plus_di'] + df['minus_di'])
        
        # 计算ADX
        adx = df['dx'].rolling(period).mean().iloc[-1]
        
        return float(adx) if not np.isnan(adx) else 0.0
        
    except Exception as e:
        logger.error(f"ADX计算失败: {str(e)}")
        return 0.0