# ETF网格策略分析系统 API协议文档

## 系统概述

- **系统名称**: ETF网格策略分析系统后端API
- **版本**: v1.0.0
- **基础URL**: `http://localhost:5002/api/v1`
- **数据格式**: JSON
- **字符编码**: UTF-8
- **数据源**: Tushare Pro API

## 通用响应格式

### 成功响应
```json
{
  "success": true,
  "data": {}, // 具体数据内容
  "count": 10, // 可选，数据条数
  "message": "操作成功" // 可选，提示信息
}
```

### 失败响应
```json
{
  "success": false,
  "error": "错误描述",
  "error_code": "ERROR_CODE",
  "timestamp": "2024-01-01T12:00:00"
}
```

## 错误码列表

| 错误码 | HTTP状态码 | 含义 | 说明 |
|--------|------------|------|------|
| ETF_NOT_FOUND | 404 | ETF不存在 | ETF代码错误或不存在 |
| INVALID_PARAMETER | 400 | 参数错误 | 请求参数格式或值错误 |
| DATA_SOURCE_ERROR | 502 | 数据源异常 | Tushare API访问失败 |
| ANALYSIS_ERROR | 500 | 分析计算异常 | 分析过程中发生错误 |
| CACHE_ERROR | 500 | 缓存异常 | 缓存操作失败 |
| STRATEGY_ERROR | 500 | 策略计算异常 | 网格策略计算失败 |
| INSUFFICIENT_DATA | 400 | 数据不足 | 历史数据不足以进行分析 |
| MARKET_CLOSED | 400 | 市场休市 | 无法获取实时数据 |
| CALCULATION_ERROR | 500 | 计算异常 | 数值计算过程错误 |
| DATA_QUALITY_ERROR | 400 | 数据质量异常 | 数据质量不符合要求 |
| EXTERNAL_API_ERROR | 502 | 外部API异常 | 外部服务调用失败 |
| CONFIGURATION_ERROR | 500 | 配置异常 | 系统配置错误 |
| DATA_VALIDATION_ERROR | 400 | 数据验证异常 | 数据验证失败 |

---

# 一、ETF相关接口 (etf_routes.py)

## 1.1 获取热门ETF列表

| 项目 | 内容 |
|------|------|
| **API路径** | `GET /api/v1/etfs/popular` |
| **功能描述** | 获取系统预设的热门ETF列表，包含基本信息 |
| **入参协议** | 无参数 |
| **出参协议** | 见下方JSON结构 |

### 响应数据结构 (包含Tushare数据)
```json
{
  "success": true,
  "data": [
    {
      "code": "510300",
      "name": "沪深300ETF",
      "category": "宽基指数",
      "is_popular": true,
      "current_price": 4.123,  // Tushare数据：最新价格
      "pct_change": 1.25       // Tushare数据：涨跌幅(%)
    }
  ],
  "count": 18
}
```

**字段说明**:
- `code`: ETF代码(6位数字)
- `name`: ETF名称
- `category`: ETF分类(宽基指数/行业主题/海外指数/策略指数)
- `current_price`: 最新价格(来源Tushare)
- `pct_change`: 涨跌幅百分比(来源Tushare)

## 1.2 获取ETF基本信息

| 项目 | 内容 |
|------|------|
| **API路径** | `GET /api/v1/etfs/{etf_code}/basic` |
| **功能描述** | 获取指定ETF的详细基本信息 |
| **入参协议** | 路径参数: `etf_code` (6位ETF代码) |
| **出参协议** | 见下方JSON结构 |

