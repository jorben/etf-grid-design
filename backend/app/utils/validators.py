"""
数据验证工具函数
"""

import re
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
from app.config.settings import Settings

def validate_etf_code(etf_code: str) -> Tuple[bool, str]:
    """
    验证ETF代码
    
    Args:
        etf_code: ETF代码
        
    Returns:
        (是否有效, 错误信息)
    """
    if not etf_code:
        return False, "ETF代码不能为空"
    
    if not isinstance(etf_code, str):
        return False, "ETF代码必须是字符串"
    
    etf_code = etf_code.strip()
    if len(etf_code) != 6:
        return False, "ETF代码必须是6位数字"
    
    if not etf_code.isdigit():
        return False, "ETF代码必须是纯数字"
    
    return True, ""

def validate_capital(capital: float) -> Tuple[bool, str]:
    """
    验证投资金额
    
    Args:
        capital: 投资金额
        
    Returns:
        (是否有效, 错误信息)
    """
    if not isinstance(capital, (int, float)):
        return False, "投资金额必须是数字"
    
    if capital <= 0:
        return False, "投资金额必须大于0"
    
    if capital < Settings.CAPITAL_CONFIG['min_capital']:
        return False, f"投资金额不能少于{Settings.CAPITAL_CONFIG['min_capital']:,}元"
    
    if capital > Settings.CAPITAL_CONFIG['max_capital']:
        return False, f"投资金额不能超过{Settings.CAPITAL_CONFIG['max_capital']:,}元"
    
    return True, ""

def validate_date_range(start_date: str, end_date: str) -> Tuple[bool, str]:
    """
    验证日期范围
    
    Args:
        start_date: 开始日期字符串 (YYYY-MM-DD)
        end_date: 结束日期字符串 (YYYY-MM-DD)
        
    Returns:
        (是否有效, 错误信息)
    """
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        if start >= end:
            return False, "开始日期必须早于结束日期"
        
        if end > datetime.now():
            return False, "结束日期不能超过当前日期"
        
        if (end - start).days > 365 * 5:  # 最多5年
            return False, "日期范围不能超过5年"
        
        if (end - start).days < 30:  # 至少30天
            return False, "日期范围至少需要30天"
        
        return True, ""
        
    except ValueError:
        return False, "日期格式错误，请使用YYYY-MM-DD格式"

def validate_grid_type(grid_type: str) -> Tuple[bool, str]:
    """
    验证网格类型
    
    Args:
        grid_type: 网格类型
        
    Returns:
        (是否有效, 错误信息)
    """
    valid_types = ['等差', '等比']
    if grid_type not in valid_types:
        return False, f"网格类型必须是{valid_types}之一"
    return True, ""

def validate_risk_preference(risk_preference: str) -> Tuple[bool, str]:
    """
    验证风险偏好
    
    Args:
        risk_preference: 风险偏好
        
    Returns:
        (是否有效, 错误信息)
    """
    valid_preferences = ['保守', '稳健', '激进']
    if risk_preference not in valid_preferences:
        return False, f"风险偏好必须是{valid_preferences}之一"
    return True, ""

def validate_parameters(params: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    验证分析参数
    
    Args:
        params: 参数字典
        
    Returns:
        (是否有效, 错误信息列表)
    """
    errors = []
    
    # 验证ETF代码
    etf_code = params.get('etfCode', '')
    is_valid, error = validate_etf_code(etf_code)
    if not is_valid:
        errors.append(error)
    
    # 验证投资金额
    total_capital = params.get('totalCapital', 0)
    try:
        total_capital = float(total_capital)
        is_valid, error = validate_capital(total_capital)
        if not is_valid:
            errors.append(error)
    except (ValueError, TypeError):
        errors.append("投资金额必须是有效数字")
    
    # 验证网格类型
    grid_type = params.get('gridType', '')
    is_valid, error = validate_grid_type(grid_type)
    if not is_valid:
        errors.append(error)
    
    # 验证风险偏好
    risk_preference = params.get('riskPreference', '')
    is_valid, error = validate_risk_preference(risk_preference)
    if not is_valid:
        errors.append(error)
    
    return len(errors) == 0, errors

def validate_price(price: float) -> Tuple[bool, str]:
    """
    验证价格
    
    Args:
        price: 价格
        
    Returns:
        (是否有效, 错误信息)
    """
    if not isinstance(price, (int, float)):
        return False, "价格必须是数字"
    
    if price <= 0:
        return False, "价格必须大于0"
    
    if price > 10000:  # 假设ETF价格不会超过10000
        return False, "价格异常，请检查数据"
    
    return True, ""

def validate_volume(volume: int) -> Tuple[bool, str]:
    """
    验证成交量
    
    Args:
        volume: 成交量
        
    Returns:
        (是否有效, 错误信息)
    """
    if not isinstance(volume, int):
        return False, "成交量必须是整数"
    
    if volume < 0:
        return False, "成交量不能为负数"
    
    return True, ""

def validate_email(email: str) -> Tuple[bool, str]:
    """
    验证邮箱格式
    
    Args:
        email: 邮箱地址
        
    Returns:
        (是否有效, 错误信息)
    """
    if not email:
        return False, "邮箱地址不能为空"
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "邮箱格式不正确"
    
    return True, ""

def validate_phone(phone: str) -> Tuple[bool, str]:
    """
    验证手机号格式
    
    Args:
        phone: 手机号
        
    Returns:
        (是否有效, 错误信息)
    """
    if not phone:
        return False, "手机号不能为空"
    
    # 简单的中国手机号验证
    pattern = r'^1[3-9]\d{9}$'
    if not re.match(pattern, phone):
        return False, "手机号格式不正确"
    
    return True, ""

def validate_date_format(date_str: str) -> bool:
    """
    验证日期格式 (YYYYMMDD)
    
    Args:
        date_str: 日期字符串
        
    Returns:
        bool: 是否有效
    """
    if not date_str or not isinstance(date_str, str):
        return False
    
    if len(date_str) != 8:
        return False
    
    if not date_str.isdigit():
        return False
    
    try:
        datetime.strptime(date_str, '%Y%m%d')
        return True
    except ValueError:
        return False

def validate_positive_number(number) -> bool:
    """
    验证正数
    
    Args:
        number: 数字
        
    Returns:
        bool: 是否为正数
    """
    try:
        num = float(number)
        return num > 0
    except (ValueError, TypeError):
        return False