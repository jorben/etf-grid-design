import numpy as np
import pandas as pd
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)


class FrequencyCalculator:
    """基于日K线数据的交易频次计算器"""
    
    def __init__(self):
        """初始化频次计算器"""
        # 用户期望的日交易频次配置 - 优化后提升收益率
        self.target_daily_frequencies = {
            'high': 8.0,    # 高频：8次/天（从5.5提升，增加45%）
            'medium': 4.5,  # 中频：4.5次/天（从2.5提升，增加80%）
            'low': 2.0      # 低频：2次/天（从1.0提升，增加100%）
        }
        
        # 市场效率参数 - 优化提升
        self.market_efficiency = 0.75  # 理论触发的75%能实际执行（从60%提升）
        self.max_volume_factor = 2.5   # 成交量调整因子上限（从2.0提升）
        self.min_daily_triggers = 0.2  # 最小日触发次数（从0.1提升）
        self.max_daily_triggers = 20   # 最大日触发次数
        
        logger.info("交易频次计算器初始化成功")
    
    def analyze_historical_patterns(self, historical_data: pd.DataFrame) -> Dict:
        """
        分析历史K线数据的交易模式
        
        Args:
            historical_data: 包含OHLCV的历史数据
            
        Returns:
            Dict: 历史交易模式分析结果
        """
        try:
            if historical_data.empty:
                raise ValueError("历史数据为空")
            
            # 使用ATR方法计算日内振幅指标
            atr_ratio = self.calculate_atr_from_historical_data(historical_data)
            
            # 传统日振幅计算（作为备用）
            daily_amplitude = (historical_data['high'] - historical_data['low']) / historical_data['open']
            
            # 使用ATR作为主要振幅指标
            avg_amplitude = atr_ratio
            
            # 计算价格波动率
            returns = historical_data['close'].pct_change().dropna()
            volatility = returns.std() * np.sqrt(252) * 100  # 年化波动率(%)
            
            # 计算成交量活跃度
            volume_ma = historical_data['vol'].rolling(20).mean()
            volume_factor = historical_data['vol'] / volume_ma
            avg_volume_factor = volume_factor.mean()
            
            # 计算价格跳跃频率（开盘价与前日收盘价差异）
            gap_ratio = abs(historical_data['open'] - historical_data['close'].shift(1)) / historical_data['close'].shift(1)
            avg_gap_ratio = gap_ratio.mean()
            
            # 计算连续性指标（衡量价格变动的平滑程度）
            price_continuity = self._calculate_price_continuity(historical_data)
            
            analysis_result = {
                'avg_daily_amplitude': avg_amplitude,  # 使用ATR作为主要振幅
                'std_daily_amplitude': daily_amplitude.std(),
                'atr_ratio': atr_ratio,  # 新增ATR指标
                'traditional_amplitude': daily_amplitude.mean(),  # 传统振幅作为参考
                'volatility': volatility,
                'avg_volume_factor': min(self.max_volume_factor, avg_volume_factor),
                'avg_gap_ratio': avg_gap_ratio,
                'price_continuity': price_continuity,
                'data_quality': self._assess_data_quality(historical_data),
                'sample_size': len(historical_data)
            }
            
            logger.info(f"历史模式分析完成 - ATR振幅: {atr_ratio:.4f}, "
                       f"传统振幅: {daily_amplitude.mean():.4f}, "
                       f"波动率: {volatility:.2f}%, 成交量因子: {avg_volume_factor:.2f}")
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"分析历史模式失败: {str(e)}")
            return {'error': f'分析历史模式失败: {str(e)}'}
    
    def calculate_optimal_grid_parameters(self, frequency_type: str, 
                                        current_price: float,
                                        historical_patterns: Dict,
                                        price_range_ratio: float) -> Dict:
        """
        根据目标频次计算最优网格参数
        
        Args:
            frequency_type: 频次类型 ('high', 'medium', 'low')
            current_price: 当前价格
            historical_patterns: 历史模式分析结果
            price_range_ratio: 价格区间比例
            
        Returns:
            Dict: 最优网格参数
        """
        try:
            if 'error' in historical_patterns:
                return historical_patterns
            
            target_daily_triggers = self.target_daily_frequencies.get(frequency_type)
            if not target_daily_triggers:
                return {'error': f'不支持的频次类型: {frequency_type}'}
            
            # 获取历史模式参数
            avg_amplitude = historical_patterns['avg_daily_amplitude']
            volume_factor = historical_patterns['avg_volume_factor']
            price_continuity = historical_patterns['price_continuity']
            
            # 计算基于ATR的理论网格步长
            theoretical_step_ratio = self._calculate_theoretical_step_size(
                target_daily_triggers, avg_amplitude, volume_factor, price_continuity
            )
            
            # 针对低价ETF的步长优化
            optimized_step_ratio = self._optimize_step_for_low_price_etf(
                theoretical_step_ratio, current_price, target_daily_triggers
            )
            
            # 根据优化后的步长计算网格数量
            optimal_grid_count = max(3, int(price_range_ratio / optimized_step_ratio))
            
            # 实际网格步长
            actual_step_ratio = price_range_ratio / optimal_grid_count
            actual_step_amount = current_price * actual_step_ratio
            
            # 预测实际交易频次
            predicted_daily_triggers = self._predict_daily_triggers(
                actual_step_ratio, avg_amplitude, volume_factor, price_continuity
            )
            
            # 计算频次匹配度
            frequency_match_score = self._calculate_frequency_match_score(
                predicted_daily_triggers, target_daily_triggers
            )
            
            # 如果匹配度不佳，进行调整
            if frequency_match_score < 0.7:
                adjusted_params = self._adjust_grid_parameters(
                    optimal_grid_count, actual_step_ratio, target_daily_triggers,
                    avg_amplitude, volume_factor, price_continuity, price_range_ratio
                )
                optimal_grid_count = adjusted_params['grid_count']
                actual_step_ratio = adjusted_params['step_ratio']
                actual_step_amount = current_price * actual_step_ratio
                predicted_daily_triggers = adjusted_params['predicted_triggers']
                frequency_match_score = adjusted_params['match_score']
            
            result = {
                'target_daily_triggers': target_daily_triggers,
                'predicted_daily_triggers': predicted_daily_triggers,
                'optimal_grid_count': optimal_grid_count,
                'grid_step_ratio': actual_step_ratio,
                'grid_step_amount': actual_step_amount,
                'frequency_match_score': frequency_match_score,
                'theoretical_step_ratio': theoretical_step_ratio,
                'adjustment_applied': frequency_match_score < 0.7
            }
            
            logger.info(f"网格参数计算完成 - 目标频次: {target_daily_triggers}/天, "
                       f"预测频次: {predicted_daily_triggers:.2f}/天, "
                       f"网格数: {optimal_grid_count}, 匹配度: {frequency_match_score:.2f}")
            
            return result
            
        except Exception as e:
            logger.error(f"计算网格参数失败: {str(e)}")
            return {'error': f'计算网格参数失败: {str(e)}'}
    
    def estimate_monthly_statistics(self, daily_triggers: float, 
                                   success_rate: float = 0.8) -> Dict:
        """
        基于日交易频次估算月度统计数据
        
        Args:
            daily_triggers: 日交易触发次数
            success_rate: 交易成功率
            
        Returns:
            Dict: 月度统计数据
        """
        try:
            # 假设每月20个交易日
            trading_days_per_month = 20
            
            # 月度触发次数
            monthly_triggers = daily_triggers * trading_days_per_month
            
            # 成功交易次数
            successful_trades = monthly_triggers * success_rate
            
            # 考虑周末和节假日的影响
            calendar_adjustment = 0.85  # 85%的理论交易日能正常交易
            
            adjusted_monthly_triggers = monthly_triggers * calendar_adjustment
            adjusted_successful_trades = successful_trades * calendar_adjustment
            
            return {
                'daily_triggers': daily_triggers,
                'monthly_triggers': int(adjusted_monthly_triggers),
                'successful_monthly_trades': int(adjusted_successful_trades),
                'success_rate': success_rate,
                'trading_days_assumption': trading_days_per_month,
                'calendar_adjustment': calendar_adjustment
            }
            
        except Exception as e:
            logger.error(f"估算月度统计失败: {str(e)}")
            return {
                'daily_triggers': daily_triggers,
                'monthly_triggers': int(daily_triggers * 20),
                'successful_monthly_trades': int(daily_triggers * 20 * 0.8),
                'success_rate': 0.8,
                'error': str(e)
            }
    
    def _calculate_theoretical_step_size(self, target_triggers: float, 
                                       avg_amplitude: float,
                                       volume_factor: float,
                                       price_continuity: float) -> float:
        """计算理论网格步长 - 基于ATR方法"""
        try:
            # 方案4：基于ATR的步长计算
            # ATR近似值 = 日振幅（已经是比例形式）
            atr_ratio = avg_amplitude
            
            # 步长 = ATR / 目标频次 * 调整系数
            # 调整系数考虑成交量和价格连续性
            adjustment_factor = volume_factor * price_continuity * 0.8
            
            theoretical_step = (atr_ratio * adjustment_factor) / target_triggers
            
            # 确保步长在合理范围内 (0.2% - 5%)
            # 提高最小步长以适应低价ETF
            return max(0.002, min(0.05, theoretical_step))
            
        except:
            # 默认步长 - 提高默认值
            return max(0.002, 0.01 / target_triggers)
    
    def _predict_daily_triggers(self, step_ratio: float, avg_amplitude: float,
                              volume_factor: float, price_continuity: float) -> float:
        """预测日交易触发次数"""
        try:
            # 基础触发次数
            base_triggers = avg_amplitude / step_ratio
            
            # 应用调整因子
            adjusted_triggers = (base_triggers * volume_factor * 
                               price_continuity * self.market_efficiency)
            
            # 限制在合理范围
            return max(self.min_daily_triggers, 
                      min(self.max_daily_triggers, adjusted_triggers))
            
        except:
            return 1.0  # 默认值
    
    def _calculate_frequency_match_score(self, predicted: float, target: float) -> float:
        """计算频次匹配度评分"""
        try:
            if target == 0:
                return 0.0
            
            # 计算相对误差
            relative_error = abs(predicted - target) / target
            
            # 转换为匹配度评分 (0-1)
            match_score = max(0.0, 1.0 - relative_error)
            
            return match_score
            
        except:
            return 0.5  # 默认中等匹配度
    
    def _adjust_grid_parameters(self, initial_grid_count: int, initial_step_ratio: float,
                              target_triggers: float, avg_amplitude: float,
                              volume_factor: float, price_continuity: float,
                              price_range_ratio: float) -> Dict:
        """调整网格参数以提高频次匹配度"""
        try:
            best_score = 0
            best_params = {
                'grid_count': initial_grid_count,
                'step_ratio': initial_step_ratio,
                'predicted_triggers': 0,
                'match_score': 0
            }
            
            # 尝试不同的网格数量
            for grid_count in range(max(3, initial_grid_count - 5), 
                                  initial_grid_count + 10):
                step_ratio = price_range_ratio / grid_count
                predicted_triggers = self._predict_daily_triggers(
                    step_ratio, avg_amplitude, volume_factor, price_continuity
                )
                match_score = self._calculate_frequency_match_score(
                    predicted_triggers, target_triggers
                )
                
                if match_score > best_score:
                    best_score = match_score
                    best_params = {
                        'grid_count': grid_count,
                        'step_ratio': step_ratio,
                        'predicted_triggers': predicted_triggers,
                        'match_score': match_score
                    }
            
            return best_params
            
        except Exception as e:
            logger.error(f"调整网格参数失败: {str(e)}")
            return {
                'grid_count': initial_grid_count,
                'step_ratio': initial_step_ratio,
                'predicted_triggers': target_triggers,
                'match_score': 0.5
            }
    
    def _calculate_price_continuity(self, historical_data: pd.DataFrame) -> float:
        """计算价格连续性指标"""
        try:
            # 计算相邻交易日的价格跳跃
            close_prices = historical_data['close']
            price_jumps = abs(close_prices.diff()) / close_prices.shift(1)
            
            # 连续性 = 1 - 平均跳跃幅度
            avg_jump = price_jumps.mean()
            continuity = max(0.3, min(1.0, 1.0 - avg_jump * 10))
            
            return continuity
            
        except:
            return 0.7  # 默认连续性
    
    def _assess_data_quality(self, historical_data: pd.DataFrame) -> Dict:
        """评估数据质量"""
        try:
            quality_score = 1.0
            issues = []
            
            # 检查数据完整性
            if len(historical_data) < 30:
                quality_score -= 0.3
                issues.append("数据量不足")
            
            # 检查价格异常
            returns = historical_data['close'].pct_change().dropna()
            extreme_returns = (abs(returns) > 0.2).sum()
            if extreme_returns > len(returns) * 0.05:  # 超过5%的极端收益
                quality_score -= 0.2
                issues.append("存在异常价格波动")
            
            # 检查成交量异常
            volume_cv = historical_data['vol'].std() / historical_data['vol'].mean()
            if volume_cv > 2.0:  # 成交量变异系数过大
                quality_score -= 0.1
                issues.append("成交量波动过大")
            
            return {
                'score': max(0.0, quality_score),
                'issues': issues,
                'sample_size': len(historical_data)
            }
            
        except:
            return {'score': 0.5, 'issues': ['数据质量评估失败'], 'sample_size': 0}
    
    def get_frequency_recommendations(self, historical_patterns: Dict, 
                                    current_market_conditions: Dict = None) -> Dict:
        """
        基于历史模式和当前市场条件推荐最适合的交易频次
        
        Args:
            historical_patterns: 历史模式分析结果
            current_market_conditions: 当前市场条件（可选）
            
        Returns:
            Dict: 频次推荐结果
        """
        try:
            if 'error' in historical_patterns:
                return historical_patterns
            
            volatility = historical_patterns.get('volatility', 25)
            avg_amplitude = historical_patterns.get('avg_daily_amplitude', 0.02)
            volume_factor = historical_patterns.get('avg_volume_factor', 1.0)
            
            recommendations = {}
            
            # 为每种频次类型评估适合度
            for freq_type, target_triggers in self.target_daily_frequencies.items():
                # 计算理论可达成的触发次数
                theoretical_triggers = self._predict_daily_triggers(
                    0.01, avg_amplitude, volume_factor, 0.7  # 使用标准参数
                )
                
                # 计算适合度评分
                suitability_score = min(1.0, theoretical_triggers / target_triggers)
                
                # 风险评估
                risk_level = self._assess_frequency_risk(freq_type, volatility, avg_amplitude)
                
                recommendations[freq_type] = {
                    'target_triggers': target_triggers,
                    'theoretical_triggers': theoretical_triggers,
                    'suitability_score': suitability_score,
                    'risk_level': risk_level,
                    'recommended': suitability_score > 0.7 and risk_level != '极高风险'
                }
            
            # 选择最佳推荐
            best_freq = max(recommendations.keys(), 
                          key=lambda x: recommendations[x]['suitability_score'] 
                          if recommendations[x]['recommended'] else 0)
            
            return {
                'recommendations': recommendations,
                'best_frequency': best_freq,
                'market_assessment': {
                    'volatility_level': self._classify_volatility(volatility),
                    'liquidity_level': self._classify_liquidity(volume_factor),
                    'overall_suitability': 'high' if recommendations[best_freq]['suitability_score'] > 0.8 else 'medium'
                }
            }
            
        except Exception as e:
            logger.error(f"生成频次推荐失败: {str(e)}")
            return {'error': f'生成频次推荐失败: {str(e)}'}
    
    def _assess_frequency_risk(self, frequency_type: str, volatility: float, 
                             avg_amplitude: float) -> str:
        """评估频次风险等级"""
        try:
            risk_score = 0
            
            # 波动率风险
            if volatility > 40:
                risk_score += 2
            elif volatility > 25:
                risk_score += 1
            
            # 振幅风险
            if avg_amplitude > 0.05:
                risk_score += 2
            elif avg_amplitude > 0.03:
                risk_score += 1
            
            # 频次风险
            if frequency_type == 'high':
                risk_score += 1
            elif frequency_type == 'low':
                risk_score -= 1
            
            # 风险等级映射
            if risk_score <= 1:
                return '低风险'
            elif risk_score <= 3:
                return '中等风险'
            elif risk_score <= 4:
                return '高风险'
            else:
                return '极高风险'
                
        except:
            return '中等风险'
    
    def _classify_volatility(self, volatility: float) -> str:
        """分类波动率水平"""
        if volatility < 15:
            return '低波动'
        elif volatility < 30:
            return '中等波动'
        else:
            return '高波动'
    
    def _classify_liquidity(self, volume_factor: float) -> str:
        """分类流动性水平"""
        if volume_factor < 0.8:
            return '低流动性'
        elif volume_factor < 1.5:
            return '正常流动性'
        else:
            return '高流动性'
    
    def _optimize_step_for_low_price_etf(self, theoretical_step_ratio: float, 
                                       current_price: float, 
                                       target_triggers: float) -> float:
        """针对低价ETF优化步长"""
        try:
            # 基于价格区间的最小步长约束 - 优化降低以增加交易机会
            if current_price <= 2:
                min_step_ratio = 0.002  # 最小0.2%（从0.5%降低）
            elif current_price <= 5:
                min_step_ratio = 0.0015 # 最小0.15%（从0.3%降低）
            elif current_price <= 10:
                min_step_ratio = 0.001  # 最小0.1%（从0.2%降低）
            else:
                min_step_ratio = 0.0008 # 最小0.08%（从0.1%降低）
            
            # 交易成本约束（假设双边成本0.06%）- 优化降低成本倍数
            transaction_cost_ratio = 0.0006
            cost_based_min_step = transaction_cost_ratio * 3  # 成本的3倍（从4倍降低）
            
            # 流动性约束 - 优化调整，更积极的步长设置
            liquidity_based_min = max(0.0015, 0.008 / target_triggers)  # 降低基础值
            
            # 取理论值和各种约束的最大值
            optimized_step = max(
                theoretical_step_ratio,
                min_step_ratio,
                cost_based_min_step,
                liquidity_based_min
            )
            
            # 确保不超过5%
            return min(optimized_step, 0.05)
            
        except Exception as e:
            logger.error(f"优化低价ETF步长失败: {str(e)}")
            return max(theoretical_step_ratio, 0.002)
    
    def calculate_atr_from_historical_data(self, historical_data: pd.DataFrame) -> float:
        """从历史数据计算ATR（平均真实波幅）"""
        try:
            if historical_data.empty or len(historical_data) < 2:
                return 0.02  # 默认2%
            
            # 计算真实波幅 (True Range)
            high = historical_data['high']
            low = historical_data['low']
            close_prev = historical_data['close'].shift(1)
            
            # TR = max(high-low, |high-close_prev|, |low-close_prev|)
            tr1 = high - low
            tr2 = abs(high - close_prev)
            tr3 = abs(low - close_prev)
            
            true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            
            # ATR = 真实波幅的移动平均 / 收盘价
            atr_period = min(14, len(true_range) // 2)  # 使用14天或数据长度的一半
            atr_values = true_range.rolling(atr_period).mean()
            avg_close = historical_data['close'].rolling(atr_period).mean()
            
            atr_ratio = (atr_values / avg_close).mean()
            
            # 确保ATR在合理范围内
            return max(0.005, min(0.1, atr_ratio))
            
        except Exception as e:
            logger.error(f"计算ATR失败: {str(e)}")
            return 0.02  # 默认2%