import React from 'react'
import { Loader2 } from 'lucide-react'

const LoadingSpinner = ({ message = '加载中...', size = 'large' }) => {
  const sizeClasses = {
    small: 'w-4 h-4',
    medium: 'w-8 h-8',
    large: 'w-12 h-12'
  }

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
