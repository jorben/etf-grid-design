import React, { useState } from 'react';
import { 
  TrendingUp, 
  BarChart3, 
  Target, 
  AlertTriangle, 
  CheckCircle, 
  XCircle,
  Info,
  DollarSign,
  Calendar,
  Percent,
  Grid3X3,
  PieChart,
  Database,
  ThermometerSun,
  Eye,
  Share2
} from 'lucide-react';
import SuitabilityCard from './report/SuitabilityCard';
import GridParametersCard from './report/GridParametersCard';
import BacktestResultCard from './report/BacktestResultCard';
import StrategyRationaleCard from './report/StrategyRationaleCard';

import LoadingSpinner from './LoadingSpinner';

const AnalysisReport = ({ data, loading, onBackToInput, onReAnalysis, showShareButton = false }) => {
  const [activeTab, setActiveTab] = useState('overview');

  // 分享功能
  const handleShare = async () => {
    const shareData = {
      title: `${data?.etf_info?.name || 'ETF'} - 网格交易策略分析报告`,
      text: `查看 ${data?.etf_info?.name || 'ETF'} 的智能网格交易策略分析结果`,
      url: window.location.href,
    };

    // 优先使用Web Share API
    if (navigator.share && navigator.canShare && navigator.canShare(shareData)) {
      try {
        await navigator.share(shareData);
        return;
      } catch (error) {
        console.log('分享取消或失败，使用备用方案:', error);
      }
    }

    // 备用方案：复制链接到剪贴板
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(window.location.href);
        alert('分析报告链接已复制到剪贴板！');
      } else {
        // 更老的浏览器备用方案
        const textArea = document.createElement('textarea');
        textArea.value = window.location.href;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
          document.execCommand('copy');
          alert('分析报告链接已复制到剪贴板！');
        } catch (err) {
          console.error('复制失败:', err);
          prompt('请手动复制以下链接:', window.location.href);
        } finally {
          document.body.removeChild(textArea);
        }
      }
    } catch (error) {
      console.error('复制到剪贴板失败:', error);
      prompt('请手动复制以下链接:', window.location.href);
    }
  };


  // 显示加载状态
  if (loading) {
    return <LoadingSpinner message="正在分析ETF数据..." showProgress={true} progress={75} />;
  }

  // 显示错误状态
  if (data?.error) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-8 text-center">
        <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <XCircle className="w-8 h-8 text-red-600" />
        </div>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">分析失败</h3>
        <p className="text-gray-600 mb-6">{data.message}</p>
        <div className="flex justify-center gap-4">
          <button
            onClick={onBackToInput}
            className="px-6 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            返回设置
          </button>
          <button
            onClick={() => onReAnalysis && onReAnalysis()}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            重新分析
          </button>
        </div>
      </div>
    );
  }

  if (!data) return null;

  const {
    etf_info,
    data_quality,
    suitability_evaluation,
    grid_strategy,
    backtest_result,
    strategy_rationale,
    adjustment_suggestions,
    input_parameters
  } = data;

  // 数据完整性检查 - 更精确的检查逻辑
  const isDataComplete = () => {
    // 检查基础对象是否存在
    if (!suitability_evaluation || !grid_strategy || !backtest_result || !etf_info) {
      console.log('基础对象缺失:', {
        suitability_evaluation: !!suitability_evaluation,
        grid_strategy: !!grid_strategy,
        backtest_result: !!backtest_result,
        etf_info: !!etf_info
      });
      return false;
    }

    // 检查关键字段是否存在
    const dataObjects = {
      suitability_evaluation: suitability_evaluation,
      grid_strategy: grid_strategy,
      backtest_result: backtest_result,
      etf_info: etf_info
    };

    const requiredFields = {
      suitability_evaluation: ['total_score', 'conclusion'],
      grid_strategy: ['grid_config', 'fund_allocation'],
      backtest_result: ['performance'],
      etf_info: ['code', 'name', 'current_price']
    };

    for (const [objName, fields] of Object.entries(requiredFields)) {
      const obj = dataObjects[objName];
      for (const field of fields) {
        if (obj[field] === undefined || obj[field] === null) {
          console.log(`缺失字段: ${objName}.${field}`, obj[field]);
          return false;
        }
      }
    }

    return true;
  };

  if (!isDataComplete()) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-8 text-center">
        <div className="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <AlertTriangle className="w-8 h-8 text-yellow-600" />
        </div>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">数据不完整</h3>
        <p className="text-gray-600 mb-6">分析数据不完整，请重新分析</p>
        <div className="flex justify-center gap-4">
          <button
            onClick={onBackToInput}
            className="px-6 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            返回设置
          </button>
          <button
            onClick={() => onReAnalysis && onReAnalysis()}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            重新分析
          </button>
        </div>
      </div>
    );
  }

  // 获取适宜度等级颜色
  const getSuitabilityColor = (score) => {
    if (score >= 70) return 'text-green-600 bg-green-100';
    if (score >= 60) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  // 获取适宜度图标
  const getSuitabilityIcon = (score) => {
    if (score >= 70) return <CheckCircle className="w-5 h-5" />;
    if (score >= 60) return <AlertTriangle className="w-5 h-5" />;
    return <XCircle className="w-5 h-5" />;
  };

  const tabs = [
    { id: 'overview', label: '概览', icon: <Eye className="w-4 h-4" /> },
    { id: 'suitability', label: '适宜度评估', icon: <ThermometerSun className="w-4 h-4" /> },
    { id: 'strategy', label: '网格策略', icon: <Grid3X3 className="w-4 h-4" /> },
    { id: 'backtest', label: '回测结果', icon: <BarChart3 className="w-4 h-4" /> },

  ];

  return (
    <div className="space-y-6">

      {/* 标签页导航 */}
      <div className="bg-white rounded-xl shadow-lg">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            {tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 py-4 px-2 border-b-2 font-medium text-sm transition-colors ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.icon}
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        <div className="p-6">
          {/* 概览标签页 */}
          {activeTab === 'overview' && (
            <div className="space-y-6">
              {/* 风险提示 */}
              {suitability_evaluation?.has_fatal_flaw && (
                <div className="bg-red-50 border border-red-200 p-4 rounded-lg">
                  <div className="flex items-center gap-2 text-red-800 font-medium mb-2">
                    <AlertTriangle className="w-5 h-5" />
                    重要风险提示
                  </div>
                  <p className="text-red-700 text-sm">
                    该标的存在致命缺陷：{suitability_evaluation?.fatal_flaws?.join('、') || '未知风险'}，不建议进行网格交易。
                  </p>
                </div>
              )}
              
              {/* 核心指标卡片 */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="bg-gradient-to-r from-orange-50 to-orange-100 p-6 rounded-lg">
                  <div className="flex items-center gap-3 mb-3">
                    <div className="p-2 bg-orange-200 rounded-lg">
                      <Target className="w-5 h-5 text-orange-700" />
                    </div>
                    <h3 className="font-semibold text-orange-900">所选标的</h3>
                  </div>
                  <div className="text-2xl font-bold text-orange-900 mb-1">
                    {etf_info?.code || '未知'}
                  </div>
                  <p className="text-orange-700 text-sm">
                    {etf_info?.name || '未知标的'}
                  </p>
                </div>

                <div className="bg-gradient-to-r from-blue-50 to-blue-100 p-6 rounded-lg">
                  <div className="flex items-center gap-3 mb-3">
                    <div className="p-2 bg-blue-200 rounded-lg">
                      <ThermometerSun className="w-5 h-5 text-blue-700" />
                    </div>
                    <h3 className="font-semibold text-blue-900">适宜度评估</h3>
                  </div>
                  <div className="text-2xl font-bold text-blue-900 mb-1">
                    {suitability_evaluation?.total_score || 0}/100分
                  </div>
                  <p className="text-blue-700 text-sm">
                    {suitability_evaluation?.recommendation || '暂无评估'}
                  </p>
                </div>

                <div className="bg-gradient-to-r from-green-50 to-green-100 p-6 rounded-lg">
                  <div className="flex items-center gap-3 mb-3">
                    <div className="p-2 bg-green-200 rounded-lg">
                      <TrendingUp className="w-5 h-5 text-green-700" />
                    </div>
                    <h3 className="font-semibold text-green-900">网格价格区间</h3>
                  </div>
                  <div className="text-2xl font-bold text-green-900 mb-1">
                    ¥{(grid_strategy?.price_range?.lower || 0).toFixed(3)} - ¥{(grid_strategy?.price_range?.upper || 0).toFixed(3)}
                  </div>
                  <p className="text-green-700 text-sm">
                    网格交易价格范围
                  </p>
                </div>

                <div className="bg-gradient-to-r from-purple-50 to-purple-100 p-6 rounded-lg">
                  <div className="flex items-center gap-3 mb-3">
                    <div className="p-2 bg-purple-200 rounded-lg">
                      <BarChart3 className="w-5 h-5 text-purple-700" />
                    </div>
                    <h3 className="font-semibold text-purple-900">网格步长</h3>
                  </div>
                  {/* 根据网格类型动态展示重点 */}
                  {grid_strategy?.grid_config?.type === '等比' ? (
                    <>
                      <div className="text-2xl font-bold text-purple-900 mb-1">
                        {((grid_strategy?.grid_config?.step_ratio || 0) * 100).toFixed(2)}%
                      </div>
                      <p className="text-purple-700 text-sm">
                        步长比例 · ¥{(grid_strategy?.grid_config?.step_size || 0).toFixed(3)}
                      </p>
                    </>
                  ) : (
                    <>
                      <div className="text-2xl font-bold text-purple-900 mb-1">
                        ¥{(grid_strategy?.grid_config?.step_size || 0).toFixed(3)}
                      </div>
                      <p className="text-purple-700 text-sm">
                        步长价格 · {((grid_strategy?.grid_config?.step_ratio || 0) * 100).toFixed(2)}%
                      </p>
                    </>
                  )}
                </div>
              </div>

              {/* 数据质量评估 */}
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-2 bg-gray-200 rounded-lg">
                    <Database className="w-5 h-5 text-gray-700" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900">数据质量评估</h4>
                    <p className="text-sm text-gray-600">分析数据的时效性和完整性</p>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="bg-white p-4 rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <Calendar className="w-4 h-4 text-blue-600" />
                        <span className="font-medium text-gray-900">数据时效性</span>
                      </div>
                      <div className={`text-sm px-2 py-1 rounded-full ${
                        data_quality?.freshness === '优秀' ? 'bg-green-100 text-green-800' :
                        data_quality?.freshness === '良好' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {data_quality?.freshness || '未知'}
                      </div>
                    </div>
                    <p className="text-xs text-gray-600 mt-1">{data_quality?.freshness_desc || '暂无描述'}</p>
                    {data_quality?.latest_date && (
                      <p className="text-xs text-gray-500 mt-1">
                        最新数据: {data_quality.latest_date}
                      </p>
                    )}
                  </div>

                  <div className="bg-white p-4 rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <CheckCircle className="w-4 h-4 text-green-600" />
                        <span className="font-medium text-gray-900">数据完整性</span>
                      </div>
                      <div className={`text-sm px-2 py-1 rounded-full ${
                        data_quality?.completeness === '优秀' ? 'bg-green-100 text-green-800' :
                        data_quality?.completeness === '良好' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {data_quality?.completeness || '未知'}
                      </div>
                    </div>
                    <p className="text-xs text-gray-600 mt-1">{data_quality?.completeness_desc || '暂无描述'}</p>
                    {data_quality?.total_records && (
                      <p className="text-xs text-gray-500 mt-1">
                        数据记录: {data_quality.total_records}条
                      </p>
                    )}
                  </div>

                  <div className="bg-white p-4 rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <BarChart3 className="w-4 h-4 text-purple-600" />
                        <span className="font-medium text-gray-900">分析范围</span>
                      </div>
                      <div className="text-sm px-2 py-1 rounded-full bg-green-100 text-green-800">
                        {data_quality?.analysis_days || 0}天
                      </div>
                    </div>
                    <p className="text-xs text-gray-600 mt-1">历史数据分析期间</p>
                    {data_quality?.start_date && (
                      <p className="text-xs text-gray-500 mt-1">
                        {data_quality.start_date} 至 {data_quality.latest_date}
                      </p>
                    )}
                  </div>
                </div>
              </div>

              {/* 快速摘要 */}
              <div className="bg-blue-50 border border-blue-200 p-6 rounded-lg">
                <h3 className="font-semibold text-blue-900 mb-3 flex items-center gap-2">
                  <Info className="w-5 h-5" />
                  策略摘要
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="font-medium text-blue-800 mb-2">投资配置</h4>
                    <ul className="space-y-1 text-sm text-blue-600">
                      <li>• 总投资资金：¥{(input_parameters?.total_capital || 0).toLocaleString()}</li>
                      <li>• 底仓资金：¥{(grid_strategy?.fund_allocation?.base_position_amount || 0).toLocaleString()}</li>
                      <li>• 网格资金：¥{(grid_strategy?.fund_allocation?.grid_trading_amount || 0).toLocaleString()}</li>
                      <li>• 资金利用率：{((grid_strategy?.fund_allocation?.utilization_rate || 0) * 100).toFixed(1)}%</li>
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-medium text-blue-800 mb-2">策略特征</h4>
                    <ul className="space-y-1 text-sm text-blue-600">
                      <li>• 价格区间：¥{(grid_strategy?.price_range?.lower || 0).toFixed(3)} - ¥{(grid_strategy?.price_range?.upper || 0).toFixed(3)}</li>
                      <li>• 网格步长：¥{(grid_strategy?.grid_config?.step_size || 0).toFixed(3)} ({((grid_strategy?.grid_config?.step_ratio || 0) * 100).toFixed(2)}%)</li>
                      <li>• 预期月交易：{(backtest_result?.trading_stats?.expected_monthly_trades || 0).toFixed(1)}次</li>
                      <li>• 预期月收益：¥{(backtest_result?.trading_stats?.expected_monthly_profit || 0).toFixed(0)}</li>
                    </ul>
                  </div>
                </div>
              </div>

              
            </div>
          )}

          {/* 适宜度评估标签页 */}
          {activeTab === 'suitability' && (
            <SuitabilityCard 
              evaluation={suitability_evaluation}
              dataQuality={data_quality}
              showDetailed={true}
            />
          )}

          {/* 网格策略标签页 */}
          {activeTab === 'strategy' && (
            <GridParametersCard 
              gridStrategy={grid_strategy}
              inputParameters={input_parameters}
              showDetailed={true}
            />
          )}

          {/* 回测结果标签页 */}
          {activeTab === 'backtest' && (
            <BacktestResultCard 
              backtestResult={backtest_result}
              strategyRationale={strategy_rationale}
              adjustmentSuggestions={adjustment_suggestions}
              showDetailed={true}
            />
          )}


        </div>
      </div>



      {/* 免责声明 */}
      <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-lg">
        <div className="flex items-start gap-2">
          <AlertTriangle className="w-5 h-5 text-yellow-600 mt-0.5 flex-shrink-0" />
          <div className="text-sm text-yellow-800">
            <p className="font-medium mb-1">重要声明</p>
            <p>
              本分析基于历史数据和数学模型，仅供投资参考，不构成投资建议。
              实际投资效果可能与预测存在差异，投资有风险，入市需谨慎。
              请根据自身风险承受能力谨慎决策。
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalysisReport;
