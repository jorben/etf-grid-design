import React, { useState, useEffect } from 'react'
import { useParams, useLocation, useNavigate, useSearchParams } from 'react-router-dom'
import Header from '../components/Header'
import ResultsPanel from '../components/ResultsPanel'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorMessage from '../components/ErrorMessage'
import { analyzeETF } from '../services/api'

const AnalysisPage = () => {
  const { etfCode } = useParams()
  const location = useLocation()
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  
  const [analysisResult, setAnalysisResult] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // 参数验证和默认值配置
  const validateAndGetParams = () => {
    // 默认值配置（与InputForm保持一致）
    const defaults = {
      frequency: 'low',
      initial_capital: 100000
    }

    // 验证交易频率参数
    const validateFrequency = (freq) => {
      const validFrequencies = ['low', 'medium', 'high']
      return validFrequencies.includes(freq) ? freq : defaults.frequency
    }

    // 验证初始资金参数
    const validateCapital = (capital) => {
      const numCapital = parseFloat(capital)
      if (isNaN(numCapital) || numCapital < 10000 || numCapital > 10000000) {
        return defaults.initial_capital
      }
      return numCapital
    }

    return { validateFrequency, validateCapital, defaults }
  }

  // 从多个来源获取表单数据，优先级：URL参数 > 路由state > 默认值
  const getFormData = () => {
    const { validateFrequency, validateCapital, defaults } = validateAndGetParams()

    // 优先级1：从路由state获取（表单提交过来的完整数据）
    if (location.state?.formData) {
      return location.state.formData
    }

    // 优先级2：从URL查询参数获取
    const urlFrequency = searchParams.get('frequency')
    const urlCapital = searchParams.get('capital')

    // 构建参数对象，缺失的参数使用默认值
    const formData = {
      etf_code: etfCode,
      frequency: urlFrequency ? validateFrequency(urlFrequency) : defaults.frequency,
      initial_capital: urlCapital ? validateCapital(urlCapital) : defaults.initial_capital
    }

    // 如果URL参数不完整或无效，更新URL以反映实际使用的参数
    const shouldUpdateUrl = (
      !urlFrequency || 
      !urlCapital || 
      validateFrequency(urlFrequency) !== urlFrequency ||
      validateCapital(urlCapital) !== parseFloat(urlCapital)
    )

    if (shouldUpdateUrl) {
      // 使用replace避免在浏览器历史中创建新条目
      const newSearchParams = new URLSearchParams()
      newSearchParams.set('frequency', formData.frequency)
      newSearchParams.set('capital', formData.initial_capital.toString())
      
      // 异步更新URL，避免在渲染过程中导航
      setTimeout(() => {
        navigate(`/analysis/${etfCode}?${newSearchParams.toString()}`, { 
          replace: true,
          state: location.state // 保持原有的state
        })
      }, 0)
    }

    return formData
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
              © 2025 Etfer.top
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default AnalysisPage