# ETF网格设计系统 - 前端开发规范

> 本规范用于指导后续前端开发工作，确保代码质量和架构一致性。

## 📁 目录结构规范

### 标准目录架构

```
frontend/src/
├── app/                          # 应用程序级配置
│   ├── AppRouter.jsx            # 路由配置
│   ├── AppLayout.jsx            # 全局布局
│   ├── AppHeader.jsx            # 应用头部
│   └── AppFooter.jsx            # 应用底部
├── pages/                       # 页面级组件
│   ├── HomePage/                # 首页模块
│   │   ├── index.js            # 统一导出
│   │   ├── HomePage.jsx        # 页面主组件
│   │   └── components/         # 页面专用组件
│   └── AnalysisPage/           # 分析页面模块
├── features/                    # 业务功能模块
│   ├── analysis/               # 分析功能
│   │   ├── components/         # 分析相关组件
│   │   ├── hooks/              # 分析相关Hooks
│   │   ├── services/           # 分析API服务
│   │   └── types/              # 类型定义
│   ├── etf/                    # ETF功能
│   └── history/                # 历史记录功能
├── shared/                     # 共享资源
│   ├── components/             # 通用组件
│   │   ├── ui/                 # 基础UI组件
│   │   ├── layout/             # 布局组件
│   │   └── feedback/           # 反馈组件
│   ├── hooks/                  # 通用Hooks
│   ├── utils/                  # 工具函数
│   ├── services/               # 通用服务
│   ├── constants/              # 常量定义
│   └── types/                  # 通用类型
└── assets/                     # 静态资源
    ├── images/                 # 图片资源
    ├── icons/                  # 图标资源
    └── styles/                 # 全局样式
```

### 目录职责定义

#### `app/` - 应用程序级

- **职责**：应用配置、路由、全局布局、全局状态
- **规则**：只能包含应用级别的配置和组件
- **不可包含**：具体业务逻辑、页面组件

#### `pages/` - 页面级组件

- **职责**：页面路由组件，协调多个功能模块
- **规则**：每个页面一个目录，包含主组件和页面专用组件
- **不可包含**：复杂业务逻辑（应抽取到features中）

#### `features/` - 业务功能模块

- **职责**：具体的业务功能实现
- **规则**：按业务域分组，每个feature包含完整的组件、逻辑、服务
- **不可包含**：跨业务域的通用逻辑（应放到shared中）

#### `shared/` - 共享资源

- **职责**：跨模块的通用代码
- **规则**：必须保证复用性，不能包含特定业务逻辑
- **不可包含**：业务相关的具体实现

## 🧩 组件开发规范

### 组件分类和职责

#### 1. 页面组件 (Page Components)

```javascript
// pages/HomePage/HomePage.jsx
/**
 * 首页组件
 * @description 首页的主要入口，负责协调子组件和处理页面级状态
 */
export default function HomePage() {
  // 页面级状态管理
  // 子组件协调
  // 页面级事件处理
}
```

#### 2. 功能组件 (Feature Components)

```javascript
// features/analysis/components/ParameterForm.jsx
/**
 * 参数表单组件
 * @description 负责ETF分析参数的收集和验证
 * @param {Function} onSubmit - 表单提交回调
 * @param {Object} initialValues - 初始值
 */
export default function ParameterForm({ onSubmit, initialValues }) {
  // 表单状态管理
  // 验证逻辑
  // 提交处理
}
```

#### 3. UI组件 (UI Components)

```javascript
// shared/components/ui/Button.jsx
/**
 * 通用按钮组件
 * @description 项目中使用的标准按钮组件
 * @param {string} variant - 按钮样式变体 'primary' | 'secondary' | 'danger'
 * @param {string} size - 按钮尺寸 'sm' | 'md' | 'lg'
 * @param {boolean} loading - 加载状态
 */
export default function Button({ 
  variant = 'primary', 
  size = 'md', 
  loading = false,
  children,
  ...props 
}) {
  // 样式逻辑
  // 状态处理
}
```

### 组件复杂度控制

- **单个组件不超过200行**
- **单个函数不超过50行**
- **最多3层嵌套**
- **Props数量不超过8个**

### 组件拆分原则

