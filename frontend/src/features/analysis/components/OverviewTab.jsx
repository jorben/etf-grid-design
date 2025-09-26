import React from "react";
import {
  TrendingUp,
  BarChart3,
  Target,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Info,
  DollarSign,
  Calendar,
  Database,
  ThermometerSun,
} from "lucide-react";

/**
 * 概览标签页组件
 * 负责展示分析报告的核心指标和摘要信息
 */
export default function OverviewTab({
  etfInfo,
  suitabilityEvaluation,
  gridStrategy,
  dataQuality,
  inputParameters,
}) {
  // 获取适宜度等级颜色
  const getSuitabilityColor = (score) => {
    if (score >= 70) return "text-green-600 bg-green-100";
    if (score >= 60) return "text-yellow-600 bg-yellow-100";
    return "text-red-600 bg-red-100";
  };

  return (
    <div className="space-y-6">
      {/* 风险提示 */}
      {suitabilityEvaluation?.has_fatal_flaw && (
        <div className="bg-red-50 border border-red-200 p-4 rounded-lg">
          <div className="flex items-center gap-2 text-red-800 font-medium mb-2">
            <AlertTriangle className="w-5 h-5" />
            重要风险提示
          </div>
          <p className="text-red-700 text-sm">
            该标的存在致命缺陷：
            {suitabilityEvaluation?.fatal_flaws?.join("、") || "未知风险"}
            ，不建议进行网格交易。
          </p>
        </div>
      )}

      {/* 核心指标卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-gradient-to-r from-orange-50 to-orange-100 p-6 rounded-lg">
          <div className="flex items-center gap-3 mb-3">
            <div className="p-2 bg-orange-200 rounded-lg">
              <Target className="w-5 h-5 text-orange-700" />
            </div>
            <h3 className="font-semibold text-orange-900">所选标的</h3>
          </div>
          <div className="text-2xl font-bold text-orange-900 mb-1">
            {etfInfo?.code || "未知"}
          </div>
          <p className="text-orange-700 text-sm">
            {etfInfo?.name || "未知标的"}
          </p>
        </div>

        <div className="bg-gradient-to-r from-blue-50 to-blue-100 p-6 rounded-lg">
          <div className="flex items-center gap-3 mb-3">
            <div className="p-2 bg-blue-200 rounded-lg">
              <ThermometerSun className="w-5 h-5 text-blue-700" />
            </div>
            <h3 className="font-semibold text-blue-900">适宜度评估</h3>
          </div>
          <div className="text-2xl font-bold text-blue-900 mb-1">
            {suitabilityEvaluation?.total_score || 0}/100分
          </div>
          <p className="text-blue-700 text-sm">
            {suitabilityEvaluation?.recommendation || "暂无评估"}
          </p>
        </div>

        <div className="bg-gradient-to-r from-green-50 to-green-100 p-6 rounded-lg">
          <div className="flex items-center gap-3 mb-3">
            <div className="p-2 bg-green-200 rounded-lg">
              <TrendingUp className="w-5 h-5 text-green-700" />
            </div>
            <h3 className="font-semibold text-green-900">网格价格区间</h3>
          </div>
          <div className="text-2xl font-bold text-green-900 mb-1">
            ¥{(gridStrategy?.price_range?.lower || 0).toFixed(3)} - ¥
            {(gridStrategy?.price_range?.upper || 0).toFixed(3)}
          </div>
          <p className="text-green-700 text-sm">网格交易价格范围</p>
        </div>

        <div className="bg-gradient-to-r from-purple-50 to-purple-100 p-6 rounded-lg">
          <div className="flex items-center gap-3 mb-3">
            <div className="p-2 bg-purple-200 rounded-lg">
              <BarChart3 className="w-5 h-5 text-purple-700" />
            </div>
            <h3 className="font-semibold text-purple-900">网格步长</h3>
          </div>
          {/* 根据网格类型动态展示重点 */}
          {gridStrategy?.grid_config?.type === "等比" ? (
            <>
              <div className="text-2xl font-bold text-purple-900 mb-1">
                {((gridStrategy?.grid_config?.step_ratio || 0) * 100).toFixed(
                  2,
                )}
                %
              </div>
              <p className="text-purple-700 text-sm">
                步长比例 · ¥
                {(gridStrategy?.grid_config?.step_size || 0).toFixed(3)}
              </p>
            </>
          ) : (
            <>
              <div className="text-2xl font-bold text-purple-900 mb-1">
                ¥{(gridStrategy?.grid_config?.step_size || 0).toFixed(3)}
              </div>
              <p className="text-purple-700 text-sm">
                步长价格 ·{" "}
                {((gridStrategy?.grid_config?.step_ratio || 0) * 100).toFixed(
                  2,
                )}
                %
              </p>
            </>
          )}
        </div>
      </div>

      {/* 数据质量评估 */}
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 bg-gray-200 rounded-lg">
            <Database className="w-5 h-5 text-gray-700" />
          </div>
          <div>
            <h4 className="font-semibold text-gray-900">数据质量评估</h4>
            <p className="text-sm text-gray-600">分析数据的时效性和完整性</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white p-4 rounded-lg">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <Calendar className="w-4 h-4 text-blue-600" />
                <span className="font-medium text-gray-900">数据时效性</span>
              </div>
              <div
                className={`text-sm px-2 py-1 rounded-full ${
                  dataQuality?.freshness === "优秀"
                    ? "bg-green-100 text-green-800"
                    : dataQuality?.freshness === "良好"
                      ? "bg-yellow-100 text-yellow-800"
                      : "bg-red-100 text-red-800"
                }`}
              >
                {dataQuality?.freshness || "未知"}
              </div>
            </div>
            <p className="text-xs text-gray-600 mt-1">
              {dataQuality?.freshness_desc || "暂无描述"}
            </p>
            {dataQuality?.latest_date && (
              <p className="text-xs text-gray-500 mt-1">
                最新数据: {dataQuality.latest_date}
              </p>
            )}
          </div>

          <div className="bg-white p-4 rounded-lg">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-green-600" />
                <span className="font-medium text-gray-900">数据完整性</span>
              </div>
              <div
                className={`text-sm px-2 py-1 rounded-full ${
                  dataQuality?.completeness === "优秀"
                    ? "bg-green-100 text-green-800"
                    : dataQuality?.completeness === "良好"
                      ? "bg-yellow-100 text-yellow-800"
                      : "bg-red-100 text-red-800"
                }`}
              >
                {dataQuality?.completeness || "未知"}
              </div>
            </div>
            <p className="text-xs text-gray-600 mt-1">
              {dataQuality?.completeness_desc || "暂无描述"}
            </p>
            {dataQuality?.total_records && (
              <p className="text-xs text-gray-500 mt-1">
                数据记录: {dataQuality.total_records}条
              </p>
            )}
          </div>

          <div className="bg-white p-4 rounded-lg">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <BarChart3 className="w-4 h-4 text-purple-600" />
                <span className="font-medium text-gray-900">分析范围</span>
              </div>
              <div className="text-sm px-2 py-1 rounded-full bg-green-100 text-green-800">
                {dataQuality?.analysis_days || 0}天
              </div>
            </div>
            <p className="text-xs text-gray-600 mt-1">历史数据分析期间</p>
            {dataQuality?.start_date && (
              <p className="text-xs text-gray-500 mt-1">
                {dataQuality.start_date} 至 {dataQuality.latest_date}
              </p>
            )}
          </div>
        </div>
      </div>

      {/* 快速摘要 */}
      <div className="bg-blue-50 border border-blue-200 p-6 rounded-lg">
        <h3 className="font-semibold text-blue-900 mb-3 flex items-center gap-2">
          <Info className="w-5 h-5" />
          策略摘要
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-blue-800 mb-2">投资配置</h4>
            <ul className="space-y-1 text-sm text-blue-600">
              <li>
                • 总投资资金：¥
                {(inputParameters?.total_capital || 0).toLocaleString()}
              </li>
              <li>
                • 底仓资金：¥
                {(
                  gridStrategy?.fund_allocation?.base_position_amount || 0
                ).toLocaleString()}
              </li>
              <li>
                • 网格资金：¥
                {(
                  gridStrategy?.fund_allocation?.grid_trading_amount || 0
                ).toLocaleString()}
              </li>
              <li>
                • 网格资金利用率：
                {(
                  (gridStrategy?.fund_allocation?.grid_fund_utilization_rate ||
                    0) * 100
                ).toFixed(1)}
                %
              </li>
            </ul>
          </div>
          <div>
            <h4 className="font-medium text-blue-800 mb-2">策略特征</h4>
            <ul className="space-y-1 text-sm text-blue-600">
              <li>
                • 价格区间：¥
                {(gridStrategy?.price_range?.lower || 0).toFixed(3)} - ¥
                {(gridStrategy?.price_range?.upper || 0).toFixed(3)}
              </li>
              <li>
                • 网格步长：¥
                {(gridStrategy?.grid_config?.step_size || 0).toFixed(3)} (
                {((gridStrategy?.grid_config?.step_ratio || 0) * 100).toFixed(
                  2,
                )}
                %)
              </li>
              <li>
                • 单笔股数：
                {gridStrategy?.fund_allocation?.single_trade_quantity || 0}股
              </li>
              <li>
                • 预估单笔收益：¥
                {(
                  gridStrategy?.fund_allocation?.expected_profit_per_trade || 0
                ).toFixed(2)}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
