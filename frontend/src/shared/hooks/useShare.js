import { useCallback } from "react";

/**
 * 分享功能Hook
 * 提供统一的分享功能实现，支持Web Share API和备用方案
 *
 * @returns {Object} 包含shareContent方法的对象
 *
 * @example
 * const { shareContent } = useShare();
 *
 * const handleShare = async () => {
 *   const result = await shareContent({
 *     title: '分享标题',
 *     text: '分享描述',
 *     url: 'https://example.com'
 *   });
 *
 *   if (result.success) {
 *     console.log('分享成功，使用方式:', result.method);
 *   }
 * };
 */
export const useShare = () => {
  /**
   * 分享内容
   * @param {Object} shareData - 分享数据
   * @param {string} shareData.title - 分享标题
   * @param {string} shareData.text - 分享描述
   * @param {string} shareData.url - 分享链接
   * @returns {Promise<Object>} 分享结果 { success: boolean, method: string }
   */
  const shareContent = useCallback(async (shareData) => {
    // 优先使用Web Share API
    if (
      navigator.share &&
      navigator.canShare &&
      navigator.canShare(shareData)
    ) {
      try {
        await navigator.share(shareData);
        return { success: true, method: "native" };
      } catch (error) {
        console.log("分享取消或失败，使用备用方案:", error);
        // 继续执行备用方案
      }
    }

    // 备用方案：复制链接到剪贴板
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(
          shareData.url || window.location.href,
        );
        alert("链接已复制到剪贴板！");
        return { success: true, method: "clipboard" };
      } else {
        // 更老的浏览器备用方案
        const textArea = document.createElement("textarea");
        textArea.value = shareData.url || window.location.href;
        textArea.style.position = "fixed";
        textArea.style.left = "-999999px";
        textArea.style.top = "-999999px";
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();

        try {
          document.execCommand("copy");
          alert("链接已复制到剪贴板！");
          return { success: true, method: "fallback" };
        } catch (err) {
          console.error("复制失败:", err);
          prompt("请手动复制以下链接:", shareData.url || window.location.href);
          return { success: false, method: "manual" };
        } finally {
          document.body.removeChild(textArea);
        }
      }
    } catch (error) {
      console.error("复制到剪贴板失败:", error);
      prompt("请手动复制以下链接:", shareData.url || window.location.href);
      return { success: false, method: "manual" };
    }
  }, []);

  return { shareContent };
};

/**
 * 检查浏览器是否支持Web Share API
 * @returns {boolean} 是否支持Web Share API
 */
export const canUseWebShare = () => {
  return !!(navigator.share && navigator.canShare);
};

/**
 * 检查浏览器是否支持剪贴板API
 * @returns {boolean} 是否支持剪贴板API
 */
export const canUseClipboard = () => {
  return !!(navigator.clipboard && navigator.clipboard.writeText);
};

/**
 * 获取当前分享能力检测结果
 * @returns {Object} 分享能力检测结果
 */
export const getShareCapabilities = () => {
  return {
    webShare: canUseWebShare(),
    clipboard: canUseClipboard(),
    fallback: true, // 总是支持备用方案
  };
};
