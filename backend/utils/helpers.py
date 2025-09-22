"""
工具函数模块
提供常用的计算、格式化和验证功能
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import re

def format_currency(amount: float, currency: str = 'CNY') -> str:
    """
    格式化货币金额
    
    Args:
        amount: 金额
        currency: 货币类型
        
    Returns:
        格式化后的货币字符串
    """
    if currency == 'CNY':
        if amount >= 100000000:  # 1亿
            return f"¥{amount/100000000:.2f}亿"
        elif amount >= 10000:  # 1万
            return f"¥{amount/10000:.2f}万"
        else:
            return f"¥{amount:,.2f}"
    else:
        return f"{amount:,.2f}"

def format_percentage(value: float, decimal_places: int = 2) -> str:
    """
    格式化百分比
    
    Args:
        value: 数值（0.1 表示 10%）
        decimal_places: 小数位数
        
    Returns:
        格式化后的百分比字符串
    """
    return f"{value * 100:.{decimal_places}f}%"

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

def validate_date_range(start_date: str, end_date: str) -> Tuple[bool, str]:
    """
    验证日期范围
    
    Args:
        start_date: 开始日期字符串 (YYYY-MM-DD)
        end_date: 结束日期字符串 (YYYY-MM-DD)
        
    Returns:
        (是否有效, 错误信息)
    """
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        if start >= end:
            return False, "开始日期必须早于结束日期"
        
        if end > datetime.now():
            return False, "结束日期不能超过当前日期"
        
        if (end - start).days > 365 * 5:  # 最多5年
            return False, "日期范围不能超过5年"
        
        if (end - start).days < 30:  # 至少30天
            return False, "日期范围至少需要30天"
        
        return True, ""
        
    except ValueError:
        return False, "日期格式错误，请使用YYYY-MM-DD格式"

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
    根据适合度评分计算等级
    
    Args:
        score: 适合度评分（0-100）
        
    Returns:
        适合度等级信息
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

def generate_strategy_summary(analysis_result: Dict) -> str:
    """
    生成策略摘要文本
    
    Args:
        analysis_result: 分析结果
        
    Returns:
        策略摘要文本
    """
    etf_info = analysis_result.get('etf_info', {})
    suitability = analysis_result.get('suitability_analysis', {})
    grid_params = analysis_result.get('grid_parameters', {})
    backtest = analysis_result.get('backtest_result', {})
    
    etf_name = etf_info.get('name', '未知ETF')
    total_score = suitability.get('total_score', 0)
    expected_return = backtest.get('performance', {}).get('annual_return', 0)
    
    summary = f"""
    【{etf_name}】网格交易策略分析摘要：
    
    ✓ 适合度评分：{total_score:.1f}/100分
    ✓ 预期年化收益：{format_percentage(expected_return)}
    ✓ 网格数量：{grid_params.get('grid_count', 0)}个
    ✓ 价格区间：¥{grid_params.get('price_lower', 0):.3f} - ¥{grid_params.get('price_upper', 0):.3f}
    
    该策略基于ATR算法设计，适合{grid_params.get('risk_preference', '稳健')}型投资者。
    """
    
    return summary.strip()

def calculate_position_size(total_capital: float, risk_per_trade: float, entry_price: float, stop_loss_price: float) -> int:
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

def detect_market_regime(price_data: pd.DataFrame, window: int = 20) -> str:
    """
    检测市场状态
    
    Args:
        price_data: 价格数据
        window: 计算窗口
        
    Returns:
        市场状态描述
    """
    if len(price_data) < window:
        return "数据不足"
    
    # 计算移动平均线
    ma_short = price_data['close'].rolling(window=window//2).mean()
    ma_long = price_data['close'].rolling(window=window).mean()
    
    # 当前价格相对于移动平均线的位置
    current_price = price_data['close'].iloc[-1]
    current_ma_short = ma_short.iloc[-1]
    current_ma_long = ma_long.iloc[-1]
    
    # 判断趋势
    if current_price > current_ma_short > current_ma_long:
        return "上升趋势"
    elif current_price < current_ma_short < current_ma_long:
        return "下降趋势"
    else:
        return "震荡市场"

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

def generate_risk_warnings(analysis_result: Dict) -> List[str]:
    """
    生成风险警告
    
    Args:
        analysis_result: 分析结果
        
    Returns:
        风险警告列表
    """
    warnings = []
    
    suitability = analysis_result.get('suitability_analysis', {})
    backtest = analysis_result.get('backtest_result', {})
    
    # 适合度评分过低
    total_score = suitability.get('total_score', 0)
    if total_score < 60:
        warnings.append("⚠️ 该ETF适合度评分较低，不建议进行网格交易")
    
    # 最大回撤过大
    max_drawdown = backtest.get('performance', {}).get('max_drawdown', 0)
    if max_drawdown > 0.2:
        warnings.append("⚠️ 历史最大回撤超过20%，存在较高风险")
    
    # 胜率过低
    win_rate = backtest.get('performance', {}).get('win_rate', 0)
    if win_rate < 0.5:
        warnings.append("⚠️ 历史交易胜率低于50%，策略效果可能不佳")
    
    # 流动性不足
    liquidity_score = suitability.get('liquidity_score', 0)
    if liquidity_score < 5:
        warnings.append("⚠️ ETF流动性不足，可能影响交易执行")
    
    # 波动率过高
    volatility_score = suitability.get('volatility_score', 0)
    if volatility_score < 15:
        warnings.append("⚠️ 波动率过高，风险较大，建议谨慎操作")
    
    return warnings

def optimize_grid_spacing(price_data: pd.DataFrame, grid_count: int, grid_type: str = 'arithmetic') -> List[float]:
    """
    优化网格间距
    
    Args:
        price_data: 价格数据
        grid_count: 网格数量
        grid_type: 网格类型 ('arithmetic' 或 'geometric')
        
    Returns:
        优化后的网格价位列表
    """
    if price_data.empty:
        return []
    
    current_price = price_data['close'].iloc[-1]
    price_std = price_data['close'].std()
    
    # 基于波动率确定价格区间
    price_range = price_std * 2  # 2倍标准差
    price_upper = current_price + price_range
    price_lower = current_price - price_range
    
    if grid_type == 'arithmetic':
        # 等差数列
        step = (price_upper - price_lower) / (grid_count - 1)
        return [price_lower + i * step for i in range(grid_count)]
    else:
        # 等比数列
        ratio = (price_upper / price_lower) ** (1 / (grid_count - 1))
        return [price_lower * (ratio ** i) for i in range(grid_count)]

def validate_parameters(params: Dict) -> Tuple[bool, List[str]]:
    """
    验证输入参数
    
    Args:
        params: 参数字典
        
    Returns:
        (是否有效, 错误信息列表)
    """
    errors = []
    
    # 验证ETF代码
    etf_code = params.get('etf_code', '')
    if not etf_code or len(etf_code) != 6 or not etf_code.isdigit():
        errors.append("ETF代码必须是6位数字")
    
    # 验证投资金额
    total_capital = params.get('total_capital', 0)
    if total_capital < 100000:  # 最少10万
        errors.append("投资金额不能少于10万元")
    elif total_capital > 5000000:  # 最多500万
        errors.append("投资金额不能超过500万元")
    
    # 验证网格类型
    grid_type = params.get('grid_type', '')
    if grid_type not in ['arithmetic', 'geometric']:
        errors.append("网格类型必须是'arithmetic'或'geometric'")
    
    # 验证交易频率
    trading_frequency = params.get('trading_frequency', '')
    if trading_frequency not in ['low', 'medium', 'high']:
        errors.append("交易频率必须是'low'、'medium'或'high'")
    
    # 验证风险偏好
    risk_preference = params.get('risk_preference', '')
    if risk_preference not in ['conservative', 'balanced', 'aggressive']:
        errors.append("风险偏好必须是'conservative'、'balanced'或'aggressive'")
    
    return len(errors) == 0, errors

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