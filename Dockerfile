# 多阶段构建 - ETF网格交易策略设计工具
# 阶段1: 前端构建
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# 复制前端依赖文件
COPY frontend/package*.json ./

# 安装所有依赖
RUN npm ci

# 复制前端源码
COPY frontend/ ./

# 构建前端应用
RUN npm run build

# 阶段2: 后端运行环境
FROM python:3.11-slim

ENV FLASK_ENV=production
ENV TUSHARE_TOKEN=

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制Python依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端代码
COPY backend/ ./backend/

# 复制前端构建结果到Flask静态目录
COPY --from=frontend-builder /app/frontend/dist ./static

# 创建非root用户
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app

# 暴露端口
EXPOSE 5001

# 复制Gunicorn配置和启动脚本
COPY deploy/gunicorn.conf.py ./
COPY deploy/entrypoint.sh ./
RUN chmod +x entrypoint.sh

# 创建日志目录
RUN mkdir -p /app/logs && chown -R app:app /app/logs

# 切换到非root用户
USER app

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5001/api/health || exit 1

# 启动命令
CMD ["./entrypoint.sh"]