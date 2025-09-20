import os
import tushare as ts
import pandas as pd
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)


class TushareClient:
    """Tushare数据客户端"""
    
    def __init__(self):
        """初始化Tushare客户端"""
        self.token = os.getenv('TUSHARE_TOKEN')
        if not self.token:
            raise ValueError("TUSHARE_TOKEN环境变量未设置")
        
        ts.set_token(self.token)
        self.pro = ts.pro_api()
        logger.info("Tushare客户端初始化成功")
    
    def get_etf_daily_data(self, etf_code: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """
        获取ETF日线数据
        
        Args:
            etf_code: ETF代码（不含市场后缀）
            start_date: 开始日期 (YYYYMMDD格式)
            end_date: 结束日期 (YYYYMMDD格式)
            
        Returns:
            DataFrame: ETF日线数据
        """
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
                logger.warning(f"未获取到ETF {etf_code} 的数据")
                return None
            
            # 数据预处理
            df['trade_date'] = pd.to_datetime(df['trade_date'])
            df = df.sort_values('trade_date')
            df = df.reset_index(drop=True)
            
            # 计算日振幅
            df['amplitude'] = (df['high'] - df['low']) / df['pre_close'] * 100
            
            logger.info(f"成功获取ETF {etf_code} 的日线数据，共{len(df)}条记录")
            return df
            
        except Exception as e:
            logger.error(f"获取ETF {etf_code} 数据失败: {str(e)}")
            return None
    
    def get_etf_basic_info(self, etf_code: str) -> Optional[Dict]:
        """
        获取ETF基本信息
        
        Args:
            etf_code: ETF代码（不含市场后缀）
            
        Returns:
            Dict: ETF基本信息
        """
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
                logger.warning(f"未找到ETF {etf_code} 的基本信息")
                return None
            
            # 获取最新价格
            latest_data = self.get_latest_price(etf_code)
            if not latest_data:
                return None
            
            basic_info = df.iloc[0].to_dict()
            basic_info.update(latest_data)
            
            logger.info(f"成功获取ETF {etf_code} 的基本信息")
            return basic_info
            
        except Exception as e:
            logger.error(f"获取ETF {etf_code} 基本信息失败: {str(e)}")
            return None
    
    def get_latest_price(self, etf_code: str) -> Optional[Dict]:
        """
        获取ETF最新价格
        
        Args:
            etf_code: ETF代码（不含市场后缀）
            
        Returns:
            Dict: 最新价格信息
        """
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
                logger.warning(f"未获取到ETF {etf_code} 的最新价格")
                return None
            
            # 按交易日期排序，取最新的数据
            df = df.sort_values('trade_date', ascending=False)
            latest_data = df.iloc[0]
            
            # 检查数据是否太旧（超过30天）
            latest_date = pd.to_datetime(latest_data['trade_date'])
            days_diff = (datetime.now() - latest_date).days
            
            if days_diff > 30:
                logger.warning(f"ETF {etf_code} 的最新数据已过期（{days_diff}天前）")
                # 仍然返回数据，但记录警告
            
            return {
                'current_price': float(latest_data['close']),
                'pre_close': float(latest_data['pre_close']),
                'pct_change': float(latest_data['pct_chg']),
                'volume': int(latest_data['vol']),
                'amount': float(latest_data['amount']),
                'trade_date': latest_data['trade_date'],
                'data_age_days': days_diff  # 添加数据年龄信息
            }
            
        except Exception as e:
            logger.error(f"获取ETF {etf_code} 最新价格失败: {str(e)}")
            return None
    
    def search_etf(self, query: str) -> List[Dict]:
        """
        搜索ETF
        
        Args:
            query: 搜索关键词（ETF代码或名称）
            
        Returns:
            List[Dict]: ETF列表
        """
        try:
            # 获取所有ETF基本信息
            df = self.pro.fund_basic(
                market='E',  # ETF市场
                fields='ts_code,name,management,found_date,list_date'
            )
            
            if df.empty:
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
            
            logger.info(f"搜索ETF '{query}'，找到{len(etf_list)}个结果")
            return etf_list
            
        except Exception as e:
            logger.error(f"搜索ETF失败: {str(e)}")
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
    
    def get_trading_calendar(self, start_date: str, end_date: str) -> List[str]:
        """
        获取交易日历
        
        Args:
            start_date: 开始日期 (YYYYMMDD格式)
            end_date: 结束日期 (YYYYMMDD格式)
            
        Returns:
            List[str]: 交易日列表
        """
        try:
            df = self.pro.trade_cal(
                exchange='SSE',
                start_date=start_date,
                end_date=end_date,
                is_open='1'
            )
            
            if df.empty:
                return []
            
            return df['cal_date'].tolist()
            
        except Exception as e:
            logger.error(f"获取交易日历失败: {str(e)}")
            return []
