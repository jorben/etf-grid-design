#!/bin/bash

# ETF网格交易策略设计工具启动脚本

echo "🚀 启动ETF网格交易策略设计工具..."
echo "=================================="

# 检查后端是否已在运行
if pgrep -f "python.*backend/app.py" > /dev/null; then
    echo "✅ 后端服务已在运行"
else
    echo "📦 启动后端服务..."
    uv run python backend/app.py &
    sleep 3
fi

# 检查前端是否已在运行
if pgrep -f "npm.*dev" > /dev/null; then
    echo "✅ 前端服务已在运行"
else
    echo "📦 启动前端服务..."
    cd frontend && npm run dev &
    sleep 3
fi

echo ""
echo "🎉 服务启动完成！"
echo "=================="
echo "🌐 前端应用: http://localhost:3000"
echo "🔧 后端API: http://localhost:5000"
echo ""
echo "💡 使用提示："
echo "  - 在浏览器中打开前端地址开始使用"
echo "  - 确保已正确配置 .env 文件中的 TUSHARE_TOKEN"
echo "  - 推荐使用热门ETF代码：510300, 510500, 159915 等"
echo ""
echo "⚠️  按 Ctrl+C 停止服务"
echo ""

# 等待用户输入来停止服务
trap 'echo "正在停止服务..."; pkill -f "python.*backend/app.py"; pkill -f "npm.*dev"; exit 0' INT
wait
