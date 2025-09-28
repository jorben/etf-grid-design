import React, { useState } from "react";
import { AlertTriangle } from "lucide-react";

/**
 * 免责声明弹窗组件
 * 用于首次使用时显示免责声明，用户必须同意才能继续
 */
const DisclaimerModal = ({ isOpen, onAccept, onCancel }) => {
  const [isChecked, setIsChecked] = useState(false);

  if (!isOpen) return null;

  const handleAccept = () => {
    if (isChecked) {
      onAccept();
    }
  };

  const disclaimerText = `本工具所有数据及分析结果仅供学习、研究之用，不构成任何形式的投资建议或交易诱导。金融市场存在极高风险，任何投资决策都应基于您本人的独立判断。用户据此工具提供的信息进行的任何投资操作，其一切后果由用户自行承担，本工具及作者不承担任何法律责任和经济赔偿责任。`;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      {/* 背景遮罩 */}
      <div className="fixed inset-0 bg-black bg-opacity-50 transition-opacity"></div>
      
      {/* 弹窗容器 */}
      <div className="flex min-h-full items-center justify-center p-4">
        <div className="relative bg-white rounded-xl shadow-lg max-w-lg w-full mx-4 transform transition-all">
          {/* 弹窗内容 */}
          <div className="p-6">
            {/* 标题区域 - 与 ParameterForm 保持一致的样式 */}
            <div className="flex items-center gap-3 mb-6">
              <div className="p-2 bg-orange-100 rounded-lg">
                <AlertTriangle className="w-6 h-6 text-orange-600" />
              </div>
              <div>
                <h3 className="text-xl font-bold text-gray-900">免责声明</h3>
                <p className="text-sm text-gray-600">
                  请仔细阅读以下重要声明
                </p>
              </div>
            </div>

            {/* 免责声明内容 */}
            <div className="mb-6">
              <div className="p-4 border border-gray-200 rounded-lg bg-gray-50">
                <p className="text-sm text-gray-700 leading-relaxed">
                  {disclaimerText}
                </p>
              </div>
            </div>

            {/* 确认复选框 */}
            <div className="mb-6">
              <label className="flex items-center gap-3 p-4 rounded-lg cursor-pointer hover:border-gray-300 transition-colors">
                <input
                  type="checkbox"
                  checked={isChecked}
                  onChange={(e) => setIsChecked(e.target.checked)}
                  className="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                />
                <span className="text-sm text-gray-700">
                  我已阅读并理解上述声明，同意承担使用本工具的风险和责任
                </span>
              </label>
            </div>

            {/* 按钮区域 */}
            <div className="flex gap-3">
              <button
                onClick={onCancel}
                className="flex-1 py-3 px-4 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors font-medium"
              >
                取消
              </button>
              <button
                onClick={handleAccept}
                disabled={!isChecked}
                className="flex-1 py-3 px-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
              >
                同意并继续
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DisclaimerModal;