import React, { useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
  Area,
  ComposedChart,
  Bar
} from 'recharts';
import { TrendingUp, BarChart3, Grid3X3, Eye, EyeOff } from 'lucide-react';

const PriceChart = ({ 
  priceData, 
  gridLevels, 
  backtestTrades,
  showGridLines = true,
  showTrades = true,
  showVolume = false 
}) => {
  const [chartOptions, setChartOptions] = useState({
    showGrid: showGridLines,
    showTrades: showTrades,
    showVolume: showVolume
  });

  if (!priceData || priceData.length === 0) {
    return (
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <div className="text-center py-8">
          <BarChart3 className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-500">暂无价格数据</p>
        </div>
      </div>
    );
  }

  // 格式化价格数据
  const formatPriceData = (data) => {
    return data.map(item => ({
      ...item,
      date: new Date(item.trade_date).toLocaleDateString('zh-CN', {
        month: 'short',
        day: 'numeric'
      }),
      fullDate: item.trade_date
    }));
  };

  const formattedData = formatPriceData(priceData);

  // 自定义Tooltip
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-medium text-gray-900 mb-2">{data.fullDate}</p>
          <div className="space-y-1 text-sm">
            <div className="flex justify-between gap-4">
              <span className="text-gray-600">开盘:</span>
              <span className="font-medium">¥{data.open?.toFixed(3)}</span>
            </div>
            <div className="flex justify-between gap-4">
              <span className="text-gray-600">最高:</span>
              <span className="font-medium text-red-600">¥{data.high?.toFixed(3)}</span>
            </div>
            <div className="flex justify-between gap-4">
              <span className="text-gray-600">最低:</span>
              <span className="font-medium text-green-600">¥{data.low?.toFixed(3)}</span>
            </div>
            <div className="flex justify-between gap-4">
              <span className="text-gray-600">收盘:</span>
              <span className="font-medium">¥{data.close?.toFixed(3)}</span>
            </div>
            {data.vol && (
              <div className="flex justify-between gap-4">
                <span className="text-gray-600">成交量:</span>
                <span className="font-medium">{(data.vol / 10000).toFixed(1)}万手</span>
              </div>
            )}
          </div>
        </div>
      );
    }
    return null;
  };

  // 获取价格范围
  const getPriceRange = () => {
    const prices = formattedData.flatMap(d => [d.high, d.low, d.open, d.close]);
    return {
      min: Math.min(...prices),
      max: Math.max(...prices)
    };
  };

  const priceRange = getPriceRange();

  // 计算网格线颜色
  const getGridLineColor = (price, currentPrice) => {
    if (Math.abs(price - currentPrice) < 0.01) return '#3b82f6'; // 当前价格线
    return price > currentPrice ? '#ef4444' : '#22c55e'; // 上方红色，下方绿色
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6">
      {/* 图表标题和控制选项 */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-100 rounded-lg">
            <TrendingUp className="w-5 h-5 text-blue-600" />
          </div>
          <div>
            <h4 className="font-semibold text-gray-900">价格走势与网格分析</h4>
            <p className="text-sm text-gray-600">历史价格走势及网格交易点位标注</p>
          </div>
        </div>

        {/* 图表控制选项 */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setChartOptions(prev => ({ ...prev, showGrid: !prev.showGrid }))}
            className={`flex items-center gap-1 px-3 py-1 rounded text-sm ${
              chartOptions.showGrid 
                ? 'bg-blue-100 text-blue-700' 
                : 'bg-gray-100 text-gray-600'
            }`}
          >
            {chartOptions.showGrid ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
            网格线
          </button>

          <button
            onClick={() => setChartOptions(prev => ({ ...prev, showTrades: !prev.showTrades }))}
            className={`flex items-center gap-1 px-3 py-1 rounded text-sm ${
              chartOptions.showTrades 
                ? 'bg-green-100 text-green-700' 
                : 'bg-gray-100 text-gray-600'
            }`}
          >
            {chartOptions.showTrades ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
            交易点
          </button>

          <button
            onClick={() => setChartOptions(prev => ({ ...prev, showVolume: !prev.showVolume }))}
            className={`flex items-center gap-1 px-3 py-1 rounded text-sm ${
              chartOptions.showVolume 
                ? 'bg-purple-100 text-purple-700' 
                : 'bg-gray-100 text-gray-600'
            }`}
          >
            {chartOptions.showVolume ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
            成交量
          </button>
        </div>
      </div>

      {/* 价格走势图 */}
      <div className="h-96 mb-6">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={formattedData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis 
              dataKey="date" 
              stroke="#666"
              fontSize={12}
              tick={{ fill: '#666' }}
            />
            <YAxis 
              domain={['dataMin - 0.1', 'dataMax + 0.1']}
              stroke="#666"
              fontSize={12}
              tick={{ fill: '#666' }}
              tickFormatter={(value) => `¥${value.toFixed(2)}`}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend />

            {/* 价格线 */}
            <Line
              type="monotone"
              dataKey="close"
              stroke="#3b82f6"
              strokeWidth={2}
              dot={false}
              name="收盘价"
            />

            {/* 最高最低价区域 */}
            <Area
              type="monotone"
              dataKey="high"
              stroke="none"
              fill="#fef2f2"
              fillOpacity={0.3}
              name="价格区间"
            />
            <Area
              type="monotone"
              dataKey="low"
              stroke="none"
              fill="#ffffff"
              fillOpacity={1}
            />

            {/* 成交量柱状图 */}
            {chartOptions.showVolume && (
              <Bar
                dataKey="vol"
                fill="#e5e7eb"
                opacity={0.6}
                name="成交量"
                yAxisId="volume"
              />
            )}

            {/* 网格线 */}
            {chartOptions.showGrid && gridLevels && gridLevels.map((level, index) => {
              const currentPrice = formattedData[formattedData.length - 1]?.close || 0;
              return (
                <ReferenceLine
                  key={index}
                  y={level.price}
                  stroke={getGridLineColor(level.price, currentPrice)}
                  strokeDasharray="2 2"
                  strokeWidth={1}
                  label={{
                    value: `¥${level.price.toFixed(3)}`,
                    position: 'right',
                    fill: getGridLineColor(level.price, currentPrice),
                    fontSize: 10
                  }}
                />
              );
            })}

            {/* 当前价格线 */}
            {formattedData.length > 0 && (
              <ReferenceLine
                y={formattedData[formattedData.length - 1].close}
                stroke="#3b82f6"
                strokeWidth={2}
                label={{
                  value: `当前价格 ¥${formattedData[formattedData.length - 1].close.toFixed(3)}`,
                  position: 'right',
                  fill: '#3b82f6',
                  fontSize: 12,
                  fontWeight: 'bold'
                }}
              />
            )}
          </ComposedChart>
        </ResponsiveContainer>
      </div>

      {/* 网格信息统计 */}
      {gridLevels && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
          <div className="text-center p-3 bg-blue-50 rounded-lg">
            <div className="text-lg font-bold text-blue-600">
              {gridLevels.length}
            </div>
            <div className="text-sm text-blue-700">网格总数</div>
          </div>

          <div className="text-center p-3 bg-green-50 rounded-lg">
            <div className="text-lg font-bold text-green-600">
              ¥{Math.min(...gridLevels.map(g => g.price)).toFixed(3)}
            </div>
            <div className="text-sm text-green-700">最低价位</div>
          </div>

          <div className="text-center p-3 bg-red-50 rounded-lg">
            <div className="text-lg font-bold text-red-600">
              ¥{Math.max(...gridLevels.map(g => g.price)).toFixed(3)}
            </div>
            <div className="text-sm text-red-700">最高价位</div>
          </div>

          <div className="text-center p-3 bg-purple-50 rounded-lg">
            <div className="text-lg font-bold text-purple-600">
              {((Math.max(...gridLevels.map(g => g.price)) - Math.min(...gridLevels.map(g => g.price))) / Math.min(...gridLevels.map(g => g.price)) * 100).toFixed(1)}%
            </div>
            <div className="text-sm text-purple-700">价格区间</div>
          </div>
        </div>
      )}

      {/* 交易点标注说明 */}
      {chartOptions.showTrades && backtestTrades && backtestTrades.length > 0 && (
        <div className="flex items-center justify-center gap-6 text-sm text-gray-600">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-red-500 rounded-full"></div>
            <span>买入点位</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            <span>卖出点位</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
            <span>当前价格</span>
          </div>
        </div>
      )}

      {/* 图表说明 */}
      <div className="mt-4 p-3 bg-gray-50 rounded-lg">
        <div className="flex items-start gap-2">
          <Grid3X3 className="w-4 h-4 text-gray-600 mt-0.5 flex-shrink-0" />
          <div className="text-xs text-gray-600">
            <p className="font-medium mb-1">图表说明：</p>
            <ul className="space-y-1">
              <li>• 蓝色实线表示历史收盘价走势</li>
              <li>• 虚线表示网格交易价位，红色为上方网格，绿色为下方网格</li>
              <li>• 浅色区域表示每日最高最低价格范围</li>
              <li>• 可通过右上角按钮控制显示内容</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PriceChart;