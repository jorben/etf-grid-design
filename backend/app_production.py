import os
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import logging
from datetime import datetime
from werkzeug.middleware.proxy_fix import ProxyFix

# 导入服务模块
from services.etf_analyzer import ETFAnalyzer
from services.grid_calculator import GridCalculator
from services.tushare_client import TushareClient

# 加载环境变量
load_dotenv()

# 配置日志 - 生产环境
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/app/logs/app.log') if os.path.exists('/app/logs') else logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 创建Flask应用 - 配置静态文件服务
app = Flask(__name__, 
           static_folder='../static',
           static_url_path='')

# 生产环境配置
app.config['ENV'] = 'production'
app.config['DEBUG'] = False
app.config['TESTING'] = False

# 配置CORS - 生产环境更严格
CORS(app, origins=['*'])  # 生产环境中应该配置具体的域名

# 配置代理支持（如果在反向代理后面）
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# 初始化服务
try:
    tushare_client = TushareClient()
    etf_analyzer = ETFAnalyzer(tushare_client)
    grid_calculator = GridCalculator()
    logger.info("服务初始化成功")
except Exception as e:
    logger.error(f"服务初始化失败: {str(e)}")
    raise


# ==================== API 路由 ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '0.1.0',
        'environment': 'production'
    })


@app.route('/api/etf/analyze', methods=['POST'])
def analyze_etf():
    """分析ETF并生成网格策略参数"""
    try:
        data = request.get_json()
        
        # 验证输入参数
        if not data:
            return jsonify({'error': '请求数据不能为空'}), 400
        
        etf_code = data.get('etf_code')
        frequency = data.get('frequency')  # high, medium, low
        initial_capital = data.get('initial_capital')
        
        if not all([etf_code, frequency, initial_capital]):
            return jsonify({'error': '缺少必要参数：etf_code, frequency, initial_capital'}), 400
        
        # 验证频率参数
        if frequency not in ['high', 'medium', 'low']:
            return jsonify({'error': 'frequency参数必须是：high, medium, low'}), 400
        
        # 验证资金量
        try:
            initial_capital = float(initial_capital)
            if initial_capital <= 0:
                return jsonify({'error': '初始资金必须大于0'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': '初始资金格式错误'}), 400
        
        logger.info(f"开始分析ETF: {etf_code}, 频率: {frequency}, 资金: {initial_capital}")
        
        # 获取ETF基础数据
        etf_info = etf_analyzer.get_etf_info(etf_code)
        if not etf_info:
            return jsonify({'error': f'无法获取ETF {etf_code} 的信息'}), 404
        
        # 获取历史数据
        historical_data = etf_analyzer.get_historical_data(etf_code, days=90)
        if historical_data is None or historical_data.empty or len(historical_data) < 30:
            return jsonify({'error': '历史数据不足，无法进行分析'}), 400
        
        # 分析ETF特征
        analysis_result = etf_analyzer.analyze_etf_characteristics(historical_data)
        
        # 计算网格策略参数 - 传递历史数据用于频次分析
        grid_params = grid_calculator.calculate_grid_parameters(
            current_price=etf_info['current_price'],
            analysis_result=analysis_result,
            frequency=frequency,
            initial_capital=initial_capital,
            historical_data=historical_data  # 新增：传递历史数据
        )
        
        # 评估适应性 - 传递用户频率参数
        adaptability = etf_analyzer.evaluate_adaptability(analysis_result, grid_params, frequency)
        
        # 生成动态调整建议
        adjustment_suggestions = grid_calculator.generate_adjustment_suggestions(
            analysis_result, grid_params
        )
        
        # 准备历史价格数据（最近30个交易日）
        historical_prices = []
        if historical_data is not None and not historical_data.empty:
            # 取最近30个交易日的数据
            recent_data = historical_data.tail(30).copy()
            for _, row in recent_data.iterrows():
                historical_prices.append({
                    'date': row['trade_date'].strftime('%Y-%m-%d'),
                    'price': float(row['close']),
                    'volume': float(row['vol']) if 'vol' in row else 0
                })

        # 组合结果
        result = {
            'etf_info': etf_info,
            'analysis': analysis_result,
            'grid_parameters': grid_params,
            'adaptability': adaptability,
            'adjustment_suggestions': adjustment_suggestions,
            'historical_prices': historical_prices,  # 新增：历史价格数据
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"ETF {etf_code} 分析完成")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"分析ETF时发生错误: {str(e)}", exc_info=True)
        return jsonify({'error': f'分析过程中发生错误: {str(e)}'}), 500


@app.route('/api/etf/search', methods=['GET'])
def search_etf():
    """搜索ETF列表"""
    try:
        query = request.args.get('query', '')
        if not query:
            return jsonify({'error': '搜索关键词不能为空'}), 400
        
        # 获取ETF列表
        etf_list = tushare_client.search_etf(query)
        
        return jsonify({
            'etf_list': etf_list,
            'count': len(etf_list)
        })
        
    except Exception as e:
        logger.error(f"搜索ETF时发生错误: {str(e)}", exc_info=True)
        return jsonify({'error': f'搜索过程中发生错误: {str(e)}'}), 500


@app.route('/api/etf/name/<etf_code>', methods=['GET'])
def get_etf_name(etf_code):
    """获取ETF名称"""
    try:
        # 验证ETF代码格式
        if not etf_code or not etf_code.isdigit() or len(etf_code) != 6:
            return jsonify({'error': 'ETF代码格式错误，应为6位数字'}), 400
        
        # 获取ETF名称
        etf_name = tushare_client.get_etf_name(etf_code)
        
        if etf_name:
            return jsonify({
                'code': etf_code,
                'name': etf_name,
                'success': True
            })
        else:
            return jsonify({
                'code': etf_code,
                'name': etf_code,  # 如果获取失败，返回代码本身
                'success': False,
                'message': '未找到该ETF的名称信息'
            })
        
    except Exception as e:
        logger.error(f"获取ETF {etf_code} 名称时发生错误: {str(e)}", exc_info=True)
        return jsonify({
            'code': etf_code,
            'name': etf_code,  # 出错时返回代码本身
            'success': False,
            'error': f'获取名称时发生错误: {str(e)}'
        }), 500


@app.route('/api/cache/info', methods=['GET'])
def get_cache_info():
    """获取缓存信息"""
    try:
        cache_info = tushare_client.cache.get_cache_info()
        return jsonify({
            'success': True,
            'cache_info': cache_info,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"获取缓存信息时发生错误: {str(e)}", exc_info=True)
        return jsonify({'error': f'获取缓存信息失败: {str(e)}'}), 500


@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    """清理缓存"""
    try:
        data = request.get_json() or {}
        method_name = data.get('method_name')
        
        if method_name:
            # 清理特定方法的缓存
            params = {k: v for k, v in data.items() if k != 'method_name'}
            tushare_client.cache.clear(method_name, **params)
            message = f"已清理 {method_name} 的缓存"
        else:
            # 清理所有缓存
            tushare_client.cache.clear()
            message = "已清理所有缓存"
        
        return jsonify({
            'success': True,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"清理缓存时发生错误: {str(e)}", exc_info=True)
        return jsonify({'error': f'清理缓存失败: {str(e)}'}), 500


# ==================== 静态文件服务 ====================

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """服务静态资源文件"""
    try:
        return send_from_directory(os.path.join(app.static_folder, 'assets'), filename)
    except Exception as e:
        logger.error(f"服务静态文件失败: {filename}, 错误: {str(e)}")
        return jsonify({'error': 'File not found'}), 404


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_spa(path):
    """
    服务SPA应用
    所有非API路由都返回index.html，让前端路由处理
    """
    # 如果是API路由，返回404
    if path.startswith('api/'):
        return jsonify({'error': '接口不存在'}), 404
    
    # 如果请求的是具体文件且存在，直接返回
    if path and '.' in path:
        try:
            return send_from_directory(app.static_folder, path)
        except:
            pass
    
    # 其他所有路由都返回index.html，让React Router处理
    try:
        return send_file(os.path.join(app.static_folder, 'index.html'))
    except Exception as e:
        logger.error(f"无法找到index.html: {str(e)}")
        return jsonify({'error': '应用未正确部署'}), 500


# ==================== 错误处理 ====================

@app.errorhandler(404)
def not_found(error):
    # 如果是API请求，返回JSON错误
    if request.path.startswith('/api/'):
        return jsonify({'error': '接口不存在'}), 404
    # 否则返回SPA应用
    return serve_spa('')


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"服务器内部错误: {str(error)}")
    return jsonify({'error': '服务器内部错误'}), 500


# ==================== 应用启动 ====================

if __name__ == '__main__':
    # 检查环境变量
    if not os.getenv('TUSHARE_TOKEN'):
        logger.warning("未找到TUSHARE_TOKEN环境变量，请在.env文件中配置")
    
    # 创建日志目录
    os.makedirs('/app/logs', exist_ok=True)
    
    # 获取配置
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5001))
    
    logger.info(f"启动ETF网格交易工具生产环境服务器 - {host}:{port}")
    
    # 启动应用
    app.run(
        host=host,
        port=port,
        debug=False,
        threaded=True
    )