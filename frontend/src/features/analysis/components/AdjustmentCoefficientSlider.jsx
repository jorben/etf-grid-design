import React from "react";
import { Sliders } from "lucide-react";

/**
 * 调节系数滑动调节器组件
 * 负责调节系数的选择和显示，范围0.0-2.0，默认1.0
 * 系数越大，频率系数越离散；系数越小，频率系数越聚拢
 */
export default function AdjustmentCoefficientSlider({ value, onChange }) {
  const handleSliderChange = (e) => {
    const newValue = parseFloat(e.target.value);
    onChange(newValue);
  };

  const getDescription = (coefficient) => {
    if (coefficient < 0.8) {
      return "频率偏好差异较小，三种模式更加接近";
    } else if (coefficient <= 1.2) {
      return "标准调节，平衡的频率差异";
    } else {
      return "频率偏好差异较大，模式区分更明显";
    }
  };

  const getColorClass = (coefficient) => {
    if (coefficient < 0.8 || coefficient > 1.2) {
      return "text-orange-600";
    }
    return "text-gray-600";
  };

  return (
    <div>
      <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-3">
        <Sliders className="w-4 h-4" />
        调节系数
      </label>
      
      <div className="bg-gray-50 rounded-lg p-4">
        {/* 当前值显示 */}
        <div className="flex justify-between items-center mb-3">
          <span className="text-sm font-medium text-gray-700">当前值:</span>
          <span className="text-lg font-bold text-blue-600">{value.toFixed(1)}</span>
        </div>

        {/* 滑动条 */}
        <div className="mb-3">
          <input
            type="range"
            min="0.0"
            max="2.0"
            step="0.1"
            value={value}
            onChange={handleSliderChange}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
            style={{
              background: `linear-gradient(to right, #3b82f6 0%, #3b82f6 ${(value / 2) * 100}%, #e5e7eb ${(value / 2) * 100}%, #e5e7eb 100%)`
            }}
          />
          
          {/* 刻度标记 */}
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>0.0</span>
            <span>1.0</span>
            <span>2.0</span>
          </div>
        </div>

        {/* 说明文字 */}
        <div className={`text-sm ${getColorClass(value)}`}>
          {getDescription(value)}
        </div>

        {/* 详细说明 */}
        <div className="text-xs text-gray-500 mt-2">
          <p>• 系数越大，频率偏好的结果差异越明显</p>
          <p>• 系数越小，频率偏好的结果趋于一致</p>
          <p>• 可以通过调节该系数获得更多差异化的方案（比如，调到最大系数后选择低频+高频的组合网格）</p>
        </div>
      </div>

      {/* 自定义样式 */}
      <style jsx>{`
        .slider::-webkit-slider-thumb {
          appearance: none;
          height: 20px;
          width: 20px;
          border-radius: 50%;
          background: #3b82f6;
          cursor: pointer;
          border: 2px solid #ffffff;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
        
        .slider::-moz-range-thumb {
          height: 20px;
          width: 20px;
          border-radius: 50%;
          background: #3b82f6;
          cursor: pointer;
          border: 2px solid #ffffff;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
      `}</style>
    </div>
  );
}