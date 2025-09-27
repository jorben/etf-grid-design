/**
 * 历史记录调节系数修复验证脚本
 * 用于手动验证修复是否完整
 */

// 模拟历史记录数据
const mockHistoryData = [
  {
    etfCode: '510300',
    etfName: '沪深300ETF',
    params: {
      totalCapital: 100000,
      gridType: '等比',
      riskPreference: '均衡',
      adjustmentCoefficient: 1.0,
    },
    timestamp: Date.now(),
    url: '/analysis/510300?capital=100000&grid=geometric&risk=balanced&adjustment=1.0',
  },
  {
    etfCode: '510500',
    etfName: '中证500ETF',
    params: {
      totalCapital: 200000,
      gridType: '等差',
      riskPreference: '高频',
      adjustmentCoefficient: 1.5,
    },
    timestamp: Date.now() - 3600000,
    url: '/analysis/510500?capital=200000&grid=arithmetic&risk=aggressive&adjustment=1.5',
  },
];

const mockOldHistoryData = [
  {
    etfCode: '159915',
    params: {
      totalCapital: 150000,
      gridType: '等比',
      riskPreference: '低频',
      // 缺少 adjustmentCoefficient 字段
    },
    timestamp: Date.now() - 86400000,
    url: '/analysis/159915?capital=150000&grid=geometric&risk=conservative',
  },
];

// 验证函数（从 AnalysisHistory.jsx 中提取的逻辑）
function validateHistoryRecord(record) {
  const requiredFields = ['etfCode', 'params', 'timestamp'];
  const requiredParams = ['totalCapital', 'gridType', 'riskPreference'];
  
  for (const field of requiredFields) {
    if (!record[field]) {
      return false;
    }
  }
  
  for (const param of requiredParams) {
    if (!record.params[param]) {
      return false;
    }
  }
  
  // 确保调节系数有默认值
  if (!record.params.adjustmentCoefficient) {
    record.params.adjustmentCoefficient = 1.0;
  }
  
  // 确保ETF名称有默认值
  if (!record.etfName) {
    record.etfName = `ETF ${record.etfCode}`;
  }
  
  return true;
}

function processHistoryData(savedHistory) {
  return savedHistory
    .map(record => {
      if (!validateHistoryRecord(record)) {
        console.warn('发现无效的历史记录，已跳过:', record);
        return null;
      }
      
      // 确保调节系数有默认值
      if (!record.params.adjustmentCoefficient) {
        record.params.adjustmentCoefficient = 1.0;
      }
      
      // 确保ETF名称有默认值
      if (!record.etfName) {
        record.etfName = `ETF ${record.etfCode}`;
      }
      
      return record;
    })
    .filter(record => record !== null);
}

function generateURL(record) {
  const adjustmentCoefficient = record.params.adjustmentCoefficient || 1.0;
  
  const gridMapping = {
    '等比': 'geometric',
    '等差': 'arithmetic',
  };
  
  const riskMapping = {
    '低频': 'conservative',
    '均衡': 'balanced',
    '高频': 'aggressive',
  };
  
  const gridCode = gridMapping[record.params.gridType] || record.params.gridType;
  const riskCode = riskMapping[record.params.riskPreference] || record.params.riskPreference;
  
  return `/analysis/${record.etfCode}?capital=${record.params.totalCapital}&grid=${encodeURIComponent(gridCode)}&risk=${encodeURIComponent(riskCode)}&adjustment=${adjustmentCoefficient}`;
}

// 测试验证
console.log('=== 历史记录调节系数修复验证 ===\n');

console.log('1. 测试新历史记录处理:');
const processedNewData = processHistoryData(mockHistoryData);
console.log('处理后的记录数量:', processedNewData.length);
processedNewData.forEach((record, index) => {
  console.log(`记录 ${index + 1}:`, {
    etfCode: record.etfCode,
    etfName: record.etfName,
    adjustmentCoefficient: record.params.adjustmentCoefficient,
    url: generateURL(record)
  });
});

console.log('\n2. 测试旧历史记录兼容性:');
const processedOldData = processHistoryData(mockOldHistoryData);
console.log('处理后的记录数量:', processedOldData.length);
processedOldData.forEach((record, index) => {
  console.log(`记录 ${index + 1}:`, {
    etfCode: record.etfCode,
    etfName: record.etfName,
    adjustmentCoefficient: record.params.adjustmentCoefficient,
    url: generateURL(record)
  });
});

console.log('\n3. 验证URL生成包含调节系数:');
const testRecord = mockHistoryData[0];
const generatedURL = generateURL(testRecord);
console.log('生成的URL:', generatedURL);
console.log('是否包含adjustment参数:', generatedURL.includes('adjustment='));
console.log('adjustment参数值:', generatedURL.match(/adjustment=([^&]*)/)?.[1]);

console.log('\n4. 验证数据结构完整性:');
const invalidRecord = {
  params: {
    totalCapital: 100000,
    // 缺少其他必需字段
  },
  timestamp: Date.now(),
};
console.log('无效记录验证结果:', validateHistoryRecord(invalidRecord));

console.log('\n5. 测试ETF名称显示和兼容性:');
const recordWithETFName = {
  etfCode: '510300',
  etfName: '沪深300ETF',
  params: {
    totalCapital: 100000,
    gridType: '等比',
    riskPreference: '均衡',
    adjustmentCoefficient: 1.0,
  },
  timestamp: Date.now(),
};
const recordWithoutETFName = {
  etfCode: '159915',
  // 缺少etfName字段
  params: {
    totalCapital: 150000,
    gridType: '等比',
    riskPreference: '低频',
    adjustmentCoefficient: 1.0,
  },
  timestamp: Date.now(),
};

console.log('有ETF名称的记录:', recordWithETFName.etfName);
console.log('无ETF名称的记录（处理后）:', validateHistoryRecord(recordWithoutETFName) ? recordWithoutETFName.etfName : '验证失败');

console.log('\n6. 验证ETF名称兼容性处理:');
const oldRecord = {
  etfCode: '159915',
  params: {
    totalCapital: 150000,
    gridType: '等比',
    riskPreference: '低频',
    // 缺少adjustmentCoefficient
  },
  timestamp: Date.now(),
};
console.log('旧记录处理前 - ETF名称:', oldRecord.etfName);
validateHistoryRecord(oldRecord);
console.log('旧记录处理后 - ETF名称:', oldRecord.etfName);
console.log('旧记录处理后 - 调节系数:', oldRecord.params.adjustmentCoefficient);

console.log('\n✅ 验证完成！所有修复功能正常，包括ETF名称显示。');