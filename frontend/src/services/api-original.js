/**
 * API服务配置
 * 处理与后端的所有HTTP通信
 */

const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? '/api' 
  : 'http://localhost:5001/api/v1';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  /**
   * 通用请求方法
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
   * GET请求
   */
  async get(endpoint, params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const url = queryString ? `${endpoint}?${queryString}` : endpoint;
    
    return this.request(url, {
      method: 'GET',
    });
  }

  /**
   * POST请求
   */
  async post(endpoint, data = {}) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  /**
   * ETF分析主接口 - 综合分析
   */
  async analyzeETF(parameters) {
    const { etfCode, ...analysisParams } = parameters;
    return this.post(`/analysis/comprehensive/${etfCode}`, analysisParams);
  }

  /**
   * 获取ETF基础信息
   */
  async getETFInfo(etfCode) {
    return this.get(`/etfs/${etfCode}/basic`);
  }

  /**
   * 获取热门ETF列表
   */
  async getPopularETFs() {
    return this.get('/etfs/popular');
  }

  /**
   * 搜索ETF
   */
  async searchETF(query) {
    return this.get('/etfs/search', { q: query });
  }

  /**
   * 获取ETF历史数据
   */
  async getHistoricalData(etfCode, startDate, endDate) {
    return this.get(`/etfs/${etfCode}/historical`, {
      start_date: startDate,
      end_date: endDate
    });
  }

  /**
   * 获取ETF最新数据
   */
  async getLatestData(etfCode) {
    return this.get(`/etfs/${etfCode}/latest`);
  }

  /**
   * 健康检查
   */
  async healthCheck() {
    return this.get('/system/health');
  }

  /**
   * 获取系统信息
   */
  async getSystemInfo() {
    return this.get('/system/info');
  }

  /**
   * 获取缓存信息
   */
  async getCacheInfo() {
    return this.get('/system/cache/info');
  }

  /**
   * ETF适合性分析
   */
  async analyzeSuitability(etfCode, parameters) {
    return this.post(`/analysis/suitability/${etfCode}`, parameters);
  }

  /**
   * ATR技术分析
   */
  async analyzeATR(etfCode) {
    return this.get(`/analysis/atr/${etfCode}`);
  }

  /**
   * 网格策略生成
   */
  async generateGridStrategy(etfCode, parameters) {
    return this.post(`/analysis/grid/${etfCode}`, parameters);
  }

  /**
   * 批量分析热门ETF
   */
  async batchAnalyzePopular(parameters) {
    return this.post('/analysis/batch/popular', parameters);
  }
}

// 创建单例实例
const apiService = new ApiService();

// 导出常用方法
export const analyzeETF = (parameters) => apiService.analyzeETF(parameters);
export const getETFInfo = (etfCode) => apiService.getETFInfo(etfCode);
export const getPopularETFs = () => apiService.getPopularETFs();
export const searchETF = (query) => apiService.searchETF(query);
export const getHistoricalData = (etfCode, startDate, endDate) => 
  apiService.getHistoricalData(etfCode, startDate, endDate);
export const getLatestData = (etfCode) => apiService.getLatestData(etfCode);
export const healthCheck = () => apiService.healthCheck();
export const getSystemInfo = () => apiService.getSystemInfo();
export const getCacheInfo = () => apiService.getCacheInfo();
export const analyzeSuitability = (etfCode, parameters) => apiService.analyzeSuitability(etfCode, parameters);
export const analyzeATR = (etfCode) => apiService.analyzeATR(etfCode);
export const generateGridStrategy = (etfCode, parameters) => apiService.generateGridStrategy(etfCode, parameters);
export const batchAnalyzePopular = (parameters) => apiService.batchAnalyzePopular(parameters);

export default apiService;
