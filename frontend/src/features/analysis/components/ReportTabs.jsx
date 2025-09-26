import React from "react";
import { Eye, ThermometerSun, Grid3X3 } from "lucide-react";

/**
 * 报告标签页导航组件
 * 负责标签页的导航和切换
 */
export default function ReportTabs({ activeTab, onTabChange }) {
  const tabs = [
    { id: "overview", label: "概览", icon: <Eye className="w-4 h-4" /> },
    {
      id: "suitability",
      label: "适宜度评估",
      icon: <ThermometerSun className="w-4 h-4" />,
    },
    {
      id: "strategy",
      label: "网格策略",
      icon: <Grid3X3 className="w-4 h-4" />,
    },
  ];

  return (
    <div className="border-b border-gray-200">
      <nav className="flex space-x-8 px-6">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            className={`flex items-center gap-2 py-4 px-2 border-b-2 font-medium text-sm transition-colors ${
              activeTab === tab.id
                ? "border-blue-500 text-blue-600"
                : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
            }`}
          >
            {tab.icon}
            {tab.label}
          </button>
        ))}
      </nav>
    </div>
  );
}
