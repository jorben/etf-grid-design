"""
等差网格计算器 - 纯算法实现
从服务层抽离的等差网格核心算法模块
"""

import numpy as np
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)

class ArithmeticGridCalculator:
    """等差网格计算器"""
    
    def calculate_grid_levels(self, price_lower: float, price_upper: float, 
                            step_size: float, base_price: float) -> List[float]:
        """
        计算等差网格价位（基于步长）
        
        Args:
            price_lower: 价格下边界
            price_upper: 价格上边界
            step_size: 网格步长（绝对值）
            base_price: 基准价格（当前价格，作为网格中心）
            
        Returns:
            价格水平列表（包含基准价格和所有网格点）
        """
        try:
            # 输入验证
            if step_size <= 0:
                logger.error(f"步长必须大于0，当前值: {step_size}")
                return [base_price]
            
            if not (price_lower <= base_price <= price_upper):
                base_price = max(price_lower, min(price_upper, base_price))
                logger.warning(f"基准价格调整到区间内: {base_price}")
            
            price_levels = [base_price]  # 基准价格作为中心点
            
            # 向上扩展网格点
            current_price = base_price
            while current_price + step_size <= price_upper:
                current_price += step_size
                price_levels.append(current_price)
            
            # 向下扩展网格点
            current_price = base_price
            while current_price - step_size >= price_lower:
                current_price -= step_size
                price_levels.append(current_price)
            
            # 按价格升序排列
            price_levels.sort()
            
            # 去除重复价格（保留3位小数精度）
            unique_levels = []
            for price in price_levels:
                rounded_price = round(price, 3)
                if not unique_levels or abs(rounded_price - unique_levels[-1]) > 0.001:
                    unique_levels.append(rounded_price)
            
            logger.info(f"等差网格生成: 基准{base_price:.3f}, 步长{step_size:.3f}, "
                       f"共{len(unique_levels)}个价格点")
            
            return unique_levels
            
        except Exception as e:
            logger.error(f"等差网格计算失败: {str(e)}")
            return [base_price]  # 至少返回基准价格
    
    def calculate_grid_count_from_step(self, price_lower: float, price_upper: float, 
                                      step_size: float, base_price: float) -> int:
        """
        基于步长准确计算等差网格数量
        
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
            
            # 等差网格：以基准价格为中心，向上下各扩展
            # 上方网格数量 = (价格上限 - 基准价格) / 步长
            # 下方网格数量 = (基准价格 - 价格下限) / 步长
            upper_grids = int((price_upper - base_price) / step_size)
            lower_grids = int((base_price - price_lower) / step_size)
            
            # 总网格数量 = 上方网格 + 下方网格
            grid_count = upper_grids + lower_grids
            
            # 限制网格数量在合理范围内（2-160个）
            original_count = grid_count
            grid_count = max(2, min(160, grid_count))
            
            if original_count != grid_count:
                logger.warning(f"网格数量调整: 原始计算{original_count}个 -> 调整后{grid_count}个")
            
            logger.info(f"等差网格数量计算: 基准价格{base_price:.3f}, 步长{step_size:.3f}, "
                       f"上方{upper_grids}格, 下方{lower_grids}格, 总计{grid_count}个")
            
            return grid_count
            
        except Exception as e:
            logger.error(f"基于步长计算等差网格数量失败: {str(e)}")
            return 50  # 默认50个
    
    def optimize_grid_spacing(self, price_data: List[float], 
                            volatility: float) -> float:
        """
        优化等差网格间距
        
        Args:
            price_data: 历史价格数据
            volatility: 年化波动率
            
        Returns:
            优化的网格间距（绝对值）
        """
        try:
            if not price_data:
                return 0.01  # 默认间距
            
            # 基于波动率计算基础间距
            avg_price = np.mean(price_data)
            base_spacing = avg_price * volatility / np.sqrt(252)  # 日波动率
            
            # 考虑价格水平调整
            price_range = max(price_data) - min(price_data)
            range_adjustment = price_range / len(price_data) * 0.1
            
            # 最终间距
            optimal_spacing = base_spacing + range_adjustment
            
            # 限制在合理范围内（0.1% - 5%）
            min_spacing = avg_price * 0.001  # 0.1%
            max_spacing = avg_price * 0.05   # 5%
            optimal_spacing = max(min_spacing, min(max_spacing, optimal_spacing))
            
            logger.info(f"等差网格间距优化: 基础{base_spacing:.4f}, 调整{range_adjustment:.4f}, "
                       f"最终{optimal_spacing:.4f}")
            
            return optimal_spacing
            
        except Exception as e:
            logger.error(f"等差网格间距优化失败: {str(e)}")
            return 0.01  # 默认间距
    
    def validate_grid_parameters(self, price_lower: float, price_upper: float,
                               grid_count: int, base_price: float) -> Tuple[bool, str]:
        """
        验证等差网格参数的有效性
        
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
            
            return True, "参数有效"
            
        except Exception as e:
            logger.error(f"网格参数验证失败: {str(e)}")
            return False, f"参数验证异常: {str(e)}"
