import React from "react";
import { Cpu, ThermometerSun, TrendingUp } from "lucide-react";

/**
 * 特性卡片组件
 * @description 展示系统的核心特性
 */
export default function FeatureCards() {
  const features = [
    {
      icon: Cpu,
      title: "ATR算法核心",
      description:
        "采用平均真实波幅算法，动态适应市场波动，考虑跳空因素，比传统方法更精确",
      bgColor: "bg-blue-50",
      iconColor: "text-blue-700",
      iconBg: "bg-blue-200",
    },
    {
      icon: ThermometerSun,
      title: "标的适宜度评估",
      description:
        "振幅、波动率、市场特征、流动性四个维度量化评分，科学评估标的适宜度",
      bgColor: "bg-green-50",
      iconColor: "text-green-700",
      iconBg: "bg-green-200",
    },
    {
      icon: TrendingUp,
      title: "智能化策略",
      description: "智能网格参数计算、资金分配优化、策略分析，提供完整策略方案",
      bgColor: "bg-purple-50",
      iconColor: "text-purple-700",
      iconBg: "bg-purple-200",
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {features.map((feature, index) => (
        <div
          key={index}
          className={`text-center p-6 ${feature.bgColor} rounded-lg`}
        >
          <div
            className={`w-12 h-12 ${feature.iconBg} rounded-full flex items-center justify-center mx-auto mb-4`}
          >
            <feature.icon className={`w-6 h-6 ${feature.iconColor}`} />
          </div>
          <h3 className="font-semibold text-gray-900 mb-2">{feature.title}</h3>
          <p className="text-sm text-gray-600">{feature.description}</p>
        </div>
      ))}
    </div>
  );
}