### 响应数据结构 (包含Tushare数据)
```json
{
  "success": true,
  "data": {
    "code": "510300",
    "name": "沪深300ETF",                    // Tushare数据
    "market": "SH",                         // Tushare数据：交易市场
    "list_date": "20121228",                // Tushare数据：上市日期
    "fund_type": "ETF",                     // Tushare数据：基金类型
    "management_fee": 0.5,                  // Tushare数据：管理费率(%)
    "custodian_fee": 0.1,                   // Tushare数据：托管费率(%)
    "benchmark": "沪深300指数",              // Tushare数据：跟踪基准
    "management": "华泰柏瑞基金管理有限公司", // Tushare数据：管理人
    "found_date": "20121211",               // Tushare数据：成立日期
    "issue_amount": 20000000000,            // Tushare数据：发行规模
    "current_price": 4.123,                 // Tushare数据：当前价格
    "pct_change": 1.25,                     // Tushare数据：涨跌幅
    "volume": 12345678,                     // Tushare数据：成交量
    "amount": 51234567.89,                  // Tushare数据：成交额
    "trade_date": "20240924"                // Tushare数据：交易日期
  }
}
```

## 1.3 获取ETF最新价格数据

| 项目 | 内容 |
|------|------|
| **API路径** | `GET /api/v1/etfs/{etf_code}/latest` |
| **功能描述** | 获取ETF最新交易日的价格数据 |
| **入参协议** | 路径参数: `etf_code` (6位ETF代码) |
| **出参协议** | 见下方JSON结构 |

### 响应数据结构 (Tushare数据)
```json
{
  "success": true,
  "data": {
    "trade_date": "20240924",    // Tushare数据：交易日期
    "open_price": 4.100,         // Tushare数据：开盘价
    "high_price": 4.150,         // Tushare数据：最高价
    "low_price": 4.080,          // Tushare数据：最低价
    "close_price": 4.123,        // Tushare数据：收盘价
    "volume": 12345678,          // Tushare数据：成交量(手)
    "amount": 51234567.89,       // Tushare数据：成交额(元)
    "pct_change": 1.25           // Tushare数据：涨跌幅(%)
  }
}
```

## 1.4 获取ETF历史数据

| 项目 | 内容 |
|------|------|
| **API路径** | `GET /api/v1/etfs/{etf_code}/historical` |
| **功能描述** | 获取ETF指定时间范围的历史价格数据 |
| **入参协议** | 路径参数: `etf_code`<br>查询参数: `start_date`, `end_date` (YYYYMMDD格式) |
| **出参协议** | 见下方JSON结构 |

### 请求示例
```
GET /api/v1/etfs/510300/historical?start_date=20240901&end_date=20240924
```

### 响应数据结构 (Tushare数据)
```json
{
  "success": true,
  "data": [
    {
      "trade_date": "20240924",    // Tushare数据：交易日期
      "open_price": 4.100,         // Tushare数据：开盘价
      "high_price": 4.150,         // Tushare数据：最高价
      "low_price": 4.080,          // Tushare数据：最低价
      "close_price": 4.123,        // Tushare数据：收盘价
      "volume": 12345678,          // Tushare数据：成交量
      "amount": 51234567.89,       // Tushare数据：成交额
      "pct_change": 1.25           // Tushare数据：涨跌幅
    }
  ],
  "count": 20,
  "period": {
    "start_date": "20240901",
    "end_date": "20240924"
  }
}
```

## 1.5 获取ETF综合信息摘要

| 项目 | 内容 |
|------|------|
| **API路径** | `GET /api/v1/etfs/{etf_code}/summary` |
| **功能描述** | 获取ETF的综合信息摘要，包含基本信息和最新价格 |
| **入参协议** | 路径参数: `etf_code` (6位ETF代码) |
| **出参协议** | 见下方JSON结构 |

### 响应数据结构
```json
{
  "success": true,
  "data": {
    "daily_cache_count": 150,
    "historical_cache_count": 25,
    "permanent_cache_count": 18,
    "cache_size_mb": 125.6,
    "last_cleanup": "2024-09-24T10:00:00",
    "cache_hit_rate": 0.85
  }
}
```

## 3.5 清理缓存

| 项目 | 内容 |
|------|------|
| **API路径** | `POST /api/v1/system/cache/clear` |
| **功能描述** | 清理系统缓存数据 |
| **入参协议** | 请求体: 见下方JSON |
| **出参协议** | 见下方JSON结构 |

### 请求数据结构
```json
{
  "cache_type": "daily",  // daily/historical/all
  "days_to_keep": 7
}
```

