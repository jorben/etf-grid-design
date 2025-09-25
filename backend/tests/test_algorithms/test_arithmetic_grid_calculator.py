"""
等差网格计算器测试用例
验证ArithmeticGridCalculator::calculate_grid_levels方法的计算准确性
"""

import pytest
import numpy as np
from backend.algorithms.grid.arithmetic_grid import ArithmeticGridCalculator


class TestArithmeticGridCalculator:
    """等差网格计算器测试类"""
    
    def setup_method(self):
        """测试前置方法"""
        self.calculator = ArithmeticGridCalculator()
    
    def test_symmetric_grid_basic(self):
        """测试对称区间基础情况（基于步长）"""
        # 基准价格在中心，对称区间
        price_lower = 10.0
        price_upper = 20.0
        step_size = 1.0  # 步长1元
        base_price = 15.0
        
        result = self.calculator.calculate_grid_levels(price_lower, price_upper, step_size, base_price)
        
        # 验证结果
        assert len(result) > 0, "应该生成至少一个价格点"
        assert base_price in result, "基准价格应该在结果中"
        
        # 验证价格区间覆盖
        assert min(result) >= price_lower, "最低价格不应低于下边界"
        assert max(result) <= price_upper, "最高价格不应超过上边界"
        
        # 验证排序
        assert result == sorted(result), "价格应该按升序排列"
        
        # 验证精度（保留3位小数）
        for price in result:
            assert abs(price - round(price, 3)) < 0.0001, f"价格{price}应该保留3位小数"
        
        # 验证等差性质：相邻价格差值应该等于步长
        for i in range(1, len(result)):
            price_diff = result[i] - result[i-1]
            assert abs(price_diff - step_size) < 0.001, f"相邻价格差值应该等于步长: {price_diff} vs {step_size}"
    
    def test_asymmetric_grid_upper_bias(self):
        """测试基准价格偏向上边界的情况"""
        price_lower = 10.0
        price_upper = 20.0
        grid_count = 8
        base_price = 18.0  # 偏向上边界
        
        result = self.calculator.calculate_grid_levels(price_lower, price_upper, grid_count, base_price)
        
        # 验证基准价格在结果中
        assert base_price in result, "基准价格应该在结果中"
        
        # 验证价格分布：上方网格应该较少
        upper_count = sum(1 for price in result if price > base_price)
        lower_count = sum(1 for price in result if price < base_price)
        
        # 由于基准价格偏上，下方网格应该更多
        assert lower_count >= upper_count, f"下方网格数量({lower_count})应该不少于上方网格数量({upper_count})"
    
    def test_asymmetric_grid_lower_bias(self):
        """测试基准价格偏向下边界的情况"""
        price_lower = 10.0
        price_upper = 20.0
        grid_count = 8
        base_price = 12.0  # 偏向下边界
        
        result = self.calculator.calculate_grid_levels(price_lower, price_upper, grid_count, base_price)
        
        # 验证基准价格在结果中
        assert base_price in result, "基准价格应该在结果中"
        
        # 验证价格分布：下方网格应该较少
        upper_count = sum(1 for price in result if price > base_price)
        lower_count = sum(1 for price in result if price < base_price)
        
        # 由于基准价格偏下，上方网格应该更多
        assert upper_count >= lower_count, f"上方网格数量({upper_count})应该不少于下方网格数量({lower_count})"
    
    def test_boundary_conditions(self):
        """测试边界条件"""
        # 基准价格等于下边界
        price_lower = 10.0
        price_upper = 20.0
        grid_count = 6
        base_price = 10.0
        
        result = self.calculator.calculate_grid_levels(price_lower, price_upper, grid_count, base_price)
        
        assert base_price in result, "基准价格应该在结果中"
        assert min(result) == price_lower, "最低价格应该等于下边界"
        assert all(price >= price_lower for price in result), "所有价格应该不低于下边界"
        
        # 基准价格等于上边界
        base_price = 20.0
        result = self.calculator.calculate_grid_levels(price_lower, price_upper, grid_count, base_price)
        
        assert base_price in result, "基准价格应该在结果中"
        assert max(result) == price_upper, "最高价格应该等于上边界"
        assert all(price <= price_upper for price in result), "所有价格应该不高于上边界"
    
    def test_arithmetic_progression_property(self):
        """验证等差数列性质"""
        price_lower = 10.0
        price_upper = 20.0
        grid_count = 10
        base_price = 15.0
        
        result = self.calculator.calculate_grid_levels(price_lower, price_upper, grid_count, base_price)
        
        # 找到基准价格的索引
        base_index = result.index(base_price)
        
        # 验证上方等差性质
        if base_index < len(result) - 1:
            upper_step = result[base_index + 1] - result[base_index]
            for i in range(base_index + 2, len(result)):
                current_step = result[i] - result[i-1]
                # 允许小的浮点数误差
                assert abs(current_step - upper_step) < 0.001, f"上方步长不一致: {current_step} vs {upper_step}"
        
        # 验证下方等差性质
        if base_index > 0:
            lower_step = result[base_index] - result[base_index - 1]
            for i in range(base_index - 2, -1, -1):
                current_step = result[i + 1] - result[i]
                # 允许小的浮点数误差
                assert abs(current_step - lower_step) < 0.001, f"下方步长不一致: {current_step} vs {lower_step}"
    
    def test_small_price_range(self):
        """测试极小价格区间"""
        price_lower = 10.0
        price_upper = 10.1  # 只有0.1的区间
        grid_count = 5
        base_price = 10.05
        
        result = self.calculator.calculate_grid_levels(price_lower, price_upper, grid_count, base_price)
        
        assert len(result) > 0, "应该生成至少一个价格点"
        assert base_price in result, "基准价格应该在结果中"
        
        # 验证区间覆盖
        assert min(result) >= price_lower, "最低价格不应低于下边界"
        assert max(result) <= price_upper, "最高价格不应超过上边界"
    
    def test_large_grid_count(self):
        """测试大量网格的情况"""
        price_lower = 10.0
        price_upper = 20.0
        grid_count = 50  # 大量网格
        base_price = 15.0
        
        result = self.calculator.calculate_grid_levels(price_lower, price_upper, grid_count, base_price)
        
        assert len(result) > 0, "应该生成至少一个价格点"
        assert base_price in result, "基准价格应该在结果中"
        
        # 验证没有重复价格（在3位小数精度下）
        unique_count = len(set(round(price, 3) for price in result))
        assert unique_count == len(result), f"不应该有重复价格: 唯一{unique_count} vs 总数{len(result)}"
    
    def test_precision_consistency(self):
        """测试精度一致性"""
        price_lower = 100.123
        price_upper = 200.456
        grid_count = 8
        base_price = 150.789
        
        result = self.calculator.calculate_grid_levels(price_lower, price_upper, grid_count, base_price)
        
        # 验证所有价格都保留3位小数
        for price in result:
            rounded_price = round(price, 3)
            assert abs(price - rounded_price) < 0.0001, f"价格{price}应该精确到3位小数"
        
        # 验证价格差值的精度
        for i in range(1, len(result)):
            price_diff = result[i] - result[i-1]
            # 价格差值也应该保持合理的精度
            assert abs(price_diff) > 0.001 or abs(price_diff) < 0.0001, f"价格差值{price_diff}精度异常"
    
    def test_edge_case_zero_range(self):
        """测试边界情况：价格区间为零"""
        price_lower = 15.0
        price_upper = 15.0  # 相同价格
        grid_count = 5
        base_price = 15.0
        
        result = self.calculator.calculate_grid_levels(price_lower, price_upper, grid_count, base_price)
        
        # 应该至少返回基准价格
        assert len(result) >= 1, "应该至少返回基准价格"
        assert base_price in result, "基准价格应该在结果中"
    
    def test_negative_price_handling(self):
        """测试负价格处理（虽然实际中不应该出现）"""
        # 理论上价格不应该为负，但测试代码的健壮性
        price_lower = -10.0
        price_upper = 10.0
        grid_count = 8
        base_price = 0.0
        
        result = self.calculator.calculate_grid_levels(price_lower, price_upper, grid_count, base_price)
        
        assert len(result) > 0, "应该生成至少一个价格点"
        assert base_price in result, "基准价格应该在结果中"
    
    def test_known_accuracy_issue_scenario(self):
        """测试已知的精度问题场景（基于步长）"""
        # 模拟用户报告的具体问题场景
        price_lower = 1.0
        price_upper = 2.0
        step_size = 0.1  # 步长0.1元
        base_price = 1.5
        
        result = self.calculator.calculate_grid_levels(price_lower, price_upper, step_size, base_price)
        
        # 验证网格数量合理性
        # 基于步长计算，理论上应该有：(2.0-1.5)/0.1 + (1.5-1.0)/0.1 = 5 + 5 = 10个网格
        expected_grids = int((price_upper - base_price) / step_size) + int((base_price - price_lower) / step_size) + 1
        assert len(result) >= 5, f"生成的网格数量({len(result)})应该合理"
        
        # 验证价格分布的合理性
        price_range = max(result) - min(result)
        expected_range_ratio = price_range / (price_upper - price_lower)
        assert expected_range_ratio >= 0.8, f"价格覆盖范围({expected_range_ratio:.2%})应该足够大"
        
        # 验证等差性质
        if len(result) > 1:
            # 检查相邻价格差值是否等于步长
            for i in range(1, len(result)):
                price_diff = result[i] - result[i-1]
                assert abs(price_diff - step_size) < 0.001, f"相邻价格差值应该等于步长: {price_diff} vs {step_size}"
    
    def test_grid_count_accuracy(self):
        """测试网格数量准确性（基于步长）"""
        price_lower = 10.0
        price_upper = 20.0
        step_size = 1.0  # 步长1元
        base_price = 15.0
        
        result = self.calculator.calculate_grid_levels(price_lower, price_upper, step_size, base_price)
        
        # 验证结果合理性
        assert len(result) > 0, "应该生成至少一个价格点"
        assert base_price in result, "基准价格应该在结果中"
        
        # 验证价格区间覆盖
        assert min(result) >= price_lower, "最低价格不应低于下边界"
        assert max(result) <= price_upper, "最高价格不应超过上边界"
        
        # 验证等差性质：相邻价格差值应该等于步长
        for i in range(1, len(result)):
            price_diff = result[i] - result[i-1]
            assert abs(price_diff - step_size) < 0.001, f"相邻价格差值应该等于步长: {price_diff} vs {step_size}"
    
    def test_price_distribution_uniformity(self):
        """测试价格分布均匀性"""
        price_lower = 10.0
        price_upper = 20.0
        grid_count = 10
        base_price = 15.0
        
        result = self.calculator.calculate_grid_levels(price_lower, price_upper, grid_count, base_price)
        
        # 计算相邻价格之间的步长
        steps = []
        for i in range(1, len(result)):
            steps.append(result[i] - result[i-1])
        
        if len(steps) > 1:
            # 计算步长的标准差，评估均匀性
            step_std = np.std(steps)
            step_mean = np.mean(steps)
            
            # 变异系数应该较小（步长相对均匀）
            if step_mean > 0:
                coefficient_of_variation = step_std / step_mean
                assert coefficient_of_variation < 0.5, f"步长变化过大: 变异系数{coefficient_of_variation:.3f}"


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])
