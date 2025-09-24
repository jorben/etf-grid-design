"""
ETF服务模块

提供ETF数据获取、缓存和基本信息管理功能
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import pandas as pd

from ..config.settings import Settings
from ..models.etf_models import ETFBasicInfo, ETFPriceData, PopularETF
from ..external.tushare_client import TushareClient
from ..services.file_cache_service import FileCacheService, TradingDateManager
from ..exceptions.business_exceptions import ETFNotFoundError, DataValidationError
from ..utils.validators import validate_etf_code, validate_date_format
from ..utils.formatters import format_currency, format_percentage

logger = logging.getLogger(__name__)


class ETFService:
    """ETF服务"""
    
    def __init__(self, settings: Settings, tushare_client: TushareClient, 
                 cache_service: FileCacheService):
        """
        初始化ETF服务
        
        Args:
            settings: 应用配置
            tushare_client: Tushare客户端
            cache_service: 缓存服务
        """
        self.settings = settings
        self.tushare_client = tushare_client
        self.cache_service = cache_service
        self.trading_date_manager = TradingDateManager(cache_service)
    
    def get_popular_etfs(self) -> List[PopularETF]:
        """
        获取热门ETF列表
        
        Returns:
            List[PopularETF]: 热门ETF列表
        """
        try:
            # 先从缓存获取
            cached_data = self.cache_service.get_permanent_cache("popular_etfs", "list")
            if cached_data:
                logger.debug("从缓存获取热门ETF列表")
                return [PopularETF(**item) for item in cached_data]
            
            # 缓存未命中，从配置获取并补充基本信息
            popular_etfs = []
            
            for etf_info in self.settings.POPULAR_ETFS:
                etf_code = etf_info['code']
                etf_name = etf_info['name']
                etf_category = etf_info['category']
                
                try:
                    # 获取基本信息
                    basic_info = self.get_etf_basic_info(etf_code)
                    
                    popular_etf = PopularETF(
                        code=etf_code,
                        name=etf_name,
                        category=etf_category
                    )
                    popular_etfs.append(popular_etf)
                    
                except Exception as e:
                    logger.warning(f"获取ETF {etf_code} 信息失败: {e}")
                    # 使用基本信息
                    popular_etf = PopularETF(
                        code=etf_code,
                        name=etf_name,
                        category=etf_category
                    )
                    popular_etfs.append(popular_etf)
            
            # 保存到缓存
            cache_data = [etf.__dict__ for etf in popular_etfs]
            self.cache_service.set_permanent_cache("popular_etfs", "list", cache_data)
            
            logger.info(f"获取热门ETF列表成功: {len(popular_etfs)}个")
            return popular_etfs
            
        except Exception as e:
            logger.error(f"获取热门ETF列表失败: {e}")
            # 返回基本的ETF列表
            return [
                PopularETF(
                    code=etf_info['code'],
                    name=etf_info['name'],
                    category=etf_info['category']
                )
                for etf_info in self.settings.POPULAR_ETFS
            ]
    
    def get_etf_basic_info(self, etf_code: str) -> Optional[ETFBasicInfo]:
        """
        获取ETF基本信息
        
        Args:
            etf_code: ETF代码
            
        Returns:
            ETFBasicInfo: ETF基本信息
        """
        if not validate_etf_code(etf_code):
            raise DataValidationError(f"无效的ETF代码: {etf_code}")
        
        try:
            # 先从缓存获取
            cached_data = self.cache_service.get_permanent_cache("etf_basic", etf_code)
            if cached_data:
                logger.debug(f"从缓存获取ETF基本信息: {etf_code}")
                return cached_data
            
            # 缓存未命中，从API获取
            df = self.tushare_client.get_etf_basic_info(etf_code)
            
            if df.empty:
                raise ETFNotFoundError(f"未找到ETF: {etf_code}")
            
            # 转换为数据模型
            row = df.iloc[0]
            # 从ts_code中提取6位数字代码
            ts_code = row.get('ts_code', etf_code)
            code_only = ts_code.split('.')[0] if '.' in ts_code else ts_code
            
            basic_info = ETFBasicInfo(
                code=code_only,
                name=row.get('name', ''),
                market=row.get('market', ''),
                list_date=row.get('list_date', ''),
                fund_type=row.get('fund_type', ''),
                management_fee=float(row.get('m_fee', 0)) if row.get('m_fee') else None,
                custodian_fee=float(row.get('c_fee', 0)) if row.get('c_fee') else None,
                benchmark=row.get('benchmark', '')
            )
            
            # 尝试获取最新价格信息
            try:
                latest_data = self.get_etf_latest_data(etf_code)
                if latest_data:
                    # 将最新价格信息添加到基本信息中
                    basic_info_dict = basic_info.__dict__.copy()
                    basic_info_dict.update({
                        'current_price': latest_data.close_price,
                        'pct_change': latest_data.pct_change,
                        'volume': latest_data.volume,
                        'amount': latest_data.amount,
                        'trade_date': latest_data.trade_date
                    })
                else:
                    basic_info_dict = basic_info.__dict__.copy()
                    basic_info_dict.update({
                        'current_price': None,
                        'pct_change': None,
                        'volume': None,
                        'amount': None,
                        'trade_date': None
                    })
            except Exception as e:
                logger.warning(f"获取ETF {etf_code} 最新价格失败: {e}")
                basic_info_dict = basic_info.__dict__.copy()
                basic_info_dict.update({
                    'current_price': None,
                    'pct_change': None,
                    'volume': None,
                    'amount': None,
                    'trade_date': None
                })
            
            # 添加管理方信息
            basic_info_dict['management'] = row.get('management', '')
            basic_info_dict['found_date'] = row.get('found_date', '')
            basic_info_dict['issue_amount'] = float(row.get('issue_amount', 0)) if row.get('issue_amount') else None
            
            # 保存到缓存
            self.cache_service.set_permanent_cache("etf_basic", etf_code, basic_info_dict)
            
            logger.info(f"获取ETF基本信息成功: {etf_code}")
            return basic_info_dict
            
        except ETFNotFoundError:
            raise
        except Exception as e:
            logger.error(f"获取ETF基本信息失败 {etf_code}: {e}")
            raise DataValidationError(f"获取ETF基本信息失败: {e}")
    
    def get_etf_latest_data(self, etf_code: str) -> Optional[ETFPriceData]:
        """
        获取ETF最新价格数据
        
        Args:
            etf_code: ETF代码
            
        Returns:
            ETFPriceData: ETF价格数据
        """
        if not validate_etf_code(etf_code):
            raise DataValidationError(f"无效的ETF代码: {etf_code}")
        
        try:
            # 获取最近交易日
            latest_trade_date = self.trading_date_manager.get_latest_trading_date(
                self.tushare_client.pro_api
            )
            
            # 先从缓存获取
            cached_data = self.cache_service.get_daily_cache(etf_code, latest_trade_date)
            if cached_data:
                logger.debug(f"从缓存获取ETF最新数据: {etf_code}")
                return ETFPriceData(**cached_data)
            
            # 缓存未命中，从API获取
            df = self.tushare_client.get_etf_daily_data(
                etf_code, 
                start_date=latest_trade_date,
                end_date=latest_trade_date
            )
            
            if df.empty:
                logger.warning(f"未获取到ETF最新数据: {etf_code}")
                return None
            
            # 转换为数据模型
            row = df.iloc[0]
            latest_data = ETFPriceData(
                trade_date=row.get('trade_date', ''),
                open_price=float(row.get('open', 0)),
                high_price=float(row.get('high', 0)),
                low_price=float(row.get('low', 0)),
                close_price=float(row.get('close', 0)),
                volume=int(row.get('vol', 0)),
                amount=float(row.get('amount', 0)),
                pct_change=float(row.get('pct_chg', 0)) if row.get('pct_chg') else None
            )
            
            # 保存到缓存
            self.cache_service.set_daily_cache(etf_code, latest_data.__dict__, latest_trade_date)
            
            logger.info(f"获取ETF最新数据成功: {etf_code}")
            return latest_data
            
        except Exception as e:
            logger.error(f"获取ETF最新数据失败 {etf_code}: {e}")
            raise DataValidationError(f"获取ETF最新数据失败: {e}")
    
    def get_etf_historical_data(self, etf_code: str, start_date: str, 
                               end_date: str) -> List[ETFPriceData]:
        """
        获取ETF历史数据
        
        Args:
            etf_code: ETF代码
            start_date: 开始日期 (YYYYMMDD格式)
            end_date: 结束日期 (YYYYMMDD格式)
            
        Returns:
            List[ETFPriceData]: ETF历史价格数据列表
        """
        if not validate_etf_code(etf_code):
            raise DataValidationError(f"无效的ETF代码: {etf_code}")
        
        if not validate_date_format(start_date) or not validate_date_format(end_date):
            raise DataValidationError("日期格式错误，应为YYYYMMDD格式")
        
        try:
            # 先从缓存获取
            cached_data = self.cache_service.get_historical_cache(etf_code, start_date, end_date)
            if cached_data:
                logger.debug(f"从缓存获取ETF历史数据: {etf_code}")
                return [ETFPriceData(**item) for item in cached_data]
            
            # 缓存未命中，从API获取
            df = self.tushare_client.get_etf_daily_data(etf_code, start_date, end_date)
            
            if df.empty:
                logger.warning(f"未获取到ETF历史数据: {etf_code}")
                return []
            
            # 转换为数据模型列表
            historical_data = []
            for _, row in df.iterrows():
                price_data = ETFPriceData(
                    trade_date=row.get('trade_date', ''),
                    open_price=float(row.get('open', 0)),
                    high_price=float(row.get('high', 0)),
                    low_price=float(row.get('low', 0)),
                    close_price=float(row.get('close', 0)),
                    volume=int(row.get('vol', 0)),
                    amount=float(row.get('amount', 0)),
                    pct_change=float(row.get('pct_chg', 0)) if row.get('pct_chg') else None
                )
                historical_data.append(price_data)
            
            # 保存到缓存
            cache_data = [data.__dict__ for data in historical_data]
            self.cache_service.set_historical_cache(etf_code, start_date, end_date, cache_data)
            
            logger.info(f"获取ETF历史数据成功: {etf_code}, {len(historical_data)}条记录")
            return historical_data
            
        except Exception as e:
            logger.error(f"获取ETF历史数据失败 {etf_code}: {e}")
            raise DataValidationError(f"获取ETF历史数据失败: {e}")
    
    def search_etf(self, keyword: str) -> List[ETFBasicInfo]:
        """
        搜索ETF
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            List[ETFBasicInfo]: 匹配的ETF列表
        """
        try:
            # 获取所有ETF基本信息
            df = self.tushare_client.get_etf_basic_info()
            
            if df.empty:
                return []
            
            # 按名称或代码搜索
            keyword_upper = keyword.upper()
            filtered_df = df[
                df['name'].str.contains(keyword, case=False, na=False) |
                df['ts_code'].str.contains(keyword_upper, case=False, na=False)
            ]
            
            # 转换为数据模型列表
            results = []
            for _, row in filtered_df.iterrows():
                ts_code = row.get('ts_code', '')
                code_only = ts_code.split('.')[0] if '.' in ts_code else ts_code
                
                basic_info = ETFBasicInfo(
                    code=code_only,
                    name=row.get('name', ''),
                    market=row.get('market', ''),
                    list_date=row.get('list_date', ''),
                    fund_type=row.get('fund_type', ''),
                    management_fee=float(row.get('m_fee', 0)) if row.get('m_fee') else None,
                    custodian_fee=float(row.get('c_fee', 0)) if row.get('c_fee') else None,
                    benchmark=row.get('benchmark', '')
                )
                results.append(basic_info)
            
            logger.info(f"ETF搜索完成: 关键词'{keyword}', 找到{len(results)}个结果")
            return results
            
        except Exception as e:
            logger.error(f"ETF搜索失败: {e}")
            return []
    
    def _get_etf_category(self, etf_name: str) -> str:
        """
        根据ETF名称推断分类
        
        Args:
            etf_name: ETF名称
            
        Returns:
            str: ETF分类
        """
        if '沪深300' in etf_name or '300ETF' in etf_name:
            return '宽基指数'
        elif '中证500' in etf_name or '500ETF' in etf_name:
            return '宽基指数'
        elif '创业板' in etf_name:
            return '宽基指数'
        elif '科创50' in etf_name:
            return '宽基指数'
        elif '红利' in etf_name:
            return '策略指数'
        elif '消费' in etf_name:
            return '行业主题'
        elif '医药' in etf_name or '生物' in etf_name:
            return '行业主题'
        elif '科技' in etf_name or '芯片' in etf_name:
            return '行业主题'
        elif '军工' in etf_name:
            return '行业主题'
        elif '新能源' in etf_name:
            return '行业主题'
        else:
            return '其他'
    
    def get_etf_summary(self, etf_code: str) -> Dict[str, Any]:
        """
        获取ETF综合信息摘要
        
        Args:
            etf_code: ETF代码
            
        Returns:
            dict: ETF综合信息
        """
        try:
            # 获取基本信息
            basic_info = self.get_etf_basic_info(etf_code)
            
            # 获取最新价格数据
            latest_data = self.get_etf_latest_data(etf_code)
            
            summary = {
                'basic_info': basic_info if isinstance(basic_info, dict) else basic_info.__dict__ if basic_info else None,
                'latest_data': latest_data.__dict__ if latest_data else None,
                'formatted_data': {}
            }
            
            # 格式化显示数据
            if latest_data:
                summary['formatted_data'] = {
                    'current_price': format_currency(latest_data.close_price),
                    'change_percent': format_percentage(latest_data.pct_change),
                    'volume': f"{latest_data.volume:,.0f}",
                    'amount': format_currency(latest_data.amount)
                }
            
            return summary
            
        except Exception as e:
            logger.error(f"获取ETF综合信息失败 {etf_code}: {e}")
            return {
                'basic_info': None,
                'latest_data': None,
                'formatted_data': {},
                'error': str(e)
            }