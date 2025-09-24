"""
ETF相关路由模块
包含ETF信息查询、热门ETF列表、资金预设等接口
"""

from flask import Blueprint, request, jsonify
from services.analysis.etf_analysis_service import ETFAnalysisService

# 创建ETF蓝图
etf_bp = Blueprint('etf', __name__)
etf_service = ETFAnalysisService()

@etf_bp.route('/api/popular-etfs', methods=['GET'])
def get_popular_etfs():
    """获取热门ETF列表"""
    try:
        popular_etfs = etf_service.get_popular_etfs()
        return jsonify({
            'success': True,
            'data': popular_etfs
        })
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"获取热门ETF列表失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': '获取热门ETF列表失败'
        }), 500

@etf_bp.route('/api/etf/basic-info/<etf_code>', methods=['GET'])
def get_etf_basic_info(etf_code):
    """获取ETF基础信息"""
    try:
        # 验证ETF代码格式
        if not etf_code or len(etf_code) != 6 or not etf_code.isdigit():
            return jsonify({
                'success': False,
                'error': 'ETF代码格式错误，请输入6位数字'
            }), 400
        
        etf_info = etf_service.get_etf_basic_info(etf_code)
        return jsonify({
            'success': True,
            'data': etf_info
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"获取ETF基础信息失败: {etf_code}, {str(e)}")
        return jsonify({
            'success': False,
            'error': '获取ETF信息失败，请检查代码是否正确'
        }), 500

@etf_bp.route('/api/capital-presets', methods=['GET'])
def get_capital_presets():
    """获取预设资金选项"""
    try:
        capital_presets = [
            {'value': 100000, 'label': '10万', 'popular': True},
            {'value': 200000, 'label': '20万', 'popular': True},
            {'value': 300000, 'label': '30万', 'popular': False},
            {'value': 500000, 'label': '50万', 'popular': True},
            {'value': 800000, 'label': '80万', 'popular': False},
            {'value': 1000000, 'label': '100万', 'popular': True},
            {'value': 1500000, 'label': '150万', 'popular': False},
            {'value': 2000000, 'label': '200万', 'popular': False}
        ]
        
        return jsonify({
            'success': True,
            'data': capital_presets
        })
        
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"获取预设资金选项失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': '获取预设资金选项失败'
        }), 500
