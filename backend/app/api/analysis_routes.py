"""
分析相关API路由
"""

import logging
from flask import request, jsonify, current_app
from typing import Dict, Any

from . import api_bp
from ..services.analysis_service import AnalysisService
from ..exceptions.business_exceptions import AnalysisError, DataValidationError
from ..utils.validators import validate_etf_code, validate_positive_number

logger = logging.getLogger(__name__)


@api_bp.route('/analysis/suitability/<etf_code>', methods=['POST'])
def analyze_etf_suitability(etf_code: str):
    """分析ETF适合性"""
    try:
        if not validate_etf_code(etf_code):
            return jsonify({
                'success': False,
                'error': '无效的ETF代码'
            }), 400
        
        data = request.get_json() or {}
        
        # 获取参数
        investment_amount = data.get('investment_amount', 10000.0)
        risk_tolerance = data.get('risk_tolerance', 'medium')
        
        # 参数验证
        if not validate_positive_number(investment_amount):
            return jsonify({
                'success': False,
                'error': '投资金额必须为正数'
            }), 400
        
        if risk_tolerance not in ['low', 'medium', 'high']:
            return jsonify({
                'success': False,
                'error': '风险承受能力必须为: low, medium, high'
            }), 400
        
        analysis_service = current_app.analysis_service
        suitability = analysis_service.analyze_etf_suitability(
            etf_code, investment_amount, risk_tolerance
        )
        
        return jsonify({
            'success': True,
            'data': suitability.__dict__ if hasattr(suitability, '__dict__') else suitability
        })
        
    except DataValidationError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except AnalysisError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 422
    except Exception as e:
        logger.error(f"适合性分析失败 {etf_code}: {e}")
        return jsonify({
            'success': False,
            'error': '服务器内部错误'
        }), 500


@api_bp.route('/analysis/atr/<etf_code>', methods=['GET'])
def calculate_atr_analysis(etf_code: str):
    """计算ATR分析"""
    try:
        if not validate_etf_code(etf_code):
            return jsonify({
                'success': False,
                'error': '无效的ETF代码'
            }), 400
        
        # 获取查询参数
        period = request.args.get('period', 20, type=int)
        
        if period <= 0 or period > 100:
            return jsonify({
                'success': False,
                'error': 'ATR周期必须在1-100之间'
            }), 400
        
        analysis_service = current_app.analysis_service
        atr_result = analysis_service.calculate_atr_analysis(etf_code, period)
        
        return jsonify({
            'success': True,
            'data': atr_result
        })
        
    except DataValidationError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except AnalysisError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 422
    except Exception as e:
        logger.error(f"ATR分析失败 {etf_code}: {e}")
        return jsonify({
            'success': False,
            'error': '服务器内部错误'
        }), 500


@api_bp.route('/analysis/grid/<etf_code>', methods=['POST'])
def generate_grid_strategy(etf_code: str):
    """生成网格策略"""
    try:
        if not validate_etf_code(etf_code):
            return jsonify({
                'success': False,
                'error': '无效的ETF代码'
            }), 400
        
        data = request.get_json() or {}
        
        # 获取参数
        investment_amount = data.get('investment_amount', 10000.0)
        grid_count = data.get('grid_count', 10)
        price_range_percent = data.get('price_range_percent', 0.2)
        
        # 参数验证
        if not validate_positive_number(investment_amount):
            return jsonify({
                'success': False,
                'error': '投资金额必须为正数'
            }), 400
        
        if not isinstance(grid_count, int) or grid_count <= 0 or grid_count > 50:
            return jsonify({
                'success': False,
                'error': '网格数量必须在1-50之间'
            }), 400
        
        if not isinstance(price_range_percent, (int, float)) or price_range_percent <= 0 or price_range_percent > 1:
            return jsonify({
                'success': False,
                'error': '价格范围百分比必须在0-1之间'
            }), 400
        
        analysis_service = current_app.analysis_service
        grid_result = analysis_service.generate_grid_strategy(
            etf_code, investment_amount, grid_count, price_range_percent
        )
        
        return jsonify({
            'success': True,
            'data': grid_result.__dict__ if hasattr(grid_result, '__dict__') else grid_result
        })
        
    except DataValidationError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except AnalysisError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 422
    except Exception as e:
        logger.error(f"网格策略生成失败 {etf_code}: {e}")
        return jsonify({
            'success': False,
            'error': '服务器内部错误'
        }), 500


