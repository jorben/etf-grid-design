"""
配置验证模块
提供配置项的验证和校验功能
"""

import os
import re
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, validator
from .constants import ETFConstants, GridConstants, ATRConstants, RiskConstants


class ConfigValidator:
    """配置验证器"""
    
    @staticmethod
    def validate_etf_code(etf_code: str) -> Tuple[bool, str]:
        """验证ETF代码格式"""
        if not etf_code:
            return False, "ETF代码不能为空"
        
        if len(etf_code) != 6:
            return False, "ETF代码必须是6位数字"
        
        if not etf_code.isdigit():
            return False, "ETF代码必须为纯数字"
        
        # 检查ETF代码前缀
        prefix = etf_code[:2]
        if prefix not in ETFConstants.STOCK_ETF_PREFIX:
            return False, f"不支持的ETF代码前缀: {prefix}"
        
        return True, ""
    
    @staticmethod
    def validate_date_format(date_str: str) -> Tuple[bool, str]:
        """验证日期格式"""
        try:
            from datetime import datetime
            datetime.strptime(date_str, "%Y-%m-%d")
            return True, ""
        except ValueError:
            return False, "日期格式错误，请使用YYYY-MM-DD格式"
    
    @staticmethod
    def validate_date_range(start_date: str, end_date: str) -> Tuple[bool, str]:
        """验证日期范围"""
        from datetime import datetime
        
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            today = datetime.now()
            
            if start >= end:
                return False, "开始日期必须早于结束日期"
            
            if end > today:
                return False, "结束日期不能超过当前日期"
            
            days_diff = (end - start).days
            if days_diff < ETFConstants.MIN_ANALYSIS_DAYS:
                return False, f"日期范围至少需要{ETFConstants.MIN_ANALYSIS_DAYS}天"
            
            if days_diff > ETFConstants.MAX_ANALYSIS_DAYS:
                return False, f"日期范围不能超过{ETFConstants.MAX_ANALYSIS_DAYS}天"
            
            return True, ""
            
        except ValueError:
            return False, "日期格式错误"
    
    @staticmethod
    def validate_grid_type(grid_type: str) -> Tuple[bool, str]:
        """验证网格类型"""
        if grid_type not in GridConstants.GRID_TYPES:
            return False, f"网格类型必须是: {', '.join(GridConstants.GRID_TYPES)}"
        return True, ""
    
    @staticmethod
    def validate_risk_preference(risk_preference: str) -> Tuple[bool, str]:
        """验证风险偏好"""
        if risk_preference not in GridConstants.RISK_PREFERENCES:
            return False, f"风险偏好必须是: {', '.join(GridConstants.RISK_PREFERENCES)}"
        return True, ""
    
    @staticmethod
    def validate_grid_count(grid_count: int) -> Tuple[bool, str]:
        """验证网格数量"""
        if grid_count < GridConstants.MIN_GRID_COUNT:
            return False, f"网格数量不能少于{GridConstants.MIN_GRID_COUNT}"
        
        if grid_count > GridConstants.MAX_GRID_COUNT:
            return False, f"网格数量不能超过{GridConstants.MAX_GRID_COUNT}"
        
        return True, ""
    
    @staticmethod
    def validate_total_capital(total_capital: float) -> Tuple[bool, str]:
        """验证总投资资金"""
        if total_capital <= 0:
            return False, "投资资金必须大于0"
        
        if total_capital < 10000:  # 最少1万
            return False, "投资金额不能少于1万元"
        
        if total_capital > 1000000:  # 最多500万
            return False, "投资金额不能超过100万元"
        
        return True, ""
    
    @staticmethod
    def validate_atr_period(atr_period: int) -> Tuple[bool, str]:
        """验证ATR周期"""
        if atr_period < ATRConstants.MIN_ATR_PERIOD:
            return False, f"ATR周期不能少于{ATRConstants.MIN_ATR_PERIOD}"
        
        if atr_period > ATRConstants.MAX_ATR_PERIOD:
            return False, f"ATR周期不能超过{ATRConstants.MAX_ATR_PERIOD}"
        
        return True, ""
    
    @staticmethod
    def validate_price_range(lower_price: float, upper_price: float) -> Tuple[bool, str]:
        """验证价格区间"""
        if lower_price <= 0:
            return False, "价格下限必须大于0"
        
        if upper_price <= 0:
            return False, "价格上限必须大于0"
        
        if lower_price >= upper_price:
            return False, "价格下限必须小于价格上限"
        
        return True, ""
    
    @staticmethod
    def validate_percentage(value: float, field_name: str = "值") -> Tuple[bool, str]:
        """验证百分比值"""
        if value < 0:
            return False, f"{field_name}不能为负数"
        
        if value > 1:
            return False, f"{field_name}不能超过100%"
        
        return True, ""
    
    @staticmethod
    def validate_file_path(file_path: str) -> Tuple[bool, str]:
        """验证文件路径"""
        if not file_path:
            return False, "文件路径不能为空"
        
        # 检查路径是否包含非法字符
        illegal_chars = ['<', '>', ':', '"', '|', '?', '*']
        if any(char in file_path for char in illegal_chars):
            return False, "文件路径包含非法字符"
        
        # 检查路径是否在允许的目录内
        allowed_dirs = ['cache', 'logs', 'data', 'temp']
        path_parts = file_path.split(os.sep)
        if path_parts and path_parts[0] not in allowed_dirs:
            return False, f"文件路径必须在允许的目录内: {', '.join(allowed_dirs)}"
        
        return True, ""
    
    @staticmethod
    def validate_port_number(port: int) -> Tuple[bool, str]:
        """验证端口号"""
        if port < 1024 or port > 65535:
            return False, "端口号必须在1024-65535之间"
        return True, ""
    
    @staticmethod
    def validate_log_level(log_level: str) -> Tuple[bool, str]:
        """验证日志级别"""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if log_level.upper() not in valid_levels:
            return False, f"日志级别必须是: {', '.join(valid_levels)}"
        return True, ""


