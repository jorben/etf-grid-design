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
  Hash,
  Lightbulb,
  CheckCircle,
  Zap,
  Activity,
  Shield,
  AlertTriangle,
} from "lucide-react";
import { formatCurrency, formatPercent, formatDate } from "@shared/utils";

const GridParametersCard = ({
  gridStrategy,
  inputParameters,
  strategyRationale,
  adjustmentSuggestions,
  showDetailed = false,
  dataQuality,
}) => {
  if (!gridStrategy) return null;

  const {
    current_price,
    price_range,
    grid_config,
    fund_allocation,
    risk_preference,
    calculation_method,
  } = gridStrategy;

  // 获取价格日期显示文本
  const getPriceDateText = () => {
    // 优先使用gridStrategy中的price_date（来自TushareClient::get_latest_price）
    const priceDate = gridStrategy?.price_date;
    if (priceDate) {
      const formattedDate = formatDate(priceDate);
      if (formattedDate) {
        return `${formattedDate} 收盘价`;
      }
    }

    // 回退到dataQuality中的latest_date
    const latestDate = dataQuality?.latest_date;
    if (latestDate) {
      const formattedDate = formatDate(latestDate);
      if (formattedDate) {
        return `${formattedDate} 收盘价`;
      }
    }

    return "最近交易日收盘价";
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
              {formatCurrency(
                inputParameters?.total_capital ||
                  inputParameters?.totalCapital ||
                  0,
              )}
            </div>
            <div className="text-sm text-orange-700 font-medium">投资资金</div>
            <div className="text-xs text-gray-600 mt-1">总投资资金量</div>
          </div>

          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <div className="text-2xl font-bold text-blue-600 mb-1">
              {formatCurrency(fund_allocation.base_position_amount)}
            </div>
            <div className="text-sm text-blue-700 font-medium">底仓资金</div>
            <div className="text-xs text-gray-600 mt-1">
              {formatPercent(fund_allocation.base_position_ratio)} 稳定仓位
            </div>
          </div>

          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-2xl font-bold text-green-600 mb-1">
              {formatCurrency(fund_allocation.grid_trading_amount)}
            </div>
            <div className="text-sm text-green-700 font-medium">网格资金</div>
            <div className="text-xs text-gray-600 mt-1">用于网格交易</div>
          </div>

          <div className="text-center p-4 bg-rose-50 rounded-lg">
            <div className="text-2xl font-bold text-rose-600 mb-1">
              {formatCurrency(fund_allocation.reserve_amount)}
            </div>
            <div className="text-sm text-rose-700 font-medium">预留资金</div>
            <div className="text-xs text-gray-600 mt-1">预留5%保障流动性</div>
          </div>

          <div className="text-center p-4 bg-purple-50 rounded-lg">
            <div className="text-2xl font-bold text-purple-600 mb-1">
              {formatPercent(fund_allocation.grid_fund_utilization_rate)}
            </div>
            <div className="text-sm text-purple-700 font-medium">
              网格资金利用率
            </div>
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
            <p className="text-sm text-gray-600">
              基于ATR算法动态计算的交易区间
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-2xl font-bold text-green-600 mb-1">
              ¥{price_range.lower.toFixed(3)}
            </div>
            <div className="text-sm text-green-700 font-medium">下边界</div>
            <div className="text-xs text-gray-600 mt-1">买入区间下限</div>
          </div>

          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <div className="text-2xl font-bold text-gray-900 mb-1">
              ¥{current_price.toFixed(3)}
            </div>
            <div className="text-sm text-gray-700 font-medium">基准价格</div>
            <div className="text-xs text-gray-600 mt-1">
              {getPriceDateText()}
            </div>
          </div>

          <div className="text-center p-4 bg-red-50 rounded-lg">
            <div className="text-2xl font-bold text-red-600 mb-1">
              ¥{price_range.upper.toFixed(3)}
            </div>
            <div className="text-sm text-red-700 font-medium">上边界</div>
            <div className="text-xs text-gray-600 mt-1">卖出区间上限</div>
          </div>
        </div>

        {/* 价格区间比例可视化Bar */}
        <div className="mt-6 mb-4">
          <div className="relative h-12 rounded-lg overflow-hidden bg-gradient-to-r from-green-400 via-yellow-400 to-red-400">
            {/* 当前价格位置指示器 */}
            <div
              className="absolute top-0 bottom-0 w-0.5 shadow-lg"
              style={{
                left: `${((current_price - price_range.lower) / (price_range.upper - price_range.lower)) * 100}%`,
              }}
            >
              <div className="absolute -top-1 left-1/2 transform -translate-x-1/2 w-2 h-2 bg-white rounded-full shadow-md"></div>
              <div className="absolute -bottom-1 left-1/2 transform -translate-x-1/2 w-2 h-2 bg-white rounded-full shadow-md"></div>
            </div>

            {/* 中央显示价格区间比例 */}
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="bg-white bg-opacity-50 px-4 py-1 rounded-full shadow-sm">
                <span className="text-sm text-gray-900">
                  区间跨度 {formatPercent(price_range.ratio)}
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
          <div className="flex justify-between items-center pl-2 pr-2 mt-2 text-xs text-gray-600">
            <span>下边界</span>
            <span>基准位置</span>
            <span>上边界</span>
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
              <span className="text-sm font-medium text-gray-700">
                网格数量
              </span>
            </div>
            <div className="text-xl font-bold text-gray-900">
              {grid_config.count}个
            </div>
            <div className="text-xs text-gray-600">基于ATR算法计算</div>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <Settings className="w-4 h-4 text-gray-600" />
              <span className="text-sm font-medium text-gray-700">
                网格类型
              </span>
            </div>
            <div className="text-xl font-bold text-gray-900">
              {grid_config.type}
            </div>
            <div className="text-xs text-gray-600">
              {grid_config.type === "等比" ? "推荐配置" : "简单配置"}
            </div>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <Activity className="w-4 h-4 text-gray-600" />
              <span className="text-sm font-medium text-gray-700">
                网格步长
              </span>
            </div>
            {/* 根据网格类型动态展示重点 */}
            {grid_config.type === "等比" ? (
              <>
                <div className="text-xl font-bold text-gray-900">
                  {formatPercent(grid_config.step_ratio)}
                </div>
                <div className="text-xs text-gray-600">
                  步长比例 · ¥{grid_config.step_size.toFixed(3)}
                </div>
              </>
            ) : (
              <>
                <div className="text-xl font-bold text-gray-900">
                  ¥{grid_config.step_size.toFixed(3)}
                </div>
                <div className="text-xs text-gray-600">
                  步长价格 · {formatPercent(grid_config.step_ratio)}
                </div>
              </>
            )}
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <Calculator className="w-4 h-4 text-gray-600" />
              <span className="text-sm font-medium text-gray-700">
                单笔数量
              </span>
            </div>
            <div className="text-xl font-bold text-gray-900">
              {fund_allocation.single_trade_quantity || 0}股
            </div>
            <div className="text-xs text-gray-600">100股整数倍</div>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <DollarSign className="w-4 h-4 text-gray-600" />
              <span className="text-sm font-medium text-gray-700">
                预估单笔收益
              </span>
            </div>
            <div className="text-xl font-bold text-gray-900">
              {formatCurrency(fund_allocation.expected_profit_per_trade)}
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
                            ? "bg-red-50 text-red-700 border border-red-200"
                            : price > current_price
                              ? "bg-green-50 text-green-700 border border-green-200"
                              : "bg-yellow-50 text-yellow-700 border border-yellow-200"
                        }`}
                      >
                        <div className="font-medium">¥{price.toFixed(3)}</div>
                        <div className="text-xs opacity-75">
                          {price < current_price
                            ? "买入"
                            : price > current_price
                              ? "卖出"
                              : "基准"}
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
                  let endIndex = Math.min(
                    priceLevels.length,
                    startIndex + maxDisplay,
                  );

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
                          ? "bg-red-50 text-red-700 border border-red-200"
                          : price > current_price
                            ? "bg-green-50 text-green-700 border border-green-200"
                            : "bg-yellow-50 text-yellow-700 border border-yellow-200"
                      }`}
                    >
                      <div className="font-medium">¥{price.toFixed(3)}</div>
                      <div className="text-xs opacity-75">
                        {price < current_price
                          ? "买入"
                          : price > current_price
                            ? "卖出"
                            : "基准"}
                      </div>
                    </div>
                  ));
                })()}
              </div>
              {gridStrategy.price_levels.length > 21 && (
                <div className="text-center mt-3 text-sm text-gray-500">
                  显示以当前价格为中心的20个价格水平，共
                  {gridStrategy.price_levels.length - 1}个网格点
                </div>
              )}
            </div>
          </>
        )}
      </div>

      {/* 策略分析依据 */}
      {strategyRationale && (
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-indigo-100 rounded-lg">
              <Lightbulb className="w-5 h-5 text-indigo-600" />
            </div>
            <div>
              <h4 className="font-semibold text-gray-900">策略分析依据</h4>
              <p className="text-sm text-gray-600">
                参数选择逻辑和算法优势说明
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* ATR算法优势 */}
            <div>
              <h5 className="font-medium text-gray-900 mb-3 flex items-center gap-2">
                <Target className="w-4 h-4 text-blue-600" />
                ATR算法优势
              </h5>
              <ul className="space-y-2 text-sm text-gray-700">
                {strategyRationale.atr_advantages?.map((advantage, index) => (
                  <li
                    key={index}
                    className="flex items-start gap-2 bg-gray-50 rounded p-2"
                  >
                    <CheckCircle className="w-4 h-4 text-green-600 mt-0.5 flex-shrink-0" />
                    {advantage}
                  </li>
                ))}
              </ul>
            </div>

            {/* 参数选择逻辑 */}
            <div>
              <h5 className="font-medium text-gray-900 mb-3 flex items-center gap-2">
                <Info className="w-4 h-4 text-purple-600" />
                参数选择逻辑
              </h5>
              <div className="space-y-2 text-sm text-gray-700">
                {strategyRationale.parameter_logic &&
                  Object.entries(strategyRationale.parameter_logic).map(
                    ([key, value]) => (
                      <div key={key} className="p-2 bg-gray-50 rounded">
                        <span className="font-medium capitalize">
                          {key.replace("_", " ")}:{" "}
                        </span>
                        {value}
                      </div>
                    ),
                  )}
              </div>
            </div>
          </div>

          {/* 市场环境分析 */}
          {strategyRationale.market_environment && (
            <div className="mt-6 p-4 bg-blue-50 rounded-lg">
              <h5 className="font-medium text-blue-900 mb-2">市场环境分析</h5>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div>
                  <span className="text-blue-700 font-medium">波动率: </span>
                  <span className="text-blue-800">
                    {strategyRationale.market_environment.volatility}
                  </span>
                </div>
                <div>
                  <span className="text-blue-700 font-medium">趋势特征: </span>
                  <span className="text-blue-800">
                    {strategyRationale.market_environment.trend_characteristic}
                  </span>
                </div>
                <div>
                  <span className="text-blue-700 font-medium">流动性: </span>
                  <span className="text-blue-800">
                    {strategyRationale.market_environment.liquidity}
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* 调整建议 */}
      {adjustmentSuggestions && (
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-yellow-100 rounded-lg">
              <Zap className="w-5 h-5 text-yellow-600" />
            </div>
            <div>
              <h4 className="font-semibold text-gray-900">策略调整建议</h4>
              <p className="text-sm text-gray-600">市场环境变化时的优化方案</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {Object.entries(adjustmentSuggestions).map(
              ([category, suggestions]) => {
                if (!suggestions || suggestions.length === 0) return null;

                const categoryNames = {
                  market_environment_changes: "市场环境应对",
                  parameter_optimization: "参数优化",
                  risk_control: "风险控制",
                  profit_enhancement: "收益增强",
                };

                const categoryIcons = {
                  market_environment_changes: <Activity className="w-4 h-4" />,
                  parameter_optimization: <Target className="w-4 h-4" />,
                  risk_control: <Shield className="w-4 h-4" />,
                  profit_enhancement: <TrendingUp className="w-4 h-4" />,
                };

                return (
                  <div key={category}>
                    <h5 className="font-medium text-gray-900 mb-3 flex items-center gap-2">
                      {categoryIcons[category]}
                      {categoryNames[category]}
                    </h5>
                    <ul className="space-y-2 text-sm text-gray-700">
                      {suggestions.map((suggestion, index) => (
                        <li key={index} className="flex items-start gap-2">
                          <AlertTriangle className="w-4 h-4 text-yellow-600 mt-0.5 flex-shrink-0" />
                          {suggestion}
                        </li>
                      ))}
                    </ul>
                  </div>
                );
              },
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default GridParametersCard;
