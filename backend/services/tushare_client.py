import os
import tushare as ts
import pandas as pd
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from .enhanced_cache import EnhancedCache, TradingDateManager

logger = logging.getLogger(__name__)


class TushareClient:
    """Tushare数据客户端 - 使用增强缓存策略"""
    
    def __init__(self, cache_dir: str = "cache"):
        """初始化Tushare客户端"""
        self.token = os.getenv('TUSHARE_TOKEN')
        if not self.token:
            raise ValueError("TUSHARE_TOKEN环境变量未设置")
        
        ts.set_token(self.token)
        self.pro = ts.pro_api()
        
        # 初始化增强缓存管理器
        self.cache = EnhancedCache(cache_dir)
        
        # 初始化交易日管理器
        self.trading_date_manager = TradingDateManager(self.cache)
        
        logger.info("Tushare客户端初始化成功（增强缓存版本）")
    
    def get_etf_daily_data(self, etf_code: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """
        获取ETF日线数据（历史数据范围缓存）
        
        Args:
            etf_code: ETF代码（不含市场后缀）
            start_date: 开始日期 (YYYYMMDD格式)
            end_date: 结束日期 (YYYYMMDD格式)
            
        Returns:
            DataFrame: ETF日线数据
        """
        # 1. 先检查历史数据缓存
        cached_data = self.cache.get_historical_cache(etf_code, start_date, end_date)
        if cached_data:
            logger.info(f"✓ 从历史缓存获取ETF {etf_code} 日线数据 ({start_date}~{end_date})")
            # 将缓存的字典数据转换回DataFrame
            df = pd.DataFrame(cached_data)
            # 确保trade_date是datetime类型
            df['trade_date'] = pd.to_datetime(df['trade_date'])
            return df
        
        # 2. 缓存未命中，调用接口
        logger.info(f"→ 历史缓存未命中，请求tushare接口获取ETF {etf_code} 日线数据 ({start_date}~{end_date})")
        
        try:
            # 自动补全市场后缀
            full_code = self._complete_etf_code(etf_code)
            
            # 获取ETF日线数据
            df = self.pro.fund_daily(
                ts_code=full_code,
                start_date=start_date,
                end_date=end_date,
                fields='ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount'
            )
            
            if df.empty:
                logger.warning(f"✗ tushare接口返回空数据，ETF {etf_code} 日线数据获取失败")
                return None
            
            # 数据预处理
            df['trade_date'] = pd.to_datetime(df['trade_date'])
            df = df.sort_values('trade_date')
            df = df.reset_index(drop=True)
            
            # 计算日振幅
            df['amplitude'] = (df['high'] - df['low']) / df['pre_close'] * 100
            
            # 3. 成功获取数据，保存到历史缓存（转换为字典格式）
            cache_data = df.to_dict('records')
            self.cache.set_historical_cache(etf_code, start_date, end_date, cache_data)
            logger.info(f"✓ ETF {etf_code} 日线数据获取成功并已缓存，共{len(df)}条记录")
            
            return df
            
        except Exception as e:
            logger.error(f"✗ 请求tushare接口失败，ETF {etf_code} 日线数据获取失败: {str(e)}")
            return None
    
    def get_etf_basic_info(self, etf_code: str) -> Optional[Dict]:
        """
        获取ETF基本信息（永久缓存）
        
        Args:
            etf_code: ETF代码（不含市场后缀）
            
        Returns:
            Dict: ETF基本信息
        """
        # 1. 先检查永久缓存
        cached_data = self.cache.get_permanent_cache("etf_basic", etf_code)
        if cached_data:
            logger.info(f"✓ 从永久缓存获取ETF {etf_code} 基本信息")
            return cached_data
        
        # 2. 缓存未命中，调用接口
        logger.info(f"→ 永久缓存未命中，请求tushare接口获取ETF {etf_code} 基本信息")
        
        try:
            # 自动补全市场后缀
            full_code = self._complete_etf_code(etf_code)
            
            # 获取ETF基本信息
            df = self.pro.fund_basic(
                ts_code=full_code,
                market='E',  # ETF市场
                fields='ts_code,name,management,found_date,list_date,issue_amount,'
                       'm_fee,c_fee,track_index_code,track_index_name'
            )
            
            if df.empty:
                logger.warning(f"✗ tushare接口返回空数据，ETF {etf_code} 基本信息获取失败")
                return None
            
            basic_info = df.iloc[0].to_dict()
            
            # 3. 成功获取数据，保存到永久缓存
            self.cache.set_permanent_cache("etf_basic", etf_code, basic_info)
            logger.info(f"✓ ETF {etf_code} 基本信息获取成功并已永久缓存")
            
            return basic_info
            
        except Exception as e:
            logger.error(f"✗ 请求tushare接口失败，ETF {etf_code} 基本信息获取失败: {str(e)}")
            return None
    
    def get_latest_price(self, etf_code: str) -> Optional[Dict]:
        """
        获取ETF最新价格（智能交易日缓存）
        
        Args:
            etf_code: ETF代码（不含市场后缀）
            
        Returns:
            Dict: 最新价格信息
        """
        # 1. 获取最近的交易日
        latest_trading_date = self.trading_date_manager.get_latest_trading_date(self.pro)
        
        # 2. 检查该交易日的缓存
        cached_data = self.cache.get_daily_cache(latest_trading_date, "price", etf_code)
        if cached_data:
            logger.info(f"✓ 从交易日缓存获取ETF {etf_code} 最新价格 (交易日: {latest_trading_date})")
            return cached_data
        
        # 3. 缓存未命中，调用接口
        logger.info(f"→ 交易日缓存未命中，请求tushare接口获取ETF {etf_code} 最新价格")
        
        try:
            # 自动补全市场后缀
            full_code = self._complete_etf_code(etf_code)
            
            # 获取最近90天的数据，取最新的一条
            end_date = datetime.now()
            start_date = end_date - timedelta(days=90)
            
            # 获取最近的价格数据，按日期倒序排列
            df = self.pro.fund_daily(
                ts_code=full_code,
                start_date=start_date.strftime('%Y%m%d'),
                end_date=end_date.strftime('%Y%m%d'),
                fields='ts_code,trade_date,close,pre_close,pct_chg,vol,amount'
            )
            
            if df.empty:
                logger.warning(f"✗ tushare接口返回空数据，ETF {etf_code} 最新价格获取失败")
                return None
            
            # 按交易日期排序，取最新的数据
            df = df.sort_values('trade_date', ascending=False)
            latest_data = df.iloc[0]
            
            # 验证并提取实际的交易日期
            actual_trade_date = self.trading_date_manager.validate_trade_date(latest_data.to_dict())
            if not actual_trade_date:
                logger.error(f"✗ 无法从tushare返回数据中提取有效交易日期: {latest_data['trade_date']}")
                return None
            
            # 检查数据是否太旧（超过30天）
            latest_date = pd.to_datetime(latest_data['trade_date'])
            days_diff = (datetime.now() - latest_date).days
            
            if days_diff > 30:
                logger.warning(f"ETF {etf_code} 的最新数据已过期（{days_diff}天前）")
            
            price_info = {
                'current_price': float(latest_data['close']),
                'pre_close': float(latest_data['pre_close']),
                'pct_change': float(latest_data['pct_chg']),
                'volume': int(latest_data['vol']),
                'amount': float(latest_data['amount']),
                'trade_date': actual_trade_date,
                'data_age_days': days_diff  # 添加数据年龄信息
            }
            
            # 4. 成功获取数据，按实际交易日缓存
            self.cache.set_daily_cache(actual_trade_date, "price", etf_code, price_info)
            logger.info(f"✓ ETF {etf_code} 最新价格获取成功并已缓存 (实际交易日: {actual_trade_date})")
            
            return price_info
            
        except Exception as e:
            logger.error(f"✗ 请求tushare接口失败，ETF {etf_code} 最新价格获取失败: {str(e)}")
            return None
    
    def search_etf(self, query: str) -> List[Dict]:
        """
        搜索ETF - 不使用缓存，保持实时性
        
        Args:
            query: 搜索关键词（ETF代码或名称）
            
        Returns:
            List[Dict]: ETF列表
        """
        logger.info(f"→ 搜索ETF: '{query}' (不使用缓存)")
        
        try:
            # 获取所有ETF基本信息
            df = self.pro.fund_basic(
                market='E',  # ETF市场
                fields='ts_code,name,management,found_date,list_date'
            )
            
            if df.empty:
                logger.warning(f"✗ 搜索ETF '{query}' 返回空结果")
                return []
            
            # 根据查询条件过滤
            query = query.upper()
            filtered_df = df[
                df['ts_code'].str.contains(query, na=False) |
                df['name'].str.contains(query, na=False)
            ]
            
            # 转换为列表格式
            etf_list = []
            for _, row in filtered_df.head(10).iterrows():
                etf_list.append({
                    'ts_code': row['ts_code'],
                    'code': row['ts_code'].split('.')[0],  # 不含市场后缀
                    'name': row['name'],
                    'management': row['management'],
                    'found_date': row['found_date'],
                    'list_date': row['list_date']
                })
            
            logger.info(f"✓ 搜索ETF '{query}' 成功，找到{len(etf_list)}个结果")
            return etf_list
            
        except Exception as e:
            logger.error(f"✗ 搜索ETF '{query}' 失败: {str(e)}")
            return []
    
    def _complete_etf_code(self, etf_code: str) -> str:
        """
        自动补全ETF代码的市场后缀
        
        Args:
            etf_code: ETF代码（不含市场后缀）
            
        Returns:
            str: 完整的ETF代码（含市场后缀）
        """
        # 移除可能存在的后缀
        etf_code = etf_code.split('.')[0]
        
        # 判断市场：15/16/18开头的是深交所，51/58开头的是上交所
        if etf_code.startswith(('15', '16', '18')):
            return f"{etf_code}.SZ"
        elif etf_code.startswith(('51', '58')):
            return f"{etf_code}.SH"
        else:
            # 默认上交所
            return f"{etf_code}.SH"
    
    def get_etf_name(self, etf_code: str) -> Optional[str]:
        """
        轻量级获取ETF名称（永久缓存）
        
        Args:
            etf_code: ETF代码（不含市场后缀）
            
        Returns:
            str: ETF名称，如果获取失败返回None
        """
        # 1. 先检查永久缓存
        cached_data = self.cache.get_permanent_cache("etf_name", etf_code)
        if cached_data:
            logger.info(f"✓ 从永久缓存获取ETF {etf_code} 名称")
            return cached_data
        
        # 2. 缓存未命中，调用接口
        logger.info(f"→ 永久缓存未命中，请求tushare接口获取ETF {etf_code} 名称")
        
        try:
            # 自动补全市场后缀
            full_code = self._complete_etf_code(etf_code)
            
            # 只获取基本信息中的名称字段
            df = self.pro.fund_basic(
                ts_code=full_code,
                market='E',  # ETF市场
                fields='ts_code,name'
            )
            
            if df.empty:
                logger.warning(f"✗ tushare接口返回空数据，ETF {etf_code} 名称获取失败")
                return None
            
            etf_name = df.iloc[0]['name']
            
            # 3. 成功获取数据，保存到永久缓存
            self.cache.set_permanent_cache("etf_name", etf_code, etf_name)
            logger.info(f"✓ ETF {etf_code} 名称获取成功并已永久缓存: {etf_name}")
            
            return etf_name
            
        except Exception as e:
            logger.error(f"✗ 请求tushare接口失败，ETF {etf_code} 名称获取失败: {str(e)}")
            return None

    def get_trading_calendar(self, start_date: str, end_date: str) -> List[str]:
        """
        获取交易日历（兼容性方法，实际使用TradingDateManager）
        
        Args:
            start_date: 开始日期 (YYYYMMDD格式)
            end_date: 结束日期 (YYYYMMDD格式)
            
        Returns:
            List[str]: 交易日列表
        """
        try:
            # 解析年份范围
            start_year = int(start_date[:4])
            end_year = int(end_date[:4])
            
            all_trading_days = []
            
            # 按年获取交易日历
            for year in range(start_year, end_year + 1):
                year_calendar = self.trading_date_manager._get_trading_calendar(self.pro, year)
                all_trading_days.extend(year_calendar)
            
            # 过滤指定日期范围
            filtered_days = [day for day in all_trading_days if start_date <= day <= end_date]
            
            logger.info(f"✓ 获取交易日历成功 ({start_date}~{end_date})，共{len(filtered_days)}个交易日")
            return filtered_days
            
        except Exception as e:
            logger.error(f"✗ 获取交易日历失败: {str(e)}")
            return []
    
    def get_cache_info(self) -> Dict:
        """
        获取缓存统计信息
        
        Returns:
            Dict: 缓存统计信息
        """
        return self.cache.get_cache_info()
    
    def get_latest_trading_date(self) -> str:
        """
        获取最近的交易日
        
        Returns:
            str: 最近的交易日 (YYYYMMDD格式)
        """
        return self.trading_date_manager.get_latest_trading_date(self.pro)
