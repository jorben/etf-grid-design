"""
网格优化器 - 纯算法实现
从服务层抽离的网格优化算法模块
"""

import numpy as np
from typing import Dict, List, Tuple
import logging
from .arithmetic_grid import ArithmeticGridCalculator
from .geometric_grid import GeometricGridCalculator

logger = logging.getLogger(__name__)

class GridOptimizer:
    """网格优化器"""
    
    def __init__(self):
        """初始化优化器"""
        self.arithmetic_calculator = ArithmeticGridCalculator()
        self.geometric_calculator = GeometricGridCalculator()
    
    def calculate_optimal_step_size(self, atr_ratio: float, current_price: float, 
                                   risk_preference: str) -> Tuple[float, float]:
        """
        基于ATR计算最优步长
        
        Args:
            atr_ratio: ATR比率
            current_price: 当前价格
            risk_preference: 风险偏好
            
        Returns:
            (step_size, step_ratio)
        """
        try:
            # ATR 基础步长系数（根据风险偏好）
            risk_multipliers = {
                '保守': 0.8,   # 0.8倍ATR作为步长，步长较大，交易频次较低
                '稳健': 0.5,   # 0.5倍ATR作为步长，平衡交易频次
                '激进': 0.2    # 0.2倍ATR作为步长，步长较小，交易频次较高
            }
            
            risk_multiplier = risk_multipliers.get(risk_preference, 1)
            
            # 计算基于ATR的步长
            atr_value = atr_ratio * current_price
            optimal_step_size = atr_value * risk_multiplier
            optimal_step_ratio = optimal_step_size / current_price
            
            # 确保步长在合理范围内（0.5% - 5%）
            min_step_ratio = 0.005  # 0.2%
            max_step_ratio = 0.05   # 5%
            optimal_step_ratio = max(min_step_ratio, min(max_step_ratio, optimal_step_ratio))
            optimal_step_size = optimal_step_ratio * current_price
            
            logger.info(f"ATR步长计算: ATR比率{atr_ratio:.1%}, 风险系数{risk_multiplier}, "
                       f"最优步长{optimal_step_size:.3f}({optimal_step_ratio:.1%})")
            
            return optimal_step_size, optimal_step_ratio
            
        except Exception as e:
            logger.error(f"ATR步长计算失败: {str(e)}")
            # 返回默认步长（1%）
            default_step_ratio = 0.01
            return current_price * default_step_ratio, default_step_ratio
    
    def calculate_base_position_ratio(self, atr_ratio: float, risk_preference: str, 
                                    adx_value: float, volatility: float) -> float:
        """
        智能底仓比例计算
        
        Args:
            atr_ratio: ATR比率
            risk_preference: 风险偏好
            adx_value: ADX指数
            volatility: 年化波动率
            
        Returns:
            底仓比例
        """
        try:
            # 基础比例（根据风险偏好）
            base_ratios = {
                '保守': 0.30,  # 35%底仓，65%网格
                '稳健': 0.20,  # 25%底仓，75%网格
                '激进': 0.10   # 15%底仓，85%网格
            }
            
            base_ratio = base_ratios.get(risk_preference, 0.25)
            
            # ATR波动调整（波动越大，底仓比例越高）
            atr_adjustment = min(atr_ratio * 5, 0.15)  # 最大调整15%
            
            # 市场趋势调整（基于ADX指数）
            if adx_value < 20:      # 震荡市
                trend_adjustment = -0.05  # 减少底仓，增加网格资金
            elif adx_value < 40:    # 弱趋势
                trend_adjustment = 0.05   # 适中调整
            else:                   # 强趋势
                trend_adjustment = 0.1    # 增加底仓比例
            
            # 波动率调整
            if volatility > 0.4:    # 高波动
                volatility_adjustment = 0.05
            elif volatility < 0.15: # 低波动
                volatility_adjustment = -0.05
            else:                   # 正常波动
                volatility_adjustment = 0
            
            # 计算最终底仓比例
            final_ratio = (base_ratio + atr_adjustment + 
                          trend_adjustment + volatility_adjustment)
            
            # 限制在10%-70%之间
            final_ratio = max(0.1, min(0.7, final_ratio))
            
            logger.info(f"底仓比例计算: 基础{base_ratio:.1%} + ATR调整{atr_adjustment:.1%} + "
                       f"趋势调整{trend_adjustment:.1%} + 波动率调整{volatility_adjustment:.1%} = {final_ratio:.1%}")
            
            return final_ratio
            
        except Exception as e:
            logger.error(f"底仓比例计算失败: {str(e)}")
            return 0.25  # 默认25%
    
    def optimize_grid_type_selection(self, price_data: List[float], 
                                   volatility: float, adx_value: float) -> str:
        """
        优化网格类型选择
        
        Args:
            price_data: 历史价格数据
            volatility: 年化波动率
            adx_value: ADX指数
            
        Returns:
            推荐的网格类型 ('等差' 或 '等比')
        """
        try:
            # 基于波动率的选择
            if volatility > 0.3:
                # 高波动环境，等比网格更适合
                volatility_score = '等比'
            else:
                # 低波动环境，等差网格更稳定
                volatility_score = '等差'
            
            # 基于趋势强度的选择
            if adx_value < 25:
                # 震荡环境，等差网格更合适
                trend_score = '等差'
            else:
                # 趋势环境，等比网格能更好跟随趋势
                trend_score = '等比'
            
            # 基于价格分布的选择
            price_range = max(price_data) - min(price_data)
            avg_price = np.mean(price_data)
            price_range_ratio = price_range / avg_price
            
            if price_range_ratio > 0.5:
                # 价格波动范围大，等比网格更适合
                distribution_score = '等比'
            else:
                # 价格波动范围小，等差网格更精确
                distribution_score = '等差'
            
            # 综合评分
            scores = {'等差': 0, '等比': 0}
            scores[volatility_score] += 1
            scores[trend_score] += 1
            scores[distribution_score] += 1
            
            # 选择得分高的类型
            recommended_type = max(scores, key=scores.get)
            
            logger.info(f"网格类型优化: 波动率{volatility_score}, 趋势{trend_score}, "
                       f"分布{distribution_score}, 推荐{recommended_type}")
            
            return recommended_type
            
        except Exception as e:
            logger.error(f"网格类型优化失败: {str(e)}")
            return '等差'  # 默认等差网格
    
    def calculate_fund_allocation(self, total_capital: float, base_position_ratio: float, 
                                grid_count: int, price_levels: List[float], base_price: float = None) -> Dict:
        """
        智能资金分配计算
        
        Args:
            total_capital: 总投资资金
            base_position_ratio: 底仓比例
            grid_count: 网格数量
            price_levels: 价格水平列表
            
        Returns:
            资金分配结果
        """
        try:
            # 1. 底仓资金计算
            base_position_amount = total_capital * base_position_ratio
            
            # 2. 网格交易资金
            grid_trading_amount = total_capital - base_position_amount
            
            # 3. 预留机动资金（5%）
            reserve_amount = total_capital * 0.05
            available_grid_amount = grid_trading_amount - reserve_amount
            
            # 4. 计算单笔数量（基于买入网格精确计算）
            single_trade_quantity = self._calculate_single_trade_quantity(
                available_grid_amount, price_levels, base_price or sum(price_levels) / len(price_levels)
            )
            
            # 5. 每格资金分配（使用统一的单笔数量）
            grid_funds = []
            total_required_fund = 0
            
            if price_levels and single_trade_quantity > 0:
                # 只计算买入网格（价格低于基准价格的网格）
                reference_price = base_price if base_price is not None else sum(price_levels) / len(price_levels)
                buy_levels = [p for p in price_levels[:-1] if p < reference_price]
                logger.info(f"计算买入网格，基准价格: {reference_price:.3f}, 买入网格: {len(buy_levels)}")
                
                for i, price in enumerate(price_levels[:-1]):
                    # 使用统一的单笔数量
                    shares = single_trade_quantity
                    actual_fund = shares * price
                    total_required_fund += actual_fund
                    
                    grid_funds.append({
                        'level': i + 1,
                        'price': round(price, 3),
                        'allocated_fund': round(actual_fund, 2),
                        'shares': shares,
                        'actual_fund': round(actual_fund, 2),
                        'is_buy_level': price < reference_price
                    })
            
            # 6. 计算网格资金利用率
            total_buy_grid_fund = sum(gf['actual_fund'] for gf in grid_funds if gf['is_buy_level'])
            grid_fund_utilization_rate = total_buy_grid_fund / available_grid_amount
            
            # 7. 计算买入网格资金占用（极端情况验证）
            buy_grid_fund = sum(gf['actual_fund'] for gf in grid_funds if gf.get('is_buy_level', False))
            buy_grid_safety_ratio = buy_grid_fund / available_grid_amount if available_grid_amount > 0 else 0
            
            # 8. 计算预期单笔收益（基于平均网格间距）
            if len(price_levels) > 1:
                avg_price = sum(price_levels) / len(price_levels)
                avg_step = (price_levels[-1] - price_levels[0]) / len(price_levels)
                expected_profit_per_trade = single_trade_quantity * avg_step
            else:
                expected_profit_per_trade = 0
            
            result = {
                'base_position_amount': round(base_position_amount, 2),
                'grid_trading_amount': round(available_grid_amount, 2),
                'reserve_amount': round(reserve_amount, 2),
                'grid_funds': grid_funds,
                'total_buy_grid_fund': round(total_buy_grid_fund, 2),
                'grid_fund_utilization_rate': round(grid_fund_utilization_rate, 4),
                'expected_profit_per_trade': round(expected_profit_per_trade, 2),
                'grid_count': len(grid_funds),
                'base_position_ratio': base_position_ratio,
                # 新增单笔数量相关字段
                'single_trade_quantity': single_trade_quantity,
                'buy_grid_fund': round(buy_grid_fund, 2),
                'buy_grid_safety_ratio': round(buy_grid_safety_ratio, 4),
                'extreme_case_safe': buy_grid_safety_ratio <= 1.0
            }
            
            logger.info(f"资金分配完成: 底仓{base_position_amount:.0f}, "
                       f"网格{available_grid_amount:.0f}, 单笔数量{single_trade_quantity}股, "
                       f"买入网格资金{buy_grid_fund:.0f}, 网格资金利用率{grid_fund_utilization_rate:.1%}")
            
            return result
            
        except Exception as e:
            logger.error(f"资金分配计算失败: {str(e)}")
            raise
    
    def _calculate_single_trade_quantity(self, available_grid_amount: float, 
                                       price_levels: List[float], 
                                       base_price: float) -> int:
        """
        改进的单笔交易数量计算（确保全部买点成交时不超出网格金额）
        
        核心思路：
        1. 识别真正的买入网格（低于基准价格的网格点）
        2. 基于买入网格的总价格成本计算单笔股数
        3. 确保所有买入网格同时成交时总费用不超过可用资金
        
        公式：单笔股数 = 可用网格资金 ÷ Σ(买入价格)
        
        Args:
            available_grid_amount: 可用网格资金
            price_levels: 价格水平列表
            base_price: 基准价格（当前价格）
            
        Returns:
            单笔交易数量（100股的整数倍）
        """
        try:
            if not price_levels or available_grid_amount <= 0:
                return 100
            
            # 1. 识别买入网格（低于基准价格的网格点）
            buy_levels = [price for price in price_levels if price < base_price]
            
            if not buy_levels:
                logger.warning("没有找到买入网格点，使用默认数量")
                return 100
            
            # 2. 计算买入网格的总价格成本
            total_buy_price_cost = sum(buy_levels)
            
            # 3. 基于总成本计算单笔股数
            # 公式：单笔股数 = 可用网格资金 ÷ 买入网格总价格成本
            theoretical_shares = available_grid_amount / total_buy_price_cost
            
            # 4. 向下取整到100股的整数倍
            shares_per_100 = int(theoretical_shares / 100)
            single_trade_quantity = max(1, shares_per_100) * 100
            
            # 5. 验证资金安全性
            total_required_fund = sum(price * single_trade_quantity for price in buy_levels)
            safety_ratio = total_required_fund / available_grid_amount
            
            # 6. 如果超出资金限制，进一步调整
            if safety_ratio > 1:  
                adjustment_factor = 1 / safety_ratio
                adjusted_shares = int(single_trade_quantity * adjustment_factor / 100) * 100
                single_trade_quantity = max(100, adjusted_shares)
                
                # 重新计算最终的资金使用情况
                final_required_fund = sum(price * single_trade_quantity for price in buy_levels)
                final_safety_ratio = final_required_fund / available_grid_amount
                
                logger.info(f"资金超限调整: 原始{safety_ratio:.1%} -> 调整后{final_safety_ratio:.1%}")
            
            logger.info(f"改进的单笔数量计算: "
                       f"买入网格{len(buy_levels)}个, "
                       f"价格区间[{min(buy_levels):.3f}, {max(buy_levels):.3f}], "
                       f"总价格成本{total_buy_price_cost:.2f}, "
                       f"理论股数{theoretical_shares:.0f}, "
                       f"最终数量{single_trade_quantity}股, "
                       f"资金利用率{safety_ratio:.1%}")
            
            return single_trade_quantity
            
        except Exception as e:
            logger.error(f"改进的单笔数量计算失败: {str(e)}")
            return 100
