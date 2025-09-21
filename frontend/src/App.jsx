import React, { useState } from 'react'
import Header from './components/Header'
import InputForm from './components/InputForm'
import ResultsPanel from './components/ResultsPanel'
import LoadingSpinner from './components/LoadingSpinner'
import ErrorMessage from './components/ErrorMessage'
import { analyzeETF } from './services/api'
import './App.css'

function App() {
  const [analysisResult, setAnalysisResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleAnalyze = async (formData) => {
    setLoading(true)
    setError(null)
    setAnalysisResult(null)

    try {
      const result = await analyzeETF(formData)
      setAnalysisResult(result)
      setError(null) // 成功后清除错误
    } catch (err) {
      setError(err.message || '分析过程中发生错误')
      // 保持错误状态，但停止loading
    } finally {
      // 无论成功还是失败，都要停止loading
      setLoading(false)
    }
  }

  const handleReset = () => {
    setAnalysisResult(null)
    setError(null)
  }

  // 定义应用状态
  const getCurrentState = () => {
    if (loading) {
      return 'loading' // 加载状态，显示LoadingSpinner
    }
    if (error && !analysisResult) {
      return 'error' // 错误状态，显示错误信息
    }
    if (analysisResult) {
      return 'result' // 结果状态，显示分析结果
    }
    return 'input' // 输入状态，显示输入表单
  }

  const currentState = getCurrentState()

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="container mx-auto px-4 py-8 max-w-7xl">
        {currentState === 'input' && (
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

        {currentState === 'loading' && (
          <div className="flex justify-center items-center min-h-[400px]">
            <LoadingSpinner 
              message="正在分析ETF数据，请稍候..." 
              error={error}
              onRetry={() => {
                setError(null)
                // 清除错误后，用户可以通过重新提交表单来重试
              }}
            />
          </div>
        )}

        {currentState === 'error' && (
          <div className="max-w-2xl mx-auto">
            <ErrorMessage 
              message={error} 
              onRetry={() => {
                setError(null)
                // 清除错误，回到输入状态
              }}
              onReset={handleReset}
            />
          </div>
        )}

        {currentState === 'result' && (
          <ResultsPanel 
            result={analysisResult} 
            onReset={handleReset}
            onNewAnalysis={() => {
              setAnalysisResult(null)
              setError(null)
            }}
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

export default App
