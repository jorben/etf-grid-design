import React, { useState } from "react";
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

      {/* 免责声明 */}
      <Disclaimer />
    </div>
  );
};

export default AnalysisReport;
