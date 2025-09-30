import akshare as ak
import pandas as pd
import logging
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from .cache_service import EnhancedCache

logger = logging.getLogger(__name__)


class AkShareClient:
    """AkShare数据客户端 - 与TushareClient接口完全兼容"""
    
    def __init__(self, cache_dir: str = "../cache/akshare"):
        """初始化AkShare客户端"""
        # 初始化缓存管理器（保持与TushareClient相同的逻辑）
        self.cache = EnhancedCache(cache_dir)
        
        # A股交易时间配置
        self.market_open_time = "09:30"
        self.market_close_time = "15:00"
        
        logger.info("AkShare客户端初始化成功（增强缓存版本）")
    
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
        # 0. 检查是否需要调整结束日期（如果包含当天且未收盘）
        adjusted_end_date = self._adjust_end_date_if_needed(end_date)
        if adjusted_end_date != end_date:
            logger.info(f"→ 调整结束日期: {end_date} -> {adjusted_end_date} (当天未收盘)")
            end_date = adjusted_end_date
        
        # 1. 先检查历史数据缓存
        cached_data = self.cache.get_historical_cache(etf_code, start_date, end_date)
        if cached_data:
            logger.info(f"✓ 从历史缓存获取ETF {etf_code} 日线数据 ({start_date}~{end_date})")
            # 将缓存的字典数据转换回DataFrame
            df = pd.DataFrame(cached_data)
            # 确保trade_date是datetime类型
            df['trade_date'] = pd.to_datetime(df['trade_date'])
            return df
        
        # 2. 缓存未命中，调用AkShare接口
        logger.info(f"→ 历史缓存未命中，请求AkShare接口获取ETF {etf_code} 日线数据 ({start_date}~{end_date})")
        
        try:
            
            # 调用AkShare接口获取ETF历史数据
            df = ak.fund_etf_hist_em(
                symbol=etf_code,
                period="daily",
                start_date=start_date,
                end_date=end_date,
                adjust="qfq"
            )
            
            if df.empty:
                logger.warning(f"✗ AkShare接口返回空数据，ETF {etf_code} 日线数据获取失败")
                return None
            
            # 数据预处理和格式转换
            df = self._convert_akshare_daily_to_tushare_format(df)
            
            # 3. 成功获取数据，保存到历史缓存（转换为字典格式）
            cache_data = df.to_dict('records')
            self.cache.set_historical_cache(etf_code, start_date, end_date, cache_data)
            logger.info(f"✓ ETF {etf_code} 日线数据获取成功并已缓存，共{len(df)}条记录")
            
            return df
            
        except Exception as e:
            logger.error(f"✗ 请求AkShare接口失败，ETF {etf_code} 日线数据获取失败: {str(e)}")
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
        logger.info(f"→ 永久缓存未命中，请求AkShare接口获取ETF {etf_code} 基本信息")
        
        try:
            # 使用AkShare获取ETF详细信息
            df = ak.fund_overview_em(symbol=etf_code)
            
            if df.empty:
                logger.warning(f"✗ 未找到ETF {etf_code} 的基本信息")
                return None
            
            # 提取基本信息并转换为Tushare格式
            row = df.iloc[0]
            basic_info = {
                'ts_code': f"{etf_code}.{self._get_market_suffix(etf_code)}",
                'name': row['基金简称'],
                'management': row.get('基金管理人', '未知')
            }
            
            # 3. 成功获取数据，保存到永久缓存
            self.cache.set_permanent_cache("etf_basic", etf_code, basic_info)
            logger.info(f"✓ ETF {etf_code} 基本信息获取成功并已永久缓存")
            
            return basic_info
            
        except Exception as e:
            logger.error(f"✗ 请求AkShare接口失败，ETF {etf_code} 基本信息获取失败: {str(e)}")
            return None
    
    def get_latest_price(self, etf_code: str) -> Optional[Dict]:
        """
        获取ETF最新价格（智能交易日缓存）
        
        Args:
            etf_code: ETF代码（不含市场后缀）
            
        Returns:
            Dict: 最新价格信息
        """
        # 1. 获取最近收盘的交易日
        latest_trading_date = self.get_latest_trading_date()
        
        # 2. 检查该交易日的缓存
        cached_data = self.cache.get_daily_cache(latest_trading_date, "price", etf_code)
        if cached_data:
            logger.info(f"✓ 从交易日缓存获取ETF {etf_code} 最新价格 (交易日: {latest_trading_date})")
            return cached_data
        
        # 3. 缓存未命中，调用接口
        logger.info(f"→ 交易日缓存未命中，请求AkShare接口获取ETF {etf_code} 最新价格")
        
        try:
            # 获取ETF实时行情
            df = ak.fund_etf_spot_em()
            
            # 查找指定ETF
            etf_data = df[df['代码'] == etf_code]
            if etf_data.empty:
                logger.warning(f"✗ 未找到ETF {etf_code} 的实时数据")
                return None
            
            # 提取价格信息
            row = etf_data.iloc[0]
            
            # 安全转换数值
            def safe_float(value, default=0.0):
                try:
                    if pd.isna(value) or value == '-' or value == '':
                        return default
                    return float(str(value).replace('%', '').replace(',', ''))
                except:
                    return default
            
            def safe_int(value, default=0):
                try:
                    if pd.isna(value) or value == '-' or value == '':
                        return default
                    return int(float(str(value).replace(',', '')))
                except:
                    return default
            
            def safe_timestamp(value, default=0):
                """专门处理时间戳字段，处理Timestamp对象和数值时间戳"""
                try:
                    if pd.isna(value) or value == '-' or value == '':
                        return default
                    
                    # 检查是否是pandas Timestamp对象
                    if hasattr(value, 'timestamp'):
                        # 如果是Timestamp对象，转换为毫秒级时间戳
                        return int(value.timestamp() * 1000)
                    else:
                        # 如果是数值，直接转换为整数
                        return int(str(value).replace(',', ''))
                except:
                    return default
            
            def safe_date_str(value, default=""):
                """将Timestamp对象转换为YYYYMMDD格式字符串"""
                try:
                    if pd.isna(value) or value == '-' or value == '':
                        return default
                    
                    # 检查是否是pandas Timestamp对象
                    if hasattr(value, 'strftime'):
                        return value.strftime('%Y%m%d')
                    else:
                        # 如果是字符串或数值，尝试解析
                        from datetime import datetime
                        if isinstance(value, (int, float)) and value > 0:
                            # 如果是数值时间戳（毫秒级）
                            dt = datetime.fromtimestamp(value / 1000)
                            return dt.strftime('%Y%m%d')
                        else:
                            # 尝试解析字符串
                            return str(value).replace('-', '')[:8]
                except:
                    return default
            
            # 根据接口返回的"数据日期"字段确定实际交易日
            data_date_str = safe_date_str(row['数据日期'])
            if data_date_str and len(data_date_str) == 8:
                actual_trading_date = data_date_str
                logger.info(f"→ 使用接口数据日期作为交易日: {actual_trading_date}")
            else:
                # 如果数据日期无效，使用预计算的交易日
                actual_trading_date = latest_trading_date
                logger.warning(f"⚠️ 接口数据日期无效，使用预计算交易日: {actual_trading_date}")
            
            # 获取更新时间戳
            update_timestamp = safe_timestamp(row['更新时间'])
            data_timestamp = safe_timestamp(row['数据日期'])
            
            # 根据示例数据修正字段名和添加缺失字段
            price_info = {
                'current_price': safe_float(row['最新价']),
                'pre_close': safe_float(row['昨收']),
                'pct_change': safe_float(row['涨跌幅']),
                'volume': safe_int(row['成交量']),
                'amount': safe_float(row['成交额']),
                'open_price': safe_float(row['开盘价']),
                'high_price': safe_float(row['最高价']),
                'low_price': safe_float(row['最低价']),
                'change_amount': safe_float(row['涨跌额']),
                'amplitude': safe_float(row['振幅']),
                'turnover_rate': safe_float(row['换手率']),
                'volume_ratio': safe_float(row['量比']),
                'iopv': safe_float(row['IOPV实时估值']),
                'discount_rate': safe_float(row['基金折价率']),
                'trade_date': actual_trading_date,  # 使用接口返回的数据日期
                'data_age_days': 0,  # 实时数据
                'etf_name': str(row['名称']) if not pd.isna(row['名称']) else '',
                'etf_code': str(etf_code),
                'timestamp': update_timestamp,  # 使用接口返回的更新时间戳
                'data_timestamp': data_timestamp  # 保存原始数据日期时间戳
            }
            
            # 4. 检查是否需要缓存（如果是当日数据且还未收盘，则不缓存）
            current_date = datetime.now().strftime('%Y%m%d')
            if actual_trading_date == current_date and not self._is_market_closed(datetime.now()):
                logger.info(f"→ 当日数据且未收盘，跳过缓存 (交易日: {actual_trading_date})")
            else:
                # 缓存数据
                self.cache.set_daily_cache(actual_trading_date, "price", etf_code, price_info)
            logger.info(f"✓ ETF {etf_code} 最新价格获取成功并已缓存 (交易日: {actual_trading_date})")
            
            return price_info
            
        except Exception as e:
            logger.error(f"✗ 请求AkShare接口失败，ETF {etf_code} 最新价格获取失败: {str(e)}")
            return None
    
    
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
            # 解析年份范围
            start_year = int(start_date[:4])
            end_year = int(end_date[:4])
            
            all_trading_days = []
            
            # 按年获取交易日历
            for year in range(start_year, end_year + 1):
                year_calendar = self._get_trading_calendar_from_akshare(year)
                all_trading_days.extend(year_calendar)
            
            # 过滤指定日期范围
            filtered_days = [day for day in all_trading_days if start_date <= day <= end_date]
            
            logger.info(f"✓ 获取交易日历成功 ({start_date}~{end_date})，共{len(filtered_days)}个交易日")
            return filtered_days
            
        except Exception as e:
            logger.error(f"✗ 获取交易日历失败: {str(e)}")
            return []
    
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
        logger.info(f"→ 永久缓存未命中，请求AkShare接口获取ETF {etf_code} 名称")
        
        try:
            # 获取ETF基本信息
            basic_info = self.get_etf_basic_info(etf_code)
            if not basic_info:
                return None
            
            etf_name = basic_info['name']
            
            # 3. 成功获取数据，保存到永久缓存
            self.cache.set_permanent_cache("etf_name", etf_code, etf_name)
            logger.info(f"✓ ETF {etf_code} 名称获取成功并已永久缓存: {etf_name}")
            
            return etf_name
            
        except Exception as e:
            logger.error(f"✗ 请求AkShare接口失败，ETF {etf_code} 名称获取失败: {str(e)}")
            return None
    
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
        current_time = datetime.now()
        current_date = current_time.strftime('%Y%m%d')
        
        # 获取当前年份的交易日历
        trading_calendar = self.get_trading_calendar(
            f"{current_time.year}0101",
            f"{current_time.year}1231"
        )
        
        if not trading_calendar:
            # 如果获取交易日历失败，使用简单逻辑
            logger.warning("获取交易日历失败，使用简单逻辑判断交易日")
            return self._get_simple_trading_date(current_time)
        
        # 判断当前日期是否为交易日
        if current_date in trading_calendar:
            # 当前是交易日
            return current_date
        else:
            # 当前不是交易日，获取上一个交易日
            return self.get_previous_trading_date(current_date)
    
    # =================== 辅助方法 ===================
    
    def _convert_akshare_daily_to_tushare_format(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        将AkShare日线数据格式转换为Tushare格式
        
        Args:
            df: AkShare原始数据
            
        Returns:
            DataFrame: 转换后的数据
        """
        # 列名映射
        column_mapping = {
            '日期': 'trade_date',
            '开盘': 'open',
            '收盘': 'close',
            '最高': 'high',
            '最低': 'low',
            '成交量': 'vol',
            '成交额': 'amount',
            "振幅": 'amplitude',
            "涨跌幅": 'change',
            "涨跌额": 'change_amount',
            "换手率": 'turnover_rate',
        }
        
        # 重命名列
        df = df.rename(columns=column_mapping)
        
        # 处理日期格式 (YYYY-MM-DD -> YYYYMMDD)
        if 'trade_date' in df.columns:
            df['trade_date'] = pd.to_datetime(df['trade_date']).dt.strftime('%Y%m%d')
            df['trade_date'] = pd.to_datetime(df['trade_date'])
        
        # 排序
        df = df.sort_values('trade_date')
        
        # 计算衍生字段
        df['pre_close'] = df['close'].shift(1)
        df['change'] = (df['close'] - df['pre_close']).round(4)
        df['pct_chg'] = ((df['close'] - df['pre_close']) / df['pre_close'] * 100).round(2)
        df['amplitude'] = ((df['high'] - df['low']) / df['pre_close'] * 100).round(2)
        
        # 处理第一行的NaN值
        df = df.fillna(0)
        
        return df.reset_index(drop=True)
    
    def _get_market_suffix(self, etf_code: str) -> str:
        """
        获取市场后缀
        
        Args:
            etf_code: ETF代码
            
        Returns:
            str: 市场后缀 (SH/SZ)
        """
        if etf_code.startswith(('15', '16', '18')):
            return 'SZ'  # 深交所
        else:
            return 'SH'  # 上交所
    
    def _adjust_end_date_if_needed(self, end_date: str, current_time: Optional[datetime] = None) -> str:
        """
        检查是否需要调整结束日期（如果包含当天且未收盘）
        
        Args:
            end_date: 原始结束日期 (YYYYMMDD格式)
            current_time: 当前时间（用于测试，默认为None时使用当前系统时间）
            
        Returns:
            str: 调整后的结束日期
        """
        try:
            # 获取当前日期和时间
            if current_time is None:
                current_time = datetime.now()
            current_date = current_time.strftime('%Y%m%d')
            
            # 如果结束日期不是当天，不需要调整
            if end_date != current_date:
                return end_date
            
            # 检查当前时间是否在交易时间内（15:00前）
            if not self._is_market_closed(current_time):
                # 未收盘，需要获取上一个交易日
                previous_trading_date = self.get_previous_trading_date(current_date)
                if previous_trading_date:
                    logger.info(f"→ 当天未收盘，将结束日期调整为上一个交易日: {previous_trading_date}")
                    return previous_trading_date
                else:
                    logger.warning(f"无法获取{current_date}的上一个交易日，使用原始日期")
                    return end_date
            else:
                # 已收盘，不需要调整
                logger.info(f"→ 当天已收盘，使用原始结束日期: {end_date}")
                return end_date
                
        except Exception as e:
            logger.error(f"调整结束日期时发生错误: {str(e)}")
            return end_date
    
    def _is_market_closed(self, current_time: datetime) -> bool:
        """
        判断市场是否已收盘（15:00后）
        
        Args:
            current_time: 当前时间
            
        Returns:
            bool: 是否已收盘
        """
        current_time_str = current_time.strftime('%H:%M')
        market_close_time = "15:00"
        return current_time_str >= market_close_time
    
    def get_previous_trading_date(self, current_date: str) -> Optional[str]:
        """
        获取指定日期的上一个交易日

        Args:
            current_date: 当前日期 (YYYYMMDD格式)

        Returns:
            str: 上一个交易日，如果获取失败返回None
        """
        try:
            # 解析年份
            year = int(current_date[:4])
            
            # 获取当前年份的交易日历
            trading_calendar = self.get_trading_calendar(
                f"{year}0101",
                f"{year}1231"
            )
            
            if not trading_calendar:
                # 如果获取失败，尝试获取前一年的交易日历
                trading_calendar = self.get_trading_calendar(
                    f"{year-1}0101",
                    f"{year-1}1231"
                )
                if not trading_calendar:
                    logger.warning(f"无法获取{year}年和{year-1}年的交易日历")
                    return None
            
            # 找到小于当前日期的最大交易日
            previous_dates = [date for date in trading_calendar if date < current_date]
            
            if previous_dates:
                previous_date = max(previous_dates)
                logger.debug(f"找到{current_date}的上一个交易日: {previous_date}")
                return previous_date
            else:
                # 如果没有找到，可能是年初，尝试获取前一年的最后一个交易日
                logger.debug(f"在当前年份未找到{current_date}之前的交易日，尝试前一年")
                previous_year_calendar = self.get_trading_calendar(
                    f"{year-1}0101",
                    f"{year-1}1231"
                )
                if previous_year_calendar:
                    previous_date = max(previous_year_calendar)
                    logger.debug(f"找到前一年的最后一个交易日: {previous_date}")
                    return previous_date
                else:
                    logger.warning(f"无法获取{current_date}的上一个交易日")
                    return None
                    
        except Exception as e:
            logger.error(f"获取上一个交易日时发生错误: {str(e)}")
            return None

    def _get_trading_calendar_from_akshare(self, year: int) -> List[str]:
        """
        从AkShare获取指定年份的交易日历
        
        Args:
            year: 年份
            
        Returns:
            List[str]: 交易日列表
        """
        try:
            # 先检查缓存
            cached_calendar = self.cache.get_permanent_cache("trading_cal", str(year))
            if cached_calendar:
                return cached_calendar
            
            # 调用AkShare交易日历接口
            df = ak.tool_trade_date_hist_sina()
            
            if df.empty:
                logger.warning(f"✗ AkShare交易日历接口返回空数据")
                return []
            
            # 处理日期格式
            df['trade_date'] = df['trade_date'].astype(str).str.replace('-', '')
            
            # 筛选年份
            year_filter = df['trade_date'].str.startswith(str(year))
            year_data = df[year_filter]['trade_date'].tolist()
            
            # 缓存结果
            self.cache.set_permanent_cache("trading_cal", str(year), year_data)
            
            logger.info(f"✓ 从AkShare获取{year}年交易日历成功，共{len(year_data)}个交易日")
            return year_data
            
        except Exception as e:
            logger.error(f"✗ 从AkShare获取{year}年交易日历失败: {str(e)}")
            return []
    
    def _complete_etf_code(self, etf_code: str) -> str:
        """
        自动补全ETF代码的市场后缀（兼容方法）

        Args:
            etf_code: ETF代码（不含市场后缀）

        Returns:
            str: 完整的ETF代码（含市场后缀）
        """
        etf_code = etf_code.split('.')[0]
        return f"{etf_code}.{self._get_market_suffix(etf_code)}"
    
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