import React, { useState } from 'react'
import { BarChart3, TrendingUp, Activity, DollarSign, BarChart, ChevronDown, ChevronUp } from 'lucide-react'
import { formatNumber, formatPercent } from '../../services/api'

const AnalysisCard = ({ data }) => {
  const [expandedSections, setExpandedSections] = useState({
    price: true,
    volatility: false,
    amplitude: false,
    trend: false,
    liquidity: false
  })

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }))
  }

  if (!data || data.error) {
    return (
      <div className="card border-danger-200 bg-danger-50">
        <div className="card-header">
          <h3 className="card-title">分析数据</h3>
        </div>
        <div className="text-danger-800">
          {data?.error || '无法获取分析数据'}
        </div>
      </div>
    )
  }

  const getVolatilityLevelColor = (level) => {
    switch (level) {
      case '低波动': return 'text-success-600 bg-success-100'
      case '中等波动': return 'text-primary-600 bg-primary-100'
      case '高波动': return 'text-warning-600 bg-warning-100'
      case '极高波动': return 'text-danger-600 bg-danger-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getAmplitudeLevelColor = (level) => {
    switch (level) {
      case '极小振幅': return 'text-gray-600 bg-gray-100'
      case '小振幅': return 'text-primary-600 bg-primary-100'
      case '中等振幅': return 'text-success-600 bg-success-100'
      case '大振幅': return 'text-warning-600 bg-warning-100'
      case '极大振幅': return 'text-danger-600 bg-danger-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getMarketCharacterColor = (character) => {
    switch (character) {
      case '震荡': return 'text-success-600 bg-success-100'
      case '弱趋势': return 'text-warning-600 bg-warning-100'
      case '强趋势': return 'text-danger-600 bg-danger-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  return (
    <div className="card">
      <div className="card-header">
        <h3 className="card-title">ETF特征分析</h3>
        <div className="text-sm text-gray-600">
          数据期间: {data.start_date || '2024-06-01'} 至 {data.end_date || '2024-08-30'} | 数据点数: {data.data_points}
        </div>
      </div>

      {/* 价格分析 */}
      <div className="mb-6">
        <button
          onClick={() => toggleSection('price')}
          className="flex items-center justify-between w-full p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
        >
          <div className="flex items-center space-x-3">
            <DollarSign className="w-5 h-5 text-gray-600" />
            <span className="font-medium">价格分析</span>
          </div>
          {expandedSections.price ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </button>
        
        {expandedSections.price && (
          <div className="mt-4 p-4 bg-white border border-gray-200 rounded-lg">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <div className="text-sm text-gray-600 mb-1">当前价格</div>
                <div className="font-medium text-lg">¥{formatNumber(data.current_price, 3)}</div>
              </div>
              <div>
                <div className="text-sm text-gray-600 mb-1">平均价格</div>
                <div className="font-medium">¥{formatNumber(data.avg_price, 3)}</div>
              </div>
              <div>
                <div className="text-sm text-gray-600 mb-1">价格标准差</div>
                <div className="font-medium">¥{formatNumber(data.price_std, 3)}</div>
              </div>
              <div>
                <div className="text-sm text-gray-600 mb-1">价格区间</div>
                <div className="font-medium">¥{formatNumber(data.price_range, 3)}</div>
              </div>
            </div>
            
            {/* 价格分布 */}
            {data.price_distribution && (
              <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                <h4 className="text-sm font-medium mb-2">价格分布特征</h4>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                  <div>
                    <span className="text-gray-600">25%分位:</span>
                    <span className="ml-1 font-medium">¥{formatNumber(data.price_distribution.q25, 3)}</span>
                  </div>
                  <div>
                    <span className="text-gray-600">中位数:</span>
                    <span className="ml-1 font-medium">¥{formatNumber(data.price_distribution.q50, 3)}</span>
                  </div>
                  <div>
                    <span className="text-gray-600">75%分位:</span>
                    <span className="ml-1 font-medium">¥{formatNumber(data.price_distribution.q75, 3)}</span>
                  </div>
                  <div>
                    <span className="text-gray-600">四分位距:</span>
                    <span className="ml-1 font-medium">¥{formatNumber(data.price_distribution.iqr, 3)}</span>
                  </div>
                </div>
                <div className="mt-2 text-xs text-gray-600">
                  分布类型: {data.price_distribution.distribution_type} | 
                  偏度: {formatNumber(data.price_distribution.skewness, 2)} | 
                  峰度: {formatNumber(data.price_distribution.kurtosis, 2)}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* 波动率分析 */}
      <div className="mb-6">
        <button
          onClick={() => toggleSection('volatility')}
          className="flex items-center justify-between w-full p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
        >
          <div className="flex items-center space-x-3">
            <BarChart3 className="w-5 h-5 text-gray-600" />
            <span className="font-medium">波动率分析</span>
          </div>
          {expandedSections.volatility ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </button>
        
        {expandedSections.volatility && (
          <div className="mt-4 p-4 bg-white border border-gray-200 rounded-lg">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <div className="text-sm text-gray-600 mb-1">年化波动率</div>
                <div className="font-medium text-lg">{formatPercent(data.volatility, 2)}</div>
                <div className={`inline-block px-2 py-1 rounded text-xs font-medium mt-1 ${getVolatilityLevelColor(data.volatility_level)}`}>
                  {data.volatility_level}
                </div>
              </div>
              <div>
                <div className="text-sm text-gray-600 mb-1">趋势斜率</div>
                <div className="font-medium">{formatNumber(data.trend_slope, 4)}</div>
              </div>
              <div>
                <div className="text-sm text-gray-600 mb-1">趋势方向</div>
                <div className="font-medium">{data.trend_direction}</div>
              </div>
            </div>
            
            <div className="mt-4 p-3 bg-gray-50 rounded-lg">
              <h4 className="text-sm font-medium mb-2">波动率解读</h4>
              <div className="text-sm text-gray-700">
                {data.volatility < 10 && "低波动率表明价格相对稳定，适合保守型网格策略。"}
                {data.volatility >= 10 && data.volatility < 25 && "中等波动率提供较好的网格交易机会，平衡了收益和风险。"}
                {data.volatility >= 25 && data.volatility < 40 && "高波动率意味着更多交易机会，但需要更严格的风险控制。"}
                {data.volatility >= 40 && "极高波动率风险较大，需要谨慎设置网格参数。"}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* 振幅分析 */}
      <div className="mb-6">
        <button
          onClick={() => toggleSection('amplitude')}
          className="flex items-center justify-between w-full p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
        >
          <div className="flex items-center space-x-3">
            <Activity className="w-5 h-5 text-gray-600" />
            <span className="font-medium">振幅分析</span>
          </div>
          {expandedSections.amplitude ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </button>
        
        {expandedSections.amplitude && (
          <div className="mt-4 p-4 bg-white border border-gray-200 rounded-lg">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <div className="text-sm text-gray-600 mb-1">平均振幅</div>
                <div className="font-medium text-lg">{formatPercent(data.avg_amplitude, 2)}</div>
                <div className={`inline-block px-2 py-1 rounded text-xs font-medium mt-1 ${getAmplitudeLevelColor(data.amplitude_level)}`}>
                  {data.amplitude_level}
                </div>
              </div>
              <div>
                <div className="text-sm text-gray-600 mb-1">最大振幅</div>
                <div className="font-medium">{formatPercent(data.max_amplitude, 2)}</div>
              </div>
              <div>
                <div className="text-sm text-gray-600 mb-1">最小振幅</div>
                <div className="font-medium">{formatPercent(data.min_amplitude, 2)}</div>
              </div>
              <div>
                <div className="text-sm text-gray-600 mb-1">振幅标准差</div>
                <div className="font-medium">{formatPercent(data.amplitude_std, 2)}</div>
              </div>
            </div>
            
            <div className="mt-4 p-3 bg-gray-50 rounded-lg">
              <h4 className="text-sm font-medium mb-2">振幅分析</h4>
              <div className="text-sm text-gray-700">
                {data.avg_amplitude < 1.0 && "振幅过小，可能难以覆盖交易成本，不适合网格交易。"}
                {data.avg_amplitude >= 1.0 && data.avg_amplitude < 1.5 && "振幅偏小，网格交易效果可能有限。"}
                {data.avg_amplitude >= 1.5 && data.avg_amplitude < 2.5 && "振幅适中，适合进行网格交易。"}
                {data.avg_amplitude >= 2.5 && data.avg_amplitude < 4.0 && "振幅较大，提供较好的网格交易机会。"}
                {data.avg_amplitude >= 4.0 && "振幅很大，交易机会多但风险也相应增加。"}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* 趋势与震荡分析 */}
      <div className="mb-6">
        <button
          onClick={() => toggleSection('trend')}
          className="flex items-center justify-between w-full p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
        >
          <div className="flex items-center space-x-3">
            <TrendingUp className="w-5 h-5 text-gray-600" />
            <span className="font-medium">市场特征</span>
          </div>
          {expandedSections.trend ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </button>
        
        {expandedSections.trend && (
          <div className="mt-4 p-4 bg-white border border-gray-200 rounded-lg">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <div className="text-sm text-gray-600 mb-1">震荡特征分数</div>
                <div className="font-medium text-lg">{formatNumber(data.oscillation_score * 100, 1)}%</div>
              </div>
              <div>
                <div className="text-sm text-gray-600 mb-1">市场特征</div>
                <div className="font-medium">{data.market_character}</div>
                <div className={`inline-block px-2 py-1 rounded text-xs font-medium mt-1 ${getMarketCharacterColor(data.market_character)}`}>
                  {data.market_character}
                </div>
              </div>
              <div>
                <div className="text-sm text-gray-600 mb-1">趋势方向</div>
                <div className="font-medium">{data.trend_direction}</div>
              </div>
            </div>
            
            <div className="mt-4 p-3 bg-gray-50 rounded-lg">
              <h4 className="text-sm font-medium mb-2">市场特征分析</h4>
              <div className="text-sm text-gray-700">
                {data.oscillation_score > 0.6 && "市场震荡特征明显，价格围绕均值波动，适合网格交易策略。"}
                {data.oscillation_score > 0.3 && data.oscillation_score <= 0.6 && "市场呈现弱趋势特征，存在一定的震荡但趋势性开始显现。"}
                {data.oscillation_score <= 0.3 && "市场趋势性较强，价格呈现明显的方向性运动，网格交易风险较大。"}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* 流动性分析 */}
      <div className="mb-6">
        <button
          onClick={() => toggleSection('liquidity')}
          className="flex items-center justify-between w-full p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
        >
          <div className="flex items-center space-x-3">
            <BarChart className="w-5 h-5 text-gray-600" />
            <span className="font-medium">流动性分析</span>
          </div>
          {expandedSections.liquidity ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </button>
        
        {expandedSections.liquidity && (
          <div className="mt-4 p-4 bg-white border border-gray-200 rounded-lg">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <div className="text-sm text-gray-600 mb-1">平均成交量</div>
                <div className="font-medium text-lg">{formatNumber(data.avg_volume)}</div>
              </div>
              <div>
                <div className="text-sm text-gray-600 mb-1">成交量标准差</div>
                <div className="font-medium">{formatNumber(data.volume_std)}</div>
              </div>
              <div>
                <div className="text-sm text-gray-600 mb-1">流动性分数</div>
                <div className="font-medium">{formatNumber(data.liquidity_score * 100, 1)}%</div>
              </div>
            </div>
            
            <div className="mt-4 p-3 bg-gray-50 rounded-lg">
              <h4 className="text-sm font-medium mb-2">流动性评估</h4>
              <div className="text-sm text-gray-700">
                {(() => {
                  if (data.liquidity_score >= 0.7 && data.avg_volume >= 1000000) {
                    return "流动性良好，成交量充足，适合大额网格交易。"
                  } else if (data.liquidity_score >= 0.5 && data.avg_volume >= 500000) {
                    return "流动性一般，需要注意交易冲击成本。"
                  } else {
                    return "流动性不足，可能存在交易风险和较大滑点。"
                  }
                })()}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default AnalysisCard