```javascript
// ❌ 避免：一个组件处理太多职责
function ComplexForm() {
  // ETF选择逻辑 (50行)
  // 资金输入逻辑 (40行)  
  // 风险选择逻辑 (30行)
  // 表单验证逻辑 (40行)
  // 提交处理逻辑 (30行)
  // 总计：190行 - 职责过多
}

// ✅ 推荐：拆分为多个专注的组件
function ParameterForm({ onSubmit }) {
  return (
    <form onSubmit={handleSubmit}>
      <ETFSelector value={etf} onChange={setEtf} />
      <CapitalInput value={capital} onChange={setCapital} />
      <RiskSelector value={risk} onChange={setRisk} />
      <SubmitButton loading={loading} />
    </form>
  );
}
```

## 📝 命名规范

### 文件命名

```bash
# 组件文件：PascalCase
HomePage.jsx
AnalysisReport.jsx
ETFSelector.jsx

# 工具文件：camelCase
formatUtils.js
validationHelpers.js
apiClient.js

# 常量文件：camelCase
etfConstants.js
appConfig.js

# Hook文件：use前缀 + camelCase
usePersistedState.js
useAnalysisData.js
useShare.js

# 类型文件：camelCase
analysisTypes.js
etfTypes.js
```

### 组件命名

```javascript
// ✅ 推荐：描述性命名
export default function ETFAnalysisReport() {}
export default function CapitalInputField() {}
export default function RiskPreferenceSelector() {}

// ❌ 避免：缩写或不清晰命名
export default function AR() {}
export default function Input() {}
export default function Selector() {}
```

### 函数命名

```javascript
// ✅ 推荐：动词 + 名词结构
const handleAnalysisSubmit = () => {};
const validateETFCode = () => {};
const formatCurrencyAmount = () => {};
const fetchETFData = () => {};

// ❌ 避免：不清晰的命名
const handle = () => {};
const check = () => {};
const get = () => {};
```

### 变量命名

```javascript
// ✅ 推荐：描述性命名
const [analysisData, setAnalysisData] = useState(null);
const [isLoading, setIsLoading] = useState(false);
const [validationErrors, setValidationErrors] = useState({});

// ❌ 避免：缩写或单字母
const [data, setData] = useState(null);
const [loading, setLoading] = useState(false);
const [errors, setErrors] = useState({});
```

### 常量命名

```javascript
// ✅ 推荐：SCREAMING_SNAKE_CASE
const API_ENDPOINTS = {
  ANALYZE_ETF: '/api/analyze',
  ETF_INFO: '/api/etf/info'
};

const VALIDATION_RULES = {
  MIN_CAPITAL: 100000,
  MAX_CAPITAL: 5000000
};

const GRID_TYPES = {
  GEOMETRIC: '等比',
  ARITHMETIC: '等差'
};
```

## 📦 导入规范

### 路径别名使用

```javascript
// ✅ 推荐：使用别名路径
import { formatCurrency } from '@shared/utils/format';
import { AnalysisReport } from '@features/analysis/components';
import { Button } from '@shared/components/ui';
import HomePage from '@pages/HomePage';

// ❌ 避免：复杂的相对路径
import { formatCurrency } from '../../../shared/utils/format';
import { AnalysisReport } from '../../features/analysis/components';
```

### 导入顺序规范

```javascript
// 1. React和第三方库
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';

// 2. 内部别名导入（按字母顺序）
import { Button, Card } from '@shared/components/ui';
import { useShare } from '@shared/hooks';
import { formatCurrency } from '@shared/utils';

// 3. 功能模块导入
import { AnalysisReport } from '@features/analysis/components';
import { ETFSelector } from '@features/etf/components';

// 4. 相对路径导入
import './HomePage.css';
```

### 导出规范

```javascript
// 组件文件：默认导出
export default function HomePage() {}

// 工具文件：命名导出
export const formatCurrency = () => {};
export const validateETFCode = () => {};

// 索引文件：统一导出
export { default as HomePage } from './HomePage';
export { default as AnalysisPage } from './AnalysisPage';

// 类型文件：命名导出
export interface AnalysisData {}
export type ETFInfo = {};
```

## 🎨 代码风格规范

### React组件结构

