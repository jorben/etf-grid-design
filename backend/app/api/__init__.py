"""
API模块初始化
"""

from flask import Blueprint

# 创建API蓝图
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# 导入路由模块
from . import etf_routes, analysis_routes, system_routes

__version__ = "1.0.0"