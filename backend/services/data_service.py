"""
数据获取服务
整合Tushare API，提供ETF数据获取功能
"""

import tushare as ts
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import os
from cachetools import TTLCache
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataService:
    """数据获取服务类"""
    
    def __init__(self):
        """初始化数据服务"""
        # 从环境变量获取Tushare token
        self.token = os.getenv('TUSHARE_TOKEN')
        
        if not self.token or self.token == 'your_tushare_token_here':
            raise ValueError("必须配置有效的TUSHARE_TOKEN环境变量才能使用本系统")
        
        try:
            ts.set_token(self.token)
            self.pro = ts.pro_api()
            logger.info("Tushare API初始化成功")
        except Exception as e:
            logger.error(f"Tushare API初始化失败: {str(e)}")
            raise RuntimeError(f"Tushare API初始化失败: {str(e)}")
        
        # 初始化缓存（TTL=1小时）
        self.cache = TTLCache(maxsize=1000, ttl=3600)
        
        # 热门ETF列表
        self.popular_etfs = [
            {'code': '510300', 'name': '沪深300ETF', 'type': '宽基指数'},
            {'code': '510500', 'name': '中证500ETF', 'type': '宽基指数'},
            {'code': '159919', 'name': '沪深300ETF', 'type': '宽基指数'},
            {'code': '159915', 'name': '创业板ETF', 'type': '宽基指数'},
            {'code': '512100', 'name': '中证1000ETF', 'type': '宽基指数'},
            {'code': '515050', 'name': '5G ETF', 'type': '行业主题'},
            {'code': '512880', 'name': '证券ETF', 'type': '行业主题'},
            {'code': '512170', 'name': '医疗ETF', 'type': '行业主题'},
            {'code': '515790', 'name': '光伏ETF', 'type': '行业主题'},
            {'code': '516160', 'name': '新能源ETF', 'type': '行业主题'},
            {'code': '159941', 'name': '纳斯达克100ETF', 'type': '海外指数'},
            {'code': '513100', 'name': '纳斯达克ETF', 'type': '海外指数'},
            {'code': '518880', 'name': '黄金ETF', 'type': '商品'},
            {'code': '159934', 'name': '黄金ETF', 'type': '商品'},
            {'code': '511010', 'name': '国债ETF', 'type': '债券'}
        ]
    
    def get_fund_basic(self, code: str) -> Dict:
        """获取基金基础信息"""
        ts_code = self._convert_to_ts_code(code)
        cache_key = f"fund_basic_{ts_code}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            fund_basic = self.pro.fund_basic(ts_code=ts_code)
            if fund_basic.empty:
                return None
            
            info = fund_basic.iloc[0]
            result = {
                'name': info['name'],
                'management': info['management'],
                'setup_date': info.get('found_date', ''),
                'list_date': info.get('list_date', ''),
                'fund_type': info.get('fund_type', 'ETF'),
                'status': info.get('status', 'L')
            }
            
            self.cache[cache_key] = result
            return result
            
        except Exception as e:
            logger.error(f"获取基金基础信息失败 {code}: {str(e)}")
            return None
    
    def get_current_price(self, code: str) -> Dict:
        """获取当前价格信息"""
        ts_code = self._convert_to_ts_code(code)
        
        try:
            # 获取最近5个交易日的数据
            end_date = datetime.now().strftime('%Y%m%d')
            start_date = (datetime.now() - timedelta(days=10)).strftime('%Y%m%d')
            
            df = self.pro.fund_daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
            if df.empty:
                return {'close': 0, 'pct_chg': 0, 'vol': 0, 'amount': 0}
            
            latest = df.iloc[0]
            return {
                'close': latest['close'],
                'pct_chg': latest.get('pct_chg', 0),
                'vol': latest.get('vol', 0),
                'amount': latest.get('amount', 0)
            }
            
        except Exception as e:
            logger.error(f"获取当前价格失败 {code}: {str(e)}")
            return {'close': 0, 'pct_chg': 0, 'vol': 0, 'amount': 0}
    
    def get_daily_data(self, code: str, start_date: str, end_date: str) -> pd.DataFrame:
        """获取日线数据"""
        ts_code = self._convert_to_ts_code(code)
        cache_key = f"daily_{ts_code}_{start_date}_{end_date}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            df = self.pro.fund_daily(
                ts_code=ts_code,
                start_date=start_date,
                end_date=end_date
            )
            
            if df.empty:
                return pd.DataFrame()
            
            # 数据清洗和格式化
            df = df.sort_values('trade_date').reset_index(drop=True)
            df['trade_date'] = pd.to_datetime(df['trade_date'])
            
            # 重命名列以匹配标准格式
            df = df.rename(columns={
                'trade_date': 'date',
                'vol': 'volume'
            })
            
            self.cache[cache_key] = df
            return df
            
        except Exception as e:
            logger.error(f"获取日线数据失败 {code}: {str(e)}")
            return pd.DataFrame()
    
    def get_popular_etfs(self) -> List[Dict]:
        """获取热门ETF列表"""
        return self.popular_etfs
    
    def search_etf(self, keyword: str) -> List[Dict]:
        """搜索ETF"""
        try:
            # 使用Tushare搜索
            df = self.pro.fund_basic(market='E')  # ETF基金
            if df.empty:
                return []
            
            # 按名称或代码搜索
            mask = df['name'].str.contains(keyword, na=False) | df['ts_code'].str.contains(keyword, na=False)
            results = df[mask].head(10)
            
            return [
                {
                    'code': row['ts_code'][:6],
                    'name': row['name'],
                    'type': row.get('fund_type', 'ETF')
                }
                for _, row in results.iterrows()
            ]
            
        except Exception as e:
            logger.error(f"搜索ETF失败: {str(e)}")
            return []
    
    def _convert_to_ts_code(self, code: str) -> str:
        """将6位ETF代码转换为Tushare格式"""
        if code.startswith(('51', '58')):
            return f"{code}.SH"
        elif code.startswith(('15', '16')):
            return f"{code}.SZ"
        else:
            return f"{code}.SH"
