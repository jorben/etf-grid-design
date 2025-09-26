import React from "react";
import { XCircle, AlertTriangle } from "lucide-react";

/**
 * 错误状态组件
 * 负责显示分析失败或数据不完整的错误状态
 */
export default function ErrorState({
  type = "error",
  message,
  onBackToInput,
  onReAnalysis,
}) {
  const isDataIncomplete = type === "data_incomplete";

  return (
    <div className="bg-white rounded-xl shadow-lg p-8 text-center">
      <div
        className={`w-16 h-16 ${isDataIncomplete ? "bg-yellow-100" : "bg-red-100"} rounded-full flex items-center justify-center mx-auto mb-4`}
      >
        {isDataIncomplete ? (
          <AlertTriangle className="w-8 h-8 text-yellow-600" />
        ) : (
          <XCircle className="w-8 h-8 text-red-600" />
        )}
      </div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">
        {isDataIncomplete ? "数据不完整" : "分析失败"}
      </h3>
      <p className="text-gray-600 mb-6">{message}</p>
      <div className="flex justify-center gap-4">
        <button
          onClick={onBackToInput}
          className="px-6 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
        >
          返回设置
        </button>
        <button
          onClick={() => onReAnalysis && onReAnalysis()}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          重新分析
        </button>
      </div>
    </div>
  );
}
