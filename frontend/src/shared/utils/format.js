/**
 * 格式化工具函数库
 * 提供统一的金额、百分比、日期格式化功能
 */

/**
 * 格式化金额为中文货币格式
 * @param {number} amount - 金额数值
 * @param {Object} [options] - 格式化选项
 * @param {number} [options.minimumFractionDigits=0] - 最小小数位数
 * @param {number} [options.maximumFractionDigits=0] - 最大小数位数
 * @returns {string} 格式化后的金额字符串
 * @throws {Error} 当amount不是有效数字时
 *
 * @example
 * formatCurrency(100000) // '¥100,000'
 * formatCurrency(1234.567, { maximumFractionDigits: 2 }) // '¥1,234.57'
 */
export const formatCurrency = (amount, options = {}) => {
  if (typeof amount !== "number" || isNaN(amount)) {
    throw new Error("Amount must be a valid number");
  }

  return new Intl.NumberFormat("zh-CN", {
    style: "currency",
    currency: "CNY",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
    ...options,
  }).format(amount);
};

/**
 * 格式化百分比
 * @param {number} value - 小数值（如 0.1234）
 * @param {number} [digits=2] - 小数位数，默认2位
 * @returns {string} 格式化后的百分比字符串
 * @throws {Error} 当value不是有效数字时
 *
 * @example
 * formatPercent(0.1234) // '12.34%'
 * formatPercent(0.05, 1) // '5.0%'
 */
export const formatPercent = (value, digits = 2) => {
  if (typeof value !== "number" || isNaN(value)) {
    throw new Error("Value must be a valid number");
  }

  return (value * 100).toFixed(digits) + "%";
};

/**
 * 格式化日期
 * @param {string} dateStr - 日期字符串（支持YYYYMMDD和YYYY-MM-DD格式）
 * @returns {string|null} 格式化后的日期字符串，无效输入返回null
 *
 * @example
 * formatDate('20240315') // '2024-03-15'
 * formatDate('2024-03-15') // '2024-03-15'
 * formatDate('') // null
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
  if (dateStr.includes("-")) {
    return dateStr;
  }

  return null;
};

/**
 * 格式化数字为千分位分隔格式
 * @param {number} number - 要格式化的数字
 * @returns {string} 格式化后的字符串
 *
 * @example
 * formatNumber(1000000) // '1,000,000'
 * formatNumber(1234.56) // '1,234.56'
 */
export const formatNumber = (number) => {
  if (typeof number !== "number" || isNaN(number)) {
    return "0";
  }

  return new Intl.NumberFormat("zh-CN").format(number);
};

/**
 * 格式化大数字为简化表示（万/亿）
 * @param {number} number - 要格式化的数字
 * @returns {string} 简化表示
 *
 * @example
 * formatLargeNumber(10000) // '1万'
 * formatLargeNumber(100000000) // '1亿'
 */
export const formatLargeNumber = (number) => {
  if (typeof number !== "number" || isNaN(number)) {
    return "0";
  }

  if (number >= 100000000) {
    return (number / 100000000).toFixed(2) + "亿";
  } else if (number >= 10000) {
    return (number / 10000).toFixed(2) + "万";
  } else {
    return formatNumber(number);
  }
};