class ConfigurationSchema(BaseModel):
    """配置项验证模式"""
    
    etf_code: str
    total_capital: float
    grid_type: str
    risk_preference: str
    analysis_days: int = 365
    
    @validator('etf_code')
    def validate_etf_code(cls, v):
        """验证ETF代码"""
        is_valid, message = ConfigValidator.validate_etf_code(v)
        if not is_valid:
            raise ValueError(message)
        return v
    
    @validator('total_capital')
    def validate_total_capital(cls, v):
        """验证总投资资金"""
        is_valid, message = ConfigValidator.validate_total_capital(v)
        if not is_valid:
            raise ValueError(message)
        return v
    
    @validator('grid_type')
    def validate_grid_type(cls, v):
        """验证网格类型"""
        is_valid, message = ConfigValidator.validate_grid_type(v)
        if not is_valid:
            raise ValueError(message)
        return v
    
    @validator('risk_preference')
    def validate_risk_preference(cls, v):
        """验证风险偏好"""
        is_valid, message = ConfigValidator.validate_risk_preference(v)
        if not is_valid:
            raise ValueError(message)
        return v
    
    @validator('analysis_days')
    def validate_analysis_days(cls, v):
        """验证分析天数"""
        if v < ETFConstants.MIN_ANALYSIS_DAYS:
            raise ValueError(f"分析天数不能少于{ETFConstants.MIN_ANALYSIS_DAYS}")
        if v > ETFConstants.MAX_ANALYSIS_DAYS:
            raise ValueError(f"分析天数不能超过{ETFConstants.MAX_ANALYSIS_DAYS}")
        return v


class EnvironmentValidator:
    """环境变量验证器"""
    
    @staticmethod
    def validate_environment() -> Tuple[bool, List[str]]:
        """验证环境变量配置"""
        errors = []
        
        # 检查必需的环境变量
        required_vars = ['TUSHARE_TOKEN']
        for var in required_vars:
            if not os.getenv(var):
                errors.append(f"必需的环境变量 {var} 未设置")
        
        # 检查TUSHARE_TOKEN格式
        tushare_token = os.getenv('TUSHARE_TOKEN')
        if tushare_token and len(tushare_token) != 32:
            errors.append("TUSHARE_TOKEN必须是32位字符")
        
        # 检查环境类型
        env = os.getenv('ENVIRONMENT', 'development')
        if env not in ['development', 'testing', 'production']:
            errors.append("ENVIRONMENT必须是development、testing或production")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_directory_permissions() -> Tuple[bool, List[str]]:
        """验证目录权限"""
        errors = []
        required_dirs = ['cache', 'logs', 'data', 'temp']
        
        for dir_name in required_dirs:
            if not os.path.exists(dir_name):
                try:
                    os.makedirs(dir_name, exist_ok=True)
                except PermissionError:
                    errors.append(f"无法创建目录 {dir_name}，权限不足")
            
            if os.path.exists(dir_name):
                # 检查目录是否可写
                test_file = os.path.join(dir_name, '.test_write')
                try:
                    with open(test_file, 'w') as f:
                        f.write('test')
                    os.remove(test_file)
                except PermissionError:
                    errors.append(f"目录 {dir_name} 不可写")
        
        return len(errors) == 0, errors


def validate_configuration(config_dict: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """验证配置字典"""
    errors = []
    
    try:
        # 验证配置模式
        ConfigurationSchema(**config_dict)
    except ValueError as e:
        errors.append(str(e))
    
    # 额外的验证
    if 'price_lower' in config_dict and 'price_upper' in config_dict:
        is_valid, message = ConfigValidator.validate_price_range(
            config_dict['price_lower'], config_dict['price_upper']
        )
        if not is_valid:
            errors.append(message)
    
    return len(errors) == 0, errors


def get_configuration_errors() -> Dict[str, List[str]]:
    """获取配置错误汇总"""
    errors = {}
    
    # 环境变量验证
    env_valid, env_errors = EnvironmentValidator.validate_environment()
    if not env_valid:
        errors['environment'] = env_errors
    
    # 目录权限验证
    dir_valid, dir_errors = EnvironmentValidator.validate_directory_permissions()
    if not dir_valid:
        errors['directories'] = dir_errors
    
    return errors


def is_configuration_valid() -> bool:
    """检查配置是否有效"""
    errors = get_configuration_errors()
    return len(errors) == 0
