import React from "react";
import { Grid3X3 } from "lucide-react";

/**
 * 网格类型选择组件
 * 负责网格间距类型的选择
 */
export default function GridTypeSelector({ value, onChange }) {
  const gridTypes = [
    { value: "等比", label: "固定每笔比例", desc: "比例间距相等，推荐使用" },
    { value: "等差", label: "固定每笔金额", desc: "价格间距相等，适合新手" },
  ];

  return (
    <div>
      <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-3">
        <Grid3X3 className="w-4 h-4" />
        网格间距类型
      </label>
      <div className="grid grid-cols-2 gap-3">
        {gridTypes.map((option) => (
          <label
            key={option.value}
            className={`p-4 border rounded-lg cursor-pointer transition-colors ${
              value === option.value
                ? "border-blue-300 bg-blue-50"
                : "border-gray-200 hover:border-gray-300"
            }`}
          >
            <input
              type="radio"
              name="gridType"
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
