"""
格式化工具函数
"""

from typing import Union

def format_currency(amount: float, currency: str = 'CNY') -> str:
    """
    格式化货币金额
    
    Args:
        amount: 金额
        currency: 货币类型
        
    Returns:
        格式化后的货币字符串
    """
    if currency == 'CNY':
        if amount >= 100000000:  # 1亿
            return f"¥{amount/100000000:.2f}亿"
        elif amount >= 10000:  # 1万
            return f"¥{amount/10000:.2f}万"
        else:
            return f"¥{amount:,.2f}"
    else:
        return f"{amount:,.2f}"

def format_percentage(value: float, decimal_places: int = 2) -> str:
    """
    格式化百分比
    
    Args:
        value: 数值（0.1 表示 10%）
        decimal_places: 小数位数
        
    Returns:
        格式化后的百分比字符串
    """
    return f"{value * 100:.{decimal_places}f}%"

def format_number(value: Union[int, float], decimal_places: int = 2) -> str:
    """
    格式化数字
    
    Args:
        value: 数值
        decimal_places: 小数位数
        
    Returns:
        格式化后的数字字符串
    """
    if isinstance(value, int):
        return f"{value:,}"
    else:
        return f"{value:,.{decimal_places}f}"

def format_ratio(value: float, decimal_places: int = 2) -> str:
    """
    格式化比率
    
    Args:
        value: 比率值
        decimal_places: 小数位数
        
    Returns:
        格式化后的比率字符串
    """
    return f"{value:.{decimal_places}f}"

def format_price(price: float, decimal_places: int = 3) -> str:
    """
    格式化价格
    
    Args:
        price: 价格
        decimal_places: 小数位数
        
    Returns:
        格式化后的价格字符串
    """
    return f"¥{price:.{decimal_places}f}"

def format_volume(volume: int) -> str:
    """
    格式化成交量
    
    Args:
        volume: 成交量
        
    Returns:
        格式化后的成交量字符串
    """
    if volume >= 100000000:  # 1亿
        return f"{volume/100000000:.2f}亿"
    elif volume >= 10000:  # 1万
        return f"{volume/10000:.2f}万"
    else:
        return f"{volume:,}"

def format_amount(amount: float) -> str:
    """
    格式化成交额
    
    Args:
        amount: 成交额
        
    Returns:
        格式化后的成交额字符串
    """
    return format_currency(amount)

def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    截断文本
    
    Args:
        text: 原始文本
        max_length: 最大长度
        suffix: 后缀
        
    Returns:
        截断后的文本
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix