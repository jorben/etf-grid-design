import React from 'react'
import { DatabaseZap, Waypoints, Brain } from 'lucide-react'

const Header = () => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="flex items-center justify-center w-10 h-10 bg-primary-600 rounded-lg">
              <Waypoints className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">
                ETF网格策略设计
              </h1>
              <p className="text-sm text-gray-600">
                便捷的ETF的量化投资策略分析工具
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-6">
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <DatabaseZap className="w-4 h-4" />
              <span>基于数据</span>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <Brain className="w-4 h-4" />
              <span>智能算法</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
