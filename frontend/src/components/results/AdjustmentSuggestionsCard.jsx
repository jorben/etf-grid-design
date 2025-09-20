import React, { useState } from 'react'
import { RefreshCw, TrendingUp, TrendingDown, AlertTriangle, CheckCircle, Info } from 'lucide-react'

const AdjustmentSuggestionsCard = ({ data }) => {
  const [activeTab, setActiveTab] = useState('volatility_increase')

  if (!data || data.error) {
    return (
      <div className="card border-danger-200 bg-danger-50">
        <div className="card-header">
          <h3 className="card-title">调整建议</h3>
        </div>
        <div className="text-danger-800">
          {data?.error || '无法获取调整建议'}
        </div>
      </div>
    )
  }

  const tabs = [
    {
      id: 'volatility_increase',
      label: '波动率上升',
      icon: TrendingUp,
      color: 'text-danger-600',
      bgColor: 'bg-danger-50'
    },
    {
      id: 'volatility_decrease',
      label: '波动率下降',
      icon: TrendingDown,
      color: 'text-primary-600',
      bgColor: 'bg-primary-50'
    },
    {
      id: 'trend_market',
      label: '趋势市场',
      icon: TrendingUp,
      color: 'text-warning-600',
      bgColor: 'bg-warning-50'
    }
  ]

  const TabContent = ({ tabData, title, color }) => {
    if (!tabData) return null

    return (
      <div className="space-y-6">
        {/* 情况描述 */}
        <div className={`p-4 rounded-lg border ${color.replace('text-', 'border-').replace('600', '200')} ${color.replace('text-', 'bg-').replace('600', '50')}`}>
          <div className="flex items-start space-x-3">
            <AlertTriangle className={`w-5 h-5 ${color} mt-0.5 flex-shrink-0`} />
            <div>
              <h4 className={`font-medium ${color} mb-2`}>{title}</h4>
              <p className={`text-sm ${color.replace('600', '700')}`}>
                {tabData.situation}
              </p>
            </div>
          </div>
        </div>

        {/* 调整建议 */}
        <div>
          <h4 className="font-medium mb-3 flex items-center">
            <RefreshCw className="w-4 h-4 mr-2" />
            调整建议
          </h4>
          <div className="space-y-3">
            {tabData.suggestions.map((suggestion, index) => (
              <div key={index} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                <div className="w-2 h-2 bg-gray-400 rounded-full mt-2 flex-shrink-0"></div>
                <div className="text-sm text-gray-700">{suggestion}</div>
              </div>
            ))}
          </div>
        </div>

        {/* 参数调整 */}
        {tabData.parameter_adjustments && Object.keys(tabData.parameter_adjustments).length > 0 && (
          <div>
            <h4 className="font-medium mb-3 flex items-center">
              <CheckCircle className="w-4 h-4 mr-2" />
              参数调整建议
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {Object.entries(tabData.parameter_adjustments).map(([param, adjustment], index) => (
                <div key={index} className="p-3 bg-white border border-gray-200 rounded-lg">
                  <div className="text-sm text-gray-600 mb-1">
                    {getParameterName(param)}
                  </div>
                  <div className="font-medium text-gray-900">{adjustment}</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    )
  }

  const getParameterName = (param) => {
    const names = {
      'price_range_ratio': '价格区间比例',
      'grid_count': '网格数量',
      'position_ratio': '仓位比例',
      'stop_loss': '止损设置',
      'profit_expectation': '收益预期',
      'grid_center': '网格中心',
      'risk_management': '风险管理'
    }
    return names[param] || param
  }

  return (
    <div className="card">
      <div className="card-header">
        <h3 className="card-title">动态调整建议</h3>
        <div className="text-sm text-gray-600">
          根据市场环境变化提供策略调整建议
        </div>
      </div>

      {/* 标签页导航 */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-4">
          {tabs.map(tab => {
            const Icon = tab.icon
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`
                  group inline-flex items-center py-3 px-4 border-b-2 font-medium text-sm
                  ${activeTab === tab.id
                    ? `border-primary-500 ${tab.color}`
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }
                `}
              >
                <Icon className={`
                  w-4 h-4 mr-2
                  ${activeTab === tab.id ? tab.color : 'text-gray-400 group-hover:text-gray-500'}
                `} />
                {tab.label}
              </button>
            )
          })}
        </nav>
      </div>

      {/* 标签内容 */}
      <div className="space-y-6">
        {activeTab === 'volatility_increase' && (
          <TabContent 
            tabData={data.volatility_increase} 
            title="波动率上升时的应对策略"
            color="text-danger-600"
          />
        )}

        {activeTab === 'volatility_decrease' && (
          <TabContent 
            tabData={data.volatility_decrease} 
            title="波动率下降时的应对策略"
            color="text-primary-600"
          />
        )}

        {activeTab === 'trend_market' && (
          <TabContent 
            tabData={data.trend_market} 
            title="趋势市场环境下的应对策略"
            color="text-warning-600"
          />
        )}
      </div>

      {/* 通用原则 */}
      <div className="mt-8 pt-6 border-t border-gray-200">
        <h4 className="font-medium mb-4 flex items-center">
          <Info className="w-4 h-4 mr-2" />
          通用交易原则
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {data.general_principles.map((principle, index) => (
            <div key={index} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
              <div className="w-2 h-2 bg-primary-400 rounded-full mt-2 flex-shrink-0"></div>
              <div className="text-sm text-gray-700">{principle}</div>
            </div>
          ))}
        </div>
      </div>

      {/* 风险提示 */}
      <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
        <div className="flex items-start space-x-3">
          <AlertTriangle className="w-5 h-5 text-yellow-600 mt-0.5 flex-shrink-0" />
          <div>
            <h4 className="text-sm font-medium text-yellow-800 mb-2">重要提醒</h4>
            <ul className="text-sm text-yellow-700 space-y-1">
              <li>• 以上建议基于历史数据分析，实际市场情况可能有所不同</li>
              <li>• 建议定期回顾和调整策略参数，适应市场变化</li>
              <li>• 任何投资策略都存在风险，请根据自身情况谨慎操作</li>
              <li>• 建议先进行小资金测试，验证策略有效性后再加大投入</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AdjustmentSuggestionsCard
