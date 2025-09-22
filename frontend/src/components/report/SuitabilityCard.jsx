import React from 'react';
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
  Database
} from 'lucide-react';

const SuitabilityCard = ({ evaluation, dataQuality, showDetailed = false }) => {
  if (!evaluation) return null;

  const { evaluations, total_score, conclusion, recommendation, has_fatal_flaw, fatal_flaws } = evaluation;

  // 获取评分颜色
  const getScoreColor = (score, maxScore) => {
    const percentage = score / maxScore;
    if (percentage >= 0.8) return 'text-green-600 bg-green-100';
    if (percentage >= 0.6) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  // 获取评分图标
  const getScoreIcon = (score, maxScore) => {
    const percentage = score / maxScore;
    if (percentage >= 0.8) return <CheckCircle className="w-5 h-5" />;
    if (percentage >= 0.6) return <AlertTriangle className="w-5 h-5" />;
    return <XCircle className="w-5 h-5" />;
  };

  // 评估维度配置
  const dimensions = [
    {
      key: 'amplitude',
      title: '振幅评估',
      icon: <TrendingUp className="w-5 h-5" />,
      description: '基于ATR算法的价格波动分析',
      maxScore: 35
    },
    {
      key: 'volatility',
      title: '波动率评估',
      icon: <BarChart3 className="w-5 h-5" />,
      description: '年化历史波动率风险收益评估',
      maxScore: 30
    },
    {
      key: 'market_characteristics',
      title: '市场特征评估',
      icon: <Activity className="w-5 h-5" />,
      description: 'ADX指数趋势震荡分析',
      maxScore: 25
    },
    {
      key: 'liquidity',
      title: '流动性评估',
      icon: <Droplets className="w-5 h-5" />,
      description: '成交量稳定性和充足性分析',
      maxScore: 10
    }
  ];

  return (
    <div className="space-y-6">
      {/* 总体评分 */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-lg border border-blue-200">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-200 rounded-lg">
              <Target className="w-6 h-6 text-blue-700" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-blue-900">标的适合度评估</h3>
              <p className="text-blue-700">4维度量化评分体系，总分100分</p>
            </div>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold text-blue-900">{total_score}/100</div>
            <div className={`px-3 py-1 rounded-full text-sm font-medium inline-flex items-center gap-1 ${getScoreColor(total_score, 100)}`}>
              {getScoreIcon(total_score, 100)}
              {conclusion}
            </div>
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-lg">
          <div className="flex items-start gap-2">
            <Info className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
            <div>
              <p className="font-medium text-gray-900 mb-1">综合结论</p>
              <p className="text-gray-700">{recommendation}</p>
            </div>
          </div>
        </div>

        {/* 致命缺陷警告 */}
        {has_fatal_flaw && (
          <div className="mt-4 bg-red-50 border border-red-200 p-4 rounded-lg">
            <div className="flex items-start gap-2">
              <XCircle className="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" />
              <div>
                <p className="font-medium text-red-800 mb-1">致命缺陷警告</p>
                <p className="text-red-700">
                  检测到致命缺陷：{fatal_flaws.join('、')}。强烈不建议进行网格交易。
                </p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* 各维度详细评分 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {dimensions.map(dimension => {
          const eval_data = evaluations[dimension.key];
          if (!eval_data) return null;

          return (
            <div key={dimension.key} className="bg-white border border-gray-200 rounded-lg p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className={`p-2 rounded-lg ${getScoreColor(eval_data.score, dimension.maxScore)}`}>
                  {dimension.icon}
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold text-gray-900">{dimension.title}</h4>
                  <p className="text-sm text-gray-600">{dimension.description}</p>
                </div>
                <div className="text-right">
                  <div className="text-xl font-bold text-gray-900">
                    {eval_data.score}/{dimension.maxScore}
                  </div>
                  <div className={`text-xs px-2 py-1 rounded-full ${getScoreColor(eval_data.score, dimension.maxScore)}`}>
                    {eval_data.level}
                  </div>
                </div>
              </div>

              {/* 进度条 */}
              <div className="mb-4">
                <div className="flex justify-between text-sm text-gray-600 mb-1">
                  <span>得分进度</span>
                  <span>{((eval_data.score / dimension.maxScore) * 100).toFixed(0)}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full transition-all duration-500 ${
                      eval_data.score / dimension.maxScore >= 0.8 ? 'bg-green-500' :
                      eval_data.score / dimension.maxScore >= 0.6 ? 'bg-yellow-500' : 'bg-red-500'
                    }`}
                    style={{ width: `${(eval_data.score / dimension.maxScore) * 100}%` }}
                  ></div>
                </div>
              </div>

              {/* 评估说明 */}
              <div className="space-y-2">
                <p className="text-sm text-gray-700 font-medium">{eval_data.description}</p>
                {eval_data.details && (
                  <p className="text-xs text-gray-600">{eval_data.details}</p>
                )}
              </div>

              {/* 详细信息 */}
              {showDetailed && (
                <div className="mt-4 pt-4 border-t border-gray-100">
                  <div className="text-xs text-gray-500 space-y-1">
                    {dimension.key === 'amplitude' && eval_data.atr_pct && (
                      <p>ATR比率: {eval_data.atr_pct.toFixed(2)}%</p>
                    )}
                    {dimension.key === 'volatility' && eval_data.volatility_pct && (
                      <p>年化波动率: {eval_data.volatility_pct.toFixed(1)}%</p>
                    )}
                    {dimension.key === 'market_characteristics' && eval_data.adx_value && (
                      <p>ADX指数: {eval_data.adx_value.toFixed(1)} ({eval_data.market_type})</p>
                    )}
                    {dimension.key === 'liquidity' && eval_data.avg_amount && (
                      <p>日均成交额: {eval_data.avg_amount.toFixed(0)}万元</p>
                    )}
                  </div>
                </div>
              )}
            </div>
          );
        })}
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
            <div className="flex items-center gap-2 mb-2">
              <Calendar className="w-4 h-4 text-blue-600" />
              <span className="font-medium text-gray-900">数据时效性</span>
            </div>
            <div className={`text-sm px-2 py-1 rounded-full inline-block ${
              dataQuality.freshness === '优秀' ? 'bg-green-100 text-green-800' :
              dataQuality.freshness === '良好' ? 'bg-yellow-100 text-yellow-800' :
              'bg-red-100 text-red-800'
            }`}>
              {dataQuality.freshness}
            </div>
            <p className="text-xs text-gray-600 mt-1">{dataQuality.freshness_desc}</p>
            {dataQuality.latest_date && (
              <p className="text-xs text-gray-500 mt-1">
                最新数据: {dataQuality.latest_date}
              </p>
            )}
          </div>

          <div className="bg-white p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <CheckCircle className="w-4 h-4 text-green-600" />
              <span className="font-medium text-gray-900">数据完整性</span>
            </div>
            <div className={`text-sm px-2 py-1 rounded-full inline-block ${
              dataQuality.completeness === '优秀' ? 'bg-green-100 text-green-800' :
              dataQuality.completeness === '良好' ? 'bg-yellow-100 text-yellow-800' :
              'bg-red-100 text-red-800'
            }`}>
              {dataQuality.completeness}
            </div>
            <p className="text-xs text-gray-600 mt-1">{dataQuality.completeness_desc}</p>
            {dataQuality.total_records && (
              <p className="text-xs text-gray-500 mt-1">
                数据记录: {dataQuality.total_records}条
              </p>
            )}
          </div>

          <div className="bg-white p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <BarChart3 className="w-4 h-4 text-purple-600" />
              <span className="font-medium text-gray-900">分析范围</span>
            </div>
            <div className="text-sm text-gray-900 font-medium">
              {dataQuality.analysis_days}天
            </div>
            <p className="text-xs text-gray-600 mt-1">历史数据分析期间</p>
            {dataQuality.start_date && (
              <p className="text-xs text-gray-500 mt-1">
                {dataQuality.start_date} 至 {dataQuality.latest_date}
              </p>
            )}
          </div>
        </div>
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
              <h5 className="font-medium text-blue-800 mb-2">振幅评估 (35分)</h5>
              <ul className="space-y-1 text-blue-700">
                <li>• ATR比率 ≥ 2.0%: 35分 (振幅充足)</li>
                <li>• ATR比率 1.5%-2.0%: 25分 (振幅适中)</li>
                <li>• ATR比率 &lt; 1.5%: 0分 (振幅不足)</li>
              </ul>
            </div>
            <div>
              <h5 className="font-medium text-blue-800 mb-2">波动率评估 (30分)</h5>
              <ul className="space-y-1 text-blue-700">
                <li>• 波动率 15%-40%: 30分 (理想区间)</li>
                <li>• 波动率 &lt; 15%: 18分 (波动偏低)</li>
                <li>• 波动率 &gt; 40%: 12分 (波动过高)</li>
              </ul>
            </div>
            <div>
              <h5 className="font-medium text-blue-800 mb-2">市场特征评估 (25分)</h5>
              <ul className="space-y-1 text-blue-700">
                <li>• ADX &lt; 20: 25分 (震荡市，适合网格)</li>
                <li>• ADX 20-25: 18分 (弱趋势)</li>
                <li>• ADX &gt; 25: 6分 (强趋势，不推荐)</li>
              </ul>
            </div>
            <div>
              <h5 className="font-medium text-blue-800 mb-2">流动性评估 (10分)</h5>
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