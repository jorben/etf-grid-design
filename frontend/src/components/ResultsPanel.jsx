import React, { useState } from 'react'
import { RefreshCw, Share2, ArrowLeft, LayoutDashboard, ScanBarcode, Grid3x3 } from 'lucide-react'
import ETFInfoCard from './results/ETFInfoCard'
import GridParametersCard from './report/GridParametersCard'
import AdaptabilityCard from './results/AdaptabilityCard'
import AnalysisCard from './results/AnalysisCard'
import AdjustmentSuggestionsCard from './results/AdjustmentSuggestionsCard'

import { formatDate, formatCurrency, formatNumber, formatPercent, formatStepAmount } from '../services/api'

const ResultsPanel = ({ result, onReset, onNewAnalysis }) => {
  const [activeTab, setActiveTab] = useState('overview')
  
  const tabs = [
    { id: 'overview', label: '概览', icon: LayoutDashboard },
    { id: 'parameters', label: '网格参数', icon: Grid3x3 },
    { id: 'analysis', label: '详细分析', icon: ScanBarcode },
    { id: 'suggestions', label: '调整建议', icon: RefreshCw }
  ]

  const handleExport = () => {
    // 实现导出功能
    const data = JSON.stringify(result, null, 2)
    const blob = new Blob([data], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `ETF网格分析_${result.etf_info?.code || 'unknown'}_${formatDate(new Date()).replace(/[/:]/g, '-')}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const handleShare = () => {
    // 实现分享功能
    if (navigator.share) {
      navigator.share({
        title: 'ETF网格交易策略分析结果',
        text: `ETF ${result.etf_info?.code} 网格策略分析结果`,
        url: window.location.href
      })
    } else {
      // 复制到剪贴板
      navigator.clipboard.writeText(window.location.href)
      alert('链接已复制到剪贴板')
    }
  }

  return (
    <div className="space-y-6">
      {/* 顶部操作栏 */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <button
            onClick={onNewAnalysis}
            className="btn-secondary inline-flex items-center"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            重新分析
          </button>
          
          <div className="text-sm text-gray-600">
            分析时间: {formatDate(result.timestamp)}
          </div>
        </div>
        
        <div className="flex items-center space-x-3">
          {/*
          <button
            onClick={handleExport}
            className="btn-secondary inline-flex items-center"
          >
            <Download className="w-4 h-4 mr-2" />
            导出
          </button>
          */}
          <button
            onClick={handleShare}
            className="btn-secondary inline-flex items-center"
          >
            <Share2 className="w-4 h-4 mr-2" />
            分享
          </button>
        </div>
      </div>

      {/* 标签页导航 */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {tabs.map(tab => {
            const Icon = tab.icon
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`
                  group inline-flex items-center py-4 px-1 border-b-2 font-medium text-sm
                  ${activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }
                `}
              >
                <Icon className={`
                  w-5 h-5 mr-2
                  ${activeTab === tab.id ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500'}
                `} />
                {tab.label}
              </button>
            )
          })}
        </nav>
      </div>

      {/* 内容区域 */}
      <div className="space-y-6">
        {activeTab === 'overview' && (
          <>
            {/* 概览卡片 */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <ETFInfoCard data={result.etf_info} />
              <AdaptabilityCard data={result.adaptability} />
            </div>
            
            {/* 关键参数摘要 */}
            <div className="card">
              <h3 className="card-title mb-4">关键策略参数</h3>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <div className="text-2xl font-bold text-primary-600">
                    {result.grid_parameters?.grid_count || 0}
                  </div>
                  <div className="text-sm text-gray-600">区间内网格数</div>
                </div>
                
                {/* 根据网格类型动态展示步长重点 */}
                {result.grid_parameters?.grid_type === '等比' ? (
                  <>
                    <div className="text-center p-4 bg-gray-50 rounded-lg">
                      <div className="text-2xl font-bold text-primary-600">
                        {formatPercent(result.grid_parameters?.step_size_ratio * 100 || 0, 2)}
                      </div>
                      <div className="text-sm text-gray-600">步长比例</div>
                      <div className="text-xs text-gray-500 mt-1">
                        {formatStepAmount(result.grid_parameters?.step_size_amount || 0)}
                      </div>
                    </div>
                    
                    <div className="text-center p-4 bg-gray-50 rounded-lg">
                      <div className="text-lg font-semibold text-gray-700">
                        {formatStepAmount(result.grid_parameters?.step_size_amount || 0)}
                      </div>
                      <div className="text-sm text-gray-600">步长金额</div>
                    </div>
                  </>
                ) : (
                  <>
                    <div className="text-center p-4 bg-gray-50 rounded-lg">
                      <div className="text-2xl font-bold text-primary-600">
                        {formatStepAmount(result.grid_parameters?.step_size_amount || 0)}
                      </div>
                      <div className="text-sm text-gray-600">步长金额</div>
                      <div className="text-xs text-gray-500 mt-1">
                        {formatPercent(result.grid_parameters?.step_size_ratio * 100 || 0, 2)}
                      </div>
                    </div>
                    
                    <div className="text-center p-4 bg-gray-50 rounded-lg">
                      <div className="text-lg font-semibold text-gray-700">
                        {formatPercent(result.grid_parameters?.step_size_ratio * 100 || 0, 2)}
                      </div>
                      <div className="text-sm text-gray-600">步长比例</div>
                    </div>
                  </>
                )}
                
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <div className="text-2xl font-bold text-primary-600">
                    {formatCurrency(result.grid_parameters?.per_grid_amount || 0)}
                  </div>
                  <div className="text-sm text-gray-600">单笔金额</div>
                </div>
                
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <div className="text-2xl font-bold text-primary-600">
                    {formatNumber(result.grid_parameters?.per_grid_shares || 0)}
                  </div>
                  <div className="text-sm text-gray-600">单笔股数</div>
                </div>
                
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <div className="text-xl font-bold text-primary-600">
                    [{formatNumber(result.grid_parameters?.price_lower_bound || 0, 3)}, {formatNumber(result.grid_parameters?.price_upper_bound || 0, 3)}]
                  </div>
                  <div className="text-sm text-gray-600">价格区间</div>
                </div>
              </div>
            </div>


          </>
        )}

        {activeTab === 'parameters' && (
          <GridParametersCard data={result.grid_parameters} />
        )}

        {activeTab === 'analysis' && (
          <AnalysisCard data={result.analysis} />
        )}

        {activeTab === 'suggestions' && (
          <AdjustmentSuggestionsCard data={result.adjustment_suggestions} />
        )}
      </div>

      {/* 底部操作栏 */}
      <div className="flex items-center justify-between pt-6 border-t border-gray-200">
        <div className="text-sm text-gray-600">
          <strong>风险提示：</strong>
          网格交易存在风险，请根据自身风险承受能力谨慎操作
        </div>
        
        <button
          onClick={onReset}
          className="btn-primary"
        >
          开始新的分析
        </button>
      </div>
    </div>
  )
}

export default ResultsPanel
