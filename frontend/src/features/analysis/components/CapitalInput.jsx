import React from "react";
import { DollarSign } from "lucide-react";

/**
 * 投资资金输入组件
 * 负责资金金额输入和常用金额快选
 */
export default function CapitalInput({ value, onChange, error, presets = [] }) {
  const defaultPresets = [
    { value: 100000, label: "10万", popular: true },
    { value: 200000, label: "20万", popular: true },
    { value: 500000, label: "50万", popular: true },
    { value: 1000000, label: "100万", popular: true },
  ];

  const capitalPresets = presets.length > 0 ? presets : defaultPresets;

  return (
    <div>
      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3 mb-3">
        <label className="flex items-center gap-2 text-sm font-medium text-gray-700">
          <DollarSign className="w-4 h-4" />
          总投资资金量
        </label>

        {/* 常用金额 */}
        <div className="flex items-center">
          <span className="text-xs text-gray-500 mr-2">常用金额:</span>
          <div className="flex flex-wrap gap-2">
            {capitalPresets
              .filter((preset) => preset.popular)
              .map((preset) => (
                <button
                  key={preset.value}
                  type="button"
                  onClick={() => onChange(preset.value.toString())}
                  className={`px-2 py-1 text-xs rounded-full border transition-colors ${
                    value === preset.value.toString()
                      ? "bg-blue-100 border-blue-300 text-blue-700"
                      : "bg-gray-50 border-gray-200 text-gray-600 hover:bg-gray-100"
                  }`}
                >
                  {preset.label}
                </button>
              ))}
          </div>
        </div>
      </div>

      <div className="relative">
        <input
          type="number"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder="请输入投资金额（1万-100万）"
          className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
            error ? "border-red-300" : "border-gray-300"
          }`}
          min={10000}
          max={1000000}
          step={10000}
        />
        <div className="absolute right-3 top-3 text-gray-400">元</div>
        {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
      </div>
    </div>
  );
}
