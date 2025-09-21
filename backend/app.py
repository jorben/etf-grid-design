import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import logging
from datetime import datetime

# 导入服务模块
from services.etf_analyzer import ETFAnalyzer
from services.grid_calculator import GridCalculator
from services.tushare_client import TushareClient

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 初始化服务
tushare_client = TushareClient()
etf_analyzer = ETFAnalyzer(tushare_client)
grid_calculator = GridCalculator()


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '0.1.0'
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


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '接口不存在'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': '服务器内部错误'}), 500


if __name__ == '__main__':
    # 检查环境变量
    if not os.getenv('TUSHARE_TOKEN'):
        logger.warning("未找到TUSHARE_TOKEN环境变量，请在.env文件中配置")
    
    # 启动应用
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )
