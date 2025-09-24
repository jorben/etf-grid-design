"""
数据获取服务
整合Tushare API，提供ETF数据获取功能
注意：此服务已被TushareClient替代，保留用于向后兼容
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict
import logging
from .tushare_client import TushareClient

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataService:
    """数据获取服务类 - 兼容性包装器"""
    
    def __init__(self):
        """初始化数据服务"""
        logger.warning("DataService已被TushareClient替代，建议直接使用TushareClient")
        self.tushare_client = TushareClient()

    
    def get_fund_basic(self, code: str) -> Dict:
        """获取基金基础信息 - 兼容性方法"""
        try:
            basic_info = self.tushare_client.get_etf_basic_info(code)
            if not basic_info:
                return None
            
            # 转换为旧格式以保持兼容性
            result = {
                'name': basic_info.get('name', ''),
                'management': basic_info.get('management', ''),
                'setup_date': basic_info.get('found_date', ''),
                'list_date': basic_info.get('list_date', ''),
                'fund_type': 'ETF',
                'status': 'L'
            }
            
            return result
            
        except Exception as e:
            logger.error(f"获取基金基础信息失败 {code}: {str(e)}")
            return None
    
    def get_current_price(self, code: str) -> Dict:
        """获取当前价格信息 - 兼容性方法"""
        try:
            price_data = self.tushare_client.get_latest_price(code)
            if not price_data:
                return {'close': 0, 'pct_chg': 0, 'vol': 0, 'amount': 0}
            
            # 转换为旧格式以保持兼容性
            return {
                'close': price_data.get('current_price', 0),
                'pct_chg': price_data.get('pct_change', 0),
                'vol': price_data.get('volume', 0),
                'amount': price_data.get('amount', 0)
            }
            
        except Exception as e:
            logger.error(f"获取当前价格失败 {code}: {str(e)}")
            return {'close': 0, 'pct_chg': 0, 'vol': 0, 'amount': 0}
    
    def get_daily_data(self, code: str, start_date: str, end_date: str) -> pd.DataFrame:
        """获取日线数据 - 兼容性方法"""
        try:
            df = self.tushare_client.get_etf_daily_data(code, start_date, end_date)
            if df is None or df.empty:
                return pd.DataFrame()
            
            # 确保列名兼容性
            if 'trade_date' in df.columns:
                df = df.rename(columns={'trade_date': 'date'})
            if 'vol' in df.columns:
                df = df.rename(columns={'vol': 'volume'})
            
            return df
            
        except Exception as e:
            logger.error(f"获取日线数据失败 {code}: {str(e)}")
            return pd.DataFrame()
