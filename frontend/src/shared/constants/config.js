// 水印配置文件
export const watermarkConfig = {
  // 水印文字
  text: "仅供学习和研究使用，不构成投资建议",

  // 基础样式配置
  fontSize: 18, // 基础字体大小
  opacity: 0.25, // 透明度 (0-1) - 调整到 0.25
  angle: -40, // 倾斜角度 (度)
  color: "#999999", // 颜色
  spacing: 380, // 水印间距 (像素) - 扩大一倍

  // 响应式配置
  responsive: {
    // 小屏幕 (< 640px)
    mobile: {
      fontSizeScale: 0.8, // 字体缩放比例
      spacingScale: 0.7, // 间距缩放比例
    },
    // 中等屏幕 (640px - 1024px)
    tablet: {
      fontSizeScale: 0.9, // 字体缩放比例
      spacingScale: 0.85, // 间距缩放比例
    },
    // 大屏幕 (>= 1024px)
    desktop: {
      fontSizeScale: 1.0, // 字体缩放比例
      spacingScale: 1.0, // 间距缩放比例
    },
  },

  // 安全配置
  security: {
    preventContextMenu: true, // 防止右键菜单
    preventSelection: true, // 防止文本选择
    preventDrag: true, // 防止拖拽
    autoRestore: true, // 自动恢复被删除的水印
  },

  // 性能配置
  performance: {
    resizeDebounceTime: 100, // 窗口大小变化防抖时间 (毫秒)
    useDevicePixelRatio: true, // 使用设备像素比
  },
};

// 获取响应式配置
export const getResponsiveConfig = (viewportWidth) => {
  if (viewportWidth < 640) {
    return watermarkConfig.responsive.mobile;
  } else if (viewportWidth < 1024) {
    return watermarkConfig.responsive.tablet;
  } else {
    return watermarkConfig.responsive.desktop;
  }
};

export default watermarkConfig;
