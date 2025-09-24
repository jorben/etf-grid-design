"""
计算工具函数
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple

def calculate_trading_days(start_date: datetime, end_date: datetime) -> int:
    """
    计算交易日天数（排除周末）
    
    Args:
        start_date: 开始日期
        end_date: 结束日期
        
    Returns:
        交易日天数
    """
    total_days = (end_date - start_date).days
    weeks = total_days // 7
    remaining_days = total_days % 7
    
    # 计算剩余天数中的工作日
    weekday_start = start_date.weekday()
    weekend_days = weeks * 2
    
    for i in range(remaining_days):
        if (weekday_start + i) % 7 in [5, 6]:  # 周六、周日
            weekend_days += 1
    
    return total_days - weekend_days

def calculate_risk_level(score: float, max_score: float = 100) -> str:
    """
    根据评分计算风险等级
    
    Args:
        score: 当前评分
        max_score: 最高评分
        
    Returns:
        风险等级描述
    """
    ratio = score / max_score
    
    if ratio >= 0.8:
        return "低风险"
    elif ratio >= 0.6:
        return "中低风险"
    elif ratio >= 0.4:
        return "中等风险"
    elif ratio >= 0.2:
        return "中高风险"
    else:
        return "高风险"

def calculate_suitability_level(score: float) -> Dict[str, Any]:
    """
    根据适宜度评分计算等级
    
    Args:
        score: 适宜度评分（0-100）
        
    Returns:
        适宜度等级信息
    """
    if score >= 70:
        return {
            'level': '非常适合',
            'color': 'green',
            'description': '该ETF非常适合进行网格交易，各项指标表现优秀',
            'recommendation': '强烈推荐'
        }
    elif score >= 60:
        return {
            'level': '基本适合',
            'color': 'yellow',
            'description': '该ETF基本适合网格交易，但需要注意风险控制',
            'recommendation': '谨慎推荐'
        }
    else:
        return {
            'level': '不适合',
            'color': 'red',
            'description': '该ETF不适合进行网格交易，存在较高风险',
            'recommendation': '不推荐'
        }

def calculate_correlation(series1: pd.Series, series2: pd.Series) -> float:
    """
    计算两个序列的相关性
    
    Args:
        series1: 序列1
        series2: 序列2
        
    Returns:
        相关系数
    """
    try:
        return series1.corr(series2)
    except:
        return 0.0

def calculate_position_size(total_capital: float, risk_per_trade: float, 
                          entry_price: float, stop_loss_price: float) -> int:
    """
    计算仓位大小
    
    Args:
        total_capital: 总资金
        risk_per_trade: 单笔交易风险比例
        entry_price: 入场价格
        stop_loss_price: 止损价格
        
    Returns:
        建议仓位大小（股数）
    """
    if entry_price <= 0 or stop_loss_price <= 0:
        return 0
    
    risk_amount = total_capital * risk_per_trade
    price_risk = abs(entry_price - stop_loss_price)
    
    if price_risk <= 0:
        return 0
    
    position_size = int(risk_amount / price_risk)
    return max(0, position_size)

def calculate_volatility(price_series: pd.Series, window: int = 20) -> float:
    """
    计算价格波动率
    
    Args:
        price_series: 价格序列
        window: 计算窗口
        
    Returns:
        波动率
    """
    if len(price_series) < window:
        return 0.0
    
    returns = price_series.pct_change().dropna()
    return returns.rolling(window=window).std().iloc[-1] * np.sqrt(252)  # 年化波动率

def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.03) -> float:
    """
    计算夏普比率
    
    Args:
        returns: 收益率序列
        risk_free_rate: 无风险利率
        
    Returns:
        夏普比率
    """
    if len(returns) == 0:
        return 0.0
    
    excess_returns = returns - risk_free_rate / 252  # 日度无风险利率
    if excess_returns.std() == 0:
        return 0.0
    
    return excess_returns.mean() / excess_returns.std() * np.sqrt(252)

def calculate_max_drawdown(price_series: pd.Series) -> float:
    """
    计算最大回撤
    
    Args:
        price_series: 价格序列
        
    Returns:
        最大回撤（负数）
    """
    if len(price_series) == 0:
        return 0.0
    
    cumulative = (1 + price_series.pct_change()).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    
    return drawdown.min()

def calculate_win_rate(returns: pd.Series) -> float:
    """
    计算胜率
    
    Args:
        returns: 收益率序列
        
    Returns:
        胜率（0-1）
    """
    if len(returns) == 0:
        return 0.0
    
    positive_returns = returns[returns > 0]
    return len(positive_returns) / len(returns)

def calculate_profit_factor(returns: pd.Series) -> float:
    """
    计算盈利因子
    
    Args:
        returns: 收益率序列
        
    Returns:
        盈利因子
    """
    if len(returns) == 0:
        return 0.0
    
    positive_returns = returns[returns > 0].sum()
    negative_returns = abs(returns[returns < 0].sum())
    
    if negative_returns == 0:
        return float('inf') if positive_returns > 0 else 0.0
    
    return positive_returns / negative_returns

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    安全除法，避免除零错误
    
    Args:
        numerator: 分子
        denominator: 分母
        default: 默认值
        
    Returns:
        除法结果或默认值
    """
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except:
        return default

def round_to_tick(price: float, tick_size: float = 0.001) -> float:
    """
    将价格舍入到最小价格单位
    
    Args:
        price: 原始价格
        tick_size: 最小价格单位
        
    Returns:
        舍入后的价格
    """
    return round(price / tick_size) * tick_size

def calculate_compound_return(returns: pd.Series) -> float:
    """
    计算复合收益率
    
    Args:
        returns: 收益率序列
        
    Returns:
        复合收益率
    """
    if len(returns) == 0:
        return 0.0
    
    return (1 + returns).prod() - 1

def calculate_annualized_return(total_return: float, days: int) -> float:
    """
    计算年化收益率
    
    Args:
        total_return: 总收益率
        days: 投资天数
        
    Returns:
        年化收益率
    """
    if days <= 0:
        return 0.0
    
    return (1 + total_return) ** (365 / days) - 1

def calculate_returns(price_series: pd.Series) -> pd.Series:
    """
    计算收益率序列
    
    Args:
        price_series: 价格序列
        
    Returns:
        收益率序列
    """
    if len(price_series) == 0:
        return pd.Series()
    
    return price_series.pct_change().dropna()