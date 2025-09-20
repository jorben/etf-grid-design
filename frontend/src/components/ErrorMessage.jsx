import React from 'react'
import { AlertCircle, RefreshCw, Home } from 'lucide-react'

const ErrorMessage = ({ message, onRetry, onReset }) => {
  return (
    <div className="card border-danger-200 bg-danger-50">
      <div className="flex items-start">
        <AlertCircle className="w-6 h-6 text-danger-600 mt-0.5 flex-shrink-0" />
        <div className="ml-3 flex-1">
          <h3 className="text-lg font-medium text-danger-900 mb-2">
            分析失败
          </h3>
          <p className="text-danger-800 mb-4">
            {message}
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
            {onReset && (
              <button
                onClick={onReset}
                className="btn-secondary inline-flex items-center"
              >
                <Home className="w-4 h-4 mr-2" />
                返回首页
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
  )
}

export default ErrorMessage
