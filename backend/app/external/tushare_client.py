"""
Tushare API客户端模块

提供与Tushare Pro API的交互接口
"""

import logging
import tushare as ts
from typing import Optional, Dict, Any
import pandas as pd

from ..config.settings import Settings
from ..exceptions.business_exceptions import ExternalAPIError, ConfigurationError

logger = logging.getLogger(__name__)


class TushareClient:
    """Tushare API客户端"""
    
    def __init__(self, settings: Settings):
        """
        初始化Tushare客户端
        
        Args:
            settings: 应用配置
        """
        self.settings = settings
        self._pro_api = None
        self._initialize_client()
    
    def _initialize_client(self):
        """初始化Tushare Pro API客户端"""
        if not self.settings.TUSHARE_TOKEN:
            raise ConfigurationError("Tushare token未配置")
        
        try:
            # 设置token
            ts.set_token(self.settings.TUSHARE_TOKEN)
            
            # 初始化pro接口
            self._pro_api = ts.pro_api()
            
            logger.info("Tushare Pro API初始化成功")
        except Exception as e:
            logger.error(f"Tushare Pro API初始化失败: {e}")
            raise ConfigurationError(f"Tushare API初始化失败: {e}")
    
    @property
    def pro_api(self):
        """获取Tushare Pro API实例"""
        if self._pro_api is None:
            self._initialize_client()
        return self._pro_api
    
    def get_etf_basic_info(self, etf_code: str = None) -> pd.DataFrame:
        """
        获取ETF基本信息
        
        Args:
            etf_code: ETF代码（6位数字，不含市场后缀），如果为None则获取所有ETF
            
        Returns:
            pd.DataFrame: ETF基本信息
        """
        try:
            # 如果提供了ETF代码，需要补全市场后缀
            ts_code = None
            if etf_code:
                ts_code = self._complete_etf_code(etf_code)
            
            df = self.pro_api.fund_basic(
                ts_code=ts_code,
                market='E',  # ETF
                fields='ts_code,name,management,custodian,fund_type,found_date,due_date,list_date,issue_date,delist_date,issue_amount,m_fee,c_fee,duration_year,p_value,min_amount,benchmark'
            )
            
            if df.empty:
                logger.warning(f"未获取到ETF基本信息: {etf_code}")
            else:
                logger.debug(f"获取ETF基本信息成功: {len(df)}条记录")
            
            return df
            
        except Exception as e:
            logger.error(f"获取ETF基本信息失败: {e}")
            raise ExternalAPIError(f"获取ETF基本信息失败: {e}")
    
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
    
    def get_etf_daily_data(self, etf_code: str, start_date: str = None, 
                          end_date: str = None) -> pd.DataFrame:
        """
        获取ETF日线数据
        
        Args:
            etf_code: ETF代码（6位数字，不含市场后缀）
            start_date: 开始日期 (YYYYMMDD格式)
            end_date: 结束日期 (YYYYMMDD格式)
            
        Returns:
            pd.DataFrame: ETF日线数据
        """
        try:
            # 补全市场后缀
            ts_code = self._complete_etf_code(etf_code)
            
            df = self.pro_api.fund_daily(
                ts_code=ts_code,
                start_date=start_date,
                end_date=end_date
            )
            
            if df.empty:
                logger.warning(f"未获取到ETF日线数据: {etf_code}, {start_date}-{end_date}")
            else:
                logger.debug(f"获取ETF日线数据成功: {etf_code}, {len(df)}条记录")
            
            return df
            
        except Exception as e:
            logger.error(f"获取ETF日线数据失败: {e}")
            raise ExternalAPIError(f"获取ETF日线数据失败: {e}")
    
    def get_trading_calendar(self, exchange: str = 'SSE', start_date: str = None,
                           end_date: str = None, is_open: str = '1') -> pd.DataFrame:
        """
        获取交易日历
        
        Args:
            exchange: 交易所代码 (SSE上交所, SZSE深交所)
            start_date: 开始日期 (YYYYMMDD格式)
            end_date: 结束日期 (YYYYMMDD格式)
            is_open: 是否交易日 ('1'是, '0'否)
            
        Returns:
            pd.DataFrame: 交易日历数据
        """
        try:
            df = self.pro_api.trade_cal(
                exchange=exchange,
                start_date=start_date,
                end_date=end_date,
                is_open=is_open
            )
            
            if df.empty:
                logger.warning(f"未获取到交易日历: {exchange}, {start_date}-{end_date}")
            else:
                logger.debug(f"获取交易日历成功: {exchange}, {len(df)}条记录")
            
            return df
            
        except Exception as e:
            logger.error(f"获取交易日历失败: {e}")
            raise ExternalAPIError(f"获取交易日历失败: {e}")
    
    def get_index_daily_data(self, ts_code: str, start_date: str = None,
                           end_date: str = None) -> pd.DataFrame:
        """
        获取指数日线数据
        
        Args:
            ts_code: 指数代码
            start_date: 开始日期 (YYYYMMDD格式)
            end_date: 结束日期 (YYYYMMDD格式)
            
        Returns:
            pd.DataFrame: 指数日线数据
        """
        try:
            df = self.pro_api.index_daily(
                ts_code=ts_code,
                start_date=start_date,
                end_date=end_date
            )
            
            if df.empty:
                logger.warning(f"未获取到指数日线数据: {ts_code}, {start_date}-{end_date}")
            else:
                logger.debug(f"获取指数日线数据成功: {ts_code}, {len(df)}条记录")
            
            return df
            
        except Exception as e:
            logger.error(f"获取指数日线数据失败: {e}")
            raise ExternalAPIError(f"获取指数日线数据失败: {e}")
    
    def test_connection(self) -> bool:
        """
        测试API连接
        
        Returns:
            bool: 连接是否正常
        """
        try:
            # 尝试获取少量数据来测试连接
            df = self.pro_api.trade_cal(
                exchange='SSE',
                start_date='20240101',
                end_date='20240101'
            )
            
            logger.info("Tushare API连接测试成功")
            return True
            
        except Exception as e:
            logger.error(f"Tushare API连接测试失败: {e}")
            return False
    
    def get_api_usage_info(self) -> Dict[str, Any]:
        """
        获取API使用情况信息
        
        Returns:
            dict: API使用情况
        """
        try:
            # 注意：这个功能需要根据实际的Tushare API文档调整
            # 目前Tushare可能没有直接的API使用情况查询接口
            return {
                'status': 'connected',
                'token_configured': bool(self.settings.TUSHARE_TOKEN),
                'api_initialized': self._pro_api is not None
            }
        except Exception as e:
            logger.error(f"获取API使用情况失败: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }