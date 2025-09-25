"""
API中间件模块
包含统一错误处理、请求日志、性能监控等中间件
"""

import time
import logging
from flask import request, jsonify
from datetime import datetime

def register_middleware(app):
    """注册所有中间件到Flask应用"""
    
    @app.before_request
    def log_request_info():
        """请求日志中间件"""
        request.start_time = time.time()
        app.logger.info(f"请求开始: {request.method} {request.path} - "
                       f"IP: {request.remote_addr} - "
                       f"User-Agent: {request.user_agent}")
        
        # 记录POST请求的JSON数据（敏感信息需要脱敏）
        if request.method == 'POST' and request.is_json:
            data = request.get_json()
            # 脱敏处理，避免记录敏感信息
            safe_data = data.copy()
            if 'etfCode' in safe_data:
                safe_data['etfCode'] = '***'  # 脱敏ETF代码
            if 'totalCapital' in safe_data:
                safe_data['totalCapital'] = '***'  # 脱敏金额
            app.logger.info(f"请求数据: {safe_data}")
    
    @app.after_request
    def log_response_info(response):
        """响应日志中间件"""
        # 计算请求处理时间
        if hasattr(request, 'start_time'):
            processing_time = time.time() - request.start_time
            app.logger.info(f"请求完成: {request.method} {request.path} - "
                           f"状态码: {response.status_code} - "
                           f"处理时间: {processing_time:.3f}s")
            
            # 添加响应头信息
            response.headers['X-Processing-Time'] = f'{processing_time:.3f}'
            # 导入版本信息
            from config import PROJECT_VERSION
            response.headers['X-Server-Version'] = PROJECT_VERSION
        
        return response
    
    @app.errorhandler(400)
    def bad_request(error):
        """400错误处理"""
        app.logger.warning(f"客户端错误: {str(error)}")
        return jsonify({
            'success': False,
            'error': '请求参数错误',
            'error_code': 400,
            'timestamp': datetime.now().isoformat()
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        """404错误处理"""
        app.logger.warning(f"接口不存在: {request.path}")
        return jsonify({
            'success': False,
            'error': '接口不存在',
            'error_code': 404,
            'timestamp': datetime.now().isoformat()
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """405错误处理"""
        app.logger.warning(f"方法不允许: {request.method} {request.path}")
        return jsonify({
            'success': False,
            'error': '请求方法不允许',
            'error_code': 405,
            'timestamp': datetime.now().isoformat()
        }), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        """500错误处理"""
        app.logger.error(f"服务器内部错误: {str(error)}")
        import traceback
        app.logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': '服务器内部错误，请稍后重试',
            'error_code': 500,
            'timestamp': datetime.now().isoformat()
        }), 500
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """未预期错误处理"""
        app.logger.error(f"未预期错误: {str(error)}")
        import traceback
        app.logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': '系统发生未知错误，请联系管理员',
            'error_code': 500,
            'timestamp': datetime.now().isoformat()
        }), 500

def setup_cors(app):
    """CORS配置中间件"""
    from flask_cors import CORS
    
    # 配置CORS
    CORS(app, 
         resources={
             r"/api/*": {
                 "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
                 "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                 "allow_headers": ["Content-Type", "Authorization"]
             }
         })
    
    app.logger.info("CORS中间件已配置")

def setup_logging(app):
    """日志配置中间件"""
    # 确保日志配置正确
    if not app.debug:
        # 生产环境日志配置
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('app.log'),
                logging.StreamHandler()
            ]
        )
    else:
        # 开发环境日志配置
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    app.logger.info("日志中间件已配置")
