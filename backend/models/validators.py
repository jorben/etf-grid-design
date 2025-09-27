"""
数据验证器
提供数据模型的验证功能
"""

import re
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
from pydantic import validator
from .base import BaseETFModel
from ..config.constants import ETFConstants, GridConstants, ATRConstants


class ETFValidators:
    """ETF数据验证器"""
    
    @staticmethod
    def validate_etf_code(code: str) -> Tuple[bool, str]:
        """验证ETF代码格式"""
        if not code:
            return False, "ETF代码不能为空"
        
        if len(code) != 6:
            return False, "ETF代码必须是6位数字"
        
        if not code.isdigit():
            return False, "ETF代码必须为纯数字"
        
        # 检查ETF代码前缀
        prefix = code[:2]
        if prefix not in ETFConstants.STOCK_ETF_PREFIX:
            return False, f"不支持的ETF代码前缀: {prefix}"
        
        return True, ""
    
    @staticmethod
    def validate_etf_name(name: str) -> Tuple[bool, str]:
        """验证ETF名称"""
        if not name:
            return False, "ETF名称不能为空"
        
        if len(name) < 2 or len(name) > 100:
            return False, "ETF名称长度必须在2-100个字符之间"
        
        # 检查名称是否包含非法字符
        illegal_chars = ['<', '>', ':', '"', '|', '?', '*']
        if any(char in name for char in illegal_chars):
            return False, "ETF名称包含非法字符"
        
        return True, ""
    
    @staticmethod
    def validate_price(price: float) -> Tuple[bool, str]:
        """验证价格"""
        if price <= 0:
            return False, "价格必须大于0"
        
        if price > 1000000:  # 假设最大价格限制
            return False, "价格不能超过1000000"
        
        return True, ""
    
    @staticmethod
    def validate_percentage(value: float, field_name: str = "百分比") -> Tuple[bool, str]:
        """验证百分比值"""
        if value < -100:
            return False, f"{field_name}不能小于-100%"
        
        if value > 1000:  # 允许较大的涨幅
            return False, f"{field_name}不能超过1000%"
        
        return True, ""
    
    @staticmethod
    def validate_volume(volume: float) -> Tuple[bool, str]:
        """验证成交量"""
        if volume < 0:
            return False, "成交量不能为负数"
        
        if volume > 1e12:  # 1万亿
            return False, "成交量过大"
        
        return True, ""
    
    @staticmethod
    def validate_amount(amount: float) -> Tuple[bool, str]:
        """验证成交额"""
        if amount < 0:
            return False, "成交额不能为负数"
        
        if amount > 1e15:  # 1000万亿
            return False, "成交额过大"
        
        return True, ""


class GridValidators:
    """网格交易验证器"""
    
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
    def validate_price_range(lower_price: float, upper_price: float) -> Tuple[bool, str]:
        """验证价格区间"""
        if lower_price <= 0:
            return False, "价格下限必须大于0"
        
        if upper_price <= 0:
            return False, "价格上限必须大于0"
        
        if lower_price >= upper_price:
            return False, "价格下限必须小于价格上限"
        
        # 检查价格区间是否合理
        price_ratio = upper_price / lower_price
        if price_ratio > 10:  # 最大价格比为10倍
            return False, "价格区间过大，价格上限不能超过下限的10倍"
        
        return True, ""
    
    @staticmethod
    def validate_ratio(ratio: float, field_name: str = "比例") -> Tuple[bool, str]:
        """验证比例值"""
        if ratio < 0:
            return False, f"{field_name}不能为负数"
        
        if ratio > 1:
            return False, f"{field_name}不能超过100%"
        
        return True, ""


class ATRValidators:
    """ATR算法验证器"""
    
    @staticmethod
    def validate_atr_period(period: int) -> Tuple[bool, str]:
        """验证ATR周期"""
        if period < ATRConstants.MIN_ATR_PERIOD:
            return False, f"ATR周期不能少于{ATRConstants.MIN_ATR_PERIOD}"
        
        if period > ATRConstants.MAX_ATR_PERIOD:
            return False, f"ATR周期不能超过{ATRConstants.MAX_ATR_PERIOD}"
        
        return True, ""
    
    @staticmethod
    def validate_atr_value(atr_value: float) -> Tuple[bool, str]:
        """验证ATR值"""
        if atr_value < 0:
            return False, "ATR值不能为负数"
        
        if atr_value > 100:  # 假设最大ATR值限制
            return False, "ATR值过大"
        
        return True, ""
    
    @staticmethod
    def validate_volatility(volatility: float) -> Tuple[bool, str]:
        """验证波动率"""
        if volatility < 0:
            return False, "波动率不能为负数"
        
        if volatility > 5:  # 500%波动率
            return False, "波动率过大"
        
        return True, ""


class DateValidators:
    """日期验证器"""
    
    @staticmethod
    def validate_date_format(date_str: str) -> Tuple[bool, str]:
        """验证日期格式"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True, ""
        except ValueError:
            return False, "日期格式错误，请使用YYYY-MM-DD格式"
    
    @staticmethod
    def validate_date_range(start_date: str, end_date: str) -> Tuple[bool, str]:
        """验证日期范围"""
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


class CommonValidators:
    """通用验证器"""
    
    @staticmethod
    def validate_positive_number(value: float, field_name: str = "数值") -> Tuple[bool, str]:
        """验证正数"""
        if value <= 0:
            return False, f"{field_name}必须大于0"
        return True, ""
    
    @staticmethod
    def validate_non_negative_number(value: float, field_name: str = "数值") -> Tuple[bool, str]:
        """验证非负数"""
        if value < 0:
            return False, f"{field_name}不能为负数"
        return True, ""
    
    @staticmethod
    def validate_integer(value: int, field_name: str = "整数") -> Tuple[bool, str]:
        """验证整数"""
        if not isinstance(value, int):
            return False, f"{field_name}必须为整数"
        return True, ""
    
    @staticmethod
    def validate_string_length(value: str, min_length: int, max_length: int, field_name: str = "字符串") -> Tuple[bool, str]:
        """验证字符串长度"""
        if not value:
            return False, f"{field_name}不能为空"
        
        if len(value) < min_length:
            return False, f"{field_name}长度不能少于{min_length}个字符"
        
        if len(value) > max_length:
            return False, f"{field_name}长度不能超过{max_length}个字符"
        
        return True, ""


# 验证器工厂类
class ValidatorFactory:
    """验证器工厂"""
    
    @staticmethod
    def get_validator(category: str):
        """获取指定类别的验证器"""
        validators = {
            'etf': ETFValidators,
            'grid': GridValidators,
            'atr': ATRValidators,
            'date': DateValidators,
            'common': CommonValidators
        }
        return validators.get(category)
    
    @staticmethod
    def validate_all(data: Dict[str, Any], validations: Dict[str, List[Tuple[str, str]]]) -> Tuple[bool, List[str]]:
        """批量验证数据"""
        errors = []
        
        for field, validation_rules in validations.items():
            value = data.get(field)
            
            for validator_name, error_message in validation_rules:
                validator_func = getattr(CommonValidators, validator_name, None)
                if validator_func:
                    is_valid, msg = validator_func(value, field)
                    if not is_valid:
                        errors.append(f"{field}: {msg}")
                else:
                    errors.append(f"未知的验证器: {validator_name}")
        
        return len(errors) == 0, errors
