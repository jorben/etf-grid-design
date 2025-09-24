"""
等比网格计算器 - 纯算法实现
从服务层抽离的等比网格核心算法模块
"""

import numpy as np
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)

class GeometricGridCalculator:
    """等比网格计算器"""
    
    def calculate_grid_levels(self, price_lower: float, price_upper: float,
                            grid_count: int, base_price: float) -> List[float]:
        """
        计算等比网格价位
        
        Args:
            price_lower: 价格下边界
            price_upper: 价格上边界
            grid_count: 网格数量
            base_price: 基准价格（当前价格，作为网格中心）
            
        Returns:
            价格水平列表（包含基准价格和所有网格点）
        """
        try:
            # 输入验证
            if not (price_lower <= base_price <= price_upper):
                base_price = max(price_lower, min(price_upper, base_price))
                logger.warning(f"基准价格调整到区间内: {base_price}")
            
            price_levels = [base_price]  # 基准价格作为中心点
            
            if price_lower > 0 and price_upper > price_lower:
                # 基于网格数量计算步长比例
                step_ratio = self._calculate_step_ratio(price_lower, price_upper, grid_count, base_price)
                
                # 重新计算实际的网格数量分配
                if price_upper > base_price and step_ratio > 0:
                    # 向上网格数量 = ln(上限/基准) / ln(1 + 步长比例)
                    upper_grids = int(np.log(price_upper / base_price) / np.log(1 + step_ratio))
                else:
                    upper_grids = 0
                    
                if base_price > price_lower and step_ratio > 0:
                    # 向下网格数量 = ln(基准/下限) / ln(1 + 步长比例)
                    lower_grids = int(np.log(base_price / price_lower) / np.log(1 + step_ratio))
                else:
                    lower_grids = 0
                
                # 生成向上网格点
                if upper_grids > 0:
                    multiplier = 1 + step_ratio
                    current_price = base_price
                    for i in range(upper_grids):
                        current_price *= multiplier
                        # 确保不超过上边界
                        if current_price <= price_upper:
                            price_levels.append(current_price)
                        else:
                            # 如果超出边界，使用边界价格作为最后一个网格点
                            if abs(current_price - price_upper) / price_upper > 0.01:  # 误差超过1%
                                price_levels.append(price_upper)
                            break
                
                # 生成向下网格点
                if lower_grids > 0:
                    divisor = 1 + step_ratio
                    current_price = base_price
                    for i in range(lower_grids):
                        current_price /= divisor
                        # 确保不低于下边界
                        if current_price >= price_lower:
                            price_levels.append(current_price)
                        else:
                            # 如果超出边界，使用边界价格作为最后一个网格点
                            if abs(current_price - price_lower) / price_lower > 0.01:  # 误差超过1%
                                price_levels.append(price_lower)
                            break
                
                logger.debug(f"等比网格生成: 基准{base_price:.3f}, 步长比例{step_ratio:.4f}, "
                           f"上方{upper_grids}格, 下方{lower_grids}格, 共{len(price_levels)}个价格点")
            
            # 按价格升序排列
            price_levels.sort()
            
            # 去除重复价格（保留3位小数精度）
            unique_levels = []
            for price in price_levels:
                rounded_price = round(price, 3)
                if not unique_levels or abs(rounded_price - unique_levels[-1]) > 0.001:
                    unique_levels.append(rounded_price)
            
            logger.info(f"等比网格生成: 基准{base_price:.3f}, 目标{grid_count}格, "
                       f"实际{len(unique_levels)}个价格点")
            
            return unique_levels
            
        except Exception as e:
            logger.error(f"等比网格计算失败: {str(e)}")
            return [base_price]  # 至少返回基准价格
    
    def calculate_grid_count_from_step(self, price_lower: float, price_upper: float, 
                                      step_size: float, base_price: float) -> int:
        """
        基于步长准确计算等比网格数量
        
        Args:
            price_lower: 价格下边界
            price_upper: 价格上边界  
            step_size: 网格步长（绝对值）
            base_price: 基准价格（当前价格，作为网格中心）
            
        Returns:
            网格数量（不包含基准价格点）
        """
        try:
            # 输入验证
            if step_size <= 0:
                logger.error(f"步长必须大于0，当前值: {step_size}")
                return 50
            
            if price_upper <= price_lower:
                logger.error(f"价格上限必须大于下限，当前: [{price_lower}, {price_upper}]")
                return 50
            
            if not (price_lower <= base_price <= price_upper):
                logger.warning(f"基准价格{base_price}超出区间[{price_lower}, {price_upper}]")
                # 将基准价格调整到区间内
                base_price = max(price_lower, min(price_upper, base_price))
                logger.info(f"基准价格调整为: {base_price}")
            
            # 将绝对步长转换为相对于基准价格的比例
            step_ratio = step_size / base_price
            
            # 等比网格：以基准价格为中心，向上下各扩展
            # 上方网格数量 = ln(价格上限/基准价格) / ln(1 + 步长比例)
            # 下方网格数量 = ln(基准价格/价格下限) / ln(1 + 步长比例)
            
            if price_upper > base_price and step_ratio > 0:
                upper_grids = int(np.log(price_upper / base_price) / np.log(1 + step_ratio))
            else:
                upper_grids = 0
                
            if base_price > price_lower and step_ratio > 0:
                lower_grids = int(np.log(base_price / price_lower) / np.log(1 + step_ratio))
            else:
                lower_grids = 0
            
            # 总网格数量 = 上方网格 + 下方网格
            grid_count = upper_grids + lower_grids
            
            # 限制网格数量在合理范围内（2-160个）
            original_count = grid_count
            grid_count = max(2, min(160, grid_count))
            
            if original_count != grid_count:
                logger.warning(f"网格数量调整: 原始计算{original_count}个 -> 调整后{grid_count}个")
            
            logger.info(f"等比网格数量计算: 基准价格{base_price:.3f}, 步长{step_size:.3f}({step_ratio:.1%}), "
                       f"上方{upper_grids}格, 下方{lower_grids}格, 总计{grid_count}个")
            
            return grid_count
            
        except Exception as e:
            logger.error(f"基于步长计算等比网格数量失败: {str(e)}")
            return 50  # 默认50个
    
    def _calculate_step_ratio(self, price_lower: float, price_upper: float,
                            grid_count: int, base_price: float) -> float:
        """
        计算等比网格的步长比例
        
        Args:
            price_lower: 价格下边界
            price_upper: 价格上边界
            grid_count: 网格数量
            base_price: 基准价格
            
        Returns:
            步长比例
        """
        try:
            # 计算上下方向的比例
            upper_ratio = (price_upper - base_price) / base_price if price_upper > base_price else 0
            lower_ratio = (base_price - price_lower) / base_price if base_price > price_lower else 0
            
            # 基于网格数量计算平均步长比例
            if upper_ratio > 0 and lower_ratio > 0:
                # 上下都有网格，取平均值
                avg_ratio = (upper_ratio + lower_ratio) / 2
                step_ratio = avg_ratio / (grid_count / 2)
            elif upper_ratio > 0:
                # 只有上方有网格
                step_ratio = upper_ratio / grid_count
            elif lower_ratio > 0:
                # 只有下方有网格
                step_ratio = lower_ratio / grid_count
            else:
                # 基准价格在边界上
                step_ratio = 0.01  # 默认1%
            
            # 限制步长比例在合理范围内（0.1% - 10%）
            step_ratio = max(0.001, min(0.1, step_ratio))
            
            return step_ratio
            
        except Exception as e:
            logger.error(f"等比网格步长比例计算失败: {str(e)}")
            return 0.01  # 默认1%
    
    def optimize_grid_spacing(self, price_data: List[float], 
                            volatility: float) -> float:
        """
        优化等比网格间距
        
        Args:
            price_data: 历史价格数据
            volatility: 年化波动率
            
        Returns:
            优化的网格间距（绝对值）
        """
        try:
            if not price_data:
                return 0.01  # 默认间距
            
            # 基于波动率计算基础间距比例
            base_spacing_ratio = volatility / np.sqrt(252)  # 日波动率
            
            # 考虑价格水平调整
            price_range = max(price_data) - min(price_data)
            avg_price = np.mean(price_data)
            range_adjustment = price_range / len(price_data) / avg_price * 0.1
            
            # 最终间距比例
            optimal_spacing_ratio = base_spacing_ratio + range_adjustment
            
            # 限制在合理范围内（0.1% - 5%）
            optimal_spacing_ratio = max(0.001, min(0.05, optimal_spacing_ratio))
            
            # 转换为绝对间距
            optimal_spacing = avg_price * optimal_spacing_ratio
            
            logger.info(f"等比网格间距优化: 基础比例{base_spacing_ratio:.4f}, 调整{range_adjustment:.4f}, "
                       f"最终比例{optimal_spacing_ratio:.4f}, 绝对间距{optimal_spacing:.4f}")
            
            return optimal_spacing
            
        except Exception as e:
            logger.error(f"等比网格间距优化失败: {str(e)}")
            return 0.01  # 默认间距
    
    def validate_grid_parameters(self, price_lower: float, price_upper: float,
                               grid_count: int, base_price: float) -> Tuple[bool, str]:
        """
        验证等比网格参数的有效性
        
        Args:
            price_lower: 价格下边界
            price_upper: 价格上边界
            grid_count: 网格数量
            base_price: 基准价格
            
        Returns:
            (是否有效, 错误信息)
        """
        try:
            # 检查价格区间
            if price_upper <= price_lower:
                return False, "价格上限必须大于下限"
            
            # 检查基准价格
            if not (price_lower <= base_price <= price_upper):
                return False, "基准价格必须在价格区间内"
            
            # 检查网格数量
            if grid_count < 2:
                return False, "网格数量至少为2个"
            if grid_count > 200:
                return False, "网格数量不能超过200个"
            
            # 检查价格区间合理性
            price_range_ratio = (price_upper - price_lower) / base_price
            if price_range_ratio < 0.05:
                return False, "价格区间过小（小于5%）"
            if price_range_ratio > 1.0:
                return False, "价格区间过大（超过100%）"
            
            # 等比网格特殊检查：价格必须为正数
            if price_lower <= 0:
                return False, "价格下边界必须为正数"
            
            return True, "参数有效"
            
        except Exception as e:
            logger.error(f"等比网格参数验证失败: {str(e)}")
            return False, f"参数验证异常: {str(e)}"
