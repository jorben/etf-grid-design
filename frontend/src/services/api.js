import axios from 'axios'

const API_BASE_URL = import.meta.env.PROD ? '/api' : 'http://localhost:5001/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30秒超时
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method.toUpperCase(), config.url, config.data)
    return config
  },
  (error) => {
    console.error('API Request Error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.data)
    return response
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message)
    
    let errorMessage = '请求失败'
    
    if (error.response) {
      // 服务器响应错误
      const { status, data } = error.response
      
      switch (status) {
        case 400:
          errorMessage = data.error || '请求参数错误'
          break
        case 404:
          errorMessage = data.error || '请求的资源不存在'
          break
        case 500:
          errorMessage = data.error || '服务器内部错误'
          break
        default:
          errorMessage = data.error || `请求失败 (状态码: ${status})`
      }
    } else if (error.request) {
      // 请求发送失败
      errorMessage = '无法连接到服务器，请检查网络连接'
    } else {
      // 其他错误
      errorMessage = error.message || '请求配置错误'
    }
    
    // 创建自定义错误对象
    const customError = new Error(errorMessage)
    customError.originalError = error
    customError.status = error.response?.status
    
    return Promise.reject(customError)
  }
)

/**
 * 分析ETF并生成网格策略参数
 * @param {Object} params - 分析参数
 * @param {string} params.etf_code - ETF代码
 * @param {string} params.frequency - 交易频率 (high/medium/low)
 * @param {number} params.initial_capital - 初始资金
 * @returns {Promise<Object>} 分析结果
 */
export const analyzeETF = async (params) => {
  try {
    const response = await api.post('/etf/analyze', params)
    return response.data
  } catch (error) {
    throw error
  }
}

/**
 * 搜索ETF
 * @param {string} query - 搜索关键词
 * @returns {Promise<Object>} ETF列表
 */
export const searchETF = async (query) => {
  try {
    const response = await api.get('/etf/search', {
      params: { query }
    })
    return response.data
  } catch (error) {
    throw error
  }
}

/**
 * 健康检查
 * @returns {Promise<Object>} 健康状态
 */
export const healthCheck = async () => {
  try {
    const response = await api.get('/health')
    return response.data
  } catch (error) {
    throw error
  }
}

// 导出API基础配置
export const API_CONFIG = {
  BASE_URL: API_BASE_URL,
  TIMEOUT: 30000,
  MAX_RETRIES: 3,
  RETRY_DELAY: 1000,
}

/**
 * 带重试机制的API调用
 * @param {Function} apiCall - API调用函数
 * @param {number} maxRetries - 最大重试次数
 * @param {number} retryDelay - 重试延迟（毫秒）
 * @returns {Promise<any>} API响应数据
 */
export const apiCallWithRetry = async (apiCall, maxRetries = API_CONFIG.MAX_RETRIES, retryDelay = API_CONFIG.RETRY_DELAY) => {
  let lastError
  
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await apiCall()
    } catch (error) {
      lastError = error
      
      // 如果是客户端错误（4xx），不重试
      if (error.status && error.status >= 400 && error.status < 500) {
        throw error
      }
      
      // 如果是最后一次尝试，抛出错误
      if (attempt === maxRetries) {
        throw new Error(`请求失败，已重试${maxRetries}次: ${error.message}`)
      }
      
      // 等待后重试
      console.log(`API调用失败，${retryDelay}ms后重试 (尝试 ${attempt + 1}/${maxRetries})`)
      await new Promise(resolve => setTimeout(resolve, retryDelay * (attempt + 1)))
    }
  }
  
  throw lastError
}

/**
 * 格式化数字
 * @param {number} num - 数字
 * @param {number} decimals - 小数位数
 * @returns {string} 格式化后的数字
 */
export const formatNumber = (num, decimals = 2) => {
  if (num === null || num === undefined) return '-'
  return Number(num).toFixed(decimals)
}

/**
 * 格式化百分比
 * @param {number} num - 数字
 * @param {number} decimals - 小数位数
 * @returns {string} 格式化后的百分比
 */
export const formatPercent = (num, decimals = 2) => {
  if (num === null || num === undefined) return '-'
  return `${Number(num).toFixed(decimals)}%`
}

/**
 * 格式化货币
 * @param {number} num - 数字
 * @returns {string} 格式化后的货币
 */
export const formatCurrency = (num) => {
  if (num === null || num === undefined) return '-'
  return `¥${Number(num).toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
}

/**
 * 格式化步长金额（保留3位小数）
 * @param {number} num - 数字
 * @returns {string} 格式化后的货币
 */
export const formatStepAmount = (num) => {
  if (num === null || num === undefined) return '-'
  return `¥${Number(num).toLocaleString('zh-CN', { minimumFractionDigits: 3, maximumFractionDigits: 3 })}`
}

/**
 * 格式化日期
 * @param {string} dateString - 日期字符串
 * @returns {string} 格式化后的日期
 */
export const formatDate = (dateString) => {
  if (!dateString) return '-'
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return dateString
  }
}

/**
 * 获取价格变化颜色类
 * @param {number} change - 变化值
 * @returns {string} 颜色类名
 */
export const getPriceChangeClass = (change) => {
  if (change > 0) return 'price-up'
  if (change < 0) return 'price-down'
  return 'price-neutral'
}

/**
 * 获取适应性状态类
 * @param {boolean} isSuitable - 是否适合
 * @returns {string} 状态类名
 */
export const getAdaptabilityClass = (isSuitable) => {
  return isSuitable ? 'status-success' : 'status-danger'
}

export default api
