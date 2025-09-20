# ETF网格交易策略设计工具

一个基于历史数据和专业算法的ETF网格交易策略参数设计工具，帮助投资者科学制定网格交易策略。

## 🎯 功能特点

- **智能分析**：基于tushare数据，分析ETF的历史价格波动特征
- **策略设计**：根据用户设定的交易频率，自动生成最优网格参数
- **适应性评估**：综合评估ETF对网格交易策略的适应性
- **风险控制**：提供详细的风险评估和资金管理建议
- **动态调整**：根据市场环境变化提供策略调整建议
- **可视化展示**：直观展示价格区间、网格分布和预期收益

## 🏗️ 技术架构

### 后端
- **框架**：Python + Flask
- **数据**：tushare金融数据接口
- **分析**：pandas + numpy 数据处理
- **算法**：专业量化分析算法

### 前端
- **框架**：React + Vite
- **UI**：Tailwind CSS 现代化设计
- **图表**：Recharts 数据可视化
- **图标**：Lucide React 图标库

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- tushare API token

### 1. 克隆项目
```bash
git clone <repository-url>
cd etf-grid-trading
```

### 2. 配置环境
创建 `.env` 文件并添加您的tushare token：
```
TUSHARE_TOKEN=your_tushare_token_here
```

### 3. 安装依赖
```bash
# 安装Python依赖
uv add flask flask-cors tushare pandas numpy python-dotenv requests

# 安装前端依赖
cd frontend
npm install
```

### 4. 启动服务
```bash
# 启动后端服务（端口5000）
uv run python backend/app.py

# 启动前端服务（端口3000）
cd frontend
npm run dev
```

### 5. 访问应用
打开浏览器访问：http://localhost:3000

## 📊 核心功能

### 1. ETF分析
- 获取ETF基本信息和最新价格
- 分析近3个月的历史数据
- 计算日振幅、波动率、趋势等关键指标

### 2. 网格策略计算
- **价格区间**：基于历史波动确定合理的网格上下边界
- **网格数量**：根据交易频率自动计算最优网格数
- **资金配置**：科学的仓位管理和资金分配方案
- **收益预估**：预测网格交易的潜在收益和风险

### 3. 适应性评估
- **振幅评估**：判断日均振幅是否适合网格交易
- **波动率评估**：分析价格波动水平对策略的影响
- **流动性评估**：确保有足够的交易量支持网格策略
- **趋势评估**：识别市场是否处于震荡状态

### 4. 动态调整建议
- **波动率上升**：扩大区间、减少网格、降低仓位
- **波动率下降**：缩小区间、增加网格、提高仓位
- **趋势市场**：调整网格中心、加强风险管理

## 📈 使用示例

### 输入参数
- ETF代码：510300（沪深300ETF）
- 交易频率：中频（约4次买卖/天）
- 初始资金：100,000元

### 输出结果
- 推荐价格区间：[4.20, 4.80]元
- 网格数量：12个
- 步长比例：0.50%
- 单笔交易：8,000元
- 月触发预估：80次
- 适应性评分：85/100（适合）

## ⚠️ 风险提示

1. **历史数据限制**：分析基于历史数据，不能保证未来表现
2. **市场风险**：网格交易仍存在亏损风险，需谨慎操作
3. **流动性风险**：确保ETF有足够的流动性支持频繁交易
4. **参数调整**：市场环境变化时需要及时调整策略参数

## 🔧 开发指南

### 后端开发
```bash
# 进入后端目录
cd backend

# 运行测试
python -m pytest

# 代码格式化
black .
```

### 前端开发
```bash
# 进入前端目录
cd frontend

# 运行开发服务器
npm run dev

# 构建生产版本
npm run build
```

## 📋 API接口

### 健康检查
```
GET /api/health
```

### ETF分析
```
POST /api/etf/analyze
Content-Type: application/json

{
  "etf_code": "510300",
  "frequency": "medium",
  "initial_capital": 100000
}
```

### ETF搜索
```
GET /api/etf/search?query=510300
```

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

- 项目维护者：[Your Name]
- 邮箱：your.email@example.com
- 问题反馈：请使用 GitHub Issues

---

**免责声明**：本工具提供的分析结果仅供参考，不构成投资建议。投资有风险，入市需谨慎。
