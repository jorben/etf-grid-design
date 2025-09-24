"""
市场数据测试数据
提供市场相关的测试数据
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta
import random


# 市场指数数据
MARKET_INDEX_DATA = {
    "000001": {  # 上证指数
        "code": "000001",
        "name": "上证指数",
        "current": 3200.45,
        "change": 15.67,
        "change_pct": 0.49,
        "volume": 35000000000,
        "amount": 450000000000.0,
        "trade_date": "2024-01-15"
    },
    "399001": {  # 深证成指
        "code": "399001",
        "name": "深证成指",
        "current": 11000.23,
        "change": -25.89,
        "change_pct": -0.23,
        "volume": 28000000000,
        "amount": 380000000000.0,
        "trade_date": "2024-01-15"
    },
    "000300": {  # 沪深300
        "code": "000300",
        "name": "沪深300",
        "current": 3850.67,
        "change": 18.45,
        "change_pct": 0.48,
        "volume": 15000000000,
        "amount": 200000000000.0,
        "trade_date": "2024-01-15"
    }
}


# 行业数据
INDUSTRY_DATA = {
    "金融": {
        "name": "金融",
        "current_price": 1250.45,
        "change_pct": 0.65,
        "pe_ratio": 8.5,
        "pb_ratio": 1.2,
        "dividend_yield": 3.2
    },
    "信息技术": {
        "name": "信息技术",
        "current_price": 2350.78,
        "change_pct": -0.35,
        "pe_ratio": 35.6,
        "pb_ratio": 4.8,
        "dividend_yield": 0.8
    },
    "消费": {
        "name": "消费",
        "current_price": 1890.23,
        "change_pct": 0.28,
        "pe_ratio": 25.3,
        "pb_ratio": 3.2,
        "dividend_yield": 1.5
    },
    "工业": {
        "name": "工业",
        "current_price": 1560.89,
        "change_pct": 0.12,
        "pe_ratio": 15.7,
        "pb_ratio": 2.1,
        "dividend_yield": 2.3
    }
}


# 宏观经济数据
MACRO_ECONOMIC_DATA = {
    "gdp": {
        "indicator": "GDP增长率",
        "value": 5.2,
        "unit": "%",
        "period": "2023年第四季度",
        "trend": "稳定"
    },
    "cpi": {
        "indicator": "消费者价格指数",
        "value": 2.1,
        "unit": "%",
        "period": "2023年12月",
        "trend": "温和"
    },
    "ppi": {
        "indicator": "生产者价格指数",
        "value": -1.2,
        "unit": "%",
        "period": "2023年12月",
        "trend": "下降"
    },
    "interest_rate": {
        "indicator": "基准利率",
        "value": 3.45,
        "unit": "%",
        "period": "当前",
        "trend": "稳定"
    }
}


# 市场情绪数据
MARKET_SENTIMENT_DATA = {
    "fear_greed_index": 65,  # 恐惧贪婪指数 (0-100)
    "volatility_index": 18.5,  # 波动率指数
    "put_call_ratio": 0.85,  # 看跌看涨比率
    "advance_decline": 1.25,  # 涨跌比
    "market_breadth": 0.68  # 市场广度
}


# 技术指标数据
TECHNICAL_INDICATORS_DATA = {
    "moving_averages": {
        "ma5": 3.82,
        "ma10": 3.78,
        "ma20": 3.75,
        "ma60": 3.68
    },
    "bollinger_bands": {
        "upper": 4.05,
        "middle": 3.82,
        "lower": 3.59,
        "width": 0.46
    },
    "rsi": 58.5,  # 相对强弱指数
    "macd": {
        "dif": 0.025,
        "dea": 0.018,
        "histogram": 0.007
    },
    "stochastic": {
        "k": 62.3,
        "d": 58.7
    }
}


def generate_market_trend_data(
    days: int = 30,
    start_date: str = "2024-01-01",
    base_value: float = 3200.0,
    volatility: float = 0.02
) -> List[Dict[str, Any]]:
    """生成市场趋势数据"""
    data = []
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    current_value = base_value
    
    for i in range(days):
        date_str = current_date.strftime("%Y-%m-%d")
        
        # 模拟市场波动
        change = random.uniform(-volatility, volatility)
        current_value = max(100, current_value * (1 + change))  # 防止变为负数
        
        # 生成交易量数据
        volume = random.randint(20000000000, 50000000000)
        amount = current_value * volume / 100000000  # 简化计算
        
        data.append({
            "date": date_str,
            "value": round(current_value, 2),
            "change": round(current_value - base_value, 2),
            "change_pct": round(change * 100, 2),
            "volume": volume,
            "amount": round(amount, 2)
        })
        
        current_date += timedelta(days=1)
    
    return data


def generate_volatility_data(
    days: int = 30,
    base_volatility: float = 0.015
) -> List[Dict[str, Any]]:
    """生成波动率数据"""
    data = []
    current_date = datetime(2024, 1, 1)
    
    for i in range(days):
        date_str = current_date.strftime("%Y-%m-%d")
        
        # 模拟波动率变化
        volatility = max(0.005, base_volatility * random.uniform(0.5, 2.0))
        
        data.append({
            "date": date_str,
            "volatility": round(volatility, 4),
            "volatility_pct": round(volatility * 100, 2),
            "trend": "上升" if i > 0 and volatility > data[i-1]["volatility"] else "下降"
        })
        
        current_date += timedelta(days=1)
    
    return data


def generate_correlation_matrix(assets: List[str]) -> Dict[str, Dict[str, float]]:
    """生成资产相关性矩阵"""
    matrix = {}
    
    for asset1 in assets:
        matrix[asset1] = {}
        for asset2 in assets:
            if asset1 == asset2:
                matrix[asset1][asset2] = 1.0
            else:
                # 模拟相关性系数 (-1 到 1)
                correlation = random.uniform(-0.8, 0.8)
                matrix[asset1][asset2] = round(correlation, 3)
    
    return matrix


# 预生成的市场数据
MARKET_TREND_DATA = generate_market_trend_data(30, "2024-01-01", 3200.0)
VOLATILITY_DATA = generate_volatility_data(30)
CORRELATION_MATRIX = generate_correlation_matrix(["510300", "510500", "159915", "000001", "399001"])


# 风险指标数据
RISK_METRICS_DATA = {
    "var_95": {  # 95%置信度的VaR
        "1_day": -0.028,
        "5_day": -0.063,
        "10_day": -0.089
    },
    "expected_shortfall": {  # 期望损失
        "1_day": -0.035,
        "5_day": -0.078,
        "10_day": -0.110
    },
    "beta": 1.05,  # Beta系数
    "alpha": 0.012,  # Alpha系数
    "sharpe_ratio": 0.85,
    "sortino_ratio": 1.12,
    "max_drawdown": -0.156
}


# 市场状态数据
MARKET_STATE_DATA = {
    "current_state": "震荡",
    "trend_direction": "横盘",
    "volatility_level": "中等",
    "liquidity_level": "充足",
    "sentiment": "中性",
    "risk_appetite": "中等"
}


# 市场事件数据
MARKET_EVENTS_DATA = [
    {
        "date": "2024-01-10",
        "event": "央行降准",
        "impact": "正面",
        "magnitude": "中等",
        "affected_assets": ["金融", "房地产"]
    },
    {
        "date": "2024-01-05",
        "event": "贸易数据发布",
        "impact": "中性",
        "magnitude": "低",
        "affected_assets": ["出口", "制造业"]
    },
    {
        "date": "2023-12-28",
        "event": "政策会议",
        "impact": "正面",
        "magnitude": "高",
        "affected_assets": ["全市场"]
    }
]


def get_market_index(index_code: str) -> Dict[str, Any]:
    """获取市场指数数据"""
    return MARKET_INDEX_DATA.get(index_code, {})


def get_industry_data(industry: str) -> Dict[str, Any]:
    """获取行业数据"""
    return INDUSTRY_DATA.get(industry, {})


def get_macro_data(indicator: str) -> Dict[str, Any]:
    """获取宏观经济数据"""
    return MACRO_ECONOMIC_DATA.get(indicator, {})


def get_technical_indicators() -> Dict[str, Any]:
    """获取技术指标数据"""
    return TECHNICAL_INDICATORS_DATA


def get_market_trend(days: int = 30) -> List[Dict[str, Any]]:
    """获取市场趋势数据"""
    return MARKET_TREND_DATA[:days] if days <= len(MARKET_TREND_DATA) else MARKET_TREND_DATA


def get_volatility_data(days: int = 30) -> List[Dict[str, Any]]:
    """获取波动率数据"""
    return VOLATILITY_DATA[:days] if days <= len(VOLATILITY_DATA) else VOLATILITY_DATA


def get_correlation_matrix() -> Dict[str, Dict[str, float]]:
    """获取相关性矩阵"""
    return CORRELATION_MATRIX


def get_risk_metrics() -> Dict[str, Any]:
    """获取风险指标数据"""
    return RISK_METRICS_DATA


def get_market_state() -> Dict[str, Any]:
    """获取市场状态数据"""
    return MARKET_STATE_DATA


def get_recent_market_events(days: int = 30) -> List[Dict[str, Any]]:
    """获取近期市场事件"""
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    return [
        event for event in MARKET_EVENTS_DATA 
        if event["date"] >= cutoff_date
    ]
