# ETF网格策略分析系统

基于ATR技术指标的ETF网格交易策略分析系统，提供ETF适合性分析、网格策略计算和投资建议。

## 功能特性

- **ETF数据管理**: 支持热门ETF查询、基本信息获取、历史数据分析
- **ATR技术分析**: 基于平均真实波幅(ATR)进行技术分析
- **网格策略计算**: 智能计算网格交易参数和资金分配
- **适合性分析**: 根据用户风险偏好进行ETF适合性评估
- **批量分析**: 支持多ETF批量分析和比较
- **缓存优化**: 文件缓存系统，提高数据访问效率

## 技术架构

### 后端架构
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # 应用入口
│   ├── config/
│   │   └── settings.py         # 配置管理
│   ├── models/                 # 数据模型
│   │   ├── etf_models.py
│   │   ├── analysis_models.py
│   │   └── strategy_models.py
│   ├── core/                   # 核心算法
│   │   ├── atr_engine.py
│   │   ├── grid_calculator.py
│   │   └── suitability_analyzer.py
│   ├── services/               # 业务服务
│   │   ├── etf_service.py
│   │   ├── analysis_service.py
│   │   └── file_cache_service.py
│   ├── external/               # 外部接口
│   │   └── tushare_client.py
│   ├── api/                    # API路由
│   │   ├── etf_routes.py
│   │   ├── analysis_routes.py
│   │   └── system_routes.py
│   ├── middleware/             # 中间件
│   │   ├── error_handler.py
│   │   └── cors_handler.py
│   ├── utils/                  # 工具函数
│   │   ├── validators.py
│   │   ├── formatters.py
│   │   ├── calculators.py
│   │   └── file_utils.py
│   └── exceptions/             # 异常处理
│       ├── base_exceptions.py
│       └── business_exceptions.py
└── run.py                      # 启动脚本
```

### 前端架构
```
frontend/
├── src/
│   ├── components/             # React组件
│   ├── services/               # API服务
│   ├── hooks/                  # 自定义Hooks
│   ├── utils/                  # 工具函数
│   └── config/                 # 配置文件
└── dist/                       # 构建输出
```

## 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- Tushare Pro账户

### 后端启动

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 配置环境变量
```bash
# 创建.env文件
TUSHARE_TOKEN=your_tushare_token_here
ENVIRONMENT=development
CACHE_DIR=./cache
```

3. 启动后端服务
```bash
cd backend
python run.py
```

后端服务将在 http://127.0.0.1:5000 启动

### 前端启动

1. 安装依赖
```bash
cd frontend
npm install
```

2. 启动开发服务器
```bash
npm run dev
```

前端服务将在 http://localhost:3000 启动

## API文档

### ETF相关接口

- `GET /api/v1/etfs/popular` - 获取热门ETF列表
- `GET /api/v1/etfs/{etf_code}/basic` - 获取ETF基本信息
- `GET /api/v1/etfs/{etf_code}/latest` - 获取ETF最新数据
- `GET /api/v1/etfs/{etf_code}/historical` - 获取ETF历史数据
- `GET /api/v1/etfs/search` - 搜索ETF

### 分析相关接口

- `POST /api/v1/analysis/suitability/{etf_code}` - ETF适合性分析
- `GET /api/v1/analysis/atr/{etf_code}` - ATR技术分析
- `POST /api/v1/analysis/grid/{etf_code}` - 网格策略生成
- `POST /api/v1/analysis/comprehensive/{etf_code}` - 综合分析
- `POST /api/v1/analysis/batch/popular` - 批量分析热门ETF

### 系统相关接口

- `GET /api/v1/system/health` - 系统健康检查
- `GET /api/v1/system/info` - 系统信息
- `GET /api/v1/system/cache/info` - 缓存信息

## 核心算法

### ATR计算
平均真实波幅(Average True Range)计算，用于衡量价格波动性：
```
TR = max(high - low, abs(high - prev_close), abs(low - prev_close))
ATR = SMA(TR, period)
```

### 网格策略
基于ATR的智能网格策略：
- 网格间距 = ATR百分比 × 调整系数
- 资金分配 = 总资金 / 网格数量
- 风险控制 = 最大回撤限制

### 适合性分析
多维度评估ETF投资适合性：
- 收益率评分 (30%)
- 波动率评分 (30%)
- 最大回撤评分 (25%)
- 流动性评分 (15%)

## 缓存策略

### 三级缓存体系
1. **永久缓存**: ETF基本信息、交易日历
2. **日缓存**: 当日价格数据，按日期目录存储
3. **历史缓存**: 历史数据区间缓存

### 缓存目录结构
```
cache/
├── permanent/          # 永久缓存
├── daily/             # 日缓存
│   └── 20240101/      # 按日期分目录
└── historical/        # 历史缓存
```

## 配置说明

### 环境变量
- `TUSHARE_TOKEN`: Tushare Pro API Token
- `ENVIRONMENT`: 运行环境 (development/production)
- `CACHE_DIR`: 缓存目录路径
- `HOST`: 服务器地址 (默认: 127.0.0.1)
- `PORT`: 服务器端口 (默认: 5000)
- `DEBUG`: 调试模式 (默认: False)

### 热门ETF配置
系统预配置了常见的热门ETF，包括：
- 沪深300ETF (510300.SH)
- 中证500ETF (510500.SH)
- 创业板ETF (159915.SZ)
- 科创50ETF (588000.SH)
- 等等...

## 开发指南

### 代码规范
- 使用Python类型注解
- 遵循PEP 8代码风格
- 完善的异常处理
- 详细的日志记录

### 测试
```bash
# 运行测试
pytest

# 生成覆盖率报告
pytest --cov=app
```

### 部署
1. 生产环境配置
2. 使用Gunicorn部署
3. 配置反向代理
4. 设置日志轮转

## 注意事项

1. **数据源**: 依赖Tushare Pro API，需要有效的Token
2. **缓存管理**: 定期清理过期缓存文件
3. **错误处理**: 完善的异常处理和错误日志
4. **性能优化**: 合理使用缓存，避免频繁API调用

## 许可证

MIT License

## 更新日志

### v1.0.0 (2024-01-01)
- 初始版本发布
- 完整的ETF分析功能
- ATR技术指标计算
- 网格策略生成
- 适合性分析系统