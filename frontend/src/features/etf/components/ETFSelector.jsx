import React, { useState, useEffect } from 'react';
import { Search, TrendingUp } from 'lucide-react';
import ETFInfoSkeleton from './ETFInfoSkeleton';

/**
 * ETF选择器组件
 * 负责ETF代码输入、热门ETF选择、ETF信息展示
 */
export default function ETFSelector({ 
  value, 
  onChange, 
  error, 
  popularETFs = [],
  etfInfo,
  loading 
}) {
  const hotETFs = ['510300', '510500', '159915', '588000', '512480', '159819'];

  // 获取热门ETF列表
  useEffect(() => {
    fetch('/api/popular-etfs')
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          // 这里可以设置popularETFs，但通过props传递更合适
        }
      })
      .catch(err => console.error('获取热门ETF失败:', err));
  }, []);

  return (
    <div>
      <div className="flex justify-between items-center mb-3">
        <label className="flex items-center gap-2 text-sm font-medium text-gray-700">
          <Search className="w-4 h-4" />
          ETF标的选择
        </label>
        
        {/* 热门ETF */}
        <div className="flex items-center">
          <span className="text-xs text-gray-500 mr-2">热门ETF：</span>
          <div className="flex flex-wrap gap-2">
            {hotETFs.map(code => {
              const etf = popularETFs.find(e => e.code === code);
              return (
                <button
                  key={code}
                  type="button"
                  onClick={() => onChange(code)}
                  className={`px-3 py-1 text-xs rounded-full border transition-colors ${
                    value === code
                      ? 'bg-blue-100 border-blue-300 text-blue-700'
                      : 'bg-gray-50 border-gray-200 text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  {code} {etf?.name || ''}
                </button>
              );
            })}
          </div>
        </div>
      </div>

      <div className="relative">
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value.replace(/\D/g, '').slice(0, 6))}
          placeholder="请输入6位ETF代码，如：510300"
          className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
            error ? 'border-red-300' : 'border-gray-300'
          }`}
          maxLength={6}
        />
        
        {/* ETF信息区域 */}
        <div className="mt-2" style={{ minHeight: '80px' }}>
          {loading && <ETFInfoSkeleton />}
          
          {!loading && etfInfo && (
            <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
              <div className="flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-blue-600" />
                <span className="font-medium text-blue-800">{etfInfo.name}</span>
                <span className="text-sm text-blue-600">
                  ¥{etfInfo.current_price?.toFixed(3)} 
                  <span className={etfInfo.change_pct >= 0 ? 'text-red-600' : 'text-green-600'}>
                    ({etfInfo.change_pct >= 0 ? '+' : ''}{etfInfo.change_pct?.toFixed(2)}%)
                  </span>
                </span>
              </div>
              <p className="text-xs text-blue-600 mt-1">{etfInfo.management_company}</p>
            </div>
          )}
          
          {!loading && error && (
            <p className="mt-1 text-sm text-red-600">{error}</p>
          )}
        </div>
      </div>
    </div>
  );
}