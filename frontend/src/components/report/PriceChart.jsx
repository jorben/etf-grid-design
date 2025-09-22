import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { TrendingUp, BarChart3 } from 'lucide-react';

const PriceChart = ({ etfInfo, gridStrategy, backtestResult }) => {
  // 模拟价格数据（实际应该从后端获取）
  const mockPriceData = [
    { date: '2024-01', price: 3.2, volume: 1000000 },
    { date: '2024-02', price: 3.1, volume: 1200000 },
    { date: '2024-03', price: 3.3, volume: 900000 },
    { date: '2024-04', price: 3.0, volume: 1500000 },
    { date: '2024-05', price: 3.4, volume: 800000 },
    { date: '2024-06', price: 3.2, volume: 1100000 },
  ];

  const currentPrice = etfInfo?.current_price || 3.2;
  const gridLevels = gridStrategy?.grid_levels || [];

  return (
    <div className="space-y-6">
      {/* 图表标题 */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-lg border border-blue-200">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 bg-blue-200 rounded-lg">
            <TrendingUp className="w-6 h-6 text-blue-700" />
          </div>
          <div>
            <h3 className="text-xl font-bold text-blue-900">价格走势与网格分析</h3>
            <p className="text-blue-700">历史价格走势及网格交易点位标注</p>
          </div>
        </div>
      </div>

      {/* 价格走势图 */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <div className="h-96 mb-4">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={mockPriceData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis 
                dataKey="date" 
                stroke="#666"
                fontSize={12}
              />
              <YAxis 
                stroke="#666"
                fontSize={12}
                tickFormatter={(value) => `¥${value.toFixed(2)}`}
              />
              <Tooltip 
                formatter={(value, name) => [`¥${value.toFixed(3)}`, '价格']}
                labelFormatter={(label) => `时间: ${label}`}
              />
              
              {/* 价格线 */}
              <Line
                type="monotone"
                dataKey="price"
                stroke="#3b82f6"
                strokeWidth={2}
                dot={{ fill: '#3b82f6', strokeWidth: 2, r: 4 }}
                name="收盘价"
              />

              {/* 当前价格线 */}
              <ReferenceLine
                y={currentPrice}
                stroke="#3b82f6"
                strokeWidth={2}
                strokeDasharray="5 5"
                label={{ value: `当前价格 ¥${currentPrice.toFixed(3)}`, position: 'right' }}
              />

              {/* 网格线 */}
              {gridLevels.slice(0, 10).map((level, index) => (
                <ReferenceLine
                  key={index}
                  y={level.price}
                  stroke={level.price > currentPrice ? '#ef4444' : '#22c55e'}
                  strokeDasharray="2 2"
                  strokeWidth={1}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* 图表说明 */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
          <div className="text-center p-3 bg-blue-50 rounded-lg">
            <div className="text-lg font-bold text-blue-600">
              {gridLevels.length || 50}
            </div>
            <div className="text-sm text-blue-700">网格总数</div>
          </div>

          <div className="text-center p-3 bg-green-50 rounded-lg">
            <div className="text-lg font-bold text-green-600">
              ¥{gridStrategy?.price_range?.lower?.toFixed(3) || '2.800'}
            </div>
            <div className="text-sm text-green-700">最低价位</div>
          </div>

          <div className="text-center p-3 bg-red-50 rounded-lg">
            <div className="text-lg font-bold text-red-600">
              ¥{gridStrategy?.price_range?.upper?.toFixed(3) || '3.600'}
            </div>
            <div className="text-sm text-red-700">最高价位</div>
          </div>

          <div className="text-center p-3 bg-purple-50 rounded-lg">
            <div className="text-lg font-bold text-purple-600">
              {((gridStrategy?.price_range?.upper - gridStrategy?.price_range?.lower) / gridStrategy?.price_range?.lower * 100)?.toFixed(1) || '25.0'}%
            </div>
            <div className="text-sm text-purple-700">价格区间</div>
          </div>
        </div>

        {/* 图例说明 */}
        <div className="flex items-center justify-center gap-6 text-sm text-gray-600">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
            <span>历史价格</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-red-500 rounded-full"></div>
            <span>上方网格</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            <span>下方网格</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-blue-500 rounded-full border-2 border-blue-300"></div>
            <span>当前价格</span>
          </div>
        </div>
      </div>

      {/* 交易点分析 */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 bg-green-100 rounded-lg">
            <BarChart3 className="w-5 h-5 text-green-600" />
          </div>
          <div>
            <h4 className="font-semibold text-gray-900">交易点位分析</h4>
            <p className="text-sm text-gray-600">基于历史数据的网格触发概率分析</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 bg-green-50 rounded-lg">
            <h5 className="font-medium text-green-900 mb-2">买入机会</h5>
            <div className="text-2xl font-bold text-green-600 mb-1">
              {backtestResult?.trading_stats?.total_trades ? Math.floor(backtestResult.trading_stats.total_trades / 2) : 15}
            </div>
            <p className="text-sm text-green-700">预期买入次数/年</p>
          </div>

          <div className="p-4 bg-blue-50 rounded-lg">
            <h5 className="font-medium text-blue-900 mb-2">卖出机会</h5>
            <div className="text-2xl font-bold text-blue-600 mb-1">
              {backtestResult?.trading_stats?.profitable_trades || 12}
            </div>
            <p className="text-sm text-blue-700">预期卖出次数/年</p>
          </div>

          <div className="p-4 bg-purple-50 rounded-lg">
            <h5 className="font-medium text-purple-900 mb-2">网格效率</h5>
            <div className="text-2xl font-bold text-purple-600 mb-1">
              {backtestResult?.performance?.win_rate ? (backtestResult.performance.win_rate * 100).toFixed(1) : '75.0'}%
            </div>
            <p className="text-sm text-purple-700">网格利用率</p>
          </div>
        </div>
      </div>

      {/* 风险提示 */}
      <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-lg">
        <div className="flex items-start gap-2">
          <div className="w-5 h-5 text-yellow-600 mt-0.5">
            <svg fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="text-sm text-yellow-800">
            <p className="font-medium mb-1">图表说明</p>
            <p>
              本图表基于历史数据模拟，实际交易中价格可能出现跳空、停牌等情况。
              网格线仅为理论价位，实际执行时请结合市场情况灵活调整。
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PriceChart;