### 响应数据结构
```json
{
  "success": true,
  "message": "缓存清理完成: daily",
  "parameters": {
    "cache_type": "daily",
    "days_to_keep": 7
  }
}
```

## 3.6 获取API使用情况

| 项目 | 内容 |
|------|------|
| **API路径** | `GET /api/v1/system/api/usage` |
| **功能描述** | 获取Tushare API使用情况 |
| **入参协议** | 无参数 |
| **出参协议** | 见下方JSON结构 |

### 响应数据结构
```json
{
  "success": true,
  "data": {
    "status": "connected",
    "token_configured": true,
    "api_initialized": true,
    "daily_requests": 245,
    "daily_limit": 500,
    "remaining_requests": 255
  }
}
```

## 3.7 获取系统配置

| 项目 | 内容 |
|------|------|
| **API路径** | `GET /api/v1/system/config` |
| **功能描述** | 获取系统配置信息（脱敏） |
| **入参协议** | 无参数 |
| **出参协议** | 见下方JSON结构 |

### 响应数据结构
```json
{
  "success": true,
  "data": {
    "cache_settings": {
      "cache_dir": "/path/to/cache",
      "cache_enabled": true
    },
    "api_settings": {
      "tushare_configured": true,
      "api_timeout": 30
    },
    "popular_etfs_count": 18,
    "environment": "development"
  }
}
```

## 3.8 获取系统统计

| 项目 | 内容 |
|------|------|
| **API路径** | `GET /api/v1/system/stats` |
| **功能描述** | 获取系统运行统计信息 |
| **入参协议** | 无参数 |
| **出参协议** | 见下方JSON结构 |

### 响应数据结构
```json
{
  "success": true,
  "data": {
    "cache_stats": {
      "daily_cache_count": 150,
      "historical_cache_count": 25,
      "permanent_cache_count": 18
    },
    "uptime": "2天3小时45分钟",
    "request_count": 1250,
    "error_count": 15,
    "last_update": "2024-09-24T16:54:00"
  }
}
```

## 3.9 测试外部连接

| 项目 | 内容 |
|------|------|
| **API路径** | `POST /api/v1/system/test/connection` |
| **功能描述** | 测试外部服务连接状态 |
| **入参协议** | 请求体: 见下方JSON |
| **出参协议** | 见下方JSON结构 |

### 请求数据结构
```json
{
  "test_type": "all"  // tushare/all
}
```

### 响应数据结构
```json
{
  "success": true,
  "data": {
    "overall_status": "success",
    "test_results": {
      "tushare": {
        "status": "success",
        "message": "Tushare API连接正常"
      }
    },
    "test_time": "2024-09-24T16:54:00"
  }
}
```

## 3.10 获取版本信息

| 项目 | 内容 |
|------|------|
| **API路径** | `GET /api/v1/system/version` |
| **功能描述** | 获取系统版本和构建信息 |
| **入参协议** | 无参数 |
| **出参协议** | 见下方JSON结构 |

### 响应数据结构
```json
{
  "success": true,
  "data": {
    "version": "1.0.0",
    "build_date": "2024-01-01",
    "git_commit": "abc123def",
    "python_version": "Python 3.8+",
    "dependencies": {
      "flask": "2.x",
      "tushare": "1.x",
      "pandas": "1.x"
    }
  }
}
```

---

# 四、接口汇总表

## ETF相关接口汇总

| 序号 | API路径 | 方法 | 功能描述 | Tushare数据 |
|------|---------|------|----------|-------------|
| 1.1 | `/api/v1/etfs/popular` | GET | 获取热门ETF列表 | ✓ 价格数据 |
| 1.2 | `/api/v1/etfs/{etf_code}/basic` | GET | 获取ETF基本信息 | ✓ 基本信息+价格 |
| 1.3 | `/api/v1/etfs/{etf_code}/latest` | GET | 获取ETF最新价格 | ✓ 完整价格数据 |
| 1.4 | `/api/v1/etfs/{etf_code}/historical` | GET | 获取ETF历史数据 | ✓ 历史价格序列 |
| 1.5 | `/api/v1/etfs/{etf_code}/summary` | GET | 获取ETF综合摘要 | ✓ 基本+价格信息 |
| 1.6 | `/api/v1/etfs/search` | GET | 搜索ETF | ✓ 基本信息 |
| 1.7 | `/api/v1/etfs/batch/latest` | POST | 批量获取最新数据 | ✓ 批量价格数据 |
| 1.8 | `/api/v1/etfs/categories` | GET | 获取ETF分类统计 | - |

