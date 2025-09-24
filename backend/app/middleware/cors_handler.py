"""
CORS处理中间件
"""

import logging
from flask import request, jsonify
from flask_cors import CORS

logger = logging.getLogger(__name__)


def setup_cors(app):
    """设置CORS支持"""
    
    # 配置CORS - 开发环境允许所有来源
    if app.config.get('ENV') == 'development' or app.settings.DEBUG:
        cors_config = {
            'origins': '*',  # 开发环境允许所有来源
            'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
            'allow_headers': [
                'Content-Type',
                'Authorization',
                'X-Requested-With',
                'Accept',
                'Origin'
            ],
            'supports_credentials': False,  # 允许所有来源时不能使用credentials
            'max_age': 86400
        }
    else:
        # 生产环境严格控制
        cors_config = {
            'origins': ['http://localhost:3000', 'http://127.0.0.1:3000'],
            'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
            'allow_headers': [
                'Content-Type',
                'Authorization',
                'X-Requested-With',
                'Accept',
                'Origin'
            ],
            'supports_credentials': True,
            'max_age': 86400
        }
    
    # 初始化CORS - flask_cors会自动处理所有CORS相关的头和OPTIONS请求
    CORS(app, **cors_config)
    
    logger.info("CORS配置完成")
    return app