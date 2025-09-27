"""
分析相关路由模块
包含ETF网格交易策略分析接口
"""

from flask import Blueprint, request, jsonify
import traceback
from services.analysis.etf_analysis_service import ETFAnalysisService

# 创建分析蓝图
analysis_bp = Blueprint('analysis', __name__)
etf_service = ETFAnalysisService()

@analysis_bp.route('/api/analyze', methods=['POST'])
def analyze_etf_strategy():
    """ETF网格交易策略分析"""
    try:
        # 获取请求参数
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': '请求参数不能为空'
            }), 400
        
        # 验证必需参数
        required_fields = ['etfCode', 'totalCapital', 'gridType', 'riskPreference']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'缺少必需参数: {field}'
                }), 400
        
        # 参数验证
        etf_code = data['etfCode'].strip()
        if not etf_code or len(etf_code) != 6 or not etf_code.isdigit():
            return jsonify({
                'success': False,
                'error': 'ETF代码格式错误，请输入6位数字'
            }), 400
        
        total_capital = float(data['totalCapital'])
        if total_capital < 10000 or total_capital > 1000000:
            return jsonify({
                'success': False,
                'error': '投资金额应在1万-100万之间'
            }), 400
        
        grid_type = data['gridType']
        if grid_type not in ['等差', '等比']:
            return jsonify({
                'success': False,
                'error': '网格类型只能是"等差"或"等比"'
            }), 400
        
        risk_preference = data['riskPreference']
        if risk_preference not in ['低频', '均衡', '高频']:
            return jsonify({
                'success': False,
                'error': '频率偏好只能是"低频"、"均衡"或"高频"'
            }), 400
        
        # 获取调节系数（可选参数，默认1.0）
        adjustment_coefficient = float(data.get('adjustmentCoefficient', 1.0))
        if adjustment_coefficient < 0.0 or adjustment_coefficient > 2.0:
            return jsonify({
                'success': False,
                'error': '调节系数应在0.0-2.0之间'
            }), 400
        
        from flask import current_app
        current_app.logger.info(f"开始分析ETF策略: {etf_code}, 资金{total_capital}, "
                   f"{grid_type}网格, {risk_preference}")
        
        # 执行分析
        analysis_result = etf_service.analyze_etf_strategy(
            etf_code=etf_code,
            total_capital=total_capital,
            grid_type=grid_type,
            risk_preference=risk_preference,
            adjustment_coefficient=adjustment_coefficient
        )
        
        current_app.logger.info(f"ETF策略分析完成: {etf_code}, "
                   f"适宜度评分{analysis_result['suitability_evaluation']['total_score']}")
        
        return jsonify({
            'success': True,
            'data': analysis_result
        })
        
    except ValueError as e:
        from flask import current_app
        current_app.logger.error(f"参数验证失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        from flask import current_app
        current_app.logger.error(f"ETF策略分析失败: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': '分析失败，请稍后重试或检查ETF代码是否正确'
        }), 500
