# ETF网格设计项目前端重构 - Phase 01: 提取共享工具函数

## 改造背景

当前ETF网格设计项目前端代码存在严重的重复代码问题：
- 分享功能在 `AnalysisPage.jsx` 和 `AnalysisReport.jsx` 中重复实现
- 格式化函数（金额、百分比、日期）在多个组件中重复定义
- 验证逻辑分散在各个组件中
- 缺乏统一的工具函数库，导致维护困难

这些问题导致：
1. 代码维护成本高
2. 功能行为不一致
3. 新功能开发效率低
4. 测试覆盖困难

## 当前阶段

**Phase 01: 提取共享工具函数**
- 预计耗时：1-2天
- 风险等级：🟢 低风险
- 优先级：高

## 本次改造目标

1. **消除重复代码**：将重复的工具函数提取到共享模块
2. **统一格式化逻辑**：建立统一的数据格式化标准
3. **创建共享Hook**：将复用逻辑封装为自定义Hook
4. **建立工具函数库**：为后续开发提供基础设施
5. **保证功能完全一致**：重构过程中不改变任何业务行为

## 本次改造的详细计划

### Step 1: 创建共享目录结构
```bash
mkdir -p frontend/src/shared/utils
mkdir -p frontend/src/shared/hooks
mkdir -p frontend/src/shared/services
mkdir -p frontend/src/shared/constants
```

### Step 2: 提取格式化工具函数

#### 2.1 创建 `frontend/src/shared/utils/format.js`
```javascript
/**
 * 格式化金额为中文货币格式
 * @param {number} amount - 金额数值
 * @returns {string} 格式化后的金额字符串
 */
export const formatCurrency = (amount) => {
  return new Intl.NumberFormat('zh-CN', {
    style: 'currency',
    currency: 'CNY',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(amount);
};

/**
 * 格式化百分比
 * @param {number} value - 小数值（如 0.1234）
 * @param {number} digits - 小数位数，默认2位
 * @returns {string} 格式化后的百分比字符串
 */
export const formatPercent = (value, digits = 2) => {
  return (value * 100).toFixed(digits) + '%';
};

/**
 * 格式化日期
 * @param {string} dateStr - 日期字符串（支持YYYYMMDD和YYYY-MM-DD格式）
 * @returns {string|null} 格式化后的日期字符串
 */
export const formatDate = (dateStr) => {
  if (!dateStr) return null;
  
  // 处理 YYYYMMDD 格式
  if (dateStr.length === 8 && /^\d{8}$/.test(dateStr)) {
    const year = dateStr.substring(0, 4);
    const month = dateStr.substring(4, 6);
    const day = dateStr.substring(6, 8);
    return `${year}-${month}-${day}`;
  }
  
  // 处理 YYYY-MM-DD 格式
  if (dateStr.includes('-')) {
    return dateStr;
  }
  
  return null;
};
```

#### 2.2 创建 `frontend/src/shared/utils/validation.js`
```javascript
/**
 * 验证ETF代码格式
 * @param {string} etfCode - ETF代码
 * @returns {boolean} 是否为有效的6位数字ETF代码
 */
export const validateETFCode = (etfCode) => {
  return etfCode && /^\d{6}$/.test(etfCode);
};

/**
 * 验证投资金额
 * @param {number} amount - 投资金额
 * @returns {Object} 验证结果 { isValid: boolean, error: string }
 */
export const validateCapital = (amount) => {
  if (!amount || isNaN(amount)) {
    return { isValid: false, error: '请输入有效的投资金额' };
  }
  
  if (amount < 100000) {
    return { isValid: false, error: '投资金额不能少于10万元' };
  }
  
  if (amount > 5000000) {
    return { isValid: false, error: '投资金额不能超过500万元' };
  }
  
  return { isValid: true, error: '' };
};
```

### Step 3: 提取共享Hook

#### 3.1 创建 `frontend/src/shared/hooks/useShare.js`
```javascript
import { useCallback } from 'react';

/**
 * 分享功能Hook
 * @returns {Object} 包含shareContent方法的对象
 */
export const useShare = () => {
  const shareContent = useCallback(async (shareData) => {
    // 优先使用Web Share API
    if (navigator.share && navigator.canShare && navigator.canShare(shareData)) {
      try {
        await navigator.share(shareData);
        return { success: true, method: 'native' };
      } catch (error) {
        console.log('分享取消或失败，使用备用方案:', error);
      }
    }

    // 备用方案：复制链接到剪贴板
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(shareData.url || window.location.href);
        alert('分析链接已复制到剪贴板！');
        return { success: true, method: 'clipboard' };
      } else {
        // 更老的浏览器备用方案
        const textArea = document.createElement('textarea');
        textArea.value = shareData.url || window.location.href;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
          document.execCommand('copy');
          alert('分析链接已复制到剪贴板！');
          return { success: true, method: 'fallback' };
        } catch (err) {
          console.error('复制失败:', err);
          prompt('请手动复制以下链接:', shareData.url || window.location.href);
          return { success: false, method: 'manual' };
        } finally {
          document.body.removeChild(textArea);
        }
      }
    } catch (error) {
      console.error('复制到剪贴板失败:', error);
      prompt('请手动复制以下链接:', shareData.url || window.location.href);
      return { success: false, method: 'manual' };
    }
  }, []);
  
  return { shareContent };
};
```

