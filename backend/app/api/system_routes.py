"""
系统相关API路由
"""

import logging
from flask import request, jsonify, current_app
from datetime import datetime

from . import api_bp
from ..services.file_cache_service import FileCacheService
from ..external.tushare_client import TushareClient

logger = logging.getLogger(__name__)


@api_bp.route('/system/capital-presets', methods=['GET'])
def get_capital_presets():
    """获取预设资金选项"""
    try:
        settings = current_app.settings
        capital_presets = settings.CAPITAL_CONFIG['presets']
        
        return jsonify({
            'success': True,
            'data': capital_presets
        })
        
    except Exception as e:
        logger.error(f"获取预设资金选项失败: {e}")
        return jsonify({
            'success': False,
            'error': '获取预设资金选项失败'
        }), 500


@api_bp.route('/system/health', methods=['GET'])
def health_check():
    """系统健康检查"""
    try:
        # 检查各个组件状态
        health_status = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'components': {}
        }
        
        # 检查Tushare API连接
        try:
            tushare_client = current_app.tushare_client
            api_status = tushare_client.test_connection()
            health_status['components']['tushare_api'] = {
                'status': 'healthy' if api_status else 'unhealthy',
                'message': 'API连接正常' if api_status else 'API连接异常'
            }
        except Exception as e:
            health_status['components']['tushare_api'] = {
                'status': 'error',
                'message': str(e)
            }
        
        # 检查缓存服务
        try:
            cache_service = current_app.cache_service
            cache_info = cache_service.get_cache_info()
            health_status['components']['cache_service'] = {
                'status': 'healthy',
                'message': '缓存服务正常',
                'cache_info': cache_info
            }
        except Exception as e:
            health_status['components']['cache_service'] = {
                'status': 'error',
                'message': str(e)
            }
        
        # 检查整体状态
        component_statuses = [comp['status'] for comp in health_status['components'].values()]
        if 'error' in component_statuses:
            health_status['status'] = 'error'
        elif 'unhealthy' in component_statuses:
            health_status['status'] = 'degraded'
        
        status_code = 200 if health_status['status'] == 'healthy' else 503
        
        return jsonify({
            'success': True,
            'data': health_status
        }), status_code
        
    except Exception as e:
        logger.error(f"健康检查失败: {e}")
        return jsonify({
            'success': False,
            'error': '健康检查失败',
            'timestamp': datetime.now().isoformat()
        }), 500


@api_bp.route('/system/info', methods=['GET'])
def get_system_info():
    """获取系统信息"""
    try:
        system_info = {
            'application': {
                'name': 'ETF Grid Design Backend',
                'version': '1.0.0',
                'description': 'ETF网格策略分析系统后端服务'
            },
            'api': {
                'version': 'v1',
                'base_url': '/api/v1',
                'documentation': '/api/v1/docs'
            },
            'features': [
                'ETF基本信息查询',
                'ATR技术分析',
                '网格策略计算',
                '适合性分析',
                '批量分析',
                '市场概览'
            ],
            'supported_etfs': 'A股ETF产品',
            'data_source': 'Tushare Pro API',
            'cache_strategy': '文件缓存系统'
        }
        
        return jsonify({
            'success': True,
            'data': system_info
        })
        
    except Exception as e:
        logger.error(f"获取系统信息失败: {e}")
        return jsonify({
            'success': False,
            'error': '获取系统信息失败'
        }), 500


@api_bp.route('/system/cache/info', methods=['GET'])
def get_cache_info():
    """获取缓存信息"""
    try:
        cache_service = current_app.cache_service
        cache_info = cache_service.get_cache_info()
        
        return jsonify({
            'success': True,
            'data': cache_info
        })
        
    except Exception as e:
        logger.error(f"获取缓存信息失败: {e}")
        return jsonify({
            'success': False,
            'error': '获取缓存信息失败'
        }), 500


