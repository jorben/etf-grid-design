import React from "react";
import {
  Target,
  TrendingUp,
  BarChart3,
  Activity,
  Droplets,
  CheckCircle,
  AlertTriangle,
  XCircle,
  Info,
  Calendar,
  Database,
  ThermometerSun,
} from "lucide-react";

const SuitabilityCard = ({ evaluation, dataQuality, showDetailed = false }) => {
  if (!evaluation) return null;

  const {
    evaluations,
    total_score,
    conclusion,
    recommendation,
    has_fatal_flaw,
    fatal_flaws,
  } = evaluation;

  // 获取适宜度等级颜色 - 与 AnalysisReport 保持一致
  const getSuitabilityColor = (score) => {
    if (score >= 70) return "text-green-600 bg-green-100";
    if (score >= 60) return "text-yellow-600 bg-yellow-100";
    return "text-red-600 bg-red-100";
  };

  // 获取维度评分颜色
  const getScoreColor = (score, maxScore) => {
    const percentage = score / maxScore;
    if (percentage >= 0.8) return "text-green-600 bg-green-100";
    if (percentage >= 0.6) return "text-yellow-600 bg-yellow-100";
    return "text-red-600 bg-red-100";
  };

  // 获取评分图标 - 与 AnalysisReport 保持一致
  const getSuitabilityIcon = (score) => {
    if (score >= 70) return <CheckCircle className="w-5 h-5" />;
    if (score >= 60) return <AlertTriangle className="w-5 h-5" />;
    return <XCircle className="w-5 h-5" />;
  };

  // 获取维度评分图标
  const getScoreIcon = (score, maxScore) => {
    const percentage = score / maxScore;
    if (percentage >= 0.8) return <CheckCircle className="w-5 h-5" />;
    if (percentage >= 0.6) return <AlertTriangle className="w-5 h-5" />;
    return <XCircle className="w-5 h-5" />;
  };

  // 评估维度配置
  const dimensions = [
    {
      key: "amplitude",
      title: "振幅评估",
      icon: <TrendingUp className="w-5 h-5" />,
      description: "基于ATR算法的价格波动分析",
      maxScore: 35,
    },
    {
      key: "volatility",
      title: "波动率评估",
      icon: <BarChart3 className="w-5 h-5" />,
      description: "年化历史波动率风险收益评估",
      maxScore: 30,
    },
    {
      key: "market_characteristics",
      title: "市场特征评估",
      icon: <Activity className="w-5 h-5" />,
      description: "ADX指数趋势震荡分析",
      maxScore: 25,
    },
    {
      key: "liquidity",
      title: "流动性评估",
      icon: <Droplets className="w-5 h-5" />,
      description: "成交量稳定性和充足性分析",
      maxScore: 10,
    },
  ];

  return (
    <div className="space-y-6">
      {/* 总体评分 */}
      <div className="bg-gradient-to-r from-green-50 to-emerald-50 p-6 rounded-lg border border-green-200">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 bg-green-200 rounded-lg">
            <ThermometerSun className="w-6 h-6 text-green-700" />
          </div>
          <div>
            <h3 className="text-xl font-bold text-green-900">
              标的网格交易适宜度评估
            </h3>
            <p className="text-green-700">从四个维度量化评分体系，总分100分</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-white p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <ThermometerSun className="w-4 h-4 text-green-600" />
              <span className="text-sm font-medium text-gray-700">
                适宜度得分
              </span>
            </div>
            <div className="text-lg font-bold text-gray-900">
              {total_score}/100
            </div>
            <div className="text-xs text-gray-600">综合评分</div>
          </div>

          <div className="bg-white p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <CheckCircle className="w-4 h-4 text-green-600" />
              <span className="text-sm font-medium text-gray-700">
                适宜度等级
              </span>
            </div>
            <div
              className={`text-lg font-bold inline-flex items-center gap-1 ${getSuitabilityColor(total_score).replace("bg-", "text-").replace("-100", "-600")}`}
            >
              {getSuitabilityIcon(total_score)}
              {conclusion}
            </div>
            <div className="text-xs text-gray-600">评估结论</div>
          </div>

          <div className="bg-white p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <BarChart3 className="w-4 h-4 text-blue-600" />
              <span className="text-sm font-medium text-gray-700">
                评估维度
              </span>
            </div>
            <div className="text-lg font-bold text-gray-900">4个</div>
            <div className="text-xs text-gray-600">振幅·波动·特征·流动</div>
          </div>

          <div className="bg-white p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <Activity className="w-4 h-4 text-purple-600" />
              <span className="text-sm font-medium text-gray-700">
                风险状态
              </span>
            </div>
            <div
              className={`text-lg font-bold ${has_fatal_flaw ? "text-red-600" : "text-green-600"}`}
            >
              {has_fatal_flaw ? "有风险" : "正常"}
            </div>
            <div className="text-xs text-gray-600">
              {has_fatal_flaw ? "存在严重缺陷" : "无严重缺陷"}
            </div>
          </div>
        </div>

        <div className="mt-4 bg-white p-4 rounded-lg">
          <div className="flex items-start gap-2">
            <Info className="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" />
            <div>
              <p className="font-medium text-gray-900 mb-1">综合结论</p>
              <p className="text-gray-700">{recommendation}</p>
            </div>
          </div>
        </div>
      </div>

      {/* 各维度详细评分 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {dimensions.map((dimension) => {
          const eval_data = evaluations[dimension.key];
          if (!eval_data) return null;

          return (
            <div
              key={dimension.key}
              className="bg-white border border-gray-200 rounded-lg p-6"
            >
              <div className="flex items-center gap-3 mb-4">
                <div
                  className={`p-2 rounded-lg ${getScoreColor(eval_data.score, dimension.maxScore)}`}
                >
                  {dimension.icon}
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold text-gray-900">
                    {dimension.title}
                  </h4>
                  <p className="text-sm text-gray-600">
                    {dimension.description}
                  </p>
                </div>
                <div className="text-right">
                  <div className="text-xl font-bold text-gray-900">
                    {eval_data.score}/{dimension.maxScore}
                  </div>
                  <div
                    className={`text-xs px-2 py-1 text-center rounded-full ${getScoreColor(eval_data.score, dimension.maxScore)}`}
                  >
                    {eval_data.level}
                  </div>
                </div>
              </div>

              {/* 进度条 */}
              <div className="mb-4">
                <div className="flex justify-between text-sm text-gray-600 mb-1">
                  <span>得分进度</span>
                  <span>
                    {((eval_data.score / dimension.maxScore) * 100).toFixed(0)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all duration-500 ${
                      eval_data.score / dimension.maxScore >= 0.8
                        ? "bg-green-500"
                        : eval_data.score / dimension.maxScore >= 0.6
                          ? "bg-yellow-500"
                          : "bg-red-500"
                    }`}
                    style={{
                      width: `${(eval_data.score / dimension.maxScore) * 100}%`,
                    }}
                  ></div>
                </div>
              </div>

              {/* 评估说明 */}
              <div className="space-y-2">
                <p className="text-sm text-gray-700 font-medium">
                  {eval_data.description}
                </p>
                {eval_data.details && (
                  <p className="text-xs text-gray-600">{eval_data.details}</p>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* 评分标准说明 */}
      {showDetailed && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h4 className="font-semibold text-blue-900 mb-4 flex items-center gap-2">
            <Info className="w-5 h-5" />
            评分标准说明
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
            <div>
              <h5 className="font-medium text-blue-800 mb-2">
                振幅评估 (35分)
              </h5>
              <ul className="space-y-1 text-blue-700">
                <li>• ATR比率 ≥ 2.0%: 35分 (振幅充足)</li>
                <li>• ATR比率 1.5%-2.0%: 25分 (振幅适中)</li>
                <li>• ATR比率 &lt; 1.5%: 0分 (振幅不足)</li>
              </ul>
            </div>
            <div>
              <h5 className="font-medium text-blue-800 mb-2">
                波动率评估 (30分)
              </h5>
              <ul className="space-y-1 text-blue-700">
                <li>• 波动率 15%-45%: 30分 (理想区间)</li>
                <li>• 波动率 &lt; 15%: 18分 (波动偏低)</li>
                <li>• 波动率 &gt; 45%: 12分 (波动过高)</li>
              </ul>
            </div>
            <div>
              <h5 className="font-medium text-blue-800 mb-2">
                市场特征评估 (25分)
              </h5>
              <ul className="space-y-1 text-blue-700">
                <li>• ADX &lt; 20: 25分 (震荡市，适合网格)</li>
                <li>• ADX 20-40: 18分 (弱趋势)</li>
                <li>• ADX &gt; 40: 6分 (强趋势，不推荐)</li>
              </ul>
            </div>
            <div>
              <h5 className="font-medium text-blue-800 mb-2">
                流动性评估 (10分)
              </h5>
              <ul className="space-y-1 text-blue-700">
                <li>• 日均成交额 &gt; 1亿: 10分 (流动性充足)</li>
                <li>• 日均成交额 5000万-1亿: 6分 (尚可)</li>
                <li>• 日均成交额 2000万-5000万: 3分 (一般)</li>
                <li>• 日均成交额 &lt; 2000万: 1分 (不足)</li>
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SuitabilityCard;
