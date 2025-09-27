import React from "react";
import { Activity } from "lucide-react";

/**
 * 频率偏好选择组件
 * 负责投资频率偏好的选择
 */
export default function RiskSelector({ value, onChange }) {
  const riskOptions = [
    { value: "低频", label: "低频型", desc: "潜心等待机会浮现", color: "green" },
    { value: "均衡", label: "均衡型", desc: "稳中求进平衡布局", color: "blue" },
    { value: "高频", label: "高频型", desc: "频繁出手波浪穿梭", color: "red" },
  ];

  return (
    <div>
      <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-3">
        <Activity className="w-4 h-4" />
        频率偏好
      </label>
      <div className="grid grid-cols-3 gap-3">
        {riskOptions.map((option) => (
          <label
            key={option.value}
            className={`p-4 border rounded-lg cursor-pointer transition-colors ${
              value === option.value
                ? `border-${option.color}-300 bg-${option.color}-50`
                : "border-gray-200 hover:border-gray-300"
            }`}
          >
            <input
              type="radio"
              name="riskPreference"
              value={option.value}
              checked={value === option.value}
              onChange={(e) => onChange(e.target.value)}
              className="sr-only"
            />
            <div className="font-medium text-gray-900">{option.label}</div>
            <div className="text-sm text-gray-600">{option.desc}</div>
          </label>
        ))}
      </div>
    </div>
  );
}
