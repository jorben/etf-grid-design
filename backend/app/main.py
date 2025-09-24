"""
主应用入口文件

整合所有组件，创建Flask应用实例
"""

import logging
import os
from flask import Flask

from .config.settings import Settings
from .external.tushare_client import TushareClient
from .services.file_cache_service import FileCacheService
from .services.etf_service import ETFService
from .services.analysis_service import AnalysisService
from .api import api_bp
from .middleware import register_error_handlers, setup_cors

# 配置日志
import os
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'log')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'app.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_file, encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)


def create_app(config_name='default'):
    """
    应用工厂函数
    
    Args:
        config_name: 配置名称
        
    Returns:
        Flask: Flask应用实例
    """
    app = Flask(__name__)
    
    try:
        # 初始化配置
        settings = Settings()
        app.settings = settings
        app.config['ENV'] = settings.ENVIRONMENT
        
        logger.info(f"应用启动，环境: {settings.ENVIRONMENT}")
        
        # 初始化外部服务
        tushare_client = TushareClient(settings)
        app.tushare_client = tushare_client
        
        # 初始化缓存服务
        cache_service = FileCacheService(settings)
        app.cache_service = cache_service
        
        # 初始化业务服务
        etf_service = ETFService(settings, tushare_client, cache_service)
        app.etf_service = etf_service
        
        analysis_service = AnalysisService(settings, etf_service)
        app.analysis_service = analysis_service
        
        # 注册蓝图
        app.register_blueprint(api_bp)
        
        # 设置中间件
        register_error_handlers(app)
        setup_cors(app)
        
        # 添加根路由
        @app.route('/')
        def index():
            return {
                'message': 'ETF Grid Design Backend API',
                'version': '1.0.0',
                'status': 'running',
                'api_docs': '/api/v1/system/info'
            }
        
        @app.route('/health')
        def health():
            return {'status': 'healthy'}
        
        logger.info("应用初始化完成")
        return app
        
    except Exception as e:
        logger.error(f"应用初始化失败: {e}")
        raise


def run_app():
    """运行应用"""
    app = create_app()
    
    # 获取运行配置
    host = app.settings.HOST
    port = app.settings.PORT
    debug = app.settings.DEBUG
    
    logger.info(f"启动服务器: http://{host}:{port}")
    
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )


if __name__ == '__main__':
    run_app()