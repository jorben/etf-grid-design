"""
等比网格计算器测试用例
验证GeometricGridCalculator::calculate_grid_levels方法的计算准确性
"""

import pytest
import numpy as np
from backend.algorithms.grid.geometric_grid import GeometricGridCalculator


class TestGeometricGridCalculator:
    """等比网格计算器测试类"""
    
    def setup_method(self):
        """测试前置方法"""
        self.calculator = GeometricGridCalculator()
    
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
        
        # 验证等比性质：相邻价格比例应该一致
        if len(result) > 1:
            step_ratio = step_size / base_price
            expected_ratio = 1 + step_ratio
            
            # 验证向上网格的比例一致性
            base_index = result.index(base_price)
            if base_index < len(result) - 1:
                for i in range(base_index + 1, len(result)):
                    actual_ratio = result[i] / result[i-1]
                    assert abs(actual_ratio - expected_ratio) < 0.001, f"向上比例不一致: {actual_ratio} vs {expected_ratio}"
            
            # 验证向下网格的比例一致性
            if base_index > 0:
                for i in range(base_index - 1, -1, -1):
                    actual_ratio = result[i+1] / result[i]
                    expected_down_ratio = 1 / expected_ratio
                    assert abs(actual_ratio - expected_down_ratio) < 0.001, f"向下比例不一致: {actual_ratio} vs {expected_down_ratio}"
    
    def test_geometric_progression_property(self):
        """验证等比数列性质（基于步长）"""
        price_lower = 1.292
        price_upper = 1.768
        step_size = 0.05  # 步长0.05元
        base_price = 1.530
        
        result = self.calculator.calculate_grid_levels(price_lower, price_upper, step_size, base_price)

        # 找到基准价格的索引
        base_index = result.index(base_price)
        
        # 验证上方等比性质
        if base_index < len(result) - 1:
            upper_ratio = result[base_index + 1] / result[base_index]
            for i in range(base_index + 2, len(result)):
                current_ratio = result[i] / result[i-1]
                # 允许小的浮点数误差
                assert abs(current_ratio - upper_ratio) < 0.001, f"上方比例不一致: {current_ratio} vs {upper_ratio}"
        
        # 验证下方等比性质
        if base_index > 0:
            lower_ratio = result[base_index] / result[base_index - 1]
            for i in range(base_index - 2, -1, -1):
                current_ratio = result[i + 1] / result[i]
                # 允许小的浮点数误差
                assert abs(current_ratio - lower_ratio) < 0.001, f"下方比例不一致: {current_ratio} vs {lower_ratio}"
    
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
        
        # 验证价格比例的精度
        for i in range(1, len(result)):
            if result[i-1] > 0:  # 避免除零
                price_ratio = result[i] / result[i-1]
                # 比例值也应该保持合理的精度
                assert price_ratio > 0, f"价格比例应该为正数: {price_ratio}"
    
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
    
    def test_very_small_prices(self):
        """测试极小价格值"""
        price_lower = 0.01
        price_upper = 0.02
        grid_count = 6
        base_price = 0.015
        
        result = self.calculator.calculate_grid_levels(price_lower, price_upper, grid_count, base_price)
        
        assert len(result) > 0, "应该生成至少一个价格点"
        assert base_price in result, "基准价格应该在结果中"
        
        # 验证所有价格为正数（等比网格的要求）
        for price in result:
            assert price > 0, f"等比网格价格必须为正数: {price}"
    
    def test_large_price_values(self):
        """测试极大价格值"""
        price_lower = 1000.0
        price_upper = 2000.0
        grid_count = 8
        base_price = 1500.0
        
        result = self.calculator.calculate_grid_levels(price_lower, price_upper, grid_count, base_price)
        
        assert len(result) > 0, "应该生成至少一个价格点"
        assert base_price in result, "基准价格应该在结果中"
        
        # 验证区间覆盖
        assert min(result) >= price_lower, "最低价格不应低于下边界"
        assert max(result) <= price_upper, "最高价格不应超过上边界"
    
    def test_known_accuracy_issue_scenario(self):
        """测试已知的精度问题场景"""
        # 模拟用户报告的具体问题场景
        price_lower = 1.0
        price_upper = 2.0
        grid_count = 10
        base_price = 1.5
        
        result = self.calculator.calculate_grid_levels(price_lower, price_upper, grid_count, base_price)
        
        # 使用Calculator工具验证关键计算
        # 这里可以添加具体的验证逻辑
        
        # 验证网格数量合理性
        expected_min_grids = grid_count // 2  # 至少应该有一半的网格
        assert len(result) >= expected_min_grids, f"生成的网格数量({len(result)})应该不少于期望值({expected_min_grids})"
        
        # 验证价格分布的合理性
        price_range = max(result) - min(result)
        expected_range_ratio = price_range / (price_upper - price_lower)
        assert expected_range_ratio >= 0.8, f"价格覆盖范围({expected_range_ratio:.2%})应该足够大"
        
        # 验证对数计算的准确性
        if len(result) > 1:
            # 检查相邻价格的比例是否相对一致
            ratios = []
            for i in range(1, len(result)):
                if result[i-1] > 0:
                    ratios.append(result[i] / result[i-1])
            
            if len(ratios) > 1:
                ratio_std = np.std(ratios)
                ratio_mean = np.mean(ratios)
                if ratio_mean > 0:
                    cv = ratio_std / ratio_mean
                    assert cv < 0.1, f"价格比例变化过大: 变异系数{cv:.3f}"
    
    def test_grid_count_accuracy(self):
        """测试网格数量准确性"""
        price_lower = 10.0
        price_upper = 20.0
        grid_count = 12
        base_price = 15.0
        
        result = self.calculator.calculate_grid_levels(price_lower, price_upper, grid_count, base_price)
        
        # 计算实际网格数量（不包括基准价格）
        actual_grid_count = len(result) - 1
        
        # 实际网格数量应该接近目标值，允许一定的偏差
        count_diff = abs(actual_grid_count - grid_count)
        assert count_diff <= grid_count * 0.3, f"网格数量偏差({count_diff})过大: 实际{actual_grid_count} vs 目标{grid_count}"
    
    def test_price_distribution_uniformity(self):
        """测试价格分布均匀性"""
        price_lower = 10.0
        price_upper = 20.0
        grid_count = 10
        base_price = 15.0
        
        result = self.calculator.calculate_grid_levels(price_lower, price_upper, grid_count, base_price)
        
        # 计算相邻价格之间的比例
        ratios = []
        for i in range(1, len(result)):
            if result[i-1] > 0:
                ratios.append(result[i] / result[i-1])
        
        if len(ratios) > 1:
            # 计算比例的统计特性
            ratio_std = np.std(ratios)
            ratio_mean = np.mean(ratios)
            
            # 变异系数应该较小（比例相对一致）
            if ratio_mean > 0:
                coefficient_of_variation = ratio_std / ratio_mean
                assert coefficient_of_variation < 0.3, f"价格比例变化过大: 变异系数{coefficient_of_variation:.3f}"
    
    def test_step_ratio_calculation_accuracy(self):
        """测试步长比例计算准确性"""
        price_lower = 10.0
        price_upper = 20.0
        grid_count = 8
        base_price = 15.0
        
        # 调用私有方法计算步长比例
        step_ratio = self.calculator._calculate_step_ratio(price_lower, price_upper, grid_count, base_price)
        
        # 验证步长比例在合理范围内
        assert 0.001 <= step_ratio <= 0.1, f"步长比例{step_ratio}应该在合理范围内(0.1%-10%)"
        
        # 使用步长比例验证网格生成
        result = self.calculator.calculate_grid_levels(price_lower, price_upper, grid_count, base_price)
        
        if len(result) > 1:
            # 验证实际生成的价格比例与计算的比例是否一致
            actual_ratios = []
            for i in range(1, len(result)):
                if result[i-1] > 0:
                    actual_ratios.append(result[i] / result[i-1])
            
            if actual_ratios:
                avg_actual_ratio = np.mean(actual_ratios)
                # 实际平均比例应该接近理论步长比例
                ratio_diff = abs(avg_actual_ratio - (1 + step_ratio))
                assert ratio_diff < 0.01, f"实际比例与理论比例差异过大: {ratio_diff}"
    
    def test_logarithmic_calculation_precision(self):
        """测试对数计算精度"""
        price_lower = 1.0
        price_upper = 10.0
        grid_count = 9  # 这样理论上应该生成10个点（包括基准）
        base_price = 3.0
        
        result = self.calculator.calculate_grid_levels(price_lower, price_upper, grid_count, base_price)
        
        # 验证对数计算的准确性
        if len(result) > 1:
            # 检查价格的对数是否呈线性关系
            log_prices = [np.log(price) for price in result if price > 0]
            
            if len(log_prices) > 2:
                # 计算对数价格的差值（应该相对均匀）
                log_diffs = []
                for i in range(1, len(log_prices)):
                    log_diffs.append(log_prices[i] - log_prices[i-1])
                
                if log_diffs:
                    log_diff_std = np.std(log_diffs)
                    log_diff_mean = np.mean(log_diffs)
                    
                    # 对数差值的变异系数应该很小
                    if log_diff_mean > 0:
                        cv = log_diff_std / log_diff_mean
                        assert cv < 0.2, f"对数价格差值变化过大: 变异系数{cv:.3f}"
    
    def test_edge_case_boundary_precision(self):
        """测试边界精度处理"""
        # 测试价格非常接近边界的情况
        price_lower = 10.0
        price_upper = 20.0
        grid_count = 100  # 大量网格，可能产生边界精度问题
        base_price = 15.0
        
        result = self.calculator.calculate_grid_levels(price_lower, price_upper, grid_count, base_price)
        
        # 验证边界处理
        assert min(result) >= price_lower, f"最低价格{min(result)}不应低于下边界{price_lower}"
        assert max(result) <= price_upper, f"最高价格{max(result)}不应超过上边界{price_upper}"
        
        # 验证没有价格超出边界（考虑浮点数精度）
        tolerance = 0.001  # 1%的容差
        for price in result:
            assert price >= price_lower - tolerance, f"价格{price}超出下边界容差范围"
            assert price <= price_upper + tolerance, f"价格{price}超出上边界容差范围"


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])
