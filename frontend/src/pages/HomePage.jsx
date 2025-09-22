import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Header from '../components/Header'
import InputForm from '../components/InputForm'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorMessage from '../components/ErrorMessage'
import { analyzeETF } from '../services/api'

const HomePage = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  const handleAnalyze = async (formData) => {
    setLoading(true)
    setError(null)

    try {
      // 构建URL查询参数，包含交易频率和初始资金
      const searchParams = new URLSearchParams()
      searchParams.set('frequency', formData.frequency)
      searchParams.set('capital', formData.initial_capital.toString())
      
      // 跳转到分析页面，URL包含完整参数，同时保持state用于向后兼容
      navigate(`/analysis/${formData.etf_code}?${searchParams.toString()}`, { 
        state: { formData } 
      })
    } catch (err) {
      setError(err.message || '跳转过程中发生错误')
      setLoading(false)
    }
  }

  const handleRetry = () => {
    setError(null)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="container mx-auto px-4 py-8 max-w-7xl">
        {loading ? (
          <div className="flex justify-center items-center min-h-[400px]">
            <LoadingSpinner 
              message="正在跳转到分析页面..." 
              error={error}
              onRetry={handleRetry}
            />
          </div>
        ) : error ? (
          <div className="max-w-2xl mx-auto">
            <ErrorMessage 
              message={error} 
              onRetry={handleRetry}
              onReset={handleRetry}
            />
          </div>
        ) : (
          <div className="max-w-2xl mx-auto">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                ETF网格交易策略设计
              </h2>
              <p className="text-lg text-gray-600">
                基于交易数据和专业算法，为您的ETF投资提供科学的网格交易策略参数
              </p>
            </div>
            
            <InputForm onSubmit={handleAnalyze} />
          </div>
        )}
      </main>

      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center text-gray-600">
            <p className="mb-2">
              <strong>免责声明：</strong>
              本工具提供的分析结果仅供参考，不构成投资建议。投资有风险，入市需谨慎。
            </p>
            <p className="text-sm">
              © 2025 Etfer.top
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default HomePage