"""
ETF网格交易策略分析系统 - Flask应用
基于ATR算法的智能网格交易策略设计及分析系统
"""

import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import traceback
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

from services.etf_analysis_service import ETFAnalysisService

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__)
CORS(app)

# 初始化服务
etf_service = ETFAnalysisService()

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'ETF Grid Trading Analysis System'
    })

@app.route('/api/popular-etfs', methods=['GET'])
def get_popular_etfs():
    """获取热门ETF列表"""
    try:
        popular_etfs = etf_service.get_popular_etfs()
        return jsonify({
            'success': True,
            'data': popular_etfs
        })
    except Exception as e:
        logger.error(f"获取热门ETF列表失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': '获取热门ETF列表失败'
        }), 500

@app.route('/api/etf/basic-info/<etf_code>', methods=['GET'])
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
        logger.error(f"获取ETF基础信息失败: {etf_code}, {str(e)}")
        return jsonify({
            'success': False,
            'error': '获取ETF信息失败，请检查代码是否正确'
        }), 500

@app.route('/api/analyze', methods=['POST'])
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
        required_fields = ['etfCode', 'totalCapital', 'gridType', 'frequencyPreference', 'riskPreference']
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
        if total_capital < 100000 or total_capital > 5000000:
            return jsonify({
                'success': False,
                'error': '投资金额应在10万-500万之间'
            }), 400
        
        grid_type = data['gridType']
        if grid_type not in ['等差', '等比']:
            return jsonify({
                'success': False,
                'error': '网格类型只能是"等差"或"等比"'
            }), 400
        
        frequency_preference = data['frequencyPreference']
        if frequency_preference not in ['低频', '中频', '高频']:
            return jsonify({
                'success': False,
                'error': '交易频率只能是"低频"、"中频"或"高频"'
            }), 400
        
        risk_preference = data['riskPreference']
        if risk_preference not in ['保守', '稳健', '激进']:
            return jsonify({
                'success': False,
                'error': '风险偏好只能是"保守"、"稳健"或"激进"'
            }), 400
        
        logger.info(f"开始分析ETF策略: {etf_code}, 资金{total_capital}, "
                   f"{grid_type}网格, {frequency_preference}, {risk_preference}")
        
        # 执行分析
        analysis_result = etf_service.analyze_etf_strategy(
            etf_code=etf_code,
            total_capital=total_capital,
            grid_type=grid_type,
            frequency_preference=frequency_preference,
            risk_preference=risk_preference
        )
        

        
        logger.info(f"ETF策略分析完成: {etf_code}, "
                   f"适宜度评分{analysis_result['suitability_evaluation']['total_score']}")
        
        return jsonify({
            'success': True,
            'data': analysis_result
        })
        
    except ValueError as e:
        logger.error(f"参数验证失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        logger.error(f"ETF策略分析失败: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': '分析失败，请稍后重试或检查ETF代码是否正确'
        }), 500

@app.route('/api/preset-configs', methods=['GET'])
def get_preset_configs():
    """获取预设配置方案"""
    try:
        preset_configs = [
            {
                'id': 'conservative',
                'name': '新手友好型',
                'description': '适合投资新手，风险较低',
                'config': {
                    'gridType': '等差',
                    'frequencyPreference': '低频',
                    'riskPreference': '保守'
                },
                'features': ['风险较低', '操作简单', '适合新手']
            },
            {
                'id': 'balanced',
                'name': '稳健增长型',
                'description': '平衡风险与收益，适合大多数投资者',
                'config': {
                    'gridType': '等比',
                    'frequencyPreference': '中频',
                    'riskPreference': '稳健'
                },
                'features': ['风险适中', '收益稳定', '推荐选择']
            },
            {
                'id': 'aggressive',
                'name': '积极进取型',
                'description': '追求高收益，适合有经验的投资者',
                'config': {
                    'gridType': '等比',
                    'frequencyPreference': '高频',
                    'riskPreference': '激进'
                },
                'features': ['收益潜力大', '交易频繁', '需要经验']
            }
        ]
        
        return jsonify({
            'success': True,
            'data': preset_configs
        })
        
    except Exception as e:
        logger.error(f"获取预设配置失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': '获取预设配置失败'
        }), 500

@app.route('/api/capital-presets', methods=['GET'])
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
        logger.error(f"获取预设资金选项失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': '获取预设资金选项失败'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({
        'success': False,
        'error': '接口不存在'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    logger.error(f"内部服务器错误: {str(error)}")
    return jsonify({
        'success': False,
        'error': '内部服务器错误'
    }), 500

if __name__ == '__main__':
    # 开发环境配置
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"启动ETF网格交易策略分析系统，端口: {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)