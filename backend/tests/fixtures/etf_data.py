"""
ETF测试数据
提供ETF相关的测试数据
"""

from typing import Dict, List, Any


# ETF基础信息测试数据
ETF_BASIC_DATA = {
    "510300": {
        "code": "510300",
        "name": "沪深300ETF",
        "current_price": 3.85,
        "change_pct": 0.52,
        "volume": 15000000,
        "amount": 57750000.0,
        "setup_date": "2012-05-28",
        "list_date": "2012-05-28",
        "fund_type": "ETF",
        "status": "L",
        "trade_date": "2024-01-15",
        "data_age_days": 1
    },
    "510500": {
        "code": "510500",
        "name": "中证500ETF",
        "current_price": 5.67,
        "change_pct": -0.35,
        "volume": 8000000,
        "amount": 45360000.0,
        "setup_date": "2013-03-15",
        "list_date": "2013-03-15",
        "fund_type": "ETF",
        "status": "L",
        "trade_date": "2024-01-15",
        "data_age_days": 1
    },
    "159915": {
        "code": "159915",
        "name": "创业板ETF",
        "current_price": 2.34,
        "change_pct": 1.25,
        "volume": 12000000,
        "amount": 28080000.0,
        "setup_date": "2011-12-09",
        "list_date": "2011-12-09",
        "fund_type": "ETF",
        "status": "L",
        "trade_date": "2024-01-15",
        "data_age_days": 1
    }
}


# ETF价格历史数据
def generate_etf_price_history(
    etf_code: str = "510300", 
    days: int = 30,
    start_price: float = 3.80
) -> List[Dict[str, Any]]:
    """生成ETF价格历史数据"""
    import random
    from datetime import datetime, timedelta
    
    prices = []
    current_price = start_price
    base_date = datetime(2024, 1, 1)
    
    for i in range(days):
        date = base_date + timedelta(days=i)
        # 模拟价格波动
        change = random.uniform(-0.03, 0.03)  # ±3%波动
        current_price = max(0.1, current_price * (1 + change))  # 防止价格变为负数
        
        prices.append({
            "date": date.strftime("%Y-%m-%d"),
            "open": round(current_price * (1 + random.uniform(-0.01, 0.01)), 3),
            "high": round(current_price * (1 + random.uniform(0, 0.02)), 3),
            "low": round(current_price * (1 + random.uniform(-0.02, 0)), 3),
            "close": round(current_price, 3),
            "volume": random.randint(1000000, 20000000),
            "amount": round(current_price * random.randint(1000000, 20000000), 2)
        })
    
    return prices


# 预生成的价格数据
ETF_PRICE_HISTORY = {
    "510300": generate_etf_price_history("510300", 30, 3.80),
    "510500": generate_etf_price_history("510500", 30, 5.60),
    "159915": generate_etf_price_history("159915", 30, 2.30)
}


# ETF投资组合数据
ETF_PORTFOLIO_DATA = {
    "510300": {
        "etf_code": "510300",
        "report_date": "2023-12-31",
        "total_assets": 15000000000.0,  # 150亿
        "total_shares": 3896103896,  # 38.96亿份
        "holdings": [
            {
                "stock_code": "600519",
                "stock_name": "贵州茅台",
                "weight": 0.035,
                "shares": 876543,
                "market_value": 150000000.0
            },
            {
                "stock_code": "601318",
                "stock_name": "中国平安",
                "weight": 0.028,
                "shares": 1234567,
                "market_value": 120000000.0
            }
        ],
        "top_10_weight": 0.25,
        "industry_distribution": {
            "金融": 0.35,
            "信息技术": 0.20,
            "消费": 0.15,
            "工业": 0.10,
            "其他": 0.20
        }
    }
}


# 分析输入参数测试数据
ANALYSIS_INPUT_DATA = {
    "basic": {
        "etf_code": "510300",
        "total_capital": 1000000.0,
        "grid_type": "等差",
        "risk_preference": "稳健",
        "analysis_days": 365
    },
    "aggressive": {
        "etf_code": "159915",
        "total_capital": 500000.0,
        "grid_type": "等比",
        "risk_preference": "激进",
        "analysis_days": 180
    },
    "conservative": {
        "etf_code": "510500",
        "total_capital": 2000000.0,
        "grid_type": "等差",
        "risk_preference": "保守",
        "analysis_days": 730
    }
}


