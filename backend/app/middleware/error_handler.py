"""
错误处理中间件
"""

import logging
from flask import jsonify, request
from werkzeug.exceptions import HTTPException
from datetime import datetime

from ..exceptions.base_exceptions import BaseAPIException
from ..exceptions.business_exceptions import (
    ETFNotFoundError, DataValidationError, AnalysisError, 
    CacheError, ExternalAPIError, ConfigurationError
)

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    """注册错误处理器"""
    
    @app.errorhandler(BaseAPIException)
    def handle_business_exception(error):
        """处理业务异常"""
        logger.warning(f"业务异常: {error}")
        return jsonify({
            'success': False,
            'error': str(error),
            'error_type': error.__class__.__name__,
            'timestamp': datetime.now().isoformat()
        }), error.status_code
    
    @app.errorhandler(ETFNotFoundError)
    def handle_etf_not_found(error):
        """处理ETF未找到异常"""
        logger.warning(f"ETF未找到: {error}")
        return jsonify({
            'success': False,
            'error': str(error),
            'error_type': 'ETFNotFoundError',
            'timestamp': datetime.now().isoformat()
        }), 404
    
    @app.errorhandler(DataValidationError)
    def handle_validation_error(error):
        """处理数据验证异常"""
        logger.warning(f"数据验证错误: {error}")
        return jsonify({
            'success': False,
            'error': str(error),
            'error_type': 'DataValidationError',
            'timestamp': datetime.now().isoformat()
        }), 400
    
    @app.errorhandler(AnalysisError)
    def handle_analysis_error(error):
        """处理分析异常"""
        logger.error(f"分析错误: {error}")
        return jsonify({
            'success': False,
            'error': str(error),
            'error_type': 'AnalysisError',
            'timestamp': datetime.now().isoformat()
        }), 422
    
    @app.errorhandler(CacheError)
    def handle_cache_error(error):
        """处理缓存异常"""
        logger.error(f"缓存错误: {error}")
        return jsonify({
            'success': False,
            'error': '缓存服务异常，请稍后重试',
            'error_type': 'CacheError',
            'timestamp': datetime.now().isoformat()
        }), 500
    
    @app.errorhandler(ExternalAPIError)
    def handle_external_api_error(error):
        """处理外部API异常"""
        logger.error(f"外部API错误: {error}")
        return jsonify({
            'success': False,
            'error': '外部数据服务异常，请稍后重试',
            'error_type': 'ExternalAPIError',
            'timestamp': datetime.now().isoformat()
        }), 503
    
    @app.errorhandler(ConfigurationError)
    def handle_configuration_error(error):
        """处理配置异常"""
        logger.error(f"配置错误: {error}")
        return jsonify({
            'success': False,
            'error': '系统配置异常',
            'error_type': 'ConfigurationError',
            'timestamp': datetime.now().isoformat()
        }), 500
    
    @app.errorhandler(400)
    def handle_bad_request(error):
        """处理400错误"""
        logger.warning(f"请求错误 400: {request.url}")
        return jsonify({
            'success': False,
            'error': '请求参数错误',
            'error_type': 'BadRequest',
            'timestamp': datetime.now().isoformat()
        }), 400
    
    @app.errorhandler(401)
    def handle_unauthorized(error):
        """处理401错误"""
        logger.warning(f"未授权访问 401: {request.url}")
        return jsonify({
            'success': False,
            'error': '未授权访问',
            'error_type': 'Unauthorized',
            'timestamp': datetime.now().isoformat()
        }), 401
    
    @app.errorhandler(403)
    def handle_forbidden(error):
        """处理403错误"""
        logger.warning(f"禁止访问 403: {request.url}")
        return jsonify({
            'success': False,
            'error': '禁止访问',
            'error_type': 'Forbidden',
            'timestamp': datetime.now().isoformat()
        }), 403
    
    @app.errorhandler(404)
    def handle_not_found(error):
        """处理404错误"""
        logger.warning(f"资源未找到 404: {request.url}")
        return jsonify({
            'success': False,
            'error': '请求的资源不存在',
            'error_type': 'NotFound',
            'timestamp': datetime.now().isoformat()
        }), 404
    
    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """处理405错误"""
        logger.warning(f"方法不允许 405: {request.method} {request.url}")
        return jsonify({
            'success': False,
            'error': '请求方法不允许',
            'error_type': 'MethodNotAllowed',
            'timestamp': datetime.now().isoformat()
        }), 405
    
    @app.errorhandler(429)
    def handle_rate_limit(error):
        """处理429错误"""
        logger.warning(f"请求频率限制 429: {request.url}")
        return jsonify({
            'success': False,
            'error': '请求过于频繁，请稍后重试',
            'error_type': 'RateLimitExceeded',
            'timestamp': datetime.now().isoformat()
        }), 429
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        """处理500错误"""
        logger.error(f"服务器内部错误 500: {request.url}, 错误: {error}")
        return jsonify({
            'success': False,
            'error': '服务器内部错误',
            'error_type': 'InternalServerError',
            'timestamp': datetime.now().isoformat()
        }), 500
    
    @app.errorhandler(502)
    def handle_bad_gateway(error):
        """处理502错误"""
        logger.error(f"网关错误 502: {request.url}")
        return jsonify({
            'success': False,
            'error': '网关错误',
            'error_type': 'BadGateway',
            'timestamp': datetime.now().isoformat()
        }), 502
    
    @app.errorhandler(503)
    def handle_service_unavailable(error):
        """处理503错误"""
        logger.error(f"服务不可用 503: {request.url}")
        return jsonify({
            'success': False,
            'error': '服务暂时不可用，请稍后重试',
            'error_type': 'ServiceUnavailable',
            'timestamp': datetime.now().isoformat()
        }), 503
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """处理其他HTTP异常"""
        logger.warning(f"HTTP异常 {error.code}: {request.url}")
        return jsonify({
            'success': False,
            'error': error.description or 'HTTP错误',
            'error_type': 'HTTPException',
            'status_code': error.code,
            'timestamp': datetime.now().isoformat()
        }), error.code
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """处理未预期的异常"""
        logger.error(f"未预期的异常: {request.url}, 错误: {error}", exc_info=True)
        return jsonify({
            'success': False,
            'error': '系统发生未知错误',
            'error_type': 'UnexpectedError',
            'timestamp': datetime.now().isoformat()
        }), 500
    
    # 请求前处理
    @app.before_request
    def log_request_info():
        """记录请求信息"""
        logger.debug(f"请求: {request.method} {request.url}")
        if request.is_json and request.get_json():
            logger.debug(f"请求数据: {request.get_json()}")
    
    # 请求后处理
    @app.after_request
    def log_response_info(response):
        """记录响应信息"""
        logger.debug(f"响应: {response.status_code}")
        return response
    
    logger.info("错误处理器注册完成")