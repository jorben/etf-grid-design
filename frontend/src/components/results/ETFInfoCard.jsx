import React from 'react'
import { TrendingUp, TrendingDown, Minus, Calendar, DollarSign, BarChart3, Clock } from 'lucide-react'
import { formatNumber, formatPercent, getPriceChangeClass } from '../../services/api'
import { getETFName } from '../../config/etfNames'

const ETFInfoCard = ({ data }) => {
  if (!data) return null

  const getPriceIcon = (change) => {
    if (change > 0) return <TrendingUp className="w-4 h-4" />
    if (change < 0) return <TrendingDown className="w-4 h-4" />
    return <Minus className="w-4 h-4" />
  }

  const getPriceColor = (change) => {
    if (change > 0) return 'text-danger-600'
    if (change < 0) return 'text-success-600'
    return 'text-gray-600'
  }

  const getDataFreshnessColor = (days) => {
    if (days <= 1) return 'text-success-600'
    if (days <= 3) return 'text-warning-600'
    return 'text-danger-600'
  }

  const getDataFreshnessText = (days) => {
    if (days <= 1) return '最新'
    if (days <= 3) return '较新'
    return days <= 7 ? '一周前' : '较旧'
  }

  return (
    <div className="card">
      <div className="card-header">
        <h3 className="card-title">ETF基本信息</h3>
        <div className={`flex items-center space-x-1 ${getPriceColor(data.pct_change)}`}>
          {getPriceIcon(data.pct_change)}
          <span className="font-medium">
            {formatPercent(data.pct_change)}
          </span>
        </div>
      </div>

      <div className="space-y-4">
        {/* 基本信息 - 四个模块同行展示 */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="text-center sm:text-left">
            <div className="text-sm text-gray-600 mb-1">代码</div>
            <div className="font-medium text-gray-900">{data.code}</div>
          </div>
          <div className="text-center sm:text-left">
            <div className="text-sm text-gray-600 mb-1">名称</div>
            <div className="font-medium text-gray-900 truncate" title={getETFName(data.code) || data.name}>
              {getETFName(data.code) || data.name}
            </div>
          </div>
          <div className="text-center sm:text-left">
            <div className="text-sm text-gray-600 mb-1">成立日期</div>
            <div className="text-sm text-gray-900">{data.found_date}</div>
          </div>
          <div className="text-center sm:text-left">
            <div className="text-sm text-gray-600 mb-1">管理人</div>
            <div className="text-sm text-gray-900 truncate" title={data.management}>
              {data.management}
            </div>
          </div>
        </div>

        {/* 价格信息 */}
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center space-x-2">
              <DollarSign className="w-5 h-5 text-gray-600" />
              <span className="font-medium">当前价格</span>
            </div>
            <div className="flex items-center space-x-2">
              <Clock className="w-4 h-4 text-gray-400" />
              <div className={`text-sm ${getDataFreshnessColor(data.data_age_days)}`}>
                {getDataFreshnessText(data.data_age_days)}
                {data.data_age_days > 0 && ` (${data.data_age_days}天前)`}
              </div>
            </div>
          </div>
          
          <div className="text-2xl font-bold text-gray-900 mb-1">
            ¥{formatNumber(data.current_price, 3)}
          </div>
          
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">数据日期: {data.trade_date}</span>
            <span className={`font-medium ${getPriceColor(data.pct_change)}`}>
              {data.pct_change >= 0 ? '+' : ''}{formatPercent(data.pct_change)}
            </span>
          </div>
        </div>

        {/* 交易信息 */}
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div className="flex items-center space-x-2">
            <BarChart3 className="w-4 h-4 text-gray-400" />
            <div>
              <div className="text-gray-600">成交量</div>
              <div className="font-medium">{formatNumber(data.volume)}</div>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Calendar className="w-4 h-4 text-gray-400" />
            <div>
              <div className="text-gray-600">上市日期</div>
              <div className="font-medium">{data.list_date}</div>
            </div>
          </div>
        </div>

        {/* 数据新鲜度提示 */}
        {data.data_age_days > 3 && (
          <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
            <div className="flex items-start space-x-2">
              <Clock className="w-4 h-4 text-yellow-600 mt-0.5" />
              <div className="text-sm text-yellow-700">
                <strong>数据提醒：</strong> 当前价格数据已过期（{data.data_age_days}天前），
                可能是由于节假日或非交易日导致。分析结果基于历史数据，请谨慎参考。
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default ETFInfoCard
