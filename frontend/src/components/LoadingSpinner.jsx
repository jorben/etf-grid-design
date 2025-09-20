import React from 'react'
import { Loader2, AlertCircle, RefreshCw } from 'lucide-react'

const LoadingSpinner = ({ message = '加载中...', size = 'large', error = null, onRetry }) => {
  const sizeClasses = {
    small: 'w-4 h-4',
    medium: 'w-8 h-8',
    large: 'w-12 h-12'
  }

  // 如果有错误，显示错误状态
  if (error) {
    return (
      <div className="flex flex-col items-center justify-center p-8 max-w-2xl mx-auto">
        <div className="card border-danger-200 bg-danger-50 w-full">
          <div className="flex items-start">
            <AlertCircle className="w-6 h-6 text-danger-600 mt-0.5 flex-shrink-0" />
            <div className="ml-3 flex-1">
              <h3 className="text-lg font-medium text-danger-900 mb-2">
                分析失败
              </h3>
              <p className="text-danger-800 mb-4">
                {error}
              </p>
              
              <div className="flex flex-wrap gap-3">
                {onRetry && (
                  <button
                    onClick={onRetry}
                    className="btn-danger inline-flex items-center"
                  >
                    <RefreshCw className="w-4 h-4 mr-2" />
                    重试
                  </button>
                )}
              </div>
            </div>
          </div>
          
          {/* 常见错误提示 */}
          <div className="mt-6 pt-6 border-t border-danger-200">
            <h4 className="text-sm font-medium text-danger-900 mb-3">
              常见问题排查：
            </h4>
            <ul className="text-sm text-danger-800 space-y-2">
              <li className="flex items-start">
                <span className="w-2 h-2 bg-danger-400 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                <span>请检查ETF代码是否正确（6位数字）</span>
              </li>
              <li className="flex items-start">
                <span className="w-2 h-2 bg-danger-400 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                <span>确保网络连接正常</span>
              </li>
              <li className="flex items-start">
                <span className="w-2 h-2 bg-danger-400 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                <span>检查ETF是否有足够的历史数据</span>
              </li>
              <li className="flex items-start">
                <span className="w-2 h-2 bg-danger-400 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                <span>尝试使用其他ETF代码</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    )
  }

  // 正常加载状态
  return (
    <div className="flex flex-col items-center justify-center p-8">
      <div className={`${sizeClasses[size]} animate-spin`}>
        <Loader2 className="w-full h-full text-primary-600" />
      </div>
      {message && (
        <p className="mt-4 text-gray-600 text-center">
          {message}
          <span className="loading-dots"></span>
        </p>
      )}
    </div>
  )
}

export default LoadingSpinner