## 分析相关接口汇总

| 序号 | API路径 | 方法 | 功能描述 | Tushare数据 |
|------|---------|------|----------|-------------|
| 2.1 | `/api/v1/analysis/suitability/{etf_code}` | POST | 分析ETF适合性 | ✓ 基于历史数据分析 |
| 2.2 | `/api/v1/analysis/atr/{etf_code}` | GET | 计算ATR分析 | ✓ 基于历史数据计算 |
| 2.3 | `/api/v1/analysis/grid/{etf_code}` | POST | 生成网格策略 | ✓ 基于当前价格计算 |
| 2.4 | `/api/v1/analysis/comprehensive/{etf_code}` | POST | 综合分析 | ✓ 全面数据分析 |
| 2.5 | `/api/v1/analysis/batch/popular` | POST | 批量分析热门ETF | ✓ 批量数据分析 |
| 2.6 | `/api/v1/analysis/market/overview` | GET | 获取市场概览 | ✓ 指数数据 |
| 2.7 | `/api/v1/analysis/compare` | POST | 比较多个ETF | ✓ 多ETF数据对比 |
| 2.8 | `/api/v1/analysis/recommendations` | POST | 获取投资建议 | ✓ 基于分析结果 |

## 系统相关接口汇总

| 序号 | API路径 | 方法 | 功能描述 | Tushare数据 |
|------|---------|------|----------|-------------|
| 3.1 | `/api/v1/system/capital-presets` | GET | 获取预设资金选项 | - |
| 3.2 | `/api/v1/system/health` | GET | 系统健康检查 | ✓ API连接状态 |
| 3.3 | `/api/v1/system/info` | GET | 获取系统信息 | - |
| 3.4 | `/api/v1/system/cache/info` | GET | 获取缓存信息 | - |
| 3.5 | `/api/v1/system/cache/clear` | POST | 清理缓存 | - |
| 3.6 | `/api/v1/system/api/usage` | GET | 获取API使用情况 | ✓ API使用统计 |
| 3.7 | `/api/v1/system/config` | GET | 获取系统配置 | - |
| 3.8 | `/api/v1/system/stats` | GET | 获取系统统计 | - |
| 3.9 | `/api/v1/system/test/connection` | POST | 测试外部连接 | ✓ API连接测试 |
| 3.10 | `/api/v1/system/version` | GET | 获取版本信息 | - |

---

# 五、Tushare数据字段详细说明

## 基本信息字段 (fund_basic接口)

| 字段名 | 中文名称 | 数据类型 | 说明 |
|--------|----------|----------|------|
| ts_code | 基金代码 | str | TS代码，如510300.SH |
| name | 基金名称 | str | 基金全称 |
| management | 管理人 | str | 基金管理公司 |
| custodian | 托管人 | str | 基金托管银行 |
| fund_type | 基金类型 | str | ETF/LOF等 |
| found_date | 成立日期 | str | YYYYMMDD格式 |
| due_date | 到期日期 | str | YYYYMMDD格式 |
| list_date | 上市日期 | str | YYYYMMDD格式 |
| issue_date | 发行日期 | str | YYYYMMDD格式 |
| issue_amount | 发行规模 | float | 发行总额(万元) |
| m_fee | 管理费 | float | 管理费率(%) |
| c_fee | 托管费 | float | 托管费率(%) |
| benchmark | 业绩基准 | str | 跟踪指数 |

## 价格数据字段 (fund_daily接口)

