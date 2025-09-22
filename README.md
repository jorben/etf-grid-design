# ETF网格交易策略设计工具

一个基于日线数据和专业算法的ETF网格交易策略参数设计工具，帮助投资者科学制定网格交易策略。

## 🎯 功能特点

- **智能分析**：基于tushare数据，分析ETF的历史价格波动特征
- **策略设计**：根据用户设定的交易频率，自动生成最优网格参数
- **适应性评估**：综合评估ETF对网格交易策略的适应性
- **风险控制**：提供详细的风险评估和资金管理建议
- **动态调整**：根据市场环境变化提供策略调整建议
- **可视化展示**：直观展示价格区间、网格分布和预期收益

## 🌟 页面展示

![index](https://raw.githubusercontent.com/jorben/etf-grid-design/refs/heads/master/screenshot/etfer-inidex.png)

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

### 方式一：Docker部署（推荐）

#### 环境要求

- Docker
- Docker Compose（可选）

#### 一键部署

```bash
# 1. 克隆项目
git clone https://github.com/jorben/etf-grid-design.git
cd etf-grid-design

# 2. 配置环境变量
cp deploy/.env.production .env
# 编辑.env文件，配置TUSHARE_TOKEN

# 3. 一键部署
docker-compose up -d
```

#### 访问应用

- **Web应用**: http://localhost:5001
- **API接口**: http://localhost:5001/api/
- **健康检查**: http://localhost:5001/api/health

### 方式二：本地开发

#### 环境要求

- Python 3.8+
- Node.js 16+
- tushare API token

#### 开发步骤

```bash
# 1. 克隆项目
git clone https://github.com/jorben/etf-grid-design.git
cd etf-grid-design

# 2. 配置环境（必须）
复制环境变量模板并配置真实的tushare token：
cp .env.example .env
# 编辑.env文件，必须配置有效的TUSHARE_TOKEN
# 获取token：https://tushare.pro/register

# 3. 安装依赖
# 安装Python依赖
uv sync

# 安装前端依赖
cd frontend && npm install

# 4. 启动服务
# 启动后端服务（端口5001）
uv run python backend/app.py

# 启动前端服务（端口3000）
cd frontend && npm run dev

# 5. 访问应用
# 开发环境：http://localhost:3000
```

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

## ⚠️ 重要说明

### 数据要求
- **token获取**：请访问 https://tushare.pro/register 注册并获取API token
- **数据质量**：所有分析结果基于tushare提供的真实市场数据

### 风险提示
1. **历史数据限制**：分析基于历史数据，不能保证未来表现
2. **市场风险**：网格交易仍存在亏损风险，需谨慎操作
3. **流动性风险**：确保ETF有足够的流动性支持频繁交易
4. **参数调整**：市场环境变化时需要及时调整策略参数

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 Apache-2.0 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

- 问题反馈：请使用 GitHub Issues

---

**免责声明**：本工具提供的分析结果仅供参考，不构成投资建议。投资有风险，入市需谨慎。
