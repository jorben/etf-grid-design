"""
ETF网格交易策略分析系统 - Flask应用
基于ATR算法的智能网格交易策略设计及分析系统
重构后的主应用文件，专注于应用初始化
"""

import os
import logging
import argparse
from flask import Flask, send_from_directory, send_file
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# 导入API模块
from api import register_routes, register_middleware, setup_cors, setup_logging

# 系统版本号
VERSION = "0.1.2"

def create_app():
    """创建Flask应用实例"""
    # 根据环境变量决定静态文件配置
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    
    if FLASK_ENV == 'production':
        # 生产环境：配置静态文件服务
        app = Flask(__name__, 
                   static_folder='../static',
                   static_url_path='/static')
        app.logger.info("生产环境模式：启用静态文件服务")
    else:
        # 开发环境：不处理静态文件（前端独立运行）
        app = Flask(__name__)
        app.logger.info("开发环境模式：仅提供API服务")
    
    # 应用配置
    app.config['ENV'] = FLASK_ENV
    app.config['DEBUG'] = FLASK_ENV == 'development'
    app.config['VERSION'] = VERSION
    
    # 设置日志
    setup_logging(app)
    
    # 配置CORS
    setup_cors(app)
    
    # 注册中间件
    register_middleware(app)
    
    # 注册路由
    register_routes(app)
    
    # 只在生产环境添加静态文件路由
    if FLASK_ENV == 'production':
        setup_static_routes(app)
    
    return app

def setup_static_routes(app):
    """设置静态文件路由（仅生产环境）"""
    
    @app.route('/')
    def serve_index():
        """服务前端主页"""
        try:
            return send_file('../static/index.html')
        except FileNotFoundError:
            app.logger.error("静态文件 index.html 不存在")
            return {
                'success': False,
                'error': '前端文件未找到，请检查构建是否完成'
            }, 404
    
    @app.route('/<path:path>')
    def serve_static_files(path):
        """服务静态文件，支持SPA路由"""
        # 如果是API路由，跳过静态文件处理
        if path.startswith('api/'):
            return None
        
        # 定义前端路由路径（这些路径应该返回 index.html）
        frontend_routes = ['analysis', 'dashboard', 'settings', 'help']
        
        # 检查是否是前端路由
        if any(path.startswith(route) for route in frontend_routes):
            try:
                return send_file('../static/index.html')
            except FileNotFoundError:
                app.logger.error("静态文件 index.html 不存在")
                return {
                    'success': False,
                    'error': '前端文件未找到'
                }, 404
        
        # 尝试提供静态文件
        try:
            return send_from_directory('../static', path)
        except FileNotFoundError:
            # 文件不存在时返回index.html（支持其他前端路由）
            try:
                return send_file('../static/index.html')
            except FileNotFoundError:
                app.logger.error("静态文件 index.html 不存在")
                return {
                    'success': False,
                    'error': '前端文件未找到'
                }, 404

# 创建应用实例
app = create_app()

if __name__ == '__main__':
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='ETF网格交易策略分析系统')
    parser.add_argument('--port', type=int, default=None, help='服务器端口号')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='服务器主机地址')
    args = parser.parse_args()
    
    # 优先级：命令行参数 > 环境变量 > 默认值
    port = args.port or int(os.environ.get('PORT', 5001))
    host = args.host
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.logger.info(f"启动ETF网格交易策略分析系统，版本: {VERSION}, 端口: {port}")
    app.run(host=host, port=port, debug=debug)