| 字段名 | 中文名称 | 数据类型 | 说明 |
|--------|----------|----------|------|
| ts_code | 基金代码 | str | TS代码 |
| trade_date | 交易日期 | str | YYYYMMDD格式 |
| open | 开盘价 | float | 当日开盘价 |
| high | 最高价 | float | 当日最高价 |
| low | 最低价 | float | 当日最低价 |
| close | 收盘价 | float | 当日收盘价 |
| pre_close | 昨收价 | float | 前一交易日收盘价 |
| change | 涨跌额 | float | 价格变动额 |
| pct_chg | 涨跌幅 | float | 涨跌幅(%) |
| vol | 成交量 | float | 成交量(手) |
| amount | 成交额 | float | 成交金额(千元) |

---

# 六、使用示例

## 获取ETF基本信息示例

```bash
curl -X GET "http://localhost:5002/api/v1/etfs/510300/basic" \
  -H "Content-Type: application/json"
```

## 进行综合分析示例

```bash
curl -X POST "http://localhost:5002/api/v1/analysis/comprehensive/510300" \
  -H "Content-Type: application/json" \
  -d '{
    "investment_amount": 100000.0,
    "risk_tolerance": "medium",
    "grid_count": 12
  }'
```

## 批量分析示例

```bash
curl -X POST "http://localhost:5002/api/v1/analysis/batch/popular" \
  -H "Content-Type: application/json" \
  -d '{
    "investment_amount": 200000.0,
    "risk_tolerance": "high"
  }'
```

---

