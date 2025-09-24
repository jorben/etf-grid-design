# Stage 2: API层重构与路由分离

## 背景
在Stage 1完成项目结构调整后，当前的Flask应用仍然将所有路由定义集中在`app.py`文件中，导致该文件过于庞大且职责不清。为了提升代码的模块化程度和可维护性，需要将API层从主应用文件中分离出来。

## 当前阶段
**阶段2：API层重构**

这是整个重构计划的第二阶段，基于Stage 1已经建立的目录结构，主要目标是重构API层，实现路由的模块化管理。

## 具体目标

### 主要目标
1. 将Flask路由从`app.py`中抽离到独立的路由模块
2. 创建统一的请求/响应数据模型
3. 实现统一的错误处理和中间件机制
4. 简化`app.py`，使其专注于应用初始化

### 详细目标
- 创建模块化的路由结构（ETF、分析、健康检查）
- 实现请求参数验证和响应格式标准化
- 添加统一的错误处理中间件
- 添加请求日志和性能监控中间件
- 保持所有现有API接口的完全兼容性

## 实现方法

### 步骤1：创建路由模块结构
```
backend/api/
├── __init__.py
├── routes/
│   ├── __init__.py
│   ├── etf_routes.py        # ETF相关路由
│   ├── analysis_routes.py   # 分析相关路由
│   └── health_routes.py     # 健康检查路由
├── schemas.py               # 请求/响应数据模型
└── middleware.py            # 中间件
```

### 步骤2：路由分离计划

#### etf_routes.py 包含：
- `GET /api/popular-etfs` - 获取热门ETF列表
- `GET /api/etf/basic-info/<etf_code>` - 获取ETF基础信息
- `GET /api/capital-presets` - 获取预设资金选项

#### analysis_routes.py 包含：
- `POST /api/analyze` - ETF网格交易策略分析

#### health_routes.py 包含：
- `GET /api/health` - 健康检查
- `GET /api/version` - 版本信息

### 步骤3：数据模型定义
在`schemas.py`中定义：
- 请求参数验证模型
- 响应数据格式模型
- 错误响应模型

### 步骤4：中间件实现
在`middleware.py`中实现：
- 统一错误处理
- 请求日志记录
- 响应时间监控
- CORS处理

### 步骤5：重构app.py
简化`app.py`，使其专注于：
- 应用初始化
- 配置加载
- 路由注册
- 中间件注册

## 约束条件

### 技术约束
1. **API兼容性**：所有现有API接口的URL、参数、响应格式必须保持完全不变
2. **功能完整性**：不能丢失任何现有功能
3. **性能要求**：重构后的性能不能低于现有水平
4. **依赖稳定**：不能引入新的外部依赖

### 操作约束
1. **渐进式重构**：一次重构一个路由模块，确保每步都可以验证
2. **向后兼容**：在重构过程中保持系统可用性
3. **测试覆盖**：每个重构的路由都要经过完整测试
4. **回滚能力**：任何时候都能快速回滚到上一个稳定状态

### 质量约束
1. **代码规范**：遵循Python和Flask的最佳实践
2. **错误处理**：统一且完善的错误处理机制
3. **日志质量**：保持现有日志功能并适当增强
4. **文档完整**：为新的API结构提供清晰的文档

## 实现细节

### 路由模块示例结构
```python
# api/routes/etf_routes.py
from flask import Blueprint, request, jsonify
from services.analysis.etf_analysis_service import ETFAnalysisService

etf_bp = Blueprint('etf', __name__)
etf_service = ETFAnalysisService()

@etf_bp.route('/api/popular-etfs', methods=['GET'])
def get_popular_etfs():
    # 实现逻辑
    pass

@etf_bp.route('/api/etf/basic-info/<etf_code>', methods=['GET'])
def get_etf_basic_info(etf_code):
    # 实现逻辑
    pass
```

### 中间件示例结构
```python
# api/middleware.py
from flask import request, jsonify
import logging
import time

def register_middleware(app):
    @app.before_request
    def log_request():
        # 请求日志
        pass
    
    @app.after_request
    def log_response(response):
        # 响应日志
        return response
    
    @app.errorhandler(Exception)
    def handle_error(error):
        # 统一错误处理
        pass
```

### 重构后的app.py结构
```python
# app.py
from flask import Flask
from flask_cors import CORS
from api.routes import register_routes
from api.middleware import register_middleware
from config.settings import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    register_middleware(app)
    register_routes(app)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
```

## 验证标准

### 功能验证
1. 所有现有API接口正常工作
2. 请求参数验证正确
3. 响应格式符合预期
4. 错误处理机制正常
5. 日志记录完整

### 结构验证
1. 路由模块正确分离
2. 中间件正常工作
3. app.py结构简化
4. 代码组织清晰

### 性能验证
1. API响应时间不增加
2. 内存使用稳定
3. 并发处理能力保持

## 风险评估

### 低风险
- 路由模块创建
- 中间件添加
- 日志增强

### 中风险
- 路由逻辑迁移
- 错误处理重构
- app.py简化

### 高风险
- 请求/响应格式变更
- 参数验证逻辑修改

### 缓解措施
1. 详细的单元测试和集成测试
2. 分阶段部署和验证
3. 完整的回滚计划
4. 生产环境监控

## 成功标准
1. ✅ 路由模块成功分离
2. ✅ 统一的错误处理机制
3. ✅ 请求/响应数据模型标准化
4. ✅ app.py结构简化
5. ✅ 所有API功能正常
6. ✅ 代码结构更加模块化

## 测试计划
1. **单元测试**：每个路由模块的独立测试
2. **集成测试**：API接口的端到端测试
3. **性能测试**：确保重构后性能不下降
4. **兼容性测试**：验证前端调用的兼容性

## 下一阶段预告
完成本阶段后，将进入**Stage 3: 服务层优化**，主要目标是优化服务层的内部结构，抽离算法模块，提升代码的复用性和可测试性。
