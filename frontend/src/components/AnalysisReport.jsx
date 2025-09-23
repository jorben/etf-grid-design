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

  Download,
  Share2,
  Eye
} from 'lucide-react';
import SuitabilityCard from './report/SuitabilityCard';
import GridParametersCard from './report/GridParametersCard';
import BacktestResultCard from './report/BacktestResultCard';
import StrategyRationaleCard from './report/StrategyRationaleCard';

import LoadingSpinner from './LoadingSpinner';

const AnalysisReport = ({ data, loading, onBackToInput, onReAnalysis }) => {
  const [activeTab, setActiveTab] = useState('overview');

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
    { id: 'suitability', label: '适宜度评估', icon: <Target className="w-4 h-4" /> },
    { id: 'strategy', label: '网格策略', icon: <Grid3X3 className="w-4 h-4" /> },
    { id: 'backtest', label: '回测结果', icon: <BarChart3 className="w-4 h-4" /> },

  ];

  return (
    <div className="space-y-6">
      {/* 报告头部 */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-4">
            <button
              onClick={onBackToInput}
              className="px-4 py-2 text-gray-600 hover:text-gray-800 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              ← 返回设置
            </button>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                ETF网格交易策略分析报告
              </h1>
              <p className="text-gray-600">
                {etf_info?.code} {etf_info?.name} - {new Date().toLocaleDateString()}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button className="flex items-center gap-2 px-4 py-2 text-gray-600 hover:text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
              <Share2 className="w-4 h-4" />
              分享
            </button>
            <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
              <Download className="w-4 h-4" />
              导出PDF
            </button>
          </div>
        </div>

        {/* ETF基础信息 */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 p-4 bg-gray-50 rounded-lg">
          <div className="text-center">
            <div className="text-2xl font-bold text-gray-900">
              ¥{etf_info?.current_price?.toFixed(3)}
            </div>
            <div className={`text-sm ${etf_info?.change_pct >= 0 ? 'text-red-600' : 'text-green-600'}`}>
              {etf_info?.change_pct >= 0 ? '+' : ''}{etf_info?.change_pct?.toFixed(2)}%
            </div>
            <div className="text-xs text-gray-500">当前价格</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-semibold text-gray-900">
              {suitability_evaluation?.total_score || 0}/100
            </div>
            <div className={`text-sm px-2 py-1 rounded-full inline-flex items-center gap-1 ${getSuitabilityColor(suitability_evaluation?.total_score || 0)}`}>
              {getSuitabilityIcon(suitability_evaluation?.total_score || 0)}
              {suitability_evaluation?.conclusion || '未知'}
            </div>
            <div className="text-xs text-gray-500">适宜度评分</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-semibold text-gray-900">
              {grid_strategy?.grid_config?.count || 0}个
            </div>
            <div className="text-sm text-gray-600">
              {grid_strategy?.grid_config?.type || '未知'}网格
            </div>
            <div className="text-xs text-gray-500">网格配置</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-semibold text-gray-900">
              {backtest_result?.performance?.annual_return >= 0 ? '+' : ''}{((backtest_result?.performance?.annual_return || 0) * 100).toFixed(1)}%
            </div>
            <div className="text-sm text-gray-600">
              预期年化收益
            </div>
            <div className="text-xs text-gray-500">基于历史回测</div>
          </div>
        </div>
      </div>

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
              {/* 核心指标卡片 */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-gradient-to-r from-blue-50 to-blue-100 p-6 rounded-lg">
                  <div className="flex items-center gap-3 mb-3">
                    <div className="p-2 bg-blue-200 rounded-lg">
                      <Target className="w-5 h-5 text-blue-700" />
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
                      <DollarSign className="w-5 h-5 text-green-700" />
                    </div>
                    <h3 className="font-semibold text-green-900">预期收益</h3>
                  </div>
                  <div className="text-2xl font-bold text-green-900 mb-1">
                    {((backtest_result?.performance?.annual_return || 0) * 100).toFixed(1)}%
                  </div>
                  <p className="text-green-700 text-sm">
                    年化收益率（基于回测）
                  </p>
                </div>

                <div className="bg-gradient-to-r from-purple-50 to-purple-100 p-6 rounded-lg">
                  <div className="flex items-center gap-3 mb-3">
                    <div className="p-2 bg-purple-200 rounded-lg">
                      <Grid3X3 className="w-5 h-5 text-purple-700" />
                    </div>
                    <h3 className="font-semibold text-purple-900">网格配置</h3>
                  </div>
                  <div className="text-2xl font-bold text-purple-900 mb-1">
                    {grid_strategy?.grid_config?.count || 0}个
                  </div>
                  <p className="text-purple-700 text-sm">
                    {grid_strategy?.grid_config?.type || '未知'}网格，{grid_strategy?.frequency_preference || '未知'}
                  </p>
                </div>
              </div>

              {/* 快速摘要 */}
              <div className="bg-gray-50 p-6 rounded-lg">
                <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                  <Info className="w-5 h-5" />
                  策略摘要
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="font-medium text-gray-800 mb-2">投资配置</h4>
                    <ul className="space-y-1 text-sm text-gray-600">
                      <li>• 总投资资金：¥{(input_parameters?.total_capital || 0).toLocaleString()}</li>
                      <li>• 底仓资金：¥{(grid_strategy?.fund_allocation?.base_position_amount || 0).toLocaleString()}</li>
                      <li>• 网格资金：¥{(grid_strategy?.fund_allocation?.grid_trading_amount || 0).toLocaleString()}</li>
                      <li>• 资金利用率：{((grid_strategy?.fund_allocation?.utilization_rate || 0) * 100).toFixed(1)}%</li>
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-800 mb-2">策略特征</h4>
                    <ul className="space-y-1 text-sm text-gray-600">
                      <li>• 价格区间：¥{(grid_strategy?.price_range?.lower || 0).toFixed(3)} - ¥{(grid_strategy?.price_range?.upper || 0).toFixed(3)}</li>
                      <li>• 网格步长：¥{(grid_strategy?.grid_config?.step_size || 0).toFixed(3)} ({((grid_strategy?.grid_config?.step_ratio || 0) * 100).toFixed(2)}%)</li>
                      <li>• 预期月交易：{(backtest_result?.trading_stats?.expected_monthly_trades || 0).toFixed(1)}次</li>
                      <li>• 预期月收益：¥{(backtest_result?.trading_stats?.expected_monthly_profit || 0).toFixed(0)}</li>
                    </ul>
                  </div>
                </div>
              </div>

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
