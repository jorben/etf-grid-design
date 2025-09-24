/**
 * API端点配置
 * 集中管理所有API路径
 */

export const API_ENDPOINTS = {
  // ETF相关接口
  ETF: {
    POPULAR: '/etfs/popular',
    BASIC_INFO: (etfCode) => `/etfs/${etfCode}/basic`,
    LATEST_DATA: (etfCode) => `/etfs/${etfCode}/latest`,
    HISTORICAL_DATA: (etfCode) => `/etfs/${etfCode}/historical`,
    SEARCH: '/etfs/search'
  },
  
  // 分析相关接口
  ANALYSIS: {
    SUITABILITY: (etfCode) => `/analysis/suitability/${etfCode}`,
    ATR: (etfCode) => `/analysis/atr/${etfCode}`,
    GRID_STRATEGY: (etfCode) => `/analysis/grid/${etfCode}`,
    COMPREHENSIVE: (etfCode) => `/analysis/comprehensive/${etfCode}`,
    BATCH_POPULAR: '/analysis/batch/popular'
  },
  
  // 系统相关接口
  SYSTEM: {
    HEALTH: '/system/health',
    INFO: '/system/info',
    CACHE_INFO: '/system/cache/info',
    CAPITAL_PRESETS: '/system/capital-presets'
  }
};

// 旧版本兼容性映射
export const LEGACY_ENDPOINTS = {
  '/analyze': (etfCode) => API_ENDPOINTS.ANALYSIS.COMPREHENSIVE(etfCode),
  '/etf/info': (etfCode) => API_ENDPOINTS.ETF.BASIC_INFO(etfCode),
  '/etf/popular': API_ENDPOINTS.ETF.POPULAR,
  '/etf/validate': API_ENDPOINTS.ETF.SEARCH,
  '/etf/historical': (etfCode) => API_ENDPOINTS.ETF.HISTORICAL_DATA(etfCode),
  '/health': API_ENDPOINTS.SYSTEM.HEALTH,
  '/version': API_ENDPOINTS.SYSTEM.INFO,
  '/popular-etfs': API_ENDPOINTS.ETF.POPULAR,
  '/capital-presets': API_ENDPOINTS.SYSTEM.CAPITAL_PRESETS
};