import React from "react";
import "./ETFInfoSkeleton.css";

const ETFInfoSkeleton = () => {
  return (
    <div className="etf-info-skeleton">
      <div className="skeleton-content">
        <div className="skeleton-row">
          <div className="skeleton-icon"></div>
          <div className="skeleton-name"></div>
          <div className="skeleton-price"></div>
        </div>
        <div className="skeleton-company"></div>
      </div>

      <div className="skeleton-loading">
        <div className="loading-spinner"></div>
        <span className="loading-text">正在加载ETF信息...</span>
      </div>
    </div>
  );
};

export default ETFInfoSkeleton;
