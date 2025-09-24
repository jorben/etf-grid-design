/**
 * API服务修复版本
 * 修复与后端接口不匹配的问题
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
        throw new Error(errorData.error || errorData.message || `HTTP error! status: ${response.status}`);
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
   * 参数转换工具 - 前端参数转后端参数
   */
  transformAnalysisParams(frontendParams) {
    const {
      etfCode,
      totalCapital,
      gridType,
      riskPreference,
      ...otherParams
    } = frontendParams;

    // 风险偏好映射
    const riskMapping = {
      '保守': 'low',
      '稳健': 'medium', 
      '激进': 'high'
    };

    // 根据网格类型和资金量计算网格数量
    const calculateGridCount = (capital, gridType, risk) => {
      const baseCount = Math.floor(capital / 10000); // 每万元一个网格
      
      if (gridType === '等比') {
        return Math.min(Math.max(baseCount, 8), 20); // 等比网格8-20个
      } else {
        return Math.min(Math.max(baseCount, 10), 30); // 等差网格10-30个
      }
    };

    return {
      investment_amount: parseFloat(totalCapital) || 100000,
      risk_tolerance: riskMapping[riskPreference] || 'medium',
      grid_count: calculateGridCount(totalCapital, gridType, riskPreference),
      // 保留其他参数
      ...otherParams
    };
  }

  /**
   * ETF分析主接口 - 综合分析 (修复版)
   */
  async analyzeETF(parameters) {
    const { etfCode, ...frontendParams } = parameters;
    const backendParams = this.transformAnalysisParams(frontendParams);
    
    return this.post(`/analysis/comprehensive/${etfCode}`, backendParams);
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
   * 搜索ETF (修复参数名)
   */
  async searchETF(query) {
    return this.get('/etfs/search', { keyword: query }); // 修复: q -> keyword
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
   * 获取资金预设 (修复版)
   */
  async getCapitalPresets() {
    return this.get('/system/capital-presets');
  }

  /**
   * ETF适合性分析 (修复版)
   */
  async analyzeSuitability(etfCode, parameters) {
    const backendParams = this.transformAnalysisParams(parameters);
    return this.post(`/analysis/suitability/${etfCode}`, {
      investment_amount: backendParams.investment_amount,
      risk_tolerance: backendParams.risk_tolerance
    });
  }

  /**
   * ATR技术分析
   */
  async analyzeATR(etfCode, period = 20) {
    return this.get(`/analysis/atr/${etfCode}`, { period });
  }

  /**
   * 网格策略生成 (修复版)
   */
  async generateGridStrategy(etfCode, parameters) {
    const backendParams = this.transformAnalysisParams(parameters);
    return this.post(`/analysis/grid/${etfCode}`, {
      investment_amount: backendParams.investment_amount,
      grid_count: backendParams.grid_count,
      price_range_percent: 0.2 // 默认20%价格范围
    });
  }

  /**
   * 批量分析热门ETF (修复版)
   */
  async batchAnalyzePopular(parameters) {
    const backendParams = this.transformAnalysisParams(parameters);
    return this.post('/analysis/batch/popular', {
      investment_amount: backendParams.investment_amount,
      risk_tolerance: backendParams.risk_tolerance
    });
  }

  /**
   * ETF比较分析 (新增)
   */
  async compareETFs(etfCodes, parameters) {
    const backendParams = this.transformAnalysisParams(parameters);
    return this.post('/analysis/compare', {
      etf_codes: etfCodes,
      investment_amount: backendParams.investment_amount,
      risk_tolerance: backendParams.risk_tolerance
    });
  }

  /**
   * 获取投资建议 (新增)
   */
  async getInvestmentRecommendations(parameters) {
    const backendParams = this.transformAnalysisParams(parameters);
    return this.post('/analysis/recommendations', {
      investment_amount: backendParams.investment_amount,
      risk_tolerance: backendParams.risk_tolerance,
      investment_period: 'medium', // 默认中期投资
      preferred_categories: [] // 默认无偏好分类
    });
  }

  /**
   * 批量获取ETF最新数据 (新增)
   */
  async getBatchETFLatest(etfCodes) {
    return this.post('/etfs/batch/latest', {
      etf_codes: etfCodes
    });
  }

  /**
   * 获取ETF分类统计 (新增)
   */
  async getETFCategories() {
    return this.get('/etfs/categories');
  }

  /**
   * 获取市场概览 (新增)
   */
  async getMarketOverview() {
    return this.get('/analysis/market/overview');
  }
}

// 创建单例实例
const apiService = new ApiService();

// 导出修复后的方法
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
export const getCapitalPresets = () => apiService.getCapitalPresets();
export const analyzeSuitability = (etfCode, parameters) => apiService.analyzeSuitability(etfCode, parameters);
export const analyzeATR = (etfCode, period) => apiService.analyzeATR(etfCode, period);
export const generateGridStrategy = (etfCode, parameters) => apiService.generateGridStrategy(etfCode, parameters);
export const batchAnalyzePopular = (parameters) => apiService.batchAnalyzePopular(parameters);
export const compareETFs = (etfCodes, parameters) => apiService.compareETFs(etfCodes, parameters);
export const getInvestmentRecommendations = (parameters) => apiService.getInvestmentRecommendations(parameters);
export const getBatchETFLatest = (etfCodes) => apiService.getBatchETFLatest(etfCodes);
export const getETFCategories = () => apiService.getETFCategories();
export const getMarketOverview = () => apiService.getMarketOverview();

export default apiService;