@api_bp.route('/analysis/comprehensive/<etf_code>', methods=['POST'])
def comprehensive_analysis(etf_code: str):
    """综合分析"""
    try:
        if not validate_etf_code(etf_code):
            return jsonify({
                'success': False,
                'error': '无效的ETF代码'
            }), 400
        
        data = request.get_json() or {}
        
        # 获取参数
        investment_amount = data.get('investment_amount', 10000.0)
        risk_tolerance = data.get('risk_tolerance', 'medium')
        grid_count = data.get('grid_count', 10)
        
        # 参数验证
        if not validate_positive_number(investment_amount):
            return jsonify({
                'success': False,
                'error': '投资金额必须为正数'
            }), 400
        
        if risk_tolerance not in ['low', 'medium', 'high']:
            return jsonify({
                'success': False,
                'error': '风险承受能力必须为: low, medium, high'
            }), 400
        
        if not isinstance(grid_count, int) or grid_count <= 0 or grid_count > 50:
            return jsonify({
                'success': False,
                'error': '网格数量必须在1-50之间'
            }), 400
        
        analysis_service = current_app.analysis_service
        comprehensive_result = analysis_service.comprehensive_analysis(
            etf_code, investment_amount, risk_tolerance, grid_count
        )
        
        return jsonify({
            'success': True,
            'data': comprehensive_result
        })
        
    except DataValidationError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except AnalysisError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 422
    except Exception as e:
        logger.error(f"综合分析失败 {etf_code}: {e}")
        return jsonify({
            'success': False,
            'error': '服务器内部错误'
        }), 500


@api_bp.route('/analysis/batch/popular', methods=['POST'])
def batch_analyze_popular_etfs():
    """批量分析热门ETF"""
    try:
        data = request.get_json() or {}
        
        # 获取参数
        investment_amount = data.get('investment_amount', 10000.0)
        risk_tolerance = data.get('risk_tolerance', 'medium')
        
        # 参数验证
        if not validate_positive_number(investment_amount):
            return jsonify({
                'success': False,
                'error': '投资金额必须为正数'
            }), 400
        
        if risk_tolerance not in ['low', 'medium', 'high']:
            return jsonify({
                'success': False,
                'error': '风险承受能力必须为: low, medium, high'
            }), 400
        
        analysis_service = current_app.analysis_service
        results = analysis_service.batch_analyze_popular_etfs(
            investment_amount, risk_tolerance
        )
        
        return jsonify({
            'success': True,
            'data': results,
            'count': len(results)
        })
        
    except AnalysisError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 422
    except Exception as e:
        logger.error(f"批量分析失败: {e}")
        return jsonify({
            'success': False,
            'error': '服务器内部错误'
        }), 500


@api_bp.route('/analysis/market/overview', methods=['GET'])
def get_market_overview():
    """获取市场概览"""
    try:
        analysis_service = current_app.analysis_service
        overview = analysis_service.get_market_overview()
        
        return jsonify({
            'success': True,
            'data': overview
        })
        
    except Exception as e:
        logger.error(f"获取市场概览失败: {e}")
        return jsonify({
            'success': False,
            'error': '服务器内部错误'
        }), 500


