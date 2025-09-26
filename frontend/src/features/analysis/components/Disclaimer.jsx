import React from "react";
import { AlertTriangle } from "lucide-react";

/**
 * 免责声明组件
 * 负责显示投资风险提示和免责声明
 */
export default function Disclaimer() {
  return (
    <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-lg">
      <div className="flex items-start gap-2">
        <AlertTriangle className="w-5 h-5 text-yellow-600 mt-0.5 flex-shrink-0" />
        <div className="text-sm text-yellow-800">
          <p className="font-medium mb-1">重要声明</p>
          <p>
            本分析基于历史数据和数学模型，仅供投资参考，不构成投资建议。
            实际投资效果可能与预测存在差异，投资有风险，入市需谨慎。
            请根据自身风险承受能力谨慎决策。
          </p>
        </div>
      </div>
    </div>
  );
}
