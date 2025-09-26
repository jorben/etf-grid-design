import React from "react";
import { Target } from "lucide-react";
import FeatureCards from "./FeatureCards";

/**
 * 首页英雄区域组件
 * @description 展示系统介绍和开始分析按钮
 * @param {Function} onStartAnalysis - 开始分析回调函数
 */
export default function HeroSection({ onStartAnalysis }) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 space-y-8 p-8">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          智能ETF网格交易策略分析
        </h2>
        <p className="text-lg text-gray-600 max-w-3xl mx-auto">
          基于ATR算法的专业网格交易策略设计系统，通过分析ETF历史数据，
          结合您的投资偏好，自动计算最适合的网格交易参数，并提供详细的策略分析和收益预测。
        </p>
      </div>

      <FeatureCards />

      {/* 开始分析按钮 */}
      <div className="text-center">
        <button
          onClick={onStartAnalysis}
          className="inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-indigo-700 transform hover:scale-105 transition-all duration-200 shadow-lg hover:shadow-xl"
        >
          <Target className="w-5 h-5" />
          选择标的，即刻分析
        </button>
      </div>
    </div>
  );
}