### Step 4: 更新现有组件引用

#### 4.1 更新 `frontend/src/components/report/GridParametersCard.jsx`
```javascript
// 替换原有的格式化函数
import { formatCurrency, formatPercent, formatDate } from '../../../shared/utils/format';

// 删除组件内部的formatAmount、formatPercent、formatDate函数
// 将所有调用替换为导入的函数
```

#### 4.2 更新 `frontend/src/components/AnalysisPage.jsx`
```javascript
// 添加导入
import { useShare } from '../shared/hooks/useShare';

// 在组件内部
const { shareContent } = useShare();

// 替换handleShare函数
const handleShare = async () => {
  const shareData = {
    title: `${analysisData?.etf_info?.name || etfCode} - ETF网格交易策略分析`,
    text: `查看 ${analysisData?.etf_info?.name || etfCode} 的智能网格交易策略分析结果`,
    url: window.location.href,
  };
  
  await shareContent(shareData);
};
```

#### 4.3 更新 `frontend/src/components/AnalysisReport.jsx`
```javascript
// 添加导入
import { useShare } from '../shared/hooks/useShare';

// 在组件内部
const { shareContent } = useShare();

// 替换handleShare函数（与AnalysisPage相同逻辑）
```

#### 4.4 更新 `frontend/src/components/ParameterForm.jsx`
```javascript
// 添加导入
import { validateETFCode, validateCapital } from '../shared/utils/validation';

// 替换validateForm函数中的验证逻辑
const validateForm = () => {
  const newErrors = {};

  if (!validateETFCode(etfCode)) {
    newErrors.etfCode = '请输入6位数字ETF代码';
  }

  const capitalValidation = validateCapital(parseFloat(totalCapital));
  if (!capitalValidation.isValid) {
    newErrors.totalCapital = capitalValidation.error;
  }

  setErrors(newErrors);
  return Object.keys(newErrors).length === 0;
};
```

### Step 5: 创建单元测试

#### 5.1 创建 `frontend/src/shared/utils/__tests__/format.test.js`
```javascript
import { formatCurrency, formatPercent, formatDate } from '../format';

describe('format utils', () => {
  test('formatCurrency should format numbers correctly', () => {
    expect(formatCurrency(100000)).toBe('¥100,000');
    expect(formatCurrency(1234567)).toBe('¥1,234,567');
  });

  test('formatPercent should format decimals correctly', () => {
    expect(formatPercent(0.1234)).toBe('12.34%');
    expect(formatPercent(0.05, 1)).toBe('5.0%');
  });

  test('formatDate should handle different formats', () => {
    expect(formatDate('20240315')).toBe('2024-03-15');
    expect(formatDate('2024-03-15')).toBe('2024-03-15');
    expect(formatDate('')).toBe(null);
  });
});
```

## 执行约束

### 功能约束
1. **零业务影响**：重构过程中不得改变任何现有业务功能
2. **完全向后兼容**：所有现有组件的行为必须保持一致
3. **渐进式迁移**：逐个组件迁移，确保每步都可回滚

### 代码质量约束
1. **函数纯度**：所有提取的工具函数必须是纯函数
2. **TypeScript支持**：如果项目使用TypeScript，需要添加完整类型定义
3. **单元测试覆盖**：新增的工具函数必须有对应的单元测试
4. **文档完整**：所有导出函数必须有完整的JSDoc注释

### 性能约束
1. **无性能退化**：重构后的代码性能不得低于原有代码
2. **包大小控制**：新增代码不得显著增加打包体积
3. **懒加载友好**：工具函数应支持tree-shaking

### 测试约束
1. **回归测试**：每个修改的组件都需要进行完整的功能测试
2. **浏览器兼容**：确保在主要浏览器中功能正常
3. **移动端测试**：验证移动端分享功能正常工作

### 提交约束
1. **原子性提交**：每个功能点独立提交，便于问题定位
2. **详细提交信息**：包含修改原因、影响范围、测试结果
3. **代码审查**：所有修改需要通过代码审查

## 验收标准

### 功能验收
- [ ] 所有页面正常加载和显示
- [ ] 分享功能在各个组件中行为一致
- [ ] 格式化显示效果与原有完全一致
- [ ] 表单验证逻辑正常工作

### 代码质量验收
- [ ] 消除所有重复的格式化函数
- [ ] 分享功能只有一个实现版本
- [ ] 新增工具函数有完整测试覆盖
- [ ] 所有组件成功迁移到新的工具函数


完成本阶段后，项目将拥有统一的工具函数库，为后续的组件拆分和架构优化奠定基础。