```javascript
/**
 * 组件文档注释
 */
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

// 外部导入
// 内部导入
// 相对导入

/**
 * 组件JSDoc注释
 */
function ComponentName({ prop1, prop2, ...props }) {
  // 1. Hooks (按顺序：useState, useEffect, 自定义hooks)
  const [state, setState] = useState(initialValue);
  const customValue = useCustomHook();
  
  // 2. 计算值和派生状态
  const computedValue = useMemo(() => {
    return state.map(item => transform(item));
  }, [state]);
  
  // 3. 事件处理函数
  const handleClick = useCallback(() => {
    // 处理逻辑
  }, [dependencies]);
  
  // 4. useEffect (按依赖复杂度排序)
  useEffect(() => {
    // 副作用逻辑
  }, [dependencies]);
  
  // 5. 条件渲染处理
  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;
  
  // 6. 主要渲染
  return (
    <div className="component-wrapper">
      {/* JSX内容 */}
    </div>
  );
}

// PropTypes定义
ComponentName.propTypes = {
  prop1: PropTypes.string.isRequired,
  prop2: PropTypes.func
};

// 默认Props
ComponentName.defaultProps = {
  prop2: () => {}
};

export default ComponentName;
```

### 函数和变量声明

```javascript
// ✅ 推荐：const优先，let次之，避免var
const immutableValue = 'constant';
let mutableValue = 'variable';

// ✅ 推荐：箭头函数用于简单表达式
const simpleFunction = (x) => x * 2;

// ✅ 推荐：函数声明用于复杂逻辑
function complexFunction(parameters) {
  // 复杂逻辑
  return result;
}

// ✅ 推荐：解构赋值
const { name, age } = user;
const [first, second] = array;
```

### 条件渲染规范

```javascript
// ✅ 推荐：简单条件使用 &&
{isLoading && <LoadingSpinner />}

// ✅ 推荐：复杂条件使用三元运算符
{data ? <DataDisplay data={data} /> : <EmptyState />}

// ✅ 推荐：多条件使用函数
const renderContent = () => {
  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;
  if (!data) return <EmptyState />;
  return <DataDisplay data={data} />;
};

return <div>{renderContent()}</div>;
```

## 🛠️ 工具函数规范

### 函数设计原则

```javascript
// ✅ 推荐：纯函数，无副作用
export const formatCurrency = (amount) => {
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency: 'CNY'
  }).format(amount);
};

// ✅ 推荐：参数验证
export const validateETFCode = (code) => {
  if (typeof code !== 'string') {
    throw new Error('ETF code must be a string');
  }
  return /^\d{6}$/.test(code);
};

// ✅ 推荐：错误处理
export const fetchETFData = async (code) => {
  try {
    const response = await api.getETFInfo(code);
    return { data: response.data, error: null };
  } catch (error) {
    return { data: null, error: error.message };
  }
};
```

### 工具函数分类

```javascript
// shared/utils/format.js - 格式化工具
export const formatCurrency = (amount) => {};
export const formatPercent = (value) => {};
export const formatDate = (date) => {};

// shared/utils/validation.js - 验证工具
export const validateETFCode = (code) => {};
export const validateCapital = (amount) => {};
export const validateForm = (data) => {};

// shared/utils/url.js - URL工具
export const generateAnalysisURL = (code, params) => {};
export const parseURLParams = (search) => {};

// shared/utils/storage.js - 存储工具
export const getStorageItem = (key) => {};
export const setStorageItem = (key, value) => {};
```

## 🔄 Hooks规范

### 自定义Hook命名和结构

```javascript
// shared/hooks/usePersistedState.js
import { useState, useEffect } from 'react';

/**
 * 持久化状态Hook
 * @param {string} key - localStorage键名
 * @param {any} defaultValue - 默认值
 * @returns {[any, Function]} 状态值和setter函数
 */
export function usePersistedState(key, defaultValue) {
  const [state, setState] = useState(() => {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : defaultValue;
    } catch (error) {
      console.warn(`Error reading localStorage key "${key}":`, error);
      return defaultValue;
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem(key, JSON.stringify(state));
    } catch (error) {
      console.warn(`Error setting localStorage key "${key}":`, error);
    }
  }, [key, state]);

  return [state, setState];
}
```

### Hook使用规范

```javascript
// ✅ 推荐：Hook调用在组件顶层
function Component() {
  const [data, setData] = useState(null);
  const { shareContent } = useShare();
  const navigate = useNavigate();
  
  // 其他逻辑...
}

// ❌ 避免：在条件或循环中调用Hook
function Component() {
  if (condition) {
    const [data, setData] = useState(null); // ❌ 错误
  }
}
```

## 📡 API服务规范

### API客户端结构

