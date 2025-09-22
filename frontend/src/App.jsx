import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import ParameterForm from './components/ParameterForm';
import AnalysisReport from './components/AnalysisReport';
import { analyzeETF } from './services/api';
import { Zap, BarChart3, Target, TrendingUp, Github, ExternalLink } from 'lucide-react';
import './App.css';

function App() {
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState('input'); // 'input' | 'analysis'

  // 处理分析请求
  const handleAnalysis = async (parameters) => {
    setLoading(true);
    setCurrentStep('analysis');
    
    try {
      const response = await analyzeETF(parameters);
      
      if (response.success) {
        setAnalysisData(response.data);
      } else {
        throw new Error(response.error || '分析失败');
      }
    } catch (error) {
      console.error('分析请求失败:', error);
      // 显示错误信息
      setAnalysisData({
        error: true,
        message: error.message || '分析请求失败，请稍后重试'
      });
    } finally {
      setLoading(false);
    }
  };

  // 返回参数输入页面
  const handleBackToInput = () => {
    setCurrentStep('input');
    setAnalysisData(null);
  };

  // 重新分析
  const handleReAnalysis = (parameters) => {
    handleAnalysis(parameters);
  };

  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
        {/* 顶部导航 */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              {/* Logo和标题 */}
              <div className="flex items-center gap-3">
                <div className="p-2 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg">
                  <Zap className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h1 className="text-xl font-bold text-gray-900">ETF网格交易策略分析系统</h1>
                  <p className="text-sm text-gray-600">基于ATR算法的智能网格交易策略设计</p>
                </div>
              </div>

              {/* 导航链接 */}
              <div className="flex items-center gap-4">
                <a
                  href="https://github.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 px-3 py-2 text-gray-600 hover:text-gray-900 transition-colors"
                >
                  <Github className="w-4 h-4" />
                  <span className="text-sm">GitHub</span>
                </a>
                <a
                  href="/docs"
                  className="flex items-center gap-2 px-3 py-2 text-gray-600 hover:text-gray-900 transition-colors"
                >
                  <ExternalLink className="w-4 h-4" />
                  <span className="text-sm">文档</span>
                </a>
              </div>
            </div>
          </div>
        </header>

        {/* 主要内容区域 */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Routes>
            <Route path="/" element={
              <div className="space-y-8">
                {/* 系统介绍 */}
                {currentStep === 'input' && (
                  <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
                    <div className="text-center mb-8">
                      <div className="flex justify-center gap-4 mb-6">
                        <div className="p-3 bg-blue-100 rounded-lg">
                          <BarChart3 className="w-8 h-8 text-blue-600" />
                        </div>
                        <div className="p-3 bg-green-100 rounded-lg">
                          <Target className="w-8 h-8 text-green-600" />
                        </div>
                        <div className="p-3 bg-purple-100 rounded-lg">
                          <TrendingUp className="w-8 h-8 text-purple-600" />
                        </div>
                      </div>
                      <h2 className="text-3xl font-bold text-gray-900 mb-4">
                        智能ETF网格交易策略分析
                      </h2>
                      <p className="text-lg text-gray-600 max-w-3xl mx-auto">
                        基于ATR算法的专业网格交易策略设计系统，通过分析ETF历史数据，
                        结合您的投资偏好，自动计算最适合的网格交易参数，并提供详细的策略分析和收益预测。
                      </p>
                    </div>

                    {/* 核心特性 */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                      <div className="text-center p-6 bg-blue-50 rounded-lg">
                        <div className="w-12 h-12 bg-blue-200 rounded-full flex items-center justify-center mx-auto mb-4">
                          <BarChart3 className="w-6 h-6 text-blue-700" />
                        </div>
                        <h3 className="font-semibold text-gray-900 mb-2">ATR算法核心</h3>
                        <p className="text-sm text-gray-600">
                          采用平均真实波幅算法，动态适应市场波动，考虑跳空因素，比传统方法更精确
                        </p>
                      </div>

                      <div className="text-center p-6 bg-green-50 rounded-lg">
                        <div className="w-12 h-12 bg-green-200 rounded-full flex items-center justify-center mx-auto mb-4">
                          <Target className="w-6 h-6 text-green-700" />
                        </div>
                        <h3 className="font-semibold text-gray-900 mb-2">4维度评估</h3>
                        <p className="text-sm text-gray-600">
                          振幅、波动率、市场特征、流动性四个维度量化评分，科学评估标的适合度
                        </p>
                      </div>

                      <div className="text-center p-6 bg-purple-50 rounded-lg">
                        <div className="w-12 h-12 bg-purple-200 rounded-full flex items-center justify-center mx-auto mb-4">
                          <TrendingUp className="w-6 h-6 text-purple-700" />
                        </div>
                        <h3 className="font-semibold text-gray-900 mb-2">智能策略</h3>
                        <p className="text-sm text-gray-600">
                          智能网格参数计算、资金分配优化、历史回测分析，提供完整策略方案
                        </p>
                      </div>
                    </div>
                  </div>
                )}

                {/* 参数输入表单 */}
                {currentStep === 'input' && (
                  <ParameterForm 
                    onAnalysis={handleAnalysis}
                    loading={loading}
                  />
                )}

                {/* 分析报告 */}
                {currentStep === 'analysis' && (
                  <AnalysisReport
                    data={analysisData}
                    loading={loading}
                    onBackToInput={handleBackToInput}
                    onReAnalysis={handleReAnalysis}
                  />
                )}
              </div>
            } />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>

        {/* 底部信息 */}
        <footer className="bg-white border-t border-gray-200 mt-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {/* 系统信息 */}
              <div>
                <h3 className="font-semibold text-gray-900 mb-4">系统特点</h3>
                <ul className="space-y-2 text-sm text-gray-600">
                  <li>• 基于ATR算法的科学分析</li>
                  <li>• 4维度量化评分体系</li>
                  <li>• 智能网格参数计算</li>
                  <li>• 历史回测与收益预测</li>
                </ul>
              </div>

              {/* 风险提示 */}
              <div>
                <h3 className="font-semibold text-gray-900 mb-4">风险提示</h3>
                <ul className="space-y-2 text-sm text-gray-600">
                  <li>• 历史数据不代表未来表现</li>
                  <li>• 投资有风险，入市需谨慎</li>
                  <li>• 本系统仅供参考，不构成投资建议</li>
                  <li>• 请根据自身情况谨慎决策</li>
                </ul>
              </div>

              {/* 技术支持 */}
              <div>
                <h3 className="font-semibold text-gray-900 mb-4">技术信息</h3>
                <ul className="space-y-2 text-sm text-gray-600">
                  <li>• 数据源：Tushare金融数据</li>
                  <li>• 算法：ATR + ADX + 统计分析</li>
                  <li>• 更新频率：每日收盘后</li>
                  <li>• 版本：v1.0.0</li>
                </ul>
              </div>
            </div>

            <div className="border-t border-gray-200 mt-8 pt-8 text-center">
              <p className="text-sm text-gray-500">
                © 2024 ETF网格交易策略分析系统. 本系统仅供学习和研究使用，不构成投资建议。
              </p>
            </div>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
