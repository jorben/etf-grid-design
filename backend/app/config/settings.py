"""
应用配置管理
集中管理所有配置项
"""

import os
from pathlib import Path
from typing import Dict, Any, List

# 加载环境变量
project_root = Path(__file__).resolve().parent.parent.parent.parent
env_path = project_root / '.env'
try:
    from dotenv import load_dotenv
    load_dotenv(env_path)
except ImportError:
    print("Warning: python-dotenv not installed, skipping .env file loading")
except Exception as e:
    print(f"Warning: Could not load .env file: {e}")

class Settings:
    """应用配置管理类"""
    
    # 应用基础配置
    APP_NAME = "ETF网格交易策略涉及分析系统"
    VERSION = "0.1.0"
    ENVIRONMENT = os.getenv('FLASK_ENV', 'production')
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    PORT = int(os.getenv('PORT', 5001))
    HOST = '0.0.0.0'
    
    # Tushare配置
    TUSHARE_TOKEN = os.getenv('TUSHARE_TOKEN')
    
    # 缓存配置
    CACHE_DIR = f"{project_root}/cache"
    
    # ATR计算配置
    ATR_PERIOD = 14  # ATR计算周期
    
    # 网格策略配置
    GRID_CONFIG = {
        'min_grid_count': 2,
        'max_grid_count': 160,
        'default_grid_count': 12,
        'min_step_ratio': 0.005,  # 最小步长比例 0.5%
        'max_step_ratio': 0.05,   # 最大步长比例 5%
    }
    
    # 风险偏好配置
    RISK_PREFERENCES = {
        '保守': {
            'base_position_ratio': 0.3,
            'risk_factor': 0.8,
            'max_grid_count': 160
        },
        '稳健': {
            'base_position_ratio': 0.2,
            'risk_factor': 0.5,
            'max_grid_count': 160
        },
        '激进': {
            'base_position_ratio': 0.1,
            'risk_factor': 0.2,
            'max_grid_count': 160
        }
    }
    
    # 资金配置
    CAPITAL_CONFIG = {
        'min_capital': 100000,    # 最小投资金额 10万
        'max_capital': 5000000,   # 最大投资金额 500万
        'presets': [
            {'value': 100000, 'label': '10万', 'popular': True},
            {'value': 200000, 'label': '20万', 'popular': True},
            {'value': 300000, 'label': '30万', 'popular': False},
            {'value': 500000, 'label': '50万', 'popular': True},
            {'value': 800000, 'label': '80万', 'popular': False},
            {'value': 1000000, 'label': '100万', 'popular': True},
            {'value': 1500000, 'label': '150万', 'popular': False},
            {'value': 2000000, 'label': '200万', 'popular': False}
        ]
    }
    
    # 热门ETF配置
    POPULAR_ETFS = [
        {'code': '510300', 'name': '沪深300ETF', 'category': '宽基指数'},
        {'code': '510500', 'name': '中证500ETF', 'category': '宽基指数'},
        {'code': '159919', 'name': '沪深300ETF', 'category': '宽基指数'},
        {'code': '159915', 'name': '创业板ETF', 'category': '宽基指数'},
        {'code': '512880', 'name': '证券ETF', 'category': '行业主题'},
        {'code': '515050', 'name': '5G通信ETF', 'category': '行业主题'},
        {'code': '512690', 'name': '酒ETF', 'category': '行业主题'},
        {'code': '516160', 'name': '新能源ETF', 'category': '行业主题'},
        {'code': '159928', 'name': '消费ETF', 'category': '行业主题'},
        {'code': '512170', 'name': '医疗ETF', 'category': '行业主题'},
        {'code': '159941', 'name': '纳指ETF', 'category': '海外指数'},
        {'code': '513100', 'name': '纳指ETF', 'category': '海外指数'},
        {'code': '159920', 'name': '恒生ETF', 'category': '海外指数'},
        {'code': '510880', 'name': '红利ETF', 'category': '策略指数'},
        {'code': '588000', 'name': '科创50ETF', 'category': '宽基指数'},
        {'code': '512480', 'name': '半导体ETF', 'category': '行业主题'},
        {'code': '159819', 'name': '人工智能ETF', 'category': '行业主题'},
        {'code': '159742', 'name': '恒生科技ETF', 'category': '海外指数'},
    ]
    
    # 适宜性评分配置
    SUITABILITY_CONFIG = {
        'amplitude_weight': 25,      # 振幅权重
        'volatility_weight': 20,     # 波动率权重
        'market_weight': 15,         # 市场特征权重
        'liquidity_weight': 25,      # 流动性权重
        'data_quality_weight': 15,   # 数据质量权重
        'total_score': 100           # 总分
    }
    
    @classmethod
    def get_all(cls) -> Dict[str, Any]:
        """获取所有配置"""
        return {k: v for k, v in cls.__dict__.items() 
                if not k.startswith('_') and not callable(v)}
    
    @classmethod
    def get_risk_config(cls, risk_preference: str) -> Dict[str, Any]:
        """获取风险偏好配置"""
        return cls.RISK_PREFERENCES.get(risk_preference, cls.RISK_PREFERENCES['稳健'])
    
    @classmethod
    def validate_capital(cls, capital: float) -> bool:
        """验证投资金额"""
        return cls.CAPITAL_CONFIG['min_capital'] <= capital <= cls.CAPITAL_CONFIG['max_capital']
    
    @classmethod
    def validate_etf_code(cls, etf_code: str) -> bool:
        """验证ETF代码格式"""
        return etf_code and len(etf_code) == 6 and etf_code.isdigit()