```javascript
// shared/services/api.js
class ApiService {
  constructor() {
    this.baseURL = '/api';
  }

  /**
   * 通用请求方法
   * @param {string} endpoint - API端点
   * @param {Object} options - 请求选项
   * @returns {Promise<Object>} 响应数据
   */
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
  
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
    
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API请求失败 [${endpoint}]:`, error);
      throw error;
    }
  }

  /**
   * ETF分析请求
   * @param {Object} parameters - 分析参数
   * @returns {Promise<Object>} 分析结果
   */
  async analyzeETF(parameters) {
    return this.request('/analyze', {
      method: 'POST',
      body: JSON.stringify(parameters),
    });
  }
}

// 导出单例
export const apiService = new ApiService();
export const analyzeETF = (params) => apiService.analyzeETF(params);
```

### 错误处理规范

```javascript
// ✅ 推荐：统一的错误处理
const handleAnalysis = async (parameters) => {
  try {
    setLoading(true);
    const response = await analyzeETF(parameters);
  
    if (response.success) {
      setData(response.data);
    } else {
      throw new Error(response.error || '分析失败');
    }
  } catch (error) {
    console.error('分析请求失败:', error);
    setError(error.message);
    // 用户友好的错误提示
    showNotification('分析请求失败，请稍后重试', 'error');
  } finally {
    setLoading(false);
  }
};
```

## 🎯 性能规范

### 组件优化

```javascript
// ✅ 推荐：使用React.memo避免不必要的重渲染
const ExpensiveComponent = React.memo(function ExpensiveComponent({ data }) {
  // 复杂渲染逻辑
}, (prevProps, nextProps) => {
  // 自定义比较逻辑
  return prevProps.data.id === nextProps.data.id;
});

// ✅ 推荐：使用useCallback缓存函数
const handleClick = useCallback((id) => {
  onItemClick(id);
}, [onItemClick]);

// ✅ 推荐：使用useMemo缓存计算结果
const expensiveValue = useMemo(() => {
  return data.map(item => complexCalculation(item));
}, [data]);
```

### 懒加载规范

```javascript
// ✅ 推荐：页面级懒加载
const HomePage = lazy(() => import('@pages/HomePage'));
const AnalysisPage = lazy(() => import('@pages/AnalysisPage'));

// ✅ 推荐：组件级懒加载
const HeavyChart = lazy(() => import('@shared/components/ui/HeavyChart'));

// 使用Suspense包装
<Suspense fallback={<LoadingSpinner />}>
  <HeavyChart data={chartData} />
</Suspense>
```

### 包大小优化

```javascript
// ✅ 推荐：按需导入
import { debounce } from 'lodash/debounce';

// ❌ 避免：全量导入
import _ from 'lodash';
```

## 🧪 测试规范

### 组件测试结构

```javascript
// __tests__/ParameterForm.test.jsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ParameterForm from '../ParameterForm';

describe('ParameterForm', () => {
  const mockOnSubmit = jest.fn();
  
  beforeEach(() => {
    mockOnSubmit.mockClear();
  });

  it('should render all form fields', () => {
    render(<ParameterForm onSubmit={mockOnSubmit} />);
  
    expect(screen.getByLabelText(/ETF代码/)).toBeInTheDocument();
    expect(screen.getByLabelText(/投资金额/)).toBeInTheDocument();
    expect(screen.getByText(/开始分析/)).toBeInTheDocument();
  });

  it('should validate ETF code input', async () => {
    render(<ParameterForm onSubmit={mockOnSubmit} />);
  
    const etfInput = screen.getByLabelText(/ETF代码/);
    fireEvent.change(etfInput, { target: { value: '123' } });
  
    const submitButton = screen.getByText(/开始分析/);
    fireEvent.click(submitButton);
  
    await waitFor(() => {
      expect(screen.getByText(/请输入6位数字ETF代码/)).toBeInTheDocument();
    });
  
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });
});
```

### 工具函数测试

```javascript
// __tests__/formatUtils.test.js
import { formatCurrency, formatPercent } from '../formatUtils';

