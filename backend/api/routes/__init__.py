"""
路由模块初始化文件
统一注册所有路由蓝图
"""

from .etf_routes import etf_bp
from .analysis_routes import analysis_bp
from .health_routes import health_bp

def register_routes(app):
    """注册所有路由蓝图到Flask应用"""
    app.register_blueprint(etf_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(health_bp)
