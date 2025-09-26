/**
 * URL参数管理工具
 * 处理分析页面的URL参数编码、解码和验证
 */

// 参数映射表 - 中文到英文的映射
export const PARAM_MAPPINGS = {
  gridType: {
    '等比': 'geometric',
    '等差': 'arithmetic'
  },
  riskPreference: {
    '保守': 'conservative',
    '稳健': 'balanced', 
    '激进': 'aggressive'
  }
};

// 反向映射表 - 英文到中文的映射
export const REVERSE_PARAM_MAPPINGS = {
  gridType: {
    'geometric': '等比',
    'arithmetic': '等差'
  },
  riskPreference: {
    'conservative': '保守',
    'balanced': '稳健',
    'aggressive': '激进'
  }
};

// 默认参数值
export const DEFAULT_PARAMS = {
  capital: '100000',
  grid: 'geometric', // 对应"等比"
  risk: 'balanced'   // 对应"稳健"
};

/**
 * 将分析参数编码为URL查询参数
 * @param {Object} params - 分析参数对象
 * @returns {URLSearchParams} URL查询参数对象
 */
export const encodeAnalysisParams = (params) => {
  const searchParams = new URLSearchParams();
  
  // 资金参数
  if (params.totalCapital) {
    searchParams.set('capital', params.totalCapital.toString());
  }
  
  // 网格类型参数
  if (params.gridType) {
    const encodedGrid = PARAM_MAPPINGS.gridType[params.gridType] || params.gridType;
    searchParams.set('grid', encodedGrid);
  }
  
  // 风险偏好参数
  if (params.riskPreference) {
    const encodedRisk = PARAM_MAPPINGS.riskPreference[params.riskPreference] || params.riskPreference;
    searchParams.set('risk', encodedRisk);
  }
  
  return searchParams;
};

/**
 * 从URL查询参数解码分析参数
 * @param {URLSearchParams} searchParams - URL查询参数对象
 * @returns {Object} 解码后的分析参数对象
 */
export const decodeAnalysisParams = (searchParams) => {
  const params = {};
  
  // 解析资金参数
  const capital = searchParams.get('capital');
  if (capital) {
    const capitalNum = parseFloat(capital);
    if (!isNaN(capitalNum) && capitalNum >= 100000 && capitalNum <= 5000000) {
      params.totalCapital = capitalNum;
    }
  }
  
  // 解析网格类型参数
  const grid = searchParams.get('grid');
  if (grid) {
    params.gridType = REVERSE_PARAM_MAPPINGS.gridType[grid] || grid;
  }
  
  // 解析风险偏好参数
  const risk = searchParams.get('risk');
  if (risk) {
    params.riskPreference = REVERSE_PARAM_MAPPINGS.riskPreference[risk] || risk;
  }
  
  return params;
};

/**
 * 验证ETF代码格式
 * @param {string} etfCode - ETF代码
 * @returns {boolean} 是否有效
 */
export const validateETFCode = (etfCode) => {
  return etfCode && /^\d{6}$/.test(etfCode);
};

/**
 * 验证分析参数完整性
 * @param {Object} params - 分析参数对象
 * @returns {Object} 验证结果和补全后的参数
 */
export const validateAndCompleteParams = (params) => {
  const result = {
    isValid: true,
    errors: [],
    params: { ...params }
  };
  
  // 验证并补全资金参数
  if (!params.totalCapital) {
    result.params.totalCapital = parseFloat(DEFAULT_PARAMS.capital);
  } else {
    const capital = parseFloat(params.totalCapital);
    if (isNaN(capital) || capital < 100000 || capital > 5000000) {
      result.errors.push('投资金额应在10万-500万之间');
      result.params.totalCapital = parseFloat(DEFAULT_PARAMS.capital);
    }
  }
  
  // 验证并补全网格类型参数
  if (!params.gridType) {
    result.params.gridType = REVERSE_PARAM_MAPPINGS.gridType[DEFAULT_PARAMS.grid];
  } else if (!['等比', '等差'].includes(params.gridType)) {
    result.errors.push('网格类型参数无效');
    result.params.gridType = REVERSE_PARAM_MAPPINGS.gridType[DEFAULT_PARAMS.grid];
  }
  
  // 验证并补全风险偏好参数
  if (!params.riskPreference) {
    result.params.riskPreference = REVERSE_PARAM_MAPPINGS.riskPreference[DEFAULT_PARAMS.risk];
  } else if (!['保守', '稳健', '激进'].includes(params.riskPreference)) {
    result.errors.push('风险偏好参数无效');
    result.params.riskPreference = REVERSE_PARAM_MAPPINGS.riskPreference[DEFAULT_PARAMS.risk];
  }
  
  return result;
};

/**
 * 生成分析页面URL
 * @param {string} etfCode - ETF代码
 * @param {Object} params - 分析参数
 * @returns {string} 完整的分析页面URL
 */
export const generateAnalysisURL = (etfCode, params) => {
  const searchParams = encodeAnalysisParams(params);
  const baseUrl = `${window.location.origin}/analysis/${etfCode}`;
  return `${baseUrl}?${searchParams.toString()}`;
};

/**
 * 解析当前URL获取分析参数
 * @param {string} pathname - 路径名
 * @param {string} search - 查询字符串
 * @returns {Object} 解析结果
 */
export const parseAnalysisURL = (pathname, search) => {
  const result = {
    etfCode: null,
    params: {},
    isValid: false
  };
  
  // 解析ETF代码
  const pathMatch = pathname.match(/^\/analysis\/(\d{6})$/);
  if (pathMatch) {
    result.etfCode = pathMatch[1];
  }
  
  // 解析查询参数
  const searchParams = new URLSearchParams(search);
  result.params = decodeAnalysisParams(searchParams);
  
  // 验证ETF代码
  if (validateETFCode(result.etfCode)) {
    result.isValid = true;
  }
  
  return result;
};