describe('formatUtils', () => {
  describe('formatCurrency', () => {
    it('should format numbers correctly', () => {
      expect(formatCurrency(100000)).toBe('¥100,000');
      expect(formatCurrency(1234567)).toBe('¥1,234,567');
    });

    it('should handle edge cases', () => {
      expect(formatCurrency(0)).toBe('¥0');
      expect(formatCurrency(-1000)).toBe('-¥1,000');
    });
  });
});
```

## 📚 文档规范

### 组件文档注释

```javascript
/**
 * ETF选择器组件
 * 
 * @description 提供ETF代码输入和热门ETF快选功能，支持实时验证和信息展示
 * 
 * @param {string} value - 当前ETF代码值
 * @param {Function} onChange - 值变化回调函数 (code: string) => void
 * @param {string} [error] - 验证错误信息
 * @param {Array<Object>} [popularETFs] - 热门ETF列表
 * @param {Object} [etfInfo] - ETF详细信息
 * @param {boolean} [loading] - 加载状态
 * 
 * @example
 * <ETFSelector 
 *   value={etfCode}
 *   onChange={setEtfCode}
 *   error={errors.etfCode}
 *   popularETFs={popularList}
 * />
 */
export default function ETFSelector({ 
  value, 
  onChange, 
  error, 
  popularETFs = [],
  etfInfo,
  loading = false 
}) {
  // 组件实现
}
```

### 函数文档注释

```javascript
/**
 * 格式化金额为中文货币格式
 * 
 * @param {number} amount - 金额数值
 * @param {Object} [options] - 格式化选项
 * @param {number} [options.minimumFractionDigits=0] - 最小小数位数
 * @param {number} [options.maximumFractionDigits=0] - 最大小数位数
 * 
 * @returns {string} 格式化后的金额字符串
 * 
 * @example
 * formatCurrency(100000) // '¥100,000'
 * formatCurrency(1234.567, { maximumFractionDigits: 2 }) // '¥1,234.57'
 * 
 * @throws {Error} 当amount不是数字时
 */
export const formatCurrency = (amount, options = {}) => {
  if (typeof amount !== 'number' || isNaN(amount)) {
    throw new Error('Amount must be a valid number');
  }
  
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency: 'CNY',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
    ...options
  }).format(amount);
};
```

## 🚀 构建和部署规范

### 打包配置优化

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
      '@shared': resolve(__dirname, './src/shared'),
      '@features': resolve(__dirname, './src/features'),
      '@pages': resolve(__dirname, './src/pages'),
      '@app': resolve(__dirname, './src/app'),
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom'],
          ui: ['lucide-react'],
        },
      },
    },
  },
});
```

### 环境配置

```javascript
// .env.development
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_ENV=development

// .env.production  
VITE_API_BASE_URL=https://api.etfer.top
VITE_APP_ENV=production
```

## 📋 代码检查配置

### ESLint配置

```javascript
// .eslintrc.js
module.exports = {
  extends: [
    'eslint:recommended',
    '@typescript-eslint/recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended'
  ],
  plugins: ['import'],
  rules: {
    'import/order': [
      'error',
      {
        groups: [
          'builtin',
          'external', 
          'internal',
          'parent',
          'sibling',
          'index'
        ],
        'newlines-between': 'always',
        alphabetize: {
          order: 'asc',
          caseInsensitive: true
        }
      }
    ],
    'react/prop-types': 'error',
    'react-hooks/exhaustive-deps': 'warn',
    'no-console': 'warn',
    'no-debugger': 'error'
  }
};
```

### Prettier配置

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false
}
```

## 🔧 开发工具配置

### package.json脚本

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint src --ext js,jsx,ts,tsx --report-unused-disable-directives --max-warnings 0",
    "lint:fix": "eslint src --ext js,jsx,ts,tsx --fix",
    "format": "prettier --write \"src/**/*.{js,jsx,ts,tsx,json,css,md}\"",
    "test": "vitest",
    "test:coverage": "vitest --coverage",
    "check-types": "tsc --noEmit",
    "analyze": "npm run build && npx vite-bundle-analyzer dist"
  }
}
```

## ❗ 禁止和必须

### 禁止使用

- ❌ `var` 声明变量
- ❌ 复杂的相对路径 (`../../../`)
- ❌ 内联样式（特殊情况除外）
- ❌ 直接操作DOM
- ❌ 全局变量
- ❌ `console.log` 在生产代码中
- ❌ 未处理的Promise
- ❌ 魔法数字和字符串

### 必须使用

- ✅ TypeScript或PropTypes进行类型检查
- ✅ ESLint和Prettier代码检查
- ✅ 别名路径导入
- ✅ 错误边界处理
- ✅ Loading和Error状态
- ✅ 响应式设计
- ✅ 无障碍性支持
- ✅ 单元测试覆盖

---

遵循以上规范，确保ETF网格设计系统前端代码的高质量、高可维护性和优秀的用户体验。所有开发者都应严格按照此规范进行开发工作。
