import React from 'react';
import { Shield } from 'lucide-react';

/**
 * 风险偏好选择组件
 * 负责投资风险偏好的选择
 */
export default function RiskSelector({ value, onChange }) {
  const riskOptions = [
    { value: '保守', label: '保守型', desc: '耐心低频交易', color: 'green' },
    { value: '稳健', label: '稳健型', desc: '平衡机会风险', color: 'blue' },
    { value: '激进', label: '激进型', desc: '更多成交机会', color: 'red' }
  ];

  return (
    <div>
      <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-3">
        <Shield className="w-4 h-4" />
        风险偏好
      </label>
      <div className="grid grid-cols-3 gap-3">
        {riskOptions.map(option => (
          <label
            key={option.value}
            className={`p-4 border rounded-lg cursor-pointer transition-colors ${
              value === option.value
                ? `border-${option.color}-300 bg-${option.color}-50`
                : 'border-gray-200 hover:border-gray-300'
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