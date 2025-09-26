import React, { useEffect, useRef } from "react";
import "./Watermark.css";
import { watermarkConfig, getResponsiveConfig } from "@shared/constants/config";

const Watermark = ({
  text = watermarkConfig.text,
  fontSize = watermarkConfig.fontSize,
  opacity = watermarkConfig.opacity,
  angle = watermarkConfig.angle,
  color = watermarkConfig.color,
  spacing = watermarkConfig.spacing,
}) => {
  const canvasRef = useRef(null);
  const containerRef = useRef(null);

  useEffect(() => {
    const updateWatermark = () => {
      const canvas = canvasRef.current;
      const container = containerRef.current;

      if (!canvas || !container) return;

      const ctx = canvas.getContext("2d");
      const devicePixelRatio = window.devicePixelRatio || 1;

      // 获取视口尺寸
      const viewportWidth = window.innerWidth;
      const viewportHeight = window.innerHeight;

      // 获取响应式配置
      const responsiveConfig = getResponsiveConfig(viewportWidth);

      // 响应式字体大小和间距调整
      const responsiveFontSize = fontSize * responsiveConfig.fontSizeScale;
      const responsiveSpacing = spacing * responsiveConfig.spacingScale;

      // 设置canvas尺寸
      canvas.width = viewportWidth * devicePixelRatio;
      canvas.height = viewportHeight * devicePixelRatio;
      canvas.style.width = `${viewportWidth}px`;
      canvas.style.height = `${viewportHeight}px`;

      // 缩放上下文以适应设备像素比
      ctx.scale(devicePixelRatio, devicePixelRatio);

      // 清除画布
      ctx.clearRect(0, 0, viewportWidth, viewportHeight);

      // 设置文字样式
      ctx.font = `${responsiveFontSize}px Arial, sans-serif`;
      ctx.fillStyle = color;
      ctx.globalAlpha = opacity;
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";

      // 计算文字尺寸
      const textMetrics = ctx.measureText(text);
      const textWidth = textMetrics.width;
      const textHeight = responsiveFontSize;

      // 计算旋转后的边界框
      const radians = (angle * Math.PI) / 180;
      const cos = Math.abs(Math.cos(radians));
      const sin = Math.abs(Math.sin(radians));
      const rotatedWidth = textWidth * cos + textHeight * sin;
      const rotatedHeight = textWidth * sin + textHeight * cos;

      // 计算网格布局
      const cols = Math.ceil(viewportWidth / responsiveSpacing) + 2;
      const rows = Math.ceil(viewportHeight / responsiveSpacing) + 2;

      // 绘制水印网格 - 实现交错效果
      for (let row = 0; row < rows; row++) {
        for (let col = 0; col < cols; col++) {
          // 交错效果：奇数行向右偏移三分之一间距，让效果更明显
          const isOddRow = row % 2 === 1;
          const offsetX = isOddRow ? responsiveSpacing * 0.3 : 0;

          const x = col * responsiveSpacing - responsiveSpacing / 2 + offsetX;
          const y = row * responsiveSpacing - responsiveSpacing / 2;

          // 确保水印在视口范围内才绘制（性能优化）
          if (
            x > -rotatedWidth &&
            x < viewportWidth + rotatedWidth &&
            y > -rotatedHeight &&
            y < viewportHeight + rotatedHeight
          ) {
            ctx.save();
            ctx.translate(x, y);
            ctx.rotate(radians);
            ctx.fillText(text, 0, 0);
            ctx.restore();
          }
        }
      }
    };

    // 初始化水印
    updateWatermark();

    // 监听窗口大小变化
    const handleResize = () => {
      // 使用防抖来优化性能
      clearTimeout(window.watermarkResizeTimeout);
      window.watermarkResizeTimeout = setTimeout(
        updateWatermark,
        watermarkConfig.performance.resizeDebounceTime,
      );
    };

    window.addEventListener("resize", handleResize);
    window.addEventListener("orientationchange", handleResize);

    // 安全功能初始化
    let observer = null;
    let preventContextMenu = null;
    let preventSelection = null;

    if (watermarkConfig.security.autoRestore) {
      // 监听DOM变化，防止水印被移除
      observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
          if (mutation.type === "childList") {
            const container = containerRef.current;
            if (container && !document.body.contains(container)) {
              // 如果水印容器被移除，重新添加
              document.body.appendChild(container);
            }
          }
        });
      });

      observer.observe(document.body, {
        childList: true,
        subtree: true,
      });
    }

    if (watermarkConfig.security.preventContextMenu) {
      // 防止右键菜单
      preventContextMenu = (e) => {
        if (e.target === canvasRef.current) {
          e.preventDefault();
        }
      };
      document.addEventListener("contextmenu", preventContextMenu);
    }

    if (watermarkConfig.security.preventSelection) {
      // 防止选择文本
      preventSelection = (e) => {
        if (e.target === canvasRef.current) {
          e.preventDefault();
        }
      };
      document.addEventListener("selectstart", preventSelection);
    }

    // 清理函数
    return () => {
      window.removeEventListener("resize", handleResize);
      window.removeEventListener("orientationchange", handleResize);

      if (preventContextMenu) {
        document.removeEventListener("contextmenu", preventContextMenu);
      }
      if (preventSelection) {
        document.removeEventListener("selectstart", preventSelection);
      }
      if (observer) {
        observer.disconnect();
      }

      clearTimeout(window.watermarkResizeTimeout);
    };
  }, [text, fontSize, opacity, angle, color, spacing]);

  return (
    <div ref={containerRef} className="watermark-container">
      <canvas ref={canvasRef} className="watermark-canvas" />
    </div>
  );
};

export default Watermark;
