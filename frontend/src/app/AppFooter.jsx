import React, { useState, useEffect } from "react";
import { getVersion } from "@shared/services/api";

/**
 * 应用底部组件
 * 负责显示系统信息、风险提示和技术支持信息
 */
export default function AppFooter() {
  const [version, setVersion] = useState("v1.0.0");

  useEffect(() => {
    const fetchVersion = async () => {
      try {
        const response = await getVersion();
        if (response.success && response.data.version) {
          setVersion(`v${response.data.version}`);
        }
      } catch (error) {
        console.error("获取版本号失败:", error);
      }
    };

    fetchVersion();
  }, []);
  return (
    <footer className="bg-white border-t border-gray-200 mt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* 系统信息 */}
          <div>
            <h3 className="font-semibold text-gray-900 mb-4">系统特点</h3>
            <ul className="space-y-2 text-sm text-gray-600">
              <li>• 基于ATR算法的科学分析</li>
              <li>• 4维度量化评分体系</li>
              <li>• 智能网格参数计算</li>
              <li>• 策略分析与收益预测</li>
            </ul>
          </div>

          {/* 风险提示 */}
          <div>
            <h3 className="font-semibold text-gray-900 mb-4">风险提示</h3>
            <ul className="space-y-2 text-sm text-gray-600">
              <li>• 历史数据不代表未来表现</li>
              <li>• 投资有风险，入市需谨慎</li>
              <li>• 本系统仅供参考，不构成投资建议</li>
              <li>• 请根据自身情况谨慎决策</li>
            </ul>
          </div>

          {/* 技术支持 */}
          <div>
            <h3 className="font-semibold text-gray-900 mb-4">技术信息</h3>
            <ul className="space-y-2 text-sm text-gray-600">
              <li>• 数据源：Tushare金融数据</li>
              <li>• 算法：ATR + ADX + 统计分析</li>
              <li>• 更新频率：每日收盘后</li>
              <li>• 版本：{version}</li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-200 mt-8 pt-8 text-center">
          <p className="text-sm text-gray-500">
            &copy; 2025 ETFer.Top 本系统仅供学习和研究使用，不构成投资建议。
          </p>
        </div>
      </div>
    </footer>
  );
}
