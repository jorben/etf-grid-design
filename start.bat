@echo off
chcp 65001 >nul

echo 🚀 启动ETF网格交易策略设计工具...
echo ==================================

:: 检查后端是否已在运行
tasklist /FI "WINDOWTITLE eq *backend*app.py*" 2>nul | find /I "python.exe" >nul
if %errorlevel%==0 (
    echo ✅ 后端服务已在运行
) else (
    echo 📦 启动后端服务...
    start "Backend" cmd /k "uv run python backend/app.py"
    timeout /t 3 /nobreak >nul
)

:: 检查前端是否已在运行
tasklist /FI "WINDOWTITLE eq *frontend*" 2>nul | find /I "node.exe" >nul
if %errorlevel%==0 (
    echo ✅ 前端服务已在运行
) else (
    echo 📦 启动前端服务...
    cd frontend
    start "Frontend" cmd /k "npm run dev"
    cd ..
    timeout /t 3 /nobreak >nul
)

echo.
echo 🎉 服务启动完成！
echo ==================
echo 🌐 前端应用: http://localhost:3000
echo 🔧 后端API: http://localhost:5000
echo.
echo 💡 使用提示：
echo   - 在浏览器中打开前端地址开始使用
echo   - 确保已正确配置 .env 文件中的 TUSHARE_TOKEN
echo   - 推荐使用热门ETF代码：510300, 510500, 159915 等
echo.
echo ⚠️  按任意键停止服务
pause >nul

echo 正在停止服务...
taskkill /F /FI "WINDOWTITLE eq Backend*" >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq Frontend*" >nul 2>&1
echo 服务已停止
pause
