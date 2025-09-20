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

      {/* 评估维度 */}
      <div className="space-y-4 mb-6">
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-600">振幅评估</span>
          <div className="flex items-center space-x-2">
            <div className="w-20 bg-gray-200 rounded-full h-2">
              <div 
                className={`h-2 rounded-full ${data.score >= 30 ? 'bg-success-500' : data.score >= 20 ? 'bg-warning-500' : 'bg-danger-500'}`}
                style={{ width: `${Math.min(100, (data.score / 100) * 120)}%` }}
              ></div>
            </div>
            <span className="text-xs text-gray-500">30分</span>
          </div>
        </div>
        
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-600">波动率评估</span>
          <div className="flex items-center space-x-2">
            <div className="w-20 bg-gray-200 rounded-full h-2">
              <div 
                className={`h-2 rounded-full ${data.score >= 55 ? 'bg-success-500' : data.score >= 40 ? 'bg-warning-500' : 'bg-danger-500'}`}
                style={{ width: `${Math.min(100, ((data.score - 30) / 100) * 120)}%` }}
              ></div>
            </div>
            <span className="text-xs text-gray-500">25分</span>
          </div>
        </div>
        
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-600">市场特征</span>
          <div className="flex items-center space-x-2">
            <div className="w-20 bg-gray-200 rounded-full h-2">
              <div 
                className={`h-2 rounded-full ${data.score >= 75 ? 'bg-success-500' : data.score >= 60 ? 'bg-warning-500' : 'bg-danger-500'}`}
                style={{ width: `${Math.min(100, ((data.score - 55) / 100) * 120)}%` }}
              ></div>
            </div>
            <span className="text-xs text-gray-500">20分</span>
          </div>
        </div>
        
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-600">流动性评估</span>
          <div className="flex items-center space-x-2">
            <div className="w-20 bg-gray-200 rounded-full h-2">
              <div 
                className={`h-2 rounded-full ${data.score >= 90 ? 'bg-success-500' : data.score >= 80 ? 'bg-warning-500' : 'bg-danger-500'}`}
                style={{ width: `${Math.min(100, ((data.score - 75) / 100) * 120)}%` }}
              ></div>
            </div>
            <span className="text-xs text-gray-500">15分</span>
          </div>
        </div>
      </div>

      {/* 推荐理由 */}
      {data.recommendation && (
        <div className={`p-4 rounded-lg ${getScoreBackground(data.score)}`}>
          <div className="flex items-start space-x-2">
            <Info className="w-5 h-5 text-gray-600 mt-0.5 flex-shrink-0" />
            <div className="text-sm text-gray-800 whitespace-pre-line">
              {data.recommendation}
            </div>
          </div>
        </div>
      )}

      {/* 警告信息 */}
      {data.warnings && data.warnings.length > 0 && (
        <div className="bg-warning-50 border border-warning-200 rounded-lg p-4">
          <div className="flex items-start space-x-2">
            <AlertTriangle className="w-5 h-5 text-warning-600 mt-0.5 flex-shrink-0" />
            <div>
              <h4 className="text-sm font-medium text-warning-800 mb-2">注意事项</h4>
              <ul className="text-sm text-warning-700 space-y-1">
                {data.warnings.map((warning, index) => (
                  <li key={index} className="flex items-start">
                    <span className="w-1 h-1 bg-warning-400 rounded-full mt-2 mr-2 flex-shrink-0"></span>
                    {warning}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* 不适合的原因 */}
      {!data.is_suitable && data.reasons && data.reasons.length > 0 && (
        <div className="bg-danger-50 border border-danger-200 rounded-lg p-4">
          <div className="flex items-start space-x-2">
            <XCircle className="w-5 h-5 text-danger-600 mt-0.5 flex-shrink-0" />
            <div>
              <h4 className="text-sm font-medium text-danger-800 mb-2">主要原因</h4>
              <ul className="text-sm text-danger-700 space-y-1">
                {data.reasons.map((reason, index) => (
                  <li key={index} className="flex items-start">
                    <span className="w-1 h-1 bg-danger-400 rounded-full mt-2 mr-2 flex-shrink-0"></span>
                    {reason}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default AdaptabilityCard
