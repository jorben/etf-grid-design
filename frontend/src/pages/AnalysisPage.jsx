import React, { useState, useEffect } from 'react'
import { useParams, useLocation, useNavigate } from 'react-router-dom'
import Header from '../components/Header'
import ResultsPanel from '../components/ResultsPanel'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorMessage from '../components/ErrorMessage'
import { analyzeETF } from '../services/api'

const AnalysisPage = () => {
  const { etfCode } = useParams()
  const location = useLocation()
  const navigate = useNavigate()
  
  const [analysisResult, setAnalysisResult] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // 从路由state获取表单数据，如果没有则使用默认值
  const getFormData = () => {
    if (location.state?.formData) {
      return location.state.formData
    }
    
    // 默认参数，用于直接访问URL的情况
    return {
      etf_code: etfCode,
      frequency: 'medium',
      initial_capital: 10000
    }
  }

  const performAnalysis = async () => {
    setLoading(true)
    setError(null)
    setAnalysisResult(null)

    try {
      const formData = getFormData()
      const result = await analyzeETF(formData)
      setAnalysisResult(result)
    } catch (err) {
      setError(err.message || '分析过程中发生错误')
    } finally {
      setLoading(false)
    }
  }

  // 页面加载时自动开始分析
  useEffect(() => {
    if (etfCode) {
      performAnalysis()
    } else {
      setError('ETF代码无效')
      setLoading(false)
    }
  }, [etfCode])

  const handleReset = () => {
    navigate('/')
  }

  const handleNewAnalysis = () => {
    navigate('/')
  }

  const handleRetry = () => {
    performAnalysis()
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="container mx-auto px-4 py-8 max-w-7xl">
        {loading && (
          <div className="flex justify-center items-center min-h-[400px]">
            <LoadingSpinner 
              message={`正在分析ETF ${etfCode}，请稍候...`}
              error={error}
              onRetry={handleRetry}
            />
          </div>
        )}

        {error && !loading && (
          <div className="max-w-2xl mx-auto">
            <ErrorMessage 
              message={error} 
              onRetry={handleRetry}
              onReset={handleReset}
            />
          </div>
        )}

        {analysisResult && !loading && !error && (
          <ResultsPanel 
            result={analysisResult} 
            onReset={handleReset}
            onNewAnalysis={handleNewAnalysis}
          />
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
              © 2024
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default AnalysisPage