"""
健康检查相关路由模块
包含系统健康检查、版本信息等接口
"""

from flask import Blueprint, jsonify
from datetime import datetime

# 创建健康检查蓝图
health_bp = Blueprint('health', __name__)

# 系统版本号
VERSION = "0.1.0"

@health_bp.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    from flask import current_app
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'ETF Grid Trading Analysis System',
        'version': VERSION,
        'environment': current_app.config.get('ENV', 'development')
    })

@health_bp.route('/api/version', methods=['GET'])
def get_version():
    """获取系统版本号"""
    return jsonify({
        'success': True,
        'data': {
            'version': VERSION,
            'timestamp': datetime.now().isoformat()
        }
    })
