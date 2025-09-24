import React from 'react';
import { 
  Grid3X3, 
  DollarSign, 
  Target, 
  TrendingUp, 
  BarChart3,
  PieChart,
  Calculator,
  Settings,
  Info,
  Percent,
  Hash
} from 'lucide-react';

const GridParametersCard = ({ gridStrategy, inputParameters, showDetailed = false }) => {
  if (!gridStrategy) return null;

  const {
    current_price,
    price_range,
    grid_config,
    fund_allocation,
    risk_preference,
    calculation_method
  } = gridStrategy;

  // 格式化金额
  const formatAmount = (amount) => {
    return new Intl.NumberFormat('zh-CN', {
      style: 'currency',
      currency: 'CNY',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  // 格式化百分比
  const formatPercent = (value) => {
    return (value * 100).toFixed(2) + '%';
  };

  return (
    <div className="space-y-6">

      {/* 资金分配策略 */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 bg-orange-100 rounded-lg">
            <PieChart className="w-5 h-5 text-orange-600" />
          </div>
          <div>
            <h4 className="font-semibold text-gray-900">智能资金分配</h4>
            <p className="text-sm text-gray-600">底仓与网格资金的优化配置</p>
          </div>
        </div>

        {/* 资金分配概览 */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-6 mb-6">
          
          <div className="text-center p-4 bg-orange-50 rounded-lg">
            <div className="text-2xl font-bold text-orange-600 mb-1">
              {formatAmount(inputParameters?.total_capital || inputParameters?.totalCapital || 0)}
            </div>
            <div className="text-sm text-orange-700 font-medium">投资资金</div>
            <div className="text-xs text-gray-600 mt-1">
              总投资资金量
            </div>
          </div>

          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <div className="text-2xl font-bold text-blue-600 mb-1">
              {formatAmount(fund_allocation.base_position_amount)}
            </div>
            <div className="text-sm text-blue-700 font-medium">底仓资金</div>
            <div className="text-xs text-gray-600 mt-1">
              {formatPercent(fund_allocation.base_position_ratio)} 风险缓冲
            </div>
          </div>

          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-2xl font-bold text-green-600 mb-1">
              {formatAmount(fund_allocation.grid_trading_amount)}
            </div>
            <div className="text-sm text-green-700 font-medium">网格资金</div>
            <div className="text-xs text-gray-600 mt-1">
              用于网格交易
            </div>
          </div>

          
          <div className="text-center p-4 bg-rose-50 rounded-lg">
            <div className="text-2xl font-bold text-rose-600 mb-1">
              {formatAmount(fund_allocation.reserve_amount)}
            </div>
            <div className="text-sm text-rose-700 font-medium">预留资金</div>
            <div className="text-xs text-gray-600 mt-1">
              预留5%保障流动性
            </div>
          </div>

          <div className="text-center p-4 bg-purple-50 rounded-lg">
            <div className="text-2xl font-bold text-purple-600 mb-1">
              {formatPercent(fund_allocation.grid_fund_utilization_rate)}
            </div>
            <div className="text-sm text-purple-700 font-medium">网格资金利用率</div>
            <div className="text-xs text-gray-600 mt-1">
              最大买入时占比网格资金
            </div>
          </div>
        </div>

      </div>

      {/* 价格区间设置 */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 bg-blue-100 rounded-lg">
            <TrendingUp className="w-5 h-5 text-blue-600" />
          </div>
          <div>
            <h4 className="font-semibold text-gray-900">价格区间设置</h4>
            <p className="text-sm text-gray-600">基于ATR算法动态计算的交易区间</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-2xl font-bold text-green-600 mb-1">
              ¥{price_range.lower.toFixed(3)}
            </div>
            <div className="text-sm text-green-700 font-medium">下边界</div>
            <div className="text-xs text-gray-600 mt-1">
              买入区间下限
            </div>
          </div>

          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <div className="text-2xl font-bold text-gray-900 mb-1">
              ¥{current_price.toFixed(3)}
            </div>
            <div className="text-sm text-gray-700 font-medium">当前价格</div>
            <div className="text-xs text-gray-600 mt-1">
              参考基准价格
            </div>
          </div>

          <div className="text-center p-4 bg-red-50 rounded-lg">
            <div className="text-2xl font-bold text-red-600 mb-1">
              ¥{price_range.upper.toFixed(3)}
            </div>
            <div className="text-sm text-red-700 font-medium">上边界</div>
            <div className="text-xs text-gray-600 mt-1">
              卖出区间上限
            </div>
          </div>
        </div>

        {/* 价格区间比例可视化Bar */}
        <div className="mt-6 mb-4">
          <div className="relative h-12 rounded-lg overflow-hidden bg-gradient-to-r from-green-400 via-yellow-400 to-red-400">
            {/* 当前价格位置指示器 */}
            <div 
              className="absolute top-0 bottom-0 w-0.5 bg-white shadow-lg"
              style={{
                left: `${((current_price - price_range.lower) / (price_range.upper - price_range.lower)) * 100}%`
              }}
            >
              <div className="absolute -top-1 left-1/2 transform -translate-x-1/2 w-2 h-2 bg-white rounded-full shadow-md"></div>
              <div className="absolute -bottom-1 left-1/2 transform -translate-x-1/2 w-2 h-2 bg-white rounded-full shadow-md"></div>
            </div>
            
            {/* 中央显示价格区间比例 */}
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="bg-white bg-opacity-90 px-4 py-1 rounded-full shadow-sm">
                <span className="text-sm font-bold text-gray-900">
                  价格区间跨度: {formatPercent(price_range.ratio)}
                </span>
              </div>
            </div>
            
            {/* 左侧标签 */}
            <div className="absolute left-2 top-1/2 transform -translate-y-1/2">
              <span className="text-xs font-medium text-white drop-shadow pl-2">
                ¥{price_range.lower.toFixed(3)}
              </span>
            </div>
            
            {/* 右侧标签 */}
            <div className="absolute right-2 top-1/2 transform -translate-y-1/2">
              <span className="text-xs font-medium text-white drop-shadow pr-2">
                ¥{price_range.upper.toFixed(3)}
              </span>
            </div>
          </div>
          
          {/* Bar下方说明 */}
          <div className="flex justify-between items-center mt-2 text-xs text-gray-600">
            <span>买入区间</span>
            <span>基准位置</span>
            <span>卖出区间</span>
          </div>
        </div>
      </div>

      {/* 网格配置详情 */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 bg-green-100 rounded-lg">
            <Grid3X3 className="w-5 h-5 text-green-600" />
          </div>
          <div>
            <h4 className="font-semibold text-gray-900">网格配置详情</h4>
            <p className="text-sm text-gray-600">网格数量、步长和类型设置</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <Hash className="w-4 h-4 text-gray-600" />
              <span className="text-sm font-medium text-gray-700">网格数量</span>
            </div>
            <div className="text-xl font-bold text-gray-900">{grid_config.count}个</div>
            <div className="text-xs text-gray-600">
              基于ATR算法计算
            </div>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <Settings className="w-4 h-4 text-gray-600" />
              <span className="text-sm font-medium text-gray-700">网格类型</span>
            </div>
            <div className="text-xl font-bold text-gray-900">{grid_config.type}</div>
            <div className="text-xs text-gray-600">
              {grid_config.type === '等比' ? '推荐配置' : '简单配置'}
            </div>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <TrendingUp className="w-4 h-4 text-gray-600" />
              <span className="text-sm font-medium text-gray-700">网格步长</span>
            </div>
            {/* 根据网格类型动态展示重点 */}
            {grid_config.type === '等比' ? (
              <>
                <div className="text-xl font-bold text-gray-900">{formatPercent(grid_config.step_ratio)}</div>
                <div className="text-xs text-gray-600">
                  步长比例 · ¥{grid_config.step_size.toFixed(3)}
                </div>
              </>
            ) : (
              <>
                <div className="text-xl font-bold text-gray-900">¥{grid_config.step_size.toFixed(3)}</div>
                <div className="text-xs text-gray-600">
                  步长价格 · {formatPercent(grid_config.step_ratio)}
                </div>
              </>
            )}
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <Calculator className="w-4 h-4 text-gray-600" />
              <span className="text-sm font-medium text-gray-700">单笔数量</span>
            </div>
            <div className="text-xl font-bold text-gray-900">
              {fund_allocation.single_trade_quantity || 0}股
            </div>
            <div className="text-xs text-gray-600">
              100股整数倍
            </div>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <DollarSign className="w-4 h-4 text-gray-600" />
              <span className="text-sm font-medium text-gray-700">预估单笔收益</span>
            </div>
            <div className="text-xl font-bold text-gray-900">
              {formatAmount(fund_allocation.expected_profit_per_trade)}
            </div>
            <div className="text-xs text-gray-600">
              按网格间距和单笔数量计算
            </div>
          </div>

        </div>

        {/* 网格价格水平 */}
        {gridStrategy.price_levels && (
          <>
          <div className="flex items-center gap-3 mb-4 mt-4">
            <div className="p-2 bg-indigo-100 rounded-lg">
              <BarChart3 className="w-5 h-5 text-indigo-600" />
            </div>
            <div>
              <h4 className="font-semibold text-gray-900">网格买卖点位</h4>
              <p className="text-sm text-gray-600">详细的买卖价格点位设置</p>
            </div>
          </div>

          <div className="max-h-64 overflow-y-auto">
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-2">
              {(() => {
                const maxDisplay = 21;
                const priceLevels = gridStrategy.price_levels;
                
                // 如果网格点总数不超过25个，直接显示全部
                if (priceLevels.length <= maxDisplay) {
                  return priceLevels.map((price, index) => (
                    <div 
                      key={index}
                      className={`p-2 text-center rounded text-sm ${
                        price < current_price 
                          ? 'bg-red-50 text-red-700 border border-red-200' 
                          : price > current_price
                          ? 'bg-green-50 text-green-700 border border-green-200'
                          : 'bg-yellow-50 text-yellow-700 border border-yellow-200'
                      }`}
                    >
                      <div className="font-medium">¥{price.toFixed(3)}</div>
                      <div className="text-xs opacity-75">
                        {price < current_price ? '买入' : price > current_price ? '卖出' : '基准'}
                      </div>
                    </div>
                  ));
                }
                
                // 找到当前价格在数组中的位置（最接近的价格点）
                let centerIndex = 0;
                let minDiff = Math.abs(priceLevels[0] - current_price);
                
                for (let i = 1; i < priceLevels.length; i++) {
                  const diff = Math.abs(priceLevels[i] - current_price);
                  if (diff < minDiff) {
                    minDiff = diff;
                    centerIndex = i;
                  }
                }
                
                // 计算显示范围，以中心点向两边扩展
                const halfDisplay = Math.floor(maxDisplay / 2);
                let startIndex = Math.max(0, centerIndex - halfDisplay);
                let endIndex = Math.min(priceLevels.length, startIndex + maxDisplay);
                
                // 如果末尾不够，向前调整起始位置
                if (endIndex - startIndex < maxDisplay) {
                  startIndex = Math.max(0, endIndex - maxDisplay);
                }
                
                const displayLevels = priceLevels.slice(startIndex, endIndex);
                
                return displayLevels.map((price, index) => (
                  <div 
                    key={startIndex + index}
                    className={`p-2 text-center rounded text-sm ${
                      price < current_price 
                        ? 'bg-red-50 text-red-700 border border-red-200' 
                        : price > current_price
                        ? 'bg-green-50 text-green-700 border border-green-200'
                        : 'bg-yellow-50 text-yellow-700 border border-yellow-200'
                    }`}
                  >
                    <div className="font-medium">¥{price.toFixed(3)}</div>
                    <div className="text-xs opacity-75">
                      {price < current_price ? '买入' : price > current_price ? '卖出' : '基准'}
                    </div>
                  </div>
                ));
              })()}
            </div>
            {gridStrategy.price_levels.length > 21 && (
              <div className="text-center mt-3 text-sm text-gray-500">
                显示以当前价格为中心的20个价格水平，共{gridStrategy.price_levels.length-1}个网格点
              </div>
            )}
          </div>
          </>
        )}
      </div>

      {/* 策略优势说明 */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <div className="flex items-center gap-2 mb-4">
          <Info className="w-5 h-5 text-blue-600" />
          <h4 className="font-semibold text-blue-900">ATR算法优势</h4>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-blue-800">
          <div>
            <h5 className="font-medium mb-2">算法特点</h5>
            <ul className="space-y-1">
              <li>• 考虑跳空因素，比传统振幅更准确</li>
              <li>• 动态适应市场波动特征</li>
              <li>• 避免静态统计方法的滞后性</li>
            </ul>
          </div>
          <div>
            <h5 className="font-medium mb-2">应用优势</h5>
            <ul className="space-y-1">
              <li>• 标准化处理，便于不同标的比较</li>
              <li>• 能够捕捉市场波动模式变化</li>
              <li>• 科学的风险偏好匹配机制</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GridParametersCard;
