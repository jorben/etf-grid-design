import React, { useState, useEffect, useRef } from "react";
import { LoadingSpinner } from "@shared/components/ui";
import { useShare } from "@shared/hooks";
import ReportTabs from "./ReportTabs";
import OverviewTab from "./OverviewTab";
import ErrorState from "./ErrorState";
import Disclaimer from "./Disclaimer";
import SuitabilityCard from "./ReportCards/SuitabilityCard";
import GridParametersCard from "./ReportCards/GridParametersCard";

/**
 * 分析报告容器组件
 * 负责协调各个报告子组件和状态管理
 */
const AnalysisReport = ({
  data,
  loading,
  onBackToInput,
  onReAnalysis,
}) => {
  const [activeTab, setActiveTab] = useState("overview");
  const { shareContent } = useShare();
  const giscusRef = useRef(null);

  // 加载 Giscus 评论组件
  useEffect(() => {
    if (data && !data.error && giscusRef.current) {
      // 清除之前的 Giscus 实例
      giscusRef.current.innerHTML = '';
      
      // 创建 Giscus 脚本
      const script = document.createElement('script');
      script.src = 'https://giscus.app/client.js';
      script.setAttribute('data-repo', 'jorben/etf-grid-design');
      script.setAttribute('data-repo-id', 'R_kgDOPzq5AA');
      script.setAttribute('data-category', 'General');
      script.setAttribute('data-category-id', 'DIC_kwDOPzq5AM4Cv-y9');
      script.setAttribute('data-mapping', 'title');
      script.setAttribute('data-strict', '0');
      script.setAttribute('data-reactions-enabled', '1');
      script.setAttribute('data-emit-metadata', '0');
      script.setAttribute('data-input-position', 'top');
      script.setAttribute('data-theme', 'preferred_color_scheme');
      script.setAttribute('data-lang', 'zh-CN');
      script.setAttribute('data-loading', 'lazy');
      script.setAttribute('crossorigin', 'anonymous');
      script.async = true;
      
      giscusRef.current.appendChild(script);
    }
  }, [data]);


  // 显示加载状态
  if (loading) {
    return (
      <LoadingSpinner
        message="正在分析ETF数据..."
        showProgress={true}
        progress={75}
      />
    );
  }

  // 显示错误状态
  if (data?.error) {
    return (
      <ErrorState
        type="error"
        message={data.message}
        onBackToInput={onBackToInput}
        onReAnalysis={onReAnalysis}
      />
    );
  }

  if (!data) return null;

  const {
    etf_info,
    data_quality,
    suitability_evaluation,
    grid_strategy,
    strategy_rationale,
    adjustment_suggestions,
    input_parameters,
  } = data;

  // 数据完整性检查
  const isDataComplete = () => {
    if (!suitability_evaluation || !grid_strategy || !etf_info) {
      return false;
    }

    const dataObjects = {
      suitability_evaluation: suitability_evaluation,
      grid_strategy: grid_strategy,
      etf_info: etf_info,
    };

    const requiredFields = {
      suitability_evaluation: ["total_score", "conclusion"],
      grid_strategy: ["grid_config", "fund_allocation"],
      etf_info: ["code", "name", "current_price"],
    };

    for (const [objName, fields] of Object.entries(requiredFields)) {
      const obj = dataObjects[objName];
      for (const field of fields) {
        if (obj[field] === undefined || obj[field] === null) {
          return false;
        }
      }
    }

    return true;
  };

  if (!isDataComplete()) {
    return (
      <ErrorState
        type="data_incomplete"
        message="分析数据不完整，请重新分析"
        onBackToInput={onBackToInput}
        onReAnalysis={onReAnalysis}
      />
    );
  }

  return (
    <div className="space-y-6">
      {/* 标签页导航 */}
      <div className="bg-white rounded-xl shadow-lg">
        <ReportTabs activeTab={activeTab} onTabChange={setActiveTab} />

        <div className="p-6">
          {/* 概览标签页 */}
          {activeTab === "overview" && (
            <OverviewTab
              etfInfo={etf_info}
              suitabilityEvaluation={suitability_evaluation}
              gridStrategy={grid_strategy}
              dataQuality={data_quality}
              inputParameters={input_parameters}
            />
          )}

          {/* 适宜度评估标签页 */}
          {activeTab === "suitability" && (
            <SuitabilityCard
              evaluation={suitability_evaluation}
              dataQuality={data_quality}
              showDetailed={true}
            />
          )}

          {/* 网格策略标签页 */}
          {activeTab === "strategy" && (
            <GridParametersCard
              gridStrategy={grid_strategy}
              inputParameters={input_parameters}
              strategyRationale={strategy_rationale}
              adjustmentSuggestions={adjustment_suggestions}
              showDetailed={true}
              dataQuality={data_quality}
            />
          )}
        </div>
      </div>

      {/* GitHub 评论组件 */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">讨论与反馈</h3>
        <div ref={giscusRef} className="giscus-container"></div>
      </div>

      {/* 免责声明 */}
      <Disclaimer />
    </div>
  );
};

export default AnalysisReport;
