import React from 'react'
import { CheckCircle, XCircle, AlertTriangle, Info } from 'lucide-react'
import { getAdaptabilityClass } from '../../services/api'

const AdaptabilityCard = ({ data }) => {
  if (!data) return null

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-success-600'
    if (score >= 60) return 'text-warning-600'
    return 'text-danger-600'
  }

  const getScoreBackground = (score) => {
    if (score >= 80) return 'bg-success-100'
    if (score >= 60) return 'bg-warning-100'
    return 'bg-danger-100'
  }

  const getStatusIcon = (isSuitable) => {
    if (isSuitable) {
      return <CheckCircle className="w-6 h-6 text-success-600" />
    }
    return <XCircle className="w-6 h-6 text-danger-600" />
  }

  // 获取维度得分 - 使用后端返回的实际得分
  const getDimensionScore = (dimensionName) => {
    if (!data.dimension_scores) {
      // 兼容旧数据：如果没有dimension_scores，使用原有逻辑
      return getOldDimensionScore(dimensionName);
    }
    
    switch(dimensionName) {
      case 'amplitude': return data.dimension_scores.amplitude_score || 0;
      case 'volatility': return data.dimension_scores.volatility_score || 0;
      case 'market': return data.dimension_scores.market_score || 0;
      case 'liquidity': return data.dimension_scores.liquidity_score || 0;
      default: return 0;
    }
  };

  // 兼容旧数据的计算逻辑 - 更新为新的分数分布
  const getOldDimensionScore = (dimensionName) => {
    switch(dimensionName) {
      case 'amplitude': 
        return Math.max(0, Math.round((data.score / 100) * 35));
      case 'volatility': 
        return Math.max(0, Math.round(((Math.max(35, data.score) - 35) / 100) * 30));
      case 'market': 
        return Math.max(0, Math.round(((Math.max(65, data.score) - 65) / 100) * 25));
      case 'liquidity': 
        return Math.max(0, Math.round(((Math.max(90, data.score) - 90) / 100) * 10));
      default: return 0;
    }
  };

  // 获取维度颜色
  const getDimensionColor = (score, maxScore) => {
    const percentage = (score / maxScore) * 100;
    if (percentage >= 80) return 'bg-success-500';
    if (percentage >= 60) return 'bg-warning-500';
    return 'bg-danger-500';
  };

  // 获取维度宽度
  const getDimensionWidth = (score, maxScore) => {
    return Math.max(0, Math.min(100, (score / maxScore) * 100));
  };

  return (
    <div className="card">
      <div className="card-header">
        <h3 className="card-title">网格交易适应性评估</h3>
        <div className={`flex items-center space-x-2 ${getAdaptabilityClass(data.is_suitable)}`}>
          {getStatusIcon(data.is_suitable)}
          <span className="font-medium">
            {data.is_suitable ? '适合' : '不适合'}
          </span>
        </div>
      </div>

      {/* 评分圆环 */}
      <div className="flex items-center justify-center mb-6">
        <div className="relative">
          <svg className="w-32 h-32 transform -rotate-90">
            <circle
              cx="64"
              cy="64"
              r="56"
              stroke="#e5e7eb"
              strokeWidth="8"
              fill="none"
            />
            <circle
              cx="64"
              cy="64"
              r="56"
              stroke={data.score >= 80 ? '#22c55e' : data.score >= 60 ? '#f59e0b' : '#ef4444'}
              strokeWidth="8"
              fill="none"
              strokeDasharray={`${(data.score / 100) * 351.86} 351.86`}
              strokeLinecap="round"
            />
          </svg>
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center">
              <div className={`text-2xl font-bold ${getScoreColor(data.score)}`}>
                {data.score}
              </div>
              <div className="text-sm text-gray-600">/ 100</div>
            </div>
          </div>
        </div>
      </div>

      {/* 评估维度 - 使用实际维度得分 (4个维度，总分100分) */}
      <div className="space-y-4 mb-6">
        {/* 振幅评估 - 35分 */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-600">振幅评估</span>
          <div className="flex items-center space-x-2">
            <div className="w-20 bg-gray-200 rounded-full h-2">
              <div 
                className={`h-2 rounded-full ${getDimensionColor(getDimensionScore('amplitude'), 35)}`}
                style={{ width: `${getDimensionWidth(getDimensionScore('amplitude'), 35)}%` }}
              ></div>
            </div>
            <span className="text-xs text-gray-500">
              {getDimensionScore('amplitude')}/35分
            </span>
          </div>
        </div>
        
        {/* 波动率评估 - 30分 */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-600">波动率评估</span>
          <div className="flex items-center space-x-2">
            <div className="w-20 bg-gray-200 rounded-full h-2">
              <div 
                className={`h-2 rounded-full ${getDimensionColor(getDimensionScore('volatility'), 30)}`}
                style={{ width: `${getDimensionWidth(getDimensionScore('volatility'), 30)}%` }}
              ></div>
            </div>
            <span className="text-xs text-gray-500">
              {getDimensionScore('volatility')}/30分
            </span>
          </div>
        </div>
        
        {/* 市场特征 - 25分 */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-600">市场特征</span>
          <div className="flex items-center space-x-2">
            <div className="w-20 bg-gray-200 rounded-full h-2">
              <div 
                className={`h-2 rounded-full ${getDimensionColor(getDimensionScore('market'), 25)}`}
                style={{ width: `${getDimensionWidth(getDimensionScore('market'), 25)}%` }}
              ></div>
            </div>
            <span className="text-xs text-gray-500">
              {getDimensionScore('market')}/25分
            </span>
          </div>
        </div>
        
        {/* 流动性评估 - 10分 */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-600">流动性评估</span>
          <div className="flex items-center space-x-2">
            <div className="w-20 bg-gray-200 rounded-full h-2">
              <div 
                className={`h-2 rounded-full ${getDimensionColor(getDimensionScore('liquidity'), 10)}`}
                style={{ width: `${getDimensionWidth(getDimensionScore('liquidity'), 10)}%` }}
              ></div>
            </div>
            <span className="text-xs text-gray-500">
              {getDimensionScore('liquidity')}/10分
            </span>
          </div>
        </div>
      </div>



      {/* 汇总信息提示框 - 只显示recommendation，避免重复 */}
      {data.recommendation && (
        <div className={`p-4 rounded-lg border ${data.is_suitable ? 'bg-success-50 border-success-200' : 'bg-warning-50 border-warning-200'}`}>
          <div className="flex items-start space-x-2">
            {data.is_suitable ? (
              <CheckCircle className="w-5 h-5 text-success-600 mt-0.5 flex-shrink-0" />
            ) : (
              <AlertTriangle className="w-5 h-5 text-warning-600 mt-0.5 flex-shrink-0" />
            )}
            <div className="flex-1">
              <div className="text-sm text-gray-800 whitespace-pre-line">
                {data.recommendation}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default AdaptabilityCard
