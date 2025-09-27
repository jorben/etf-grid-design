/**
 * 验证工具函数库
 * 提供统一的表单验证和业务规则验证功能
 */

/**
 * 验证ETF代码格式
 * @param {string} etfCode - ETF代码
 * @returns {boolean} 是否为有效的6位数字ETF代码
 *
 * @example
 * validateETFCode('510300') // true
 * validateETFCode('123') // false
 */
export const validateETFCode = (etfCode) => {
  return etfCode && /^\d{6}$/.test(etfCode);
};

/**
 * 验证投资金额
 * @param {number} amount - 投资金额
 * @returns {Object} 验证结果 { isValid: boolean, error: string }
 *
 * @example
 * validateCapital(100000) // { isValid: true, error: '' }
 * validateCapital(5000) // { isValid: false, error: '投资金额不能少于10万元' }
 */
export const validateCapital = (amount) => {
  if (!amount || isNaN(amount)) {
    return { isValid: false, error: "请输入有效的投资金额" };
  }

  if (amount < 10000) {
    return { isValid: false, error: "投资金额不能少于1万元" };
  }

  if (amount > 1000000) {
    return { isValid: false, error: "投资金额不能超过100万元" };
  }

  return { isValid: true, error: "" };
};

/**
 * 验证百分比值
 * @param {number} value - 百分比值（0-1之间的小数）
 * @param {Object} [options] - 验证选项
 * @param {number} [options.min=0] - 最小值
 * @param {number} [options.max=1] - 最大值
 * @returns {Object} 验证结果 { isValid: boolean, error: string }
 */
export const validatePercentage = (value, options = {}) => {
  const { min = 0, max = 1 } = options;

  if (typeof value !== "number" || isNaN(value)) {
    return { isValid: false, error: "请输入有效的百分比值" };
  }

  if (value < min) {
    return { isValid: false, error: `百分比值不能小于${min * 100}%` };
  }

  if (value > max) {
    return { isValid: false, error: `百分比值不能大于${max * 100}%` };
  }

  return { isValid: true, error: "" };
};

/**
 * 验证日期格式
 * @param {string} dateStr - 日期字符串
 * @param {string} [format='YYYY-MM-DD'] - 期望的日期格式
 * @returns {Object} 验证结果 { isValid: boolean, error: string }
 */
export const validateDate = (dateStr, format = "YYYY-MM-DD") => {
  if (!dateStr) {
    return { isValid: false, error: "请输入日期" };
  }

  // 验证 YYYY-MM-DD 格式
  if (format === "YYYY-MM-DD") {
    const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
    if (!dateRegex.test(dateStr)) {
      return { isValid: false, error: "日期格式应为 YYYY-MM-DD" };
    }

    const date = new Date(dateStr);
    if (isNaN(date.getTime())) {
      return { isValid: false, error: "请输入有效的日期" };
    }
  }

  // 验证 YYYYMMDD 格式
  if (format === "YYYYMMDD") {
    const dateRegex = /^\d{8}$/;
    if (!dateRegex.test(dateStr)) {
      return { isValid: false, error: "日期格式应为 YYYYMMDD" };
    }

    const year = parseInt(dateStr.substring(0, 4));
    const month = parseInt(dateStr.substring(4, 6)) - 1;
    const day = parseInt(dateStr.substring(6, 8));
    const date = new Date(year, month, day);

    if (
      date.getFullYear() !== year ||
      date.getMonth() !== month ||
      date.getDate() !== day
    ) {
      return { isValid: false, error: "请输入有效的日期" };
    }
  }

  return { isValid: true, error: "" };
};

/**
 * 验证必填字段
 * @param {any} value - 字段值
 * @param {string} fieldName - 字段名称
 * @returns {Object} 验证结果 { isValid: boolean, error: string }
 */
export const validateRequired = (value, fieldName) => {
  if (value === null || value === undefined || value === "") {
    return { isValid: false, error: `${fieldName}是必填项` };
  }

  return { isValid: true, error: "" };
};

/**
 * 验证数字范围
 * @param {number} value - 数字值
 * @param {Object} range - 范围配置
 * @param {number} range.min - 最小值
 * @param {number} range.max - 最大值
 * @param {string} fieldName - 字段名称
 * @returns {Object} 验证结果 { isValid: boolean, error: string }
 */
export const validateNumberRange = (value, { min, max }, fieldName) => {
  if (typeof value !== "number" || isNaN(value)) {
    return { isValid: false, error: `${fieldName}必须是有效的数字` };
  }

  if (value < min) {
    return { isValid: false, error: `${fieldName}不能小于${min}` };
  }

  if (value > max) {
    return { isValid: false, error: `${fieldName}不能大于${max}` };
  }

  return { isValid: true, error: "" };
};

/**
 * 验证表单数据
 * @param {Object} formData - 表单数据对象
 * @param {Object} validationRules - 验证规则对象
 * @returns {Object} 验证结果 { isValid: boolean, errors: Object }
 *
 * @example
 * const formData = { etfCode: '510300', totalCapital: 100000 };
 * const rules = {
 *   etfCode: [validateRequired, validateETFCode],
 *   totalCapital: [validateRequired, validateCapital]
 * };
 * validateForm(formData, rules);
 */
export const validateForm = (formData, validationRules) => {
  const errors = {};
  let isValid = true;

  for (const [fieldName, rules] of Object.entries(validationRules)) {
    const value = formData[fieldName];

    for (const rule of rules) {
      const result = typeof rule === "function" ? rule(value, fieldName) : rule;

      if (!result.isValid) {
        errors[fieldName] = result.error;
        isValid = false;
        break;
      }
    }
  }

  return { isValid, errors };
};
