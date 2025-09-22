import React from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts'
import { formatNumber } from '../../services/api'

const PriceChart = ({ currentPrice, gridPrices, priceRange, historicalPrices = [] }) => {
  // 处理历史价格数据
  const processHistoricalData = () => {
    if (historicalPrices && historicalPrices.length > 0) {
      // 使用真实历史数据
      return historicalPrices.map((item, index) => ({
        date: item.date,
        price: item.price,
        volume: item.volume,
        day: index + 1
      }))
    } else {
      // 如果没有历史数据，返回空数组
      return []
    }
  }

  const chartData = processHistoricalData()
  const hasData = historicalPrices && historicalPrices.length > 0
  
  // 格式化价格显示
  const formatPrice = (value) => {
    return `¥${formatNumber(value, 2)}`
  }

  // 自定义工具提示
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="text-sm text-gray-600">{`日期: ${label}`}</p>
          <p className="text-sm font-medium">
            {`价格: ${formatPrice(payload[0].value)}`}
          </p>
        </div>
      )
    }
    return null
  }

  // 生成网格线数据
  const gridLineData = gridPrices.map((price, index) => ({
    price: price,
    name: `网格${index + 1}`
  }))

  return (
    <div className="card">
      <div className="card-header">
        <h3 className="card-title">价格区间与网格分布</h3>
        <div className="text-sm text-gray-600">
          当前价格: ¥{formatNumber(currentPrice, 3)}
        </div>
      </div>

      {/* 价格区间信息 */}
      <div className="mb-6 p-4 bg-gray-50 rounded-lg">
        <div className="flex items-center justify-between mb-3">
          <div className="text-center">
            <div className="text-sm text-gray-600">下边界</div>
            <div className="font-medium text-success-600">¥{formatNumber(priceRange[0], 3)}</div>
          </div>
          <div className="text-center">
            <div className="text-sm text-gray-600">当前价格</div>
            <div className="font-medium text-lg">¥{formatNumber(currentPrice, 3)}</div>
          </div>
          <div className="text-center">
            <div className="text-sm text-gray-600">上边界</div>
            <div className="font-medium text-danger-600">¥{formatNumber(priceRange[1], 3)}</div>
          </div>
        </div>
        
        {/* 价格区间可视化 */}
        <div className="relative h-4 bg-gradient-to-r from-green-200 via-gray-200 to-red-200 rounded-full">
          <div 
            className="absolute top-0 w-1 h-4 bg-blue-600 rounded-full transform -translate-x-1/2"
            style={{
              left: `${((currentPrice - priceRange[0]) / (priceRange[1] - priceRange[0])) * 100}%`
            }}
            title={`当前价格: ¥${formatNumber(currentPrice, 3)}`}
          />
        </div>
        <div className="flex justify-between text-xs text-gray-500 mt-1">
          <span>下边界</span>
          <span>价格区间</span>
          <span>上边界</span>
        </div>
      </div>

      {/* 价格走势图 */}
      <div className="mb-6">
        <h4 className="font-medium mb-3">
          历史价格走势{hasData ? '（最近30个交易日）' : '（暂无数据）'}
        </h4>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis 
                dataKey="day" 
                tick={{ fontSize: 12 }}
                axisLine={{ stroke: '#d1d5db' }}
              />
              <YAxis 
                tick={{ fontSize: 12 }}
                axisLine={{ stroke: '#d1d5db' }}
                tickFormatter={formatPrice}
                domain={[
                  Math.min(currentPrice, priceRange[0]) * 0.98, 
                  Math.max(currentPrice, priceRange[1]) * 1.02
                ]}
                padding={{ top: 20, bottom: 20 }}
              />
              <Tooltip content={<CustomTooltip />} />
              <ReferenceLine 
                y={currentPrice} 
                stroke="#3b82f6" 
                strokeDasharray="5 5"
                label={{ value: "当前价格", position: "right" }}
              />
              <ReferenceLine 
                y={priceRange[0]} 
                stroke="#22c55e" 
                strokeDasharray="3 3"
                label={{ value: "下边界", position: "left" }}
              />
              <ReferenceLine 
                y={priceRange[1]} 
                stroke="#ef4444" 
                strokeDasharray="3 3"
                label={{ value: "上边界", position: "left" }}
              />
              <Line 
                type="monotone" 
                dataKey="price" 
                stroke="#6b7280" 
                strokeWidth={2}
                dot={{ fill: '#6b7280', strokeWidth: 2, r: 3 }}
                activeDot={{ r: 5, fill: '#3b82f6' }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* 网格价格分布 */}
      <div>
        <h4 className="font-medium mb-3">网格价格分布</h4>
        <div className="text-sm text-gray-600 mb-3">
          共 {gridPrices.length} 个网格，步长 {formatNumber((priceRange[1] - priceRange[0]) / (gridPrices.length - 1), 3)} 元
        </div>
        
        <div className="grid grid-cols-5 md:grid-cols-8 lg:grid-cols-10 gap-2">
          {gridPrices.map((price, index) => (
            <div 
              key={index} 
              className={`
                p-2 text-center text-xs rounded border transition-all
                ${Math.abs(price - currentPrice) < 0.01 ? 'bg-blue-100 border-blue-300 text-blue-800 font-medium' : 'bg-gray-50 border-gray-200 text-gray-700'}
                hover:bg-gray-100 hover:border-gray-300
              `}
              title={`网格${index + 1}: ¥${formatNumber(price, 3)}`}
            >
              <div className="font-medium">¥{formatNumber(price, 3)}</div>
            </div>
          ))}
        </div>
        
        <div className="mt-3 text-xs text-gray-500">
          💡 提示：蓝色标记为当前价格所在的网格位置
        </div>
      </div>

      {/* 图表说明 */}
      <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
        <div className="flex items-start space-x-2">
          <div className="w-2 h-2 bg-blue-400 rounded-full mt-2 flex-shrink-0"></div>
          <div className="text-xs text-blue-700">
            <strong>图表说明：</strong>
            <ul className="mt-1 space-y-1">
              <li>• 灰色线条：历史价格走势{hasData ? '' : '（需要真实数据支持）'}</li>
              <li>• 蓝色虚线：当前价格水平</li>
              <li>• 绿色虚线：网格下边界</li>
              <li>• 红色虚线：网格上边界</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PriceChart