# 分析结果测试数据
ANALYSIS_RESULT_DATA = {
    "510300_basic": {
        "etf_info": ETF_BASIC_DATA["510300"],
        "analysis_input": ANALYSIS_INPUT_DATA["basic"],
        "suitability_evaluation": {
            "total_score": 78,
            "max_total_score": 100,
            "conclusion": "适合进行网格交易",
            "recommendation": "推荐",
            "risk_level": "中低风险",
            "has_fatal_flaw": False,
            "fatal_flaws": [],
            "evaluations": {
                "amplitude": {"score": 20, "max_score": 25, "level": "优秀", "description": "振幅适中"},
                "volatility": {"score": 18, "max_score": 20, "level": "良好", "description": "波动率合理"},
                "liquidity": {"score": 25, "max_score": 25, "level": "优秀", "description": "流动性充足"},
                "market_characteristics": {"score": 10, "max_score": 15, "level": "一般", "description": "市场特征正常"},
                "data_quality": {"score": 5, "max_score": 15, "level": "较差", "description": "数据质量一般"}
            },
            "data_quality": {
                "freshness": "新鲜",
                "freshness_desc": "数据更新及时",
                "completeness": "完整",
                "completeness_desc": "数据记录完整",
                "latest_date": "2024-01-15",
                "start_date": "2023-01-15",
                "analysis_days": 365,
                "total_records": 242,
                "missing_rate": 0.02,
                "days_since_update": 1
            }
        },
        "grid_strategy": {
            "current_price": 3.85,
            "price_range": {"lower": 3.20, "upper": 4.50},
            "grid_config": {"type": "等差", "count": 20},
            "price_levels": [3.20 + i * 0.065 for i in range(21)],
            "fund_allocation": {
                "base_position_amount": 300000.0,
                "grid_trading_amount": 600000.0,
                "reserve_amount": 100000.0,
                "grid_funds": [
                    {"level": i+1, "price": 3.20 + i * 0.065, "allocated_fund": 30000.0, "shares": 7792, "actual_fund": 30000.0, "is_buy_level": i < 10}
                    for i in range(20)
                ],
                "total_buy_grid_fund": 300000.0,
                "grid_fund_utilization_rate": 0.9,
                "expected_profit_per_trade": 1950.0,
                "grid_count": 20,
                "base_position_ratio": 0.3,
                "single_trade_quantity": 10000,
                "buy_grid_fund": 300000.0,
                "buy_grid_safety_ratio": 1.2,
                "extreme_case_safe": True
            },
            "risk_preference": "稳健",
            "atr_based": True,
            "atr_score": 85,
            "atr_description": "基于ATR的网格策略",
            "calculation_method": "标准计算",
            "calculation_logic": {"method": "standard", "parameters": {"atr_period": 14}}
        }
    }
}


# 性能指标测试数据
PERFORMANCE_METRICS_DATA = {
    "510300": {
        "etf_code": "510300",
        "period": "2023",
        "total_return": 0.125,
        "annual_return": 0.125,
        "volatility": 0.18,
        "sharpe_ratio": 0.69,
        "max_drawdown": -0.15,
        "calmar_ratio": 0.83,
        "tracking_error": 0.02,
        "information_ratio": 0.25
    }
}


# 错误场景测试数据
ERROR_SCENARIOS = {
    "invalid_etf_code": {
        "etf_code": "12345",  # 无效代码
        "total_capital": 1000000.0,
        "grid_type": "等差",
        "risk_preference": "稳健"
    },
    "insufficient_capital": {
        "etf_code": "510300",
        "total_capital": 50000.0,  # 资金不足
        "grid_type": "等差",
        "risk_preference": "稳健"
    },
    "invalid_grid_type": {
        "etf_code": "510300",
        "total_capital": 1000000.0,
        "grid_type": "无效类型",  # 无效网格类型
        "risk_preference": "稳健"
    },
    "invalid_risk_preference": {
        "etf_code": "510300",
        "total_capital": 1000000.0,
        "grid_type": "等差",
        "risk_preference": "无效偏好"  # 无效风险偏好
    }
}


def get_etf_data(etf_code: str) -> Dict[str, Any]:
    """获取指定ETF的测试数据"""
    return ETF_BASIC_DATA.get(etf_code, {})


def get_price_history(etf_code: str, days: int = 30) -> List[Dict[str, Any]]:
    """获取价格历史数据"""
    if etf_code in ETF_PRICE_HISTORY:
        return ETF_PRICE_HISTORY[etf_code][:days]
    return generate_etf_price_history(etf_code, days)


def get_analysis_input(scenario: str = "basic") -> Dict[str, Any]:
    """获取分析输入参数"""
    return ANALYSIS_INPUT_DATA.get(scenario, ANALYSIS_INPUT_DATA["basic"])


def get_analysis_result(etf_code: str = "510300") -> Dict[str, Any]:
    """获取分析结果数据"""
    key = f"{etf_code}_basic"
    return ANALYSIS_RESULT_DATA.get(key, ANALYSIS_RESULT_DATA["510300_basic"])


def get_error_scenario(scenario: str) -> Dict[str, Any]:
    """获取错误场景数据"""
    return ERROR_SCENARIOS.get(scenario, {})
