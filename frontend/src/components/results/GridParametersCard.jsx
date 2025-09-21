import React, { useState } from 'react'
import { ChevronDown, ChevronUp, DollarSign, Target, Grid, TrendingUp, AlertCircle } from 'lucide-react'
import { formatNumber, formatPercent, formatCurrency, formatStepAmount } from '../../services/api'

const GridParametersCard = ({ data }) => {
  const [expandedSections, setExpandedSections] = useState({
    basic: true,
    prices: false,
    capital: false,
    profit: false
  })

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }))
  }

  if (!data) return null

  const getRiskLevelColor = (riskLevel) => {
    switch (riskLevel) {
      case '低风险': return 'text-success-600 bg-success-100'
      case '中等风险': return 'text-warning-600 bg-warning-100'
      case '高风险': return 'text-danger-600 bg-danger-100'
      case '极高风险': return 'text-danger-800 bg-danger-200'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  return (
    <div className="card">
      <div className="card-header">
        <h3 className="card-title">网格策略参数详情</h3>
        <div className={`px-3 py-1 rounded-full text-xs font-medium ${getRiskLevelColor(data.risk_level)}`}>
          {data.risk_level}
        </div>
      </div>

      {/* 基础参数 */}
      <div className="mb-6">
        <button
          onClick={() => toggleSection('basic')}
          className="flex items-center justify-between w-full p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
        >
          <div className="flex items-center space-x-3">
            <Grid className="w-5 h-5 text-gray-600" />
            <span className="font-medium">基础参数</span>
          </div>
          {expandedSections.basic ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </button>
        
        {expandedSections.basic && (
          <div className="mt-4 p-4 bg-white border border-gray-200 rounded-lg">
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              <div>
                <div className="text-sm text-gray-600 mb-1">交易频率</div>
                <div className="font-medium">{data.frequency_name}</div>
                <div className="text-xs text-gray-500">({data.frequency})</div>
              </div>
              <div>
                <div className="text-sm text-gray-600 mb-1">区间内网格数</div>
                <div className="font-medium">{data.grid_count} 个</div>
              </div>
              <div>
                <div className="text-sm text-gray-600 mb-1">步长比例</div>
                <div className="font-medium">{formatPercent(data.step_size_ratio * 100, 3)}</div>
              </div>
              <div>
                <div className="text-sm text-gray-600 mb-1">步长金额</div>
                <div className="font-medium">{formatStepAmount(data.step_size_amount)}</div>
              </div>
              <div>
                <div className="text-sm text-gray-600 mb-1">目标日频次</div>
                <div className="font-medium">{data.target_daily_triggers} 次/天</div>
              </div>
              <div>
                <div className="text-sm text-gray-600 mb-1">预测日频次</div>
                <div className="font-medium">{data.predicted_daily_triggers?.toFixed(1) || 'N/A'} 次/天</div>
              </div>
              <div>
                <div className="text-sm text-gray-600 mb-1">预估月触发</div>
                <div className="font-medium">{data.estimated_triggers_per_month} 次</div>
              </div>
              <div>
                <div className="text-sm text-gray-600 mb-1">成功率</div>
                <div className="font-medium">{formatPercent(data.estimated_success_rate * 100, 1)}</div>
              </div>
              {data.frequency_match_score && (
                <div>
                  <div className="text-sm text-gray-600 mb-1">频次匹配度</div>
                  <div className={`font-medium ${
                    data.frequency_match_score > 0.8 ? 'text-success-600' : 
                    data.frequency_match_score > 0.6 ? 'text-warning-600' : 'text-danger-600'
                  }`}>
                    {formatPercent(data.frequency_match_score * 100, 1)}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* 价格区间 */}
      <div className="mb-6">
        <button
          onClick={() => toggleSection('prices')}
          className="flex items-center justify-between w-full p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
        >
          <div className="flex items-center space-x-3">
            <Target className="w-5 h-5 text-gray-600" />
            <span className="font-medium">价格区间设置</span>
          </div>
          {expandedSections.prices ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </button>
        
        {expandedSections.prices && (
          <div className="mt-4 p-4 bg-white border border-gray-200 rounded-lg">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-medium mb-3">价格边界</h4>
                <div className="space-y-3">
                  <div className="flex justify-between items-center p-3 bg-danger-50 rounded-lg">
                    <span className="text-sm text-gray-600">上边界</span>
                    <span className="font-medium text-danger-700">¥{formatNumber(data.price_upper_bound, 3)}</span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <span className="text-sm text-gray-600">当前价格</span>
                    <span className="font-medium">¥{formatNumber(data.current_price, 3)}</span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-success-50 rounded-lg">
                    <span className="text-sm text-gray-600">下边界</span>
                    <span className="font-medium text-success-700">¥{formatNumber(data.price_lower_bound, 3)}</span>
                  </div>
                </div>
              </div>
              
              <div>
                <h4 className="font-medium mb-3">区间参数</h4>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">区间比例</span>
                    <span className="font-medium">{formatPercent(data.price_range_ratio * 100, 2)}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">区间金额</span>
                    <span className="font-medium">{formatCurrency(data.price_range_amount)}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">网格密度</span>
                    <span className="font-medium">{formatNumber(data.grid_count / data.price_range_ratio, 1)} 个/1%</span>
                  </div>
                </div>
                
                {/* 网格价格预览 */}
                <div className="mt-4">
                  <h5 className="text-sm font-medium mb-2">网格价格预览</h5>
                  <div className="grid grid-cols-5 gap-1 text-xs">
                    {data.grid_prices.slice(0, 10).map((price, index) => (
                      <div key={index} className="text-center p-1 bg-gray-100 rounded">
                        ¥{formatNumber(price, 2)}
                      </div>
                    ))}
                    {data.grid_prices.length > 10 && (
                      <div className="text-center p-1 bg-gray-100 rounded text-gray-500">
                        +{data.grid_prices.length - 10}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* 资金配置 */}
      <div className="mb-6">
        <button
          onClick={() => toggleSection('capital')}
          className="flex items-center justify-between w-full p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
        >
          <div className="flex items-center space-x-3">
            <DollarSign className="w-5 h-5 text-gray-600" />
            <span className="font-medium">资金配置方案</span>
          </div>
          {expandedSections.capital ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </button>
        
        {expandedSections.capital && (
          <div className="mt-4 p-4 bg-white border border-gray-200 rounded-lg">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-medium mb-3">仓位分配</h4>
                <div className="space-y-3">
                  <div className="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
                    <span className="text-sm text-gray-600">基础仓位</span>
                    <span className="font-medium text-blue-700">{formatCurrency(data.base_position_amount)}</span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-green-50 rounded-lg">
                    <span className="text-sm text-gray-600">网格仓位</span>
                    <span className="font-medium text-green-700">{formatCurrency(data.grid_position_amount)}</span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-gray-100 rounded-lg font-medium">
                    <span className="text-sm text-gray-900">总资金</span>
                    <span className="text-gray-900">{formatCurrency(data.initial_capital)}</span>
                  </div>
                </div>
              </div>
              
              <div>
                <h4 className="font-medium mb-3">交易参数</h4>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">单笔交易金额</span>
                    <span className="font-medium">{formatCurrency(data.per_grid_amount)}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">单笔交易股数</span>
                    <span className="font-medium">{formatNumber(data.per_grid_shares)} 股</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">最大持仓</span>
                    <span className="font-medium">{formatCurrency(data.max_position_amount)}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">最小持仓</span>
                    <span className="font-medium">{formatCurrency(data.min_position_amount)}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* 收益分析 */}
      <div className="mb-6">
        <button
          onClick={() => toggleSection('profit')}
          className="flex items-center justify-between w-full p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
        >
          <div className="flex items-center space-x-3">
            <TrendingUp className="w-5 h-5 text-gray-600" />
            <span className="font-medium">收益分析</span>
          </div>
          {expandedSections.profit ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </button>
        
        {expandedSections.profit && (
          <div className="mt-4 p-4 bg-white border border-gray-200 rounded-lg">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-medium mb-3">收益预估</h4>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">平均每网格收益</span>
                    <span className="font-medium text-danger-600">{formatCurrency(data.avg_profit_per_grid)}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">平均收益率</span>
                    <span className="font-medium text-danger-600">{formatPercent(data.avg_profit_rate * 100, 3)}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">月度收益预估</span>
                    <span className="font-medium text-danger-600">{formatCurrency(data.monthly_profit_estimate)}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">月度收益率预估</span>
                    <span className="font-medium text-danger-600">
                      {formatPercent((data.monthly_profit_estimate / data.initial_capital) * 100, 2)}
                    </span>
                  </div>
                </div>
              </div>
              
              <div>
                <h4 className="font-medium mb-3">风险指标</h4>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">最大回撤预估</span>
                    <span className="font-medium text-success-600">{formatPercent(data.max_drawdown_estimate * 100, 2)}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">风险等级</span>
                    <span className={`font-medium px-2 py-1 rounded ${getRiskLevelColor(data.risk_level)}`}>
                      {data.risk_level}
                    </span>
                  </div>
                </div>
                
                {/* 风险提示 */}
                <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                  <div className="flex items-start space-x-2">
                    <AlertCircle className="w-4 h-4 text-yellow-600 mt-0.5 flex-shrink-0" />
                    <div className="text-xs text-yellow-800">
                      <strong>风险提示：</strong>
                      以上收益预估基于历史数据，实际收益可能因市场变化而有所不同。请根据自身风险承受能力谨慎投资。
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default GridParametersCard