@api_bp.route('/analysis/compare', methods=['POST'])
def compare_etfs():
    """比较多个ETF"""
    try:
        data = request.get_json()
        
        if not data or 'etf_codes' not in data:
            return jsonify({
                'success': False,
                'error': '缺少必要参数: etf_codes'
            }), 400
        
        etf_codes = data['etf_codes']
        investment_amount = data.get('investment_amount', 10000.0)
        risk_tolerance = data.get('risk_tolerance', 'medium')
        
        if not isinstance(etf_codes, list) or not etf_codes:
            return jsonify({
                'success': False,
                'error': 'etf_codes必须是非空数组'
            }), 400
        
        if len(etf_codes) > 10:
            return jsonify({
                'success': False,
                'error': '单次最多比较10个ETF'
            }), 400
        
        # 验证ETF代码
        for etf_code in etf_codes:
            if not validate_etf_code(etf_code):
                return jsonify({
                    'success': False,
                    'error': f'无效的ETF代码: {etf_code}'
                }), 400
        
        # 参数验证
        if not validate_positive_number(investment_amount):
            return jsonify({
                'success': False,
                'error': '投资金额必须为正数'
            }), 400
        
        if risk_tolerance not in ['low', 'medium', 'high']:
            return jsonify({
                'success': False,
                'error': '风险承受能力必须为: low, medium, high'
            }), 400
        
        analysis_service = current_app.analysis_service
        comparison_results = []
        
        for etf_code in etf_codes:
            try:
                # 进行适合性分析
                suitability = analysis_service.analyze_etf_suitability(
                    etf_code, investment_amount, risk_tolerance
                )
                
                # 获取ATR分析
                atr_result = analysis_service.calculate_atr_analysis(etf_code)
                
                comparison_results.append({
                    'etf_code': etf_code,
                    'suitability': suitability.__dict__ if hasattr(suitability, '__dict__') else suitability,
                    'atr_analysis': atr_result.__dict__ if hasattr(atr_result, '__dict__') else atr_result
                })
                
            except Exception as e:
                logger.warning(f"分析ETF {etf_code} 失败: {e}")
                comparison_results.append({
                    'etf_code': etf_code,
                    'error': str(e)
                })
        
        # 按适合性评分排序
        valid_results = [r for r in comparison_results if 'error' not in r]
        valid_results.sort(
            key=lambda x: x['suitability']['total_score'], 
            reverse=True
        )
        
        return jsonify({
            'success': True,
            'data': {
                'comparison_results': comparison_results,
                'ranked_results': valid_results,
                'parameters': {
                    'investment_amount': investment_amount,
                    'risk_tolerance': risk_tolerance
                }
            },
            'count': len(etf_codes)
        })
        
    except Exception as e:
        logger.error(f"ETF比较失败: {e}")
        return jsonify({
            'success': False,
            'error': '服务器内部错误'
        }), 500


@api_bp.route('/analysis/recommendations', methods=['POST'])
def get_investment_recommendations():
    """获取投资建议"""
    try:
        data = request.get_json() or {}
        
        # 获取参数
        investment_amount = data.get('investment_amount', 10000.0)
        risk_tolerance = data.get('risk_tolerance', 'medium')
        investment_period = data.get('investment_period', 'medium')  # short/medium/long
        preferred_categories = data.get('preferred_categories', [])
        
        # 参数验证
        if not validate_positive_number(investment_amount):
            return jsonify({
                'success': False,
                'error': '投资金额必须为正数'
            }), 400
        
        if risk_tolerance not in ['low', 'medium', 'high']:
            return jsonify({
                'success': False,
                'error': '风险承受能力必须为: low, medium, high'
            }), 400
        
        if investment_period not in ['short', 'medium', 'long']:
            return jsonify({
                'success': False,
                'error': '投资期限必须为: short, medium, long'
            }), 400
        
        analysis_service = current_app.analysis_service
        
        # 批量分析热门ETF
        analysis_results = analysis_service.batch_analyze_popular_etfs(
            investment_amount, risk_tolerance
        )
        
        # 过滤和排序
        suitable_etfs = [r for r in analysis_results if r.get('is_suitable', False)]
        
        # 如果有偏好分类，优先推荐
        if preferred_categories:
            preferred_etfs = [r for r in suitable_etfs if r.get('category') in preferred_categories]
            other_etfs = [r for r in suitable_etfs if r.get('category') not in preferred_categories]
            suitable_etfs = preferred_etfs + other_etfs
        
        # 取前5个推荐
        recommendations = suitable_etfs[:5]
        
        return jsonify({
            'success': True,
            'data': {
                'recommendations': recommendations,
                'total_analyzed': len(analysis_results),
                'suitable_count': len(suitable_etfs),
                'parameters': {
                    'investment_amount': investment_amount,
                    'risk_tolerance': risk_tolerance,
                    'investment_period': investment_period,
                    'preferred_categories': preferred_categories
                }
            }
        })
        
    except Exception as e:
        logger.error(f"获取投资建议失败: {e}")
        return jsonify({
            'success': False,
            'error': '服务器内部错误'
        }), 500
