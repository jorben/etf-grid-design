"""
ETF相关API路由
"""

import logging
from flask import request, jsonify, current_app
from typing import Dict, Any

from . import api_bp
from ..services.etf_service import ETFService
from ..exceptions.business_exceptions import ETFNotFoundError, DataValidationError
from ..utils.validators import validate_etf_code, validate_date_format

logger = logging.getLogger(__name__)


@api_bp.route('/etfs/popular', methods=['GET'])
def get_popular_etfs():
    """获取热门ETF列表"""
    try:
        etf_service = current_app.etf_service
        popular_etfs = etf_service.get_popular_etfs()
        
        return jsonify({
            'success': True,
            'data': [etf.__dict__ for etf in popular_etfs],
            'count': len(popular_etfs)
        })
        
    except Exception as e:
        logger.error(f"获取热门ETF列表失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/etfs/<etf_code>/basic', methods=['GET'])
def get_etf_basic_info(etf_code: str):
    """获取ETF基本信息"""
    try:
        if not validate_etf_code(etf_code):
            return jsonify({
                'success': False,
                'error': '无效的ETF代码'
            }), 400
        
        etf_service = current_app.etf_service
        basic_info = etf_service.get_etf_basic_info(etf_code)
        
        if not basic_info:
            return jsonify({
                'success': False,
                'error': f'未找到ETF: {etf_code}'
            }), 404
        
        return jsonify({
            'success': True,
            'data': basic_info if isinstance(basic_info, dict) else basic_info.__dict__
        })
        
    except ETFNotFoundError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except DataValidationError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        logger.error(f"获取ETF基本信息失败 {etf_code}: {e}")
        return jsonify({
            'success': False,
            'error': '服务器内部错误'
        }), 500


@api_bp.route('/etfs/<etf_code>/latest', methods=['GET'])
def get_etf_latest_data(etf_code: str):
    """获取ETF最新价格数据"""
    try:
        if not validate_etf_code(etf_code):
            return jsonify({
                'success': False,
                'error': '无效的ETF代码'
            }), 400
        
        etf_service = current_app.etf_service
        latest_data = etf_service.get_etf_latest_data(etf_code)
        
        if not latest_data:
            return jsonify({
                'success': False,
                'error': f'未找到ETF最新数据: {etf_code}'
            }), 404
        
        return jsonify({
            'success': True,
            'data': latest_data.__dict__
        })
        
    except ETFNotFoundError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except DataValidationError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        logger.error(f"获取ETF最新数据失败 {etf_code}: {e}")
        return jsonify({
            'success': False,
            'error': '服务器内部错误'
        }), 500


@api_bp.route('/etfs/<etf_code>/historical', methods=['GET'])
def get_etf_historical_data(etf_code: str):
    """获取ETF历史数据"""
    try:
        if not validate_etf_code(etf_code):
            return jsonify({
                'success': False,
                'error': '无效的ETF代码'
            }), 400
        
        # 获取查询参数
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({
                'success': False,
                'error': '缺少必要参数: start_date, end_date'
            }), 400
        
        if not validate_date_format(start_date) or not validate_date_format(end_date):
            return jsonify({
                'success': False,
                'error': '日期格式错误，应为YYYYMMDD格式'
            }), 400
        
        etf_service = current_app.etf_service
        historical_data = etf_service.get_etf_historical_data(etf_code, start_date, end_date)
        
        return jsonify({
            'success': True,
            'data': [data.__dict__ for data in historical_data],
            'count': len(historical_data),
            'period': {
                'start_date': start_date,
                'end_date': end_date
            }
        })
        
    except DataValidationError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        logger.error(f"获取ETF历史数据失败 {etf_code}: {e}")
        return jsonify({
            'success': False,
            'error': '服务器内部错误'
        }), 500


@api_bp.route('/etfs/<etf_code>/summary', methods=['GET'])
def get_etf_summary(etf_code: str):
    """获取ETF综合信息摘要"""
    try:
        if not validate_etf_code(etf_code):
            return jsonify({
                'success': False,
                'error': '无效的ETF代码'
            }), 400
        
        etf_service = current_app.etf_service
        summary = etf_service.get_etf_summary(etf_code)
        
        return jsonify({
            'success': True,
            'data': summary
        })
        
    except Exception as e:
        logger.error(f"获取ETF综合信息失败 {etf_code}: {e}")
        return jsonify({
            'success': False,
            'error': '服务器内部错误'
        }), 500


@api_bp.route('/etfs/search', methods=['GET'])
def search_etfs():
    """搜索ETF"""
    try:
        keyword = request.args.get('keyword', '').strip()
        
        if not keyword:
            return jsonify({
                'success': False,
                'error': '搜索关键词不能为空'
            }), 400
        
        if len(keyword) < 2:
            return jsonify({
                'success': False,
                'error': '搜索关键词至少需要2个字符'
            }), 400
        
        etf_service = current_app.etf_service
        results = etf_service.search_etf(keyword)
        
        return jsonify({
            'success': True,
            'data': [result.__dict__ for result in results],
            'count': len(results),
            'keyword': keyword
        })
        
    except Exception as e:
        logger.error(f"搜索ETF失败: {e}")
        return jsonify({
            'success': False,
            'error': '服务器内部错误'
        }), 500


@api_bp.route('/etfs/batch/latest', methods=['POST'])
def get_batch_etf_latest():
    """批量获取ETF最新数据"""
    try:
        data = request.get_json()
        
        if not data or 'etf_codes' not in data:
            return jsonify({
                'success': False,
                'error': '缺少必要参数: etf_codes'
            }), 400
        
        etf_codes = data['etf_codes']
        
        if not isinstance(etf_codes, list) or not etf_codes:
            return jsonify({
                'success': False,
                'error': 'etf_codes必须是非空数组'
            }), 400
        
        if len(etf_codes) > 20:
            return jsonify({
                'success': False,
                'error': '单次最多查询20个ETF'
            }), 400
        
        etf_service = current_app.etf_service
        results = {}
        errors = {}
        
        for etf_code in etf_codes:
            try:
                if not validate_etf_code(etf_code):
                    errors[etf_code] = '无效的ETF代码'
                    continue
                
                latest_data = etf_service.get_etf_latest_data(etf_code)
                if latest_data:
                    results[etf_code] = latest_data.__dict__
                else:
                    errors[etf_code] = '未找到数据'
                    
            except Exception as e:
                errors[etf_code] = str(e)
        
        return jsonify({
            'success': True,
            'data': results,
            'errors': errors,
            'success_count': len(results),
            'error_count': len(errors)
        })
        
    except Exception as e:
        logger.error(f"批量获取ETF数据失败: {e}")
        return jsonify({
            'success': False,
            'error': '服务器内部错误'
        }), 500


@api_bp.route('/etfs/categories', methods=['GET'])
def get_etf_categories():
    """获取ETF分类统计"""
    try:
        etf_service = current_app.etf_service
        popular_etfs = etf_service.get_popular_etfs()
        
        # 统计分类
        categories = {}
        for etf in popular_etfs:
            category = etf.category
            if category not in categories:
                categories[category] = {
                    'name': category,
                    'count': 0,
                    'etfs': []
                }
            categories[category]['count'] += 1
            categories[category]['etfs'].append({
                'code': etf.code,
                'name': etf.name
            })
        
        return jsonify({
            'success': True,
            'data': list(categories.values()),
            'total_categories': len(categories)
        })
        
    except Exception as e:
        logger.error(f"获取ETF分类失败: {e}")
        return jsonify({
            'success': False,
            'error': '服务器内部错误'
        }), 500