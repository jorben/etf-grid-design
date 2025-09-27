import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { History, Clock, TrendingUp, ExternalLink, Trash2 } from "lucide-react";

const AnalysisHistory = ({ className = "" }) => {
  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);
  const navigate = useNavigate();

  // 加载分析历史
  useEffect(() => {
    loadAnalysisHistory();
  }, []);

  const loadAnalysisHistory = () => {
    try {
      const savedHistory = JSON.parse(
        localStorage.getItem("analysisHistory") || "[]",
      );
      
      // 处理兼容性：为旧历史记录设置默认值，并验证数据结构
      const processedHistory = savedHistory
        .map(record => {
          // 验证并补全记录结构
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
        .filter(record => record !== null); // 过滤掉无效记录
      
      setHistory(processedHistory);
    } catch (error) {
      console.error("加载分析历史失败:", error);
      setHistory([]);
    }
  };

  // 清除历史记录
  const clearHistory = () => {
    if (window.confirm("确定要清除所有分析历史记录吗？")) {
      localStorage.removeItem("analysisHistory");
      setHistory([]);
    }
  };

  // 删除单条记录
  const deleteHistoryItem = (index, event) => {
    event.stopPropagation();

    const newHistory = history.filter((_, i) => i !== index);
    setHistory(newHistory);
    localStorage.setItem("analysisHistory", JSON.stringify(newHistory));
  };

  // 验证历史记录数据结构完整性
  const validateHistoryRecord = (record) => {
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
  };

  // 跳转到分析页面
  const navigateToAnalysis = (record) => {
    const adjustmentCoefficient = record.params.adjustmentCoefficient || 1.0;
    const url = `/analysis/${record.etfCode}?capital=${record.params.totalCapital}&grid=${encodeURIComponent(getGridTypeCode(record.params.gridType))}&risk=${encodeURIComponent(getRiskCode(record.params.riskPreference))}&adjustment=${adjustmentCoefficient}`;
    navigate(url);
  };

  // 获取网格类型编码
  const getGridTypeCode = (gridType) => {
    const mapping = {
      等比: "geometric",
      等差: "arithmetic",
    };
    return mapping[gridType] || gridType;
  };

  // 获取频率偏好编码
  const getRiskCode = (risk) => {
    const mapping = {
      低频: "conservative",
      均衡: "balanced",
      高频: "aggressive",
    };
    return mapping[risk] || risk;
  };

  // 格式化时间
  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / (1000 * 60));
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (diffMins < 1) return "刚刚";
    if (diffMins < 60) return `${diffMins}分钟前`;
    if (diffHours < 24) return `${diffHours}小时前`;
    if (diffDays < 7) return `${diffDays}天前`;

    return date.toLocaleDateString("zh-CN", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  if (history.length === 0) {
    return null;
  }

  return (
    <div
      className={`bg-white rounded-xl shadow-sm border border-gray-200 ${className}`}
    >
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <button
            onClick={() => setShowHistory(!showHistory)}
            className="flex items-center gap-2 text-gray-700 hover:text-gray-900"
          >
            <History className="w-5 h-5" />
            <span className="font-medium">分析历史</span>
            <span className="text-sm text-gray-500">({history.length})</span>
          </button>

          {history.length > 0 && (
            <button
              onClick={clearHistory}
              className="flex items-center gap-1 px-2 py-1 text-xs text-gray-500 hover:text-red-600 transition-colors"
            >
              <Trash2 className="w-3 h-3" />
              清空
            </button>
          )}
        </div>
      </div>

      {showHistory && (
        <div className="p-4">
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {history.map((record, index) => (
              <div
                key={index}
                onClick={() => navigateToAnalysis(record)}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer transition-colors group"
              >
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <TrendingUp className="w-4 h-4 text-blue-600" />
                    <span className="font-medium text-gray-900">
                      {`${record.etfName} (${record.etfCode})` || `ETF ${record.etfCode}`}
                    </span>
                  </div>

                  <div className="text-sm text-gray-600">
                    <span>
                      资金: {record.params.totalCapital?.toLocaleString()}元
                    </span>
                    <span className="mx-2">•</span>
                    <span>{record.params.gridType}</span>
                    <span className="mx-2">•</span>
                    <span>{record.params.riskPreference}</span>
                    <span className="mx-2">•</span>
                    <span>调节: {record.params.adjustmentCoefficient || 1.0}</span>
                  </div>

                  <div className="flex items-center gap-1 mt-1 text-xs text-gray-500">
                    <Clock className="w-3 h-3" />
                    {formatTime(record.timestamp)}
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <ExternalLink className="w-4 h-4 text-gray-400 group-hover:text-blue-600 transition-colors" />
                  <button
                    onClick={(e) => deleteHistoryItem(index, e)}
                    className="p-1 text-gray-400 hover:text-red-600 transition-colors opacity-0 group-hover:opacity-100"
                  >
                    <Trash2 className="w-3 h-3" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default AnalysisHistory;
