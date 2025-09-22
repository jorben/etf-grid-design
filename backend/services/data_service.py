"""
数据获取服务
整合Tushare API，提供ETF数据获取功能
支持模拟数据用于开发测试
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
        self.use_mock_data = False
        
        if not self.token or self.token == 'your_tushare_token_here':
            logger.warning("未配置有效的TUSHARE_TOKEN，将使用模拟数据进行开发测试")
            self.use_mock_data = True
            self.pro = None
        else:
            try:
                ts.set_token(self.token)
                self.pro = ts.pro_api()
                logger.info("Tushare API初始化成功")
            except Exception as e:
                logger.error(f"Tushare API初始化失败: {str(e)}，将使用模拟数据")
                self.use_mock_data = True
                self.pro = None
        
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
        if self.use_mock_data:
            return self._get_mock_fund_basic(code)
        
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
        if self.use_mock_data:
            return self._get_mock_current_price(code)
        
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
        if self.use_mock_data:
            return self._get_mock_daily_data(code, start_date, end_date)
        
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
        if self.use_mock_data:
            # 模拟搜索
            results = []
            for etf in self.popular_etfs:
                if keyword.lower() in etf['name'].lower() or keyword in etf['code']:
                    results.append(etf)
            return results[:10]  # 返回前10个结果
        
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
    
    def _get_mock_fund_basic(self, code: str) -> Dict:
        """获取模拟基金基础信息"""
        # 查找热门ETF列表中的信息
        for etf in self.popular_etfs:
            if etf['code'] == code:
                return {
                    'name': etf['name'],
                    'management': '模拟基金公司',
                    'setup_date': '20100101',
                    'list_date': '20100101',
                    'fund_type': 'ETF',
                    'status': 'L'
                }
        
        # 默认信息
        return {
            'name': f'模拟ETF{code}',
            'management': '模拟基金公司',
            'setup_date': '20100101',
            'list_date': '20100101',
            'fund_type': 'ETF',
            'status': 'L'
        }
    
    def _get_mock_current_price(self, code: str) -> Dict:
        """获取模拟当前价格"""
        # 基于代码生成模拟价格
        base_price = float(code) / 100000  # 简单的价格生成逻辑
        base_price = max(base_price, 1.0)  # 确保价格合理
        
        # 根据ETF类型生成更真实的成交数据
        if code in ['510300', '159919']:  # 沪深300ETF
            vol = int(np.random.uniform(500000, 2000000))  # 50万-200万手
            amount = vol * base_price * np.random.uniform(8, 15)  # 成交额放大
        elif code in ['510500', '159915', '512100']:  # 其他主要宽基ETF
            vol = int(np.random.uniform(200000, 800000))  # 20万-80万手
            amount = vol * base_price * np.random.uniform(5, 10)
        elif code.startswith(('515', '516', '512')):  # 行业主题ETF
            vol = int(np.random.uniform(50000, 300000))  # 5万-30万手
            amount = vol * base_price * np.random.uniform(3, 8)
        else:  # 其他ETF
            vol = int(np.random.uniform(10000, 100000))  # 1万-10万手
            amount = vol * base_price * np.random.uniform(2, 5)
        
        return {
            'close': round(base_price, 3),
            'pct_chg': round(np.random.uniform(-3, 3), 2),
            'vol': vol,
            'amount': int(amount)
        }
    
    def _get_mock_daily_data(self, code: str, start_date: str, end_date: str) -> pd.DataFrame:
        """生成模拟日线数据"""
        start = datetime.strptime(start_date, '%Y%m%d')
        end = datetime.strptime(end_date, '%Y%m%d')
        
        # 生成交易日期（排除周末）
        dates = []
        current = start
        while current <= end:
            if current.weekday() < 5:  # 周一到周五
                dates.append(current)
            current += timedelta(days=1)
        
        if not dates:
            return pd.DataFrame()
        
        # 基于代码生成基础价格
        base_price = float(code) / 100000
        base_price = max(base_price, 1.0)
        
        # 生成价格序列（随机游走）
        n_days = len(dates)
        returns = np.random.normal(0.0005, 0.02, n_days)  # 日收益率
        prices = [base_price]
        
        for i in range(1, n_days):
            new_price = prices[-1] * (1 + returns[i])
            prices.append(max(new_price, 0.1))  # 确保价格为正
        
        # 生成OHLC数据
        data = []
        for i, (date, close) in enumerate(zip(dates, prices)):
            # 生成开盘价（基于前一日收盘价）
            if i == 0:
                open_price = close * np.random.uniform(0.98, 1.02)
            else:
                open_price = prices[i-1] * np.random.uniform(0.98, 1.02)
            
            # 生成最高价和最低价
            high = max(open_price, close) * np.random.uniform(1.0, 1.03)
            low = min(open_price, close) * np.random.uniform(0.97, 1.0)
            
            # 根据ETF类型生成更真实的成交量和成交额
            if code in ['510300', '159919']:  # 沪深300ETF
                volume = int(np.random.uniform(500000, 2000000))  # 50万-200万手
                amount = volume * close * np.random.uniform(8, 15)  # 成交额放大
            elif code in ['510500', '159915', '512100']:  # 其他主要宽基ETF
                volume = int(np.random.uniform(200000, 800000))  # 20万-80万手
                amount = volume * close * np.random.uniform(5, 10)
            elif code.startswith(('515', '516', '512')):  # 行业主题ETF
                volume = int(np.random.uniform(50000, 300000))  # 5万-30万手
                amount = volume * close * np.random.uniform(3, 8)
            else:  # 其他ETF
                volume = int(np.random.uniform(10000, 100000))  # 1万-10万手
                amount = volume * close * np.random.uniform(2, 5)
            
            data.append({
                'date': date,
                'open': round(open_price, 3),
                'high': round(high, 3),
                'low': round(low, 3),
                'close': round(close, 3),
                'volume': volume,
                'amount': round(amount, 2)
            })
        
        return pd.DataFrame(data)