**文档版本**: v1.0.0  
**最后更新**: 2024-09-24  
**维护人员**: 后端开发团队
    "basic_info": {
      // ETF基本信息，结构同1.2接口
    },
    "latest_data": {
      // 最新价格数据，结构同1.3接口
    },
    "formatted_data": {
      "current_price": "¥4.12",
      "change_percent": "+1.25%",
      "volume": "12,345,678",
      "amount": "¥51,234,567.89"
    }
  }
}
```

## 1.6 搜索ETF

| 项目 | 内容 |
|------|------|
| **API路径** | `GET /api/v1/etfs/search` |
| **功能描述** | 根据关键词搜索ETF |
| **入参协议** | 查询参数: `keyword` (搜索关键词，至少2个字符) |
| **出参协议** | 见下方JSON结构 |

### 请求示例
```
GET /api/v1/etfs/search?keyword=300
```

### 响应数据结构 (Tushare数据)
```json
{
  "success": true,
  "data": [
    {
      "code": "510300",
      "name": "沪深300ETF",        // Tushare数据
      "market": "SH",             // Tushare数据
      "list_date": "20121228"     // Tushare数据
    }
  ],
  "count": 5,
  "keyword": "300"
}
```

## 1.7 批量获取ETF最新数据

| 项目 | 内容 |
|------|------|
| **API路径** | `POST /api/v1/etfs/batch/latest` |
| **功能描述** | 批量获取多个ETF的最新价格数据 |
| **入参协议** | 见下方JSON结构 |
| **出参协议** | 见下方JSON结构 |

### 请求数据结构
```json
{
  "etf_codes": ["510300", "510500", "159919"]
}
```

### 响应数据结构
```json
{
  "success": true,
  "data": {
    "510300": {
      // 最新价格数据，结构同1.3接口
    },
    "510500": {
      // 最新价格数据，结构同1.3接口
    }
  },
  "errors": {
    "159919": "未找到数据"
  },
  "success_count": 2,
  "error_count": 1
}
```

## 1.8 获取ETF分类统计

| 项目 | 内容 |
|------|------|
| **API路径** | `GET /api/v1/etfs/categories` |
| **功能描述** | 获取ETF按分类的统计信息 |
| **入参协议** | 无参数 |
| **出参协议** | 见下方JSON结构 |

### 响应数据结构
```json
{
  "success": true,
  "data": [
    {
      "name": "宽基指数",
      "count": 5,
      "etfs": [
        {"code": "510300", "name": "沪深300ETF"},
        {"code": "510500", "name": "中证500ETF"}
      ]
    }
  ],
  "total_categories": 4
}
```

---

# 二、分析相关接口 (analysis_routes.py)

## 2.1 分析ETF适合性

| 项目 | 内容 |
|------|------|
| **API路径** | `POST /api/v1/analysis/suitability/{etf_code}` |
| **功能描述** | 分析ETF是否适合网格策略交易 |
| **入参协议** | 路径参数: `etf_code`<br>请求体: 见下方JSON |
| **出参协议** | 见下方JSON结构 |

### 请求数据结构
```json
{
  "investment_amount": 100000.0,
  "risk_tolerance": "medium"  // low/medium/high
}
```

### 响应数据结构
```json
{
  "success": true,
  "data": {
    "total_score": 85.5,
    "amplitude_score": 90,
    "volatility_score": 85,
    "market_score": 80,
    "liquidity_score": 88,
    "data_quality_score": 92,
    "level": "非常适合",           // 非常适合/基本适合/不适合
    "color": "green",            // green/yellow/red
    "description": "该ETF具有良好的波动性和流动性，适合网格策略",
    "recommendation": "建议使用12-15个网格进行交易",
    "details": {
      "volatility": 0.025,      // 基于Tushare历史数据计算
      "avg_volume": 12345678,   // 基于Tushare数据计算的平均成交量
      "price_range": {
        "min": 3.80,
        "max": 4.50
      }
    }
  }
}
```

## 2.2 计算ATR分析

| 项目 | 内容 |
|------|------|
| **API路径** | `GET /api/v1/analysis/atr/{etf_code}` |
| **功能描述** | 计算ETF的ATR(平均真实波幅)技术分析 |
| **入参协议** | 路径参数: `etf_code`<br>查询参数: `period` (ATR周期，默认20) |
| **出参协议** | 见下方JSON结构 |

### 请求示例
```
GET /api/v1/analysis/atr/510300?period=20
```

### 响应数据结构 (基于Tushare数据计算)
```json
{
  "success": true,
  "data": {
    "current_atr": 0.085,           // 基于Tushare历史数据计算
    "atr_ratio": 0.021,             // ATR/当前价格比率
    "atr_score": 85,                // ATR评分(0-100)
    "atr_level": "适中",            // 高/适中/低
    "price_range": {
      "lower": 3.95,               // 基于ATR计算的价格下限
      "upper": 4.35                // 基于ATR计算的价格上限
    },
    "volatility": 0.025,            // 基于Tushare数据计算的波动率
    "adx_value": 25.6               // ADX指标值
  }
}
```

## 2.3 生成网格策略

| 项目 | 内容 |
|------|------|
| **API路径** | `POST /api/v1/analysis/grid/{etf_code}` |
| **功能描述** | 为ETF生成网格交易策略参数 |
| **入参协议** | 路径参数: `etf_code`<br>请求体: 见下方JSON |
| **出参协议** | 见下方JSON结构 |

### 请求数据结构
```json
{
  "investment_amount": 100000.0,
  "grid_count": 10,
  "price_range_percent": 0.2
}
```

### 响应数据结构
```json
{
  "success": true,
  "data": {
    "grid_count": 10,
    "grid_type": "等差",
    "step_size": 0.04,
    "step_ratio": 0.01,
    "price_lower": 3.80,           // 基于Tushare当前价格和ATR计算
    "price_upper": 4.60,           // 基于Tushare当前价格和ATR计算
    "price_levels": [3.80, 3.84, 3.88, 3.92, 3.96, 4.00, 4.04, 4.08, 4.12, 4.16],
    "base_position_ratio": 0.2,
    "single_trade_quantity": 5000
  }
}
```

## 2.4 综合分析

| 项目 | 内容 |
|------|------|
| **API路径** | `POST /api/v1/analysis/comprehensive/{etf_code}` |
| **功能描述** | 对ETF进行全面的综合分析，包含适合性、ATR和网格策略 |
| **入参协议** | 路径参数: `etf_code`<br>请求体: 见下方JSON |
| **出参协议** | 见下方JSON结构 |

### 请求数据结构
```json
{
  "investment_amount": 100000.0,
  "risk_tolerance": "medium",
  "grid_count": 10
}
```

### 响应数据结构 (包含大量Tushare数据)
```json
{
  "success": true,
  "data": {
    "etf_info": {
      // ETF基本信息，包含Tushare数据
    },
    "atr_analysis": {
      // ATR分析结果，基于Tushare历史数据
    },
    "suitability_evaluation": {
      // 适合性评估结果
    },
    "grid_parameters": {
      // 网格参数，基于Tushare价格数据计算
    },
    "fund_allocation": {
      "total_capital": 100000.0,
      "base_position_amount": 20000.0,
      "grid_amount": 80000.0,
      "single_trade_amount": 8000.0,
      "buy_grid_count": 5,
      "buy_grid_amount": 40000.0,
      "grid_utilization_rate": 0.8
    },
    "strategy_rationale": "基于该ETF的历史波动特征和流动性分析...",
    "adjustment_suggestions": [
      "建议在市场震荡期使用",
      "注意控制单次交易金额"
    ],
    "risk_warnings": [
      "网格策略适合震荡市场",
      "单边趋势市场需谨慎"
    ],
    "analysis_timestamp": "2024-09-24T16:54:00"
  }
}
```

## 2.5 批量分析热门ETF

| 项目 | 内容 |
|------|------|
| **API路径** | `POST /api/v1/analysis/batch/popular` |
| **功能描述** | 批量分析所有热门ETF的适合性 |
| **入参协议** | 请求体: 见下方JSON |
| **出参协议** | 见下方JSON结构 |

### 请求数据结构
```json
{
  "investment_amount": 100000.0,
  "risk_tolerance": "medium"
}
```

### 响应数据结构
```json
{
  "success": true,
  "data": [
    {
      "etf_code": "510300",
      "etf_name": "沪深300ETF",
      "suitability_score": 85.5,
      "is_suitable": true,
      "category": "宽基指数"
    }
  ],
  "count": 18
}
```

## 2.6 获取市场概览

| 项目 | 内容 |
|------|------|
| **API路径** | `GET /api/v1/analysis/market/overview` |
| **功能描述** | 获取整体市场概览信息 |
| **入参协议** | 无参数 |
| **出参协议** | 见下方JSON结构 |

### 响应数据结构 (基于Tushare数据)
```json
{
  "success": true,
  "data": {
    "market_regime": "震荡市场",
    "confidence": 0.75,
    "trend_strength": 0.3,
    "volatility_level": "中等",
    "suitable_etf_count": 12,
    "total_etf_count": 18,
    "avg_suitability_score": 78.5,
    "market_indicators": {
      "sh_index": {              // 基于Tushare指数数据
        "current": 3150.25,
        "change": 1.2
      },
      "sz_index": {              // 基于Tushare指数数据
        "current": 10250.80,
        "change": 0.8
      }
    }
  }
}
```

## 2.7 比较多个ETF

| 项目 | 内容 |
|------|------|
| **API路径** | `POST /api/v1/analysis/compare` |
| **功能描述** | 比较多个ETF的适合性和特征 |
| **入参协议** | 请求体: 见下方JSON |
| **出参协议** | 见下方JSON结构 |

### 请求数据结构
```json
{
  "etf_codes": ["510300", "510500", "159919"],
  "investment_amount": 100000.0,
  "risk_tolerance": "medium"
}
```

### 响应数据结构
```json
{
  "success": true,
  "data": {
    "comparison_results": [
      {
        "etf_code": "510300",
        "suitability": {
          // 适合性分析结果
        },
        "atr_analysis": {
          // ATR分析结果，基于Tushare数据
        }
      }
    ],
    "ranked_results": [
      // 按适合性评分排序的结果
    ],
    "parameters": {
      "investment_amount": 100000.0,
      "risk_tolerance": "medium"
    }
  },
  "count": 3
}
```

## 2.8 获取投资建议

| 项目 | 内容 |
|------|------|
| **API路径** | `POST /api/v1/analysis/recommendations` |
| **功能描述** | 根据用户偏好获取个性化投资建议 |
| **入参协议** | 请求体: 见下方JSON |
| **出参协议** | 见下方JSON结构 |

### 请求数据结构
```json
{
  "investment_amount": 100000.0,
  "risk_tolerance": "medium",
  "investment_period": "medium",  // short/medium/long
  "preferred_categories": ["宽基指数", "行业主题"]
}
```

### 响应数据结构
```json
{
  "success": true,
  "data": {
    "recommendations": [
      {
        "etf_code": "510300",
        "etf_name": "沪深300ETF",
        "suitability_score": 85.5,
        "recommendation_reason": "波动性适中，流动性良好",
        "expected_return": "年化8-12%",
        "risk_level": "中等风险"
      }
    ],
    "total_analyzed": 18,
    "suitable_count": 12,
    "parameters": {
      "investment_amount": 100000.0,
      "risk_tolerance": "medium",
      "investment_period": "medium",
      "preferred_categories": ["宽基指数", "行业主题"]
    }
  }
}
```

---

# 三、系统相关接口 (system_routes.py)

## 3.1 获取预设资金选项

| 项目 | 内容 |
|------|------|
| **API路径** | `GET /api/v1/system/capital-presets` |
| **功能描述** | 获取系统预设的投资金额选项 |
| **入参协议** | 无参数 |
| **出参协议** | 见下方JSON结构 |

### 响应数据结构
```json
{
  "success": true,
  "data": [
    {"value": 100000, "label": "10万", "popular": true},
    {"value": 200000, "label": "20万", "popular": true},
    {"value": 300000, "label": "30万", "popular": false},
    {"value": 500000, "label": "50万", "popular": true},
    {"value": 800000, "label": "80万", "popular": false},
    {"value": 1000000, "label": "100万", "popular": true},
    {"value": 1500000, "label": "150万", "popular": false},
    {"value": 2000000, "label": "200万", "popular": false}
  ]
}
```

## 3.2 系统健康检查

| 项目 | 内容 |
|------|------|
| **API路径** | `GET /api/v1/system/health` |
| **功能描述** | 检查系统各组件的健康状态 |
| **入参协议** | 无参数 |
| **出参协议** | 见下方JSON结构 |

### 响应数据结构
```json
{
  "success": true,
  "data": {
    "status": "healthy",  // healthy/degraded/error
    "timestamp": "2024-09-24T16:54:00",
    "version": "1.0.0",
    "components": {
      "tushare_api": {
        "status": "healthy",
        "message": "API连接正常"
      },
      "cache_service": {
        "status": "healthy",
        "message": "缓存服务正常",
        "cache_info": {
          "daily_cache_count": 150,
          "historical_cache_count": 25,
          "permanent_cache_count": 18
        }
      }
    }
  }
}
```

## 3.3 获取系统信息

| 项目 | 内容 |
|------|------|
| **API路径** | `GET /api/v1/system/info` |
| **功能描述** | 获取系统基本信息和功能介绍 |
| **入参协议** | 无参数 |
| **出参协议** | 见下方JSON结构 |

### 响应数据结构
```json
{
  "success": true,
  "data": {
    "application": {
      "name": "ETF Grid Design Backend",
      "version": "1.0.0",
      "description": "ETF网格策略分析系统后端服务"
    },
    "api": {
      "version": "v1",
      "base_url": "/api/v1",
      "documentation": "/api/v1/docs"
    },
    "features": [
      "ETF基本信息查询",
      "ATR技术分析",
      "网格策略计算",
      "适合性分析",
      "批量分析",
      "市场概览"
    ],
    "supported_etfs": "A股ETF产品",
    "data_source": "Tushare Pro API",
    "cache_strategy": "文件缓存系统"
  }
}
```

## 3.4 获取缓存信息

| 项目 | 内容 |
|------|------|
| **API路径** | `GET /api/v1/system/cache/info` |
| **功能描述** | 获取系统缓存使用情况 |
| **入参协议** | 无参数 |
| **出参协议** | 见下方JSON结构 |

### 响应数据结构
```json
{
  "success": true,
  "data": {