@api_bp.route('/system/cache/clear', methods=['POST'])
def clear_cache():
    """清理缓存"""
    try:
        data = request.get_json() or {}
        cache_type = data.get('cache_type', 'daily')  # daily/historical/all
        days_to_keep = data.get('days_to_keep', 7)
        
        if cache_type not in ['daily', 'historical', 'all']:
            return jsonify({
                'success': False,
                'error': 'cache_type必须为: daily, historical, all'
            }), 400
        
        cache_service = current_app.cache_service
        
        if cache_type in ['daily', 'all']:
            cache_service.clear_expired_daily_cache(days_to_keep)
        
        # 注意：历史缓存和永久缓存通常不清理，这里只是示例
        # 实际生产环境中需要更谨慎的缓存清理策略
        
        return jsonify({
            'success': True,
            'message': f'缓存清理完成: {cache_type}',
            'parameters': {
                'cache_type': cache_type,
                'days_to_keep': days_to_keep
            }
        })
        
    except Exception as e:
        logger.error(f"清理缓存失败: {e}")
        return jsonify({
            'success': False,
            'error': '清理缓存失败'
        }), 500


@api_bp.route('/system/api/usage', methods=['GET'])
def get_api_usage():
    """获取API使用情况"""
    try:
        tushare_client = current_app.tushare_client
        usage_info = tushare_client.get_api_usage_info()
        
        return jsonify({
            'success': True,
            'data': usage_info
        })
        
    except Exception as e:
        logger.error(f"获取API使用情况失败: {e}")
        return jsonify({
            'success': False,
            'error': '获取API使用情况失败'
        }), 500


@api_bp.route('/system/config', methods=['GET'])
def get_system_config():
    """获取系统配置信息（脱敏）"""
    try:
        settings = current_app.settings
        
        # 返回脱敏的配置信息
        config_info = {
            'cache_settings': {
                'cache_dir': settings.CACHE_DIR,
                'cache_enabled': True
            },
            'api_settings': {
                'tushare_configured': bool(settings.TUSHARE_TOKEN),
                'api_timeout': 30
            },
            'popular_etfs_count': len(settings.POPULAR_ETFS),
            'environment': settings.ENVIRONMENT
        }
        
        return jsonify({
            'success': True,
            'data': config_info
        })
        
    except Exception as e:
        logger.error(f"获取系统配置失败: {e}")
        return jsonify({
            'success': False,
            'error': '获取系统配置失败'
        }), 500


@api_bp.route('/system/stats', methods=['GET'])
def get_system_stats():
    """获取系统统计信息"""
    try:
        # 这里可以添加更多统计信息，如请求次数、响应时间等
        # 目前只返回基本的缓存统计
        
        cache_service = current_app.cache_service
        cache_info = cache_service.get_cache_info()
        
        stats = {
            'cache_stats': cache_info,
            'uptime': 'N/A',  # 可以添加应用启动时间统计
            'request_count': 'N/A',  # 可以添加请求计数
            'error_count': 'N/A',  # 可以添加错误计数
            'last_update': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'data': stats
        })
        
    except Exception as e:
        logger.error(f"获取系统统计失败: {e}")
        return jsonify({
            'success': False,
            'error': '获取系统统计失败'
        }), 500


@api_bp.route('/system/test/connection', methods=['POST'])
def test_external_connections():
    """测试外部连接"""
    try:
        data = request.get_json() or {}
        test_type = data.get('test_type', 'all')  # tushare/all
        
        results = {}
        
        if test_type in ['tushare', 'all']:
            try:
                tushare_client = current_app.tushare_client
                tushare_status = tushare_client.test_connection()
                results['tushare'] = {
                    'status': 'success' if tushare_status else 'failed',
                    'message': 'Tushare API连接正常' if tushare_status else 'Tushare API连接失败'
                }
            except Exception as e:
                results['tushare'] = {
                    'status': 'error',
                    'message': str(e)
                }
        
        # 可以添加其他外部服务的连接测试
        
        overall_status = 'success' if all(r['status'] == 'success' for r in results.values()) else 'failed'
        
        return jsonify({
            'success': True,
            'data': {
                'overall_status': overall_status,
                'test_results': results,
                'test_time': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"连接测试失败: {e}")
        return jsonify({
            'success': False,
            'error': '连接测试失败'
        }), 500


@api_bp.route('/system/version', methods=['GET'])
def get_version():
    """获取版本信息"""
    try:
        version_info = {
            'version': '1.0.0',
            'build_date': '2024-01-01',
            'git_commit': 'N/A',
            'python_version': 'Python 3.8+',
            'dependencies': {
                'flask': '2.x',
                'tushare': '1.x',
                'pandas': '1.x'
            }
        }
        
        return jsonify({
            'success': True,
            'data': version_info
        })
        
    except Exception as e:
        logger.error(f"获取版本信息失败: {e}")
        return jsonify({
            'success': False,
            'error': '获取版本信息失败'
        }), 500