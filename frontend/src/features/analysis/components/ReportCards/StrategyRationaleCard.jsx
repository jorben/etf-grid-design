import React from "react";
import {
  Lightbulb,
  Target,
  TrendingUp,
  BarChart3,
  CheckCircle,
  Info,
  Activity,
  Shield,
  Zap,
  AlertTriangle,
} from "lucide-react";

const StrategyRationaleCard = ({
  strategyRationale,
  adjustmentSuggestions,
}) => {
  if (!strategyRationale) return null;

  const { atr_advantages, parameter_logic, profit_basis, market_environment } =
    strategyRationale;

  return (
    <div className="space-y-6">
      {/* 策略分析依据概览 */}
      <div className="bg-gradient-to-r from-indigo-50 to-purple-50 p-6 rounded-lg border border-indigo-200">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 bg-indigo-200 rounded-lg">
            <Lightbulb className="w-6 h-6 text-indigo-700" />
          </div>
          <div>
            <h3 className="text-xl font-bold text-indigo-900">
              策略分析依据与调整建议
            </h3>
            <p className="text-indigo-700">
              科学的参数选择逻辑和市场适应性分析
            </p>
          </div>
        </div>
      </div>

      {/* ATR算法优势 */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 bg-blue-100 rounded-lg">
            <Target className="w-5 h-5 text-blue-600" />
          </div>
          <div>
            <h4 className="font-semibold text-gray-900">ATR算法优势</h4>
            <p className="text-sm text-gray-600">相比传统方法的技术优势</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {atr_advantages?.map((advantage, index) => (
            <div
              key={index}
              className="flex items-start gap-3 p-4 bg-blue-50 rounded-lg"
            >
              <CheckCircle className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
              <div>
                <p className="text-sm text-blue-800 font-medium">{advantage}</p>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-4 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg">
          <h5 className="font-medium text-indigo-900 mb-2">核心技术特点</h5>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div className="text-center">
              <div className="w-12 h-12 bg-indigo-200 rounded-full flex items-center justify-center mx-auto mb-2">
                <TrendingUp className="w-6 h-6 text-indigo-700" />
              </div>
              <p className="font-medium text-indigo-900">跳空处理</p>
              <p className="text-indigo-700 text-xs">考虑隔夜跳空影响</p>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-indigo-200 rounded-full flex items-center justify-center mx-auto mb-2">
                <Activity className="w-6 h-6 text-indigo-700" />
              </div>
              <p className="font-medium text-indigo-900">动态适应</p>
              <p className="text-indigo-700 text-xs">自动适应波动特征</p>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-indigo-200 rounded-full flex items-center justify-center mx-auto mb-2">
                <BarChart3 className="w-6 h-6 text-indigo-700" />
              </div>
              <p className="font-medium text-indigo-900">标准化</p>
              <p className="text-indigo-700 text-xs">便于不同标的比较</p>
            </div>
          </div>
        </div>
      </div>

      {/* 参数选择逻辑 */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 bg-purple-100 rounded-lg">
            <Info className="w-5 h-5 text-purple-600" />
          </div>
          <div>
            <h4 className="font-semibold text-gray-900">参数选择逻辑</h4>
            <p className="text-sm text-gray-600">
              基于历史数据和交易偏好的科学匹配
            </p>
          </div>
        </div>

        <div className="space-y-4">
          {parameter_logic &&
            Object.entries(parameter_logic).map(([key, value]) => {
              const keyNames = {
                price_range: "价格区间设定",
                grid_count: "网格数量确定",
                fund_allocation: "资金分配策略",
                grid_type: "网格类型选择",
              };

              const keyIcons = {
                price_range: <TrendingUp className="w-4 h-4 text-green-600" />,
                grid_count: <BarChart3 className="w-4 h-4 text-blue-600" />,
                fund_allocation: <Target className="w-4 h-4 text-purple-600" />,
                grid_type: <Activity className="w-4 h-4 text-orange-600" />,
              };

              return (
                <div key={key} className="p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    {keyIcons[key]}
                    <h5 className="font-medium text-gray-900">
                      {keyNames[key] || key}
                    </h5>
                  </div>
                  <p className="text-sm text-gray-700">{value}</p>
                </div>
              );
            })}
        </div>
      </div>

      {/* 收益预测依据 */}
      {profit_basis && (
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-green-100 rounded-lg">
              <TrendingUp className="w-5 h-5 text-green-600" />
            </div>
            <div>
              <h4 className="font-semibold text-gray-900">收益预测依据</h4>
              <p className="text-sm text-gray-600">
                基于ATR算法的收益估算和风险评估
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(profit_basis).map(([key, value]) => {
              const keyNames = {
                historical_performance: "历史表现",
                trading_frequency: "交易统计",
                win_rate: "胜率分析",
                risk_control: "风险控制",
              };

              return (
                <div key={key} className="p-4 bg-green-50 rounded-lg">
                  <h5 className="font-medium text-green-900 mb-1">
                    {keyNames[key] || key}
                  </h5>
                  <p className="text-sm text-green-800">{value}</p>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* 市场环境分析 */}
      {market_environment && (
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-orange-100 rounded-lg">
              <Activity className="w-5 h-5 text-orange-600" />
            </div>
            <div>
              <h4 className="font-semibold text-gray-900">市场环境分析</h4>
              <p className="text-sm text-gray-600">当前市场特征和适应性评估</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center p-4 bg-orange-50 rounded-lg">
              <div className="text-lg font-bold text-orange-900 mb-1">
                {market_environment.volatility}
              </div>
              <div className="text-sm text-orange-700 font-medium">
                波动率水平
              </div>
              <div className="text-xs text-gray-600 mt-1">年化历史波动率</div>
            </div>

            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <div className="text-lg font-bold text-blue-900 mb-1">
                {market_environment.trend_characteristic}
              </div>
              <div className="text-sm text-blue-700 font-medium">趋势特征</div>
              <div className="text-xs text-gray-600 mt-1">基于ADX指数分析</div>
            </div>

            <div className="text-center p-4 bg-purple-50 rounded-lg">
              <div className="text-lg font-bold text-purple-900 mb-1">
                {market_environment.liquidity}
              </div>
              <div className="text-sm text-purple-700 font-medium">
                流动性状况
              </div>
              <div className="text-xs text-gray-600 mt-1">成交量稳定性</div>
            </div>
          </div>
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
                  parameter_optimization: "参数优化建议",
                  risk_control: "风险控制措施",
                  profit_enhancement: "收益增强策略",
                };

                const categoryIcons = {
                  market_environment_changes: (
                    <Activity className="w-4 h-4 text-blue-600" />
                  ),
                  parameter_optimization: (
                    <Target className="w-4 h-4 text-green-600" />
                  ),
                  risk_control: <Shield className="w-4 h-4 text-red-600" />,
                  profit_enhancement: (
                    <TrendingUp className="w-4 h-4 text-purple-600" />
                  ),
                };

                const categoryColors = {
                  market_environment_changes: "bg-blue-50 border-blue-200",
                  parameter_optimization: "bg-green-50 border-green-200",
                  risk_control: "bg-red-50 border-red-200",
                  profit_enhancement: "bg-purple-50 border-purple-200",
                };

                return (
                  <div
                    key={category}
                    className={`p-4 rounded-lg border ${categoryColors[category]}`}
                  >
                    <h5 className="font-medium text-gray-900 mb-3 flex items-center gap-2">
                      {categoryIcons[category]}
                      {categoryNames[category]}
                    </h5>
                    <ul className="space-y-2">
                      {suggestions.map((suggestion, index) => (
                        <li
                          key={index}
                          className="flex items-start gap-2 text-sm text-gray-700"
                        >
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

      {/* 策略优化流程 */}
      <div className="bg-gradient-to-r from-gray-50 to-blue-50 p-6 rounded-lg border border-gray-200">
        <h4 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <Info className="w-5 h-5 text-blue-600" />
          策略优化流程建议
        </h4>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="w-12 h-12 bg-blue-200 rounded-full flex items-center justify-center mx-auto mb-2">
              <span className="text-blue-700 font-bold">1</span>
            </div>
            <h5 className="font-medium text-gray-900 mb-1">监控市场</h5>
            <p className="text-xs text-gray-600">定期检查ATR和ADX指标变化</p>
          </div>

          <div className="text-center">
            <div className="w-12 h-12 bg-green-200 rounded-full flex items-center justify-center mx-auto mb-2">
              <span className="text-green-700 font-bold">2</span>
            </div>
            <h5 className="font-medium text-gray-900 mb-1">评估表现</h5>
            <p className="text-xs text-gray-600">分析实际交易效果与预期差异</p>
          </div>

          <div className="text-center">
            <div className="w-12 h-12 bg-yellow-200 rounded-full flex items-center justify-center mx-auto mb-2">
              <span className="text-yellow-700 font-bold">3</span>
            </div>
            <h5 className="font-medium text-gray-900 mb-1">调整参数</h5>
            <p className="text-xs text-gray-600">根据市场变化优化网格设置</p>
          </div>

          <div className="text-center">
            <div className="w-12 h-12 bg-purple-200 rounded-full flex items-center justify-center mx-auto mb-2">
              <span className="text-purple-700 font-bold">4</span>
            </div>
            <h5 className="font-medium text-gray-900 mb-1">持续优化</h5>
            <p className="text-xs text-gray-600">建立长期的策略改进机制</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StrategyRationaleCard;
