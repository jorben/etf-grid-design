import os
import json
import logging
from datetime import datetime, timedelta
from typing import Any, Optional, Dict, List
import pandas as pd

logger = logging.getLogger(__name__)


class EnhancedCache:
    """增强版缓存管理器 - 支持分层缓存策略"""
    
    def __init__(self, cache_dir: str = "cache"):
        """
        初始化增强缓存管理器
        
        Args:
            cache_dir: 缓存根目录路径
        """
        self.cache_dir = cache_dir
        self.permanent_dir = os.path.join(cache_dir, "permanent")
        self.daily_dir = os.path.join(cache_dir, "daily")
        self.historical_dir = os.path.join(cache_dir, "historical")
        
        # 确保所有缓存目录存在
        for dir_path in [self.cache_dir, self.permanent_dir, self.daily_dir, self.historical_dir]:
            os.makedirs(dir_path, exist_ok=True)
        
        logger.info(f"增强缓存管理器初始化完成，缓存目录: {cache_dir}")
    
    def get_permanent_cache(self, cache_type: str, key: str) -> Optional[Any]:
        """
        获取永久缓存数据
        
        Args:
            cache_type: 缓存类型 (etf_basic, etf_name, trading_cal)
            key: 缓存键
            
        Returns:
            缓存的数据，如果不存在返回None
        """
        cache_file = os.path.join(self.permanent_dir, f"{cache_type}_{key}.json")
        return self._safe_load_cache(cache_file, f"永久缓存-{cache_type}-{key}")
    
    def set_permanent_cache(self, cache_type: str, key: str, data: Any):
        """
        保存永久缓存数据
        
        Args:
            cache_type: 缓存类型
            key: 缓存键
            data: 要缓存的数据
        """
        if not data:
            logger.debug(f"数据为空，不缓存: {cache_type}-{key}")
            return
        
        cache_file = os.path.join(self.permanent_dir, f"{cache_type}_{key}.json")
        self._safe_save_cache(cache_file, data, f"永久缓存-{cache_type}-{key}")
    
    def get_daily_cache(self, trade_date: str, cache_type: str, key: str) -> Optional[Any]:
        """
        获取交易日缓存数据
        
        Args:
            trade_date: 交易日期 (YYYYMMDD格式)
            cache_type: 缓存类型 (price, quote)
            key: 缓存键 (通常是ETF代码)
            
        Returns:
            缓存的数据，如果不存在返回None
        """
        daily_cache_dir = os.path.join(self.daily_dir, trade_date)
        cache_file = os.path.join(daily_cache_dir, f"{cache_type}_{key}.json")
        return self._safe_load_cache(cache_file, f"交易日缓存-{trade_date}-{cache_type}-{key}")
    
    def set_daily_cache(self, trade_date: str, cache_type: str, key: str, data: Any):
        """
        保存交易日缓存数据
        
        Args:
            trade_date: 交易日期 (YYYYMMDD格式)
            cache_type: 缓存类型
            key: 缓存键
            data: 要缓存的数据
        """
        if not data:
            logger.debug(f"数据为空，不缓存: {trade_date}-{cache_type}-{key}")
            return
        
        daily_cache_dir = os.path.join(self.daily_dir, trade_date)
        os.makedirs(daily_cache_dir, exist_ok=True)
        
        cache_file = os.path.join(daily_cache_dir, f"{cache_type}_{key}.json")
        self._safe_save_cache(cache_file, data, f"交易日缓存-{trade_date}-{cache_type}-{key}")
    
    def get_historical_cache(self, etf_code: str, start_date: str, end_date: str) -> Optional[Any]:
        """
        获取历史数据缓存
        
        Args:
            etf_code: ETF代码
            start_date: 开始日期 (YYYYMMDD格式)
            end_date: 结束日期 (YYYYMMDD格式)
            
        Returns:
            缓存的数据，如果不存在返回None
        """
        cache_file = os.path.join(self.historical_dir, f"{etf_code}_{start_date}_{end_date}.json")
        return self._safe_load_cache(cache_file, f"历史缓存-{etf_code}-{start_date}-{end_date}")
    
    def set_historical_cache(self, etf_code: str, start_date: str, end_date: str, data: Any):
        """
        保存历史数据缓存
        
        Args:
            etf_code: ETF代码
            start_date: 开始日期
            end_date: 结束日期
            data: 要缓存的数据
        """
        if not data:
            logger.debug(f"数据为空，不缓存: {etf_code}-{start_date}-{end_date}")
            return
        
        cache_file = os.path.join(self.historical_dir, f"{etf_code}_{start_date}_{end_date}.json")
        self._safe_save_cache(cache_file, data, f"历史缓存-{etf_code}-{start_date}-{end_date}")
    
    def _safe_load_cache(self, cache_file: str, cache_desc: str) -> Optional[Any]:
        """
        安全加载缓存文件
        
        Args:
            cache_file: 缓存文件路径
            cache_desc: 缓存描述（用于日志）
            
        Returns:
            缓存数据或None
        """
        if not os.path.exists(cache_file):
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.debug(f"缓存命中: {cache_desc}")
                return data
        except (json.JSONDecodeError, IOError, OSError) as e:
            # 缓存文件损坏，删除并返回None
            logger.warning(f"缓存文件损坏，已删除: {cache_file}, 错误: {e}")
            try:
                os.remove(cache_file)
            except:
                pass
            return None
        except Exception as e:
            logger.error(f"加载缓存文件异常: {cache_file}, 错误: {e}")
            return None
    
    def _safe_save_cache(self, cache_file: str, data: Any, cache_desc: str):
        """
        安全保存缓存文件
        
        Args:
            cache_file: 缓存文件路径
            data: 要保存的数据
            cache_desc: 缓存描述（用于日志）
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(cache_file), exist_ok=True)
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            logger.debug(f"缓存保存成功: {cache_desc}")
        except Exception as e:
            logger.error(f"缓存保存失败: {cache_file}, 错误: {e}")
    
    def get_cache_info(self) -> Dict:
        """
        获取缓存统计信息
        
        Returns:
            dict: 缓存统计信息
        """
        try:
            info = {
                'cache_dir': self.cache_dir,
                'permanent': self._get_dir_info(self.permanent_dir),
                'daily': self._get_dir_info(self.daily_dir),
                'historical': self._get_dir_info(self.historical_dir)
            }
            
            # 计算总计
            total_files = sum(dir_info['file_count'] for dir_info in info.values() if isinstance(dir_info, dict))
            total_size = sum(dir_info['total_size_mb'] for dir_info in info.values() if isinstance(dir_info, dict))
            
            info['total'] = {
                'file_count': total_files,
                'total_size_mb': round(total_size, 2)
            }
            
            return info
        except Exception as e:
            logger.error(f"获取缓存信息失败: {e}")
            return {
                'cache_dir': self.cache_dir,
                'error': str(e)
            }
    
    def _get_dir_info(self, dir_path: str) -> Dict:
        """获取目录信息"""
        try:
            if not os.path.exists(dir_path):
                return {'file_count': 0, 'total_size_mb': 0, 'subdirs': []}
            
            total_size = 0
            file_count = 0
            subdirs = []
            
            for root, dirs, files in os.walk(dir_path):
                subdirs.extend(dirs)
                for file in files:
                    if file.endswith('.json'):
                        file_path = os.path.join(root, file)
                        total_size += os.path.getsize(file_path)
                        file_count += 1
            
            return {
                'file_count': file_count,
                'total_size_mb': round(total_size / 1024 / 1024, 2),
                'subdirs': list(set(subdirs))  # 去重
            }
        except Exception as e:
            logger.error(f"获取目录信息失败 {dir_path}: {e}")
            return {'file_count': 0, 'total_size_mb': 0, 'subdirs': [], 'error': str(e)}


class TradingDateManager:
    """交易日管理器"""
    
    def __init__(self, cache: EnhancedCache):
        """
        初始化交易日管理器
        
        Args:
            cache: 缓存管理器实例
        """
        self.cache = cache
        
        # A股交易时间配置
        self.market_open_time = "09:30"
        self.market_close_time = "15:00"
    
    def get_latest_trading_date(self, tushare_pro) -> str:
        """
        获取最近的交易日
        
        Args:
            tushare_pro: tushare pro接口实例
            
        Returns:
            str: 最近的交易日 (YYYYMMDD格式)
        """
        current_time = datetime.now()
        current_date = current_time.strftime('%Y%m%d')
        
        # 获取交易日历
        trading_calendar = self._get_trading_calendar(tushare_pro, current_time.year)
        
        if not trading_calendar:
            # 如果获取交易日历失败，使用简单逻辑
            logger.warning("获取交易日历失败，使用简单逻辑判断交易日")
            return self._get_simple_trading_date(current_time)
        
        # 判断当前日期是否为交易日
        if current_date in trading_calendar:
            # 当前是交易日，判断是否已收盘
            if self._is_market_closed(current_time):
                # 已收盘，当前日期就是最近交易日
                return current_date
            else:
                # 未收盘，使用上一个交易日
                return self._get_previous_trading_date(current_date, trading_calendar)
        else:
            # 当前不是交易日，获取上一个交易日
            return self._get_previous_trading_date(current_date, trading_calendar)
    
    def _get_trading_calendar(self, tushare_pro, year: int) -> List[str]:
        """
        获取交易日历（带缓存）
        
        Args:
            tushare_pro: tushare pro接口实例
            year: 年份
            
        Returns:
            List[str]: 交易日列表
        """
        # 先检查缓存
        cached_calendar = self.cache.get_permanent_cache("trading_cal", str(year))
        if cached_calendar:
            logger.debug(f"从缓存获取{year}年交易日历")
            return cached_calendar
        
        # 缓存未命中，调用接口
        try:
            start_date = f"{year}0101"
            end_date = f"{year}1231"
            
            df = tushare_pro.trade_cal(
                exchange='SSE',
                start_date=start_date,
                end_date=end_date,
                is_open='1'
            )
            
            if df.empty:
                logger.warning(f"获取{year}年交易日历失败：返回空数据")
                return []
            
            trading_days = df['cal_date'].tolist()
            
            # 保存到缓存
            self.cache.set_permanent_cache("trading_cal", str(year), trading_days)
            logger.info(f"获取{year}年交易日历成功，共{len(trading_days)}个交易日")
            
            return trading_days
            
        except Exception as e:
            logger.error(f"获取{year}年交易日历失败: {e}")
            return []
    
    def _is_market_closed(self, current_time: datetime) -> bool:
        """
        判断市场是否已收盘
        
        Args:
            current_time: 当前时间
            
        Returns:
            bool: 是否已收盘
        """
        current_time_str = current_time.strftime('%H:%M')
        return current_time_str >= self.market_close_time
    
    def _get_previous_trading_date(self, current_date: str, trading_calendar: List[str]) -> str:
        """
        获取上一个交易日
        
        Args:
            current_date: 当前日期 (YYYYMMDD格式)
            trading_calendar: 交易日历列表
            
        Returns:
            str: 上一个交易日
        """
        # 找到小于当前日期的最大交易日
        previous_dates = [date for date in trading_calendar if date < current_date]
        
        if previous_dates:
            return max(previous_dates)
        else:
            # 如果没有找到，可能是年初，尝试获取去年的交易日历
            logger.warning(f"在当前年份交易日历中未找到{current_date}之前的交易日")
            return self._get_simple_trading_date(datetime.strptime(current_date, '%Y%m%d'))
    
    def _get_simple_trading_date(self, current_time: datetime) -> str:
        """
        简单的交易日判断逻辑（当交易日历获取失败时使用）
        
        Args:
            current_time: 当前时间
            
        Returns:
            str: 估算的交易日
        """
        # 简单逻辑：排除周末，不考虑节假日
        date = current_time
        
        # 如果是交易时间内，且是工作日，返回当天
        if (date.weekday() < 5 and  # 周一到周五
            self._is_market_closed(current_time)):
            return date.strftime('%Y%m%d')
        
        # 否则往前找最近的工作日
        while date.weekday() >= 5:  # 周末
            date = date - timedelta(days=1)
        
        return date.strftime('%Y%m%d')
    
    def validate_trade_date(self, data: Dict) -> Optional[str]:
        """
        验证并提取数据中的交易日期
        
        Args:
            data: 包含交易数据的字典
            
        Returns:
            str: 交易日期 (YYYYMMDD格式)，如果无效返回None
        """
        if not data:
            return None
        
        # 尝试从不同字段提取交易日期
        trade_date_fields = ['trade_date', 'cal_date', 'date']
        
        for field in trade_date_fields:
            if field in data:
                trade_date = data[field]
                
                # 处理不同的日期格式
                if isinstance(trade_date, str):
                    # 移除可能的分隔符
                    trade_date = trade_date.replace('-', '').replace('/', '')
                    if len(trade_date) == 8 and trade_date.isdigit():
                        return trade_date
                
                # 处理pandas Timestamp或datetime对象
                elif hasattr(trade_date, 'strftime'):
                    return trade_date.strftime('%Y%m%d')
        
        logger.warning(f"无法从数据中提取有效的交易日期: {data}")
        return None