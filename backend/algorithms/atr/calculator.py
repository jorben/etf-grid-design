"""
ATR计算器 - 纯算法实现
从服务层抽离的ATR核心算法模块
"""

import pandas as pd
import numpy as np
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

class ATRCalculator:
    """ATR计算器 - 纯算法实现"""
    
    def __init__(self, period: int = 14):
        """
        初始化ATR计算器
        
        Args:
            period: ATR计算周期，默认14天
        """
        self.period = period
    
    def _validate_data(self, df: pd.DataFrame) -> None:
        """验证输入数据质量"""
        required_columns = ['date', 'open', 'high', 'low', 'close']
        for col in required_columns:
            if col not in df.columns:
                raise KeyError(f"缺少必要列: {col}")
        
        if df.empty:
            raise ValueError("数据为空")
        
        # 检查价格数据合理性
        if (df['high'] < df['low']).any():
            raise ValueError("最高价低于最低价")
        
        if (df['high'] <= 0).any() or (df['low'] <= 0).any() or (df['close'] <= 0).any():
            raise ValueError("价格数据包含非正值")
        
        # 检查缺失值
        if df[required_columns].isnull().any().any():
            raise ValueError("数据包含缺失值")
    
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
            # 验证数据质量
            self._validate_data(df)
            
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
            df: 包含OHLC数据的DataFrame
            
        Returns:
            添加了ATR相关指标的DataFrame
        """
        try:
            # 先计算真实波幅
            df = self.calculate_true_range(df)
            
            # 计算ATR（真实波幅的移动平均）
            df['ATR'] = df['tr'].rolling(window=self.period, min_periods=1).mean()
            
            # 计算ATR比率（标准化处理）
            df['close_avg'] = df['close'].rolling(window=self.period, min_periods=1).mean()
            df['atr_ratio'] = df['ATR'] / df['close_avg']
            
            # 计算ATR百分比（更直观的表示）
            df['atr_pct'] = df['atr_ratio'] * 100
            
            logger.info(f"计算ATR完成，周期: {self.period}天")
            return df
            
        except Exception as e:
            logger.error(f"计算ATR失败: {str(e)}")
            raise
    
    def process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        完整的ATR数据处理流程
        
        Args:
            df: 原始OHLC数据
            
        Returns:
            处理后的DataFrame
        """
        try:
            # 1. 计算真实波幅
            df = self.calculate_true_range(df)
            
            # 2. 计算ATR
            df = self.calculate_atr(df)
            
            logger.info("ATR数据处理完成")
            return df
            
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
