// ETF代码与名称映射配置
export const etfNameMap = {
  // 沪深300相关
  510300: "沪深300ETF",
  159919: "沪深300ETF",

  // 中证500相关
  510500: "中证500ETF",

  // 创业板相关
  159915: "创业板ETF",

  // 上证50相关
  510050: "上证50ETF",

  // 深证100相关
  159901: "深证100ETF",

  // 中小板相关
  159902: "中小板ETF",

  // 红利指数相关
  510880: "红利ETF",

  // 消费行业相关
  159928: "消费ETF",

  // 恒生指数相关
  510900: "H股ETF",

  // 其他常见ETF
  512000: "券商ETF",
  512880: "证券ETF",
  515030: "新能源车ETF",
  515700: "新能车ETF",
  159949: "创业板50ETF",
  159995: "芯片ETF",
  512480: "半导体ETF",
  159870: "化工ETF",
  159825: "农业ETF",
  512690: "酒ETF",
  159992: "创新药ETF",
  512010: "医药ETF",
  159938: "医药卫生ETF",
  515050: "5GETF",
  159869: "人工智能ETF",
  516160: "新能源ETF",
  159790: "碳中和ETF",
  512660: "军工ETF",
  159967: "科技ETF",
  159845: "中证1000ETF",
  512100: "中证1000ETF",
  588000: "科创50ETF",
  588080: "科创板50ETF",
  159781: "沪深300增强ETF",
  510310: "HS300ETF",
  510330: "华夏300ETF",
  159742: "恒生ETF",
};

// 热门ETF列表（带名称）
export const popularETFsWithNames = [
  { code: "510300", name: "沪深300ETF" },
  { code: "510500", name: "中证500ETF" },
  { code: "159915", name: "创业板ETF" },
  { code: "588000", name: "科创50ETF" },
  { code: "159919", name: "沪深300ETF" },
  { code: "510050", name: "上证50ETF" },
  { code: "159901", name: "深证100ETF" },
  { code: "159902", name: "中小板ETF" },
  { code: "510880", name: "红利ETF" },
  { code: "159928", name: "消费ETF" },
  { code: "512000", name: "券商ETF" },
  { code: "512660", name: "军工ETF" },
  { code: "515030", name: "新能源车ETF" },
  { code: "159967", name: "科技ETF" },
  { code: "159742", name: "恒生ETF" },
];

// 根据ETF代码获取名称
export const getETFName = (code) => {
  return etfNameMap[code] || code;
};

// 异步获取ETF名称（优先使用后端API）
export const getETFNameAsync = async (code) => {
  // 首先检查本地映射表
  if (etfNameMap[code]) {
    return etfNameMap[code];
  }

  // 如果本地没有，尝试从后端API获取
  try {
    const { getETFName: getETFNameAPI } = await import("../services/api");
    const response = await getETFNameAPI(code);

    if (response.success && response.name !== code) {
      // 缓存到本地映射表中，避免重复请求
      etfNameMap[code] = response.name;
      return response.name;
    }
  } catch (error) {
    console.warn(`获取ETF ${code} 名称失败:`, error.message);
  }

  // 如果API调用失败，返回代码本身
  return code;
};

// 从带名称的字符串中提取ETF代码（数字编号）
export const extractETFCode = (input) => {
  // 如果输入是纯数字，直接返回
  if (/^\d{6}$/.test(input)) {
    return input;
  }

  // 如果输入包含ETF代码和名称，提取数字部分
  const match = input.match(/(\d{6})/);
  return match ? match[1] : input;
};
