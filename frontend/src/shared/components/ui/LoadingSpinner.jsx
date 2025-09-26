import React from "react";
import { Loader2, BarChart3, Target, TrendingUp, Zap } from "lucide-react";

const LoadingSpinner = ({
  message = "正在分析中...",
  progress = 0,
  showProgress = false,
}) => {
  const steps = [
    { icon: BarChart3, text: "获取ETF数据", color: "text-blue-600" },
    { icon: Target, text: "计算ATR指标", color: "text-green-600" },
    { icon: TrendingUp, text: "评估适宜度", color: "text-purple-600" },
    { icon: Zap, text: "生成策略参数", color: "text-orange-600" },
  ];

  const currentStep = Math.floor((progress / 100) * steps.length);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl shadow-2xl p-8 max-w-md w-full mx-4">
        {/* 主要加载动画 */}
        <div className="text-center mb-6">
          <div className="relative">
            <div className="w-16 h-16 mx-auto mb-4">
              <Loader2 className="w-16 h-16 text-blue-600 animate-spin" />
            </div>
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                <BarChart3 className="w-4 h-4 text-blue-600" />
              </div>
            </div>
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            {message}
          </h3>
          <p className="text-sm text-gray-600">
            基于ATR算法进行智能分析，请稍候...
          </p>
        </div>

        {/* 进度条 */}
        {showProgress && (
          <div className="mb-6">
            <div className="flex justify-between text-sm text-gray-600 mb-2">
              <span>分析进度</span>
              <span>{progress}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all duration-300 ease-out"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
          </div>
        )}

        {/* 分析步骤 */}
        <div className="space-y-3">
          {steps.map((step, index) => {
            const Icon = step.icon;
            const isActive = index === currentStep;
            const isCompleted = index < currentStep;

            return (
              <div
                key={index}
                className={`flex items-center gap-3 p-3 rounded-lg transition-all duration-300 ${
                  isActive
                    ? "bg-blue-50 border border-blue-200"
                    : isCompleted
                      ? "bg-green-50 border border-green-200"
                      : "bg-gray-50 border border-gray-200"
                }`}
              >
                <div
                  className={`p-2 rounded-lg ${
                    isActive
                      ? "bg-blue-200"
                      : isCompleted
                        ? "bg-green-200"
                        : "bg-gray-200"
                  }`}
                >
                  <Icon
                    className={`w-4 h-4 ${
                      isActive
                        ? "text-blue-700"
                        : isCompleted
                          ? "text-green-700"
                          : "text-gray-500"
                    }`}
                  />
                </div>
                <div className="flex-1">
                  <p
                    className={`text-sm font-medium ${
                      isActive
                        ? "text-blue-900"
                        : isCompleted
                          ? "text-green-900"
                          : "text-gray-600"
                    }`}
                  >
                    {step.text}
                  </p>
                </div>
                {isActive && (
                  <Loader2 className="w-4 h-4 text-blue-600 animate-spin" />
                )}
                {isCompleted && (
                  <div className="w-4 h-4 bg-green-600 rounded-full flex items-center justify-center">
                    <svg
                      className="w-2 h-2 text-white"
                      fill="currentColor"
                      viewBox="0 0 8 8"
                    >
                      <path d="M6.564.75l-3.59 3.612-1.538-1.55L0 4.26l2.974 2.99L8 2.193z" />
                    </svg>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* 提示信息 */}
        <div className="mt-6 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
          <div className="flex items-start gap-2">
            <div className="w-4 h-4 text-yellow-600 mt-0.5">
              <svg fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
            <div className="text-xs text-yellow-800">
              <p className="font-medium mb-1">分析说明</p>
              <p>
                系统正在基于1年历史数据进行ATR算法分析，通常需要10-30秒完成。分析结果仅供参考，不构成投资建议。
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoadingSpinner;
