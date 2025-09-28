/**
 * 免责声明相关工具函数
 */

/**
 * 检查免责声明是否需要重新确认
 * @returns {boolean} true: 已确认且未过期, false: 未确认或已过期
 */
export const checkDisclaimerStatus = () => {
  const disclaimerAccepted = localStorage.getItem('disclaimer_accepted');
  
  if (!disclaimerAccepted) {
    return false; // 未做过确认
  }

  try {
    const acceptedDate = new Date(disclaimerAccepted);
    const now = new Date();
    const daysDiff = Math.floor((now - acceptedDate) / (1000 * 60 * 60 * 24));
    
    return daysDiff <= 30; // 30天内有效
  } catch (error) {
    console.error('解析免责声明日期失败:', error);
    return false; // 解析失败，重新确认
  }
};

/**
 * 记录用户同意免责声明
 */
export const acceptDisclaimer = () => {
  localStorage.setItem('disclaimer_accepted', new Date().toISOString());
};

/**
 * 获取免责声明的剩余有效天数
 * @returns {number} 剩余天数，如果未确认或已过期返回0
 */
export const getDisclaimerRemainingDays = () => {
  const disclaimerAccepted = localStorage.getItem('disclaimer_accepted');
  
  if (!disclaimerAccepted) {
    return 0;
  }

  try {
    const acceptedDate = new Date(disclaimerAccepted);
    const now = new Date();
    const daysDiff = Math.floor((now - acceptedDate) / (1000 * 60 * 60 * 24));
    const remainingDays = 30 - daysDiff;
    
    return Math.max(0, remainingDays);
  } catch (error) {
    console.error('解析免责声明日期失败:', error);
    return 0;
  }
};