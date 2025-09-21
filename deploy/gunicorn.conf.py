# ETF网格交易工具 - Gunicorn生产环境配置

import os
import multiprocessing

# 服务器配置
bind = f"0.0.0.0:{os.getenv('PORT', 5001)}"
backlog = 2048

# 工作进程配置
workers = int(os.getenv('WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = "gevent"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = int(os.getenv('TIMEOUT', 30))
keepalive = 2

# 性能优化
preload_app = True
reuse_port = True

# 日志配置
accesslog = "/app/logs/access.log"
errorlog = "/app/logs/error.log"
loglevel = os.getenv('LOG_LEVEL', 'info').lower()
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# 进程管理
pidfile = "/tmp/gunicorn.pid"
user = "app"
group = "app"
tmp_upload_dir = None

# 安全配置
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# 启动钩子
def on_starting(server):
    server.log.info("ETF网格交易工具启动中...")

def on_reload(server):
    server.log.info("ETF网格交易工具重新加载...")

def when_ready(server):
    server.log.info("ETF网格交易工具已就绪，开始接受请求")

def on_exit(server):
    server.log.info("ETF网格交易工具正在关闭...")

def worker_int(worker):
    worker.log.info("工作进程收到中断信号")

def pre_fork(server, worker):
    server.log.info(f"工作进程 {worker.pid} 即将启动")

def post_fork(server, worker):
    server.log.info(f"工作进程 {worker.pid} 已启动")

def post_worker_init(worker):
    worker.log.info(f"工作进程 {worker.pid} 初始化完成")

def worker_abort(worker):
    worker.log.info(f"工作进程 {worker.pid} 异常终止")