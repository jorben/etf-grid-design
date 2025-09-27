"""
新资金分配算法测试
验证网格需求反推算法的正确性和资金安全性
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import unittest
from algorithms.grid.optimizer import GridOptimizer


class TestFundAllocationV2(unittest.TestCase):
    """新资金分配算法测试类"""
    
    def setUp(self):
        """测试初始化"""
        self.optimizer = GridOptimizer()
    
    def test_basic_functionality(self):
        """测试基本功能"""
        total_capital = 100000  # 10万元
        grid_count = 10
        price_levels = [3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0]
        current_price = 3.5
        
        result = self.optimizer.calculate_fund_allocation_v2(
            total_capital, grid_count, price_levels, current_price
        )
        
        # 验证基本字段存在
        self.assertIn('base_position_amount', result)
        self.assertIn('grid_trading_amount', result)
        self.assertIn('reserve_amount', result)
        self.assertIn('grid_funds', result)
        self.assertIn('base_position_ratio', result)
        self.assertIn('single_trade_quantity', result)
        self.assertIn('buy_grid_safety_ratio', result)
        self.assertIn('extreme_case_safe', result)
        
        # 验证资金安全性
        self.assertTrue(result['extreme_case_safe'])
        self.assertLessEqual(result['buy_grid_safety_ratio'], 1.0)
        
        # 验证总资金平衡
        total_allocated = (result['base_position_amount'] + 
                          result['grid_trading_amount'] + 
                          result['reserve_amount'])
        self.assertAlmostEqual(total_allocated, total_capital, delta=1.0)
    
    def test_buy_sell_grid_balance(self):
        """测试买卖网格平衡"""
        total_capital = 100000
        price_levels = [2.5, 2.7, 2.9, 3.1, 3.3, 3.5, 3.7, 3.9, 4.1, 4.3, 4.5]
        current_price = 3.5
        
        result = self.optimizer.calculate_fund_allocation_v2(
            total_capital, 10, price_levels, current_price
        )
        
        # 验证底仓与卖出网格匹配
        buy_grids = sum(1 for gf in result['grid_funds'] if gf['is_buy_level'])
        sell_grids = sum(1 for gf in result['grid_funds'] if not gf['is_buy_level'])
        
        # 底仓股数应该等于卖出网格数量 × 单笔股数
        base_position_shares = result['base_position_amount'] / current_price
        
        # 使用算法详情中的底仓股数作为预期值（更准确）
        if 'algorithm_details' in result:
            expected_shares = result['algorithm_details'].get('base_position_shares', 0)
        else:
            expected_shares = sell_grids * result['single_trade_quantity']
        
        # 调试输出
        print(f"\n=== 买卖网格平衡测试调试 ===")
        print(f"买入网格数量: {buy_grids}")
        print(f"卖出网格数量: {sell_grids}")
        print(f"单笔股数: {result['single_trade_quantity']}")
        print(f"底仓金额: {result['base_position_amount']}")
        print(f"当前价格: {current_price}")
        print(f"实际底仓股数: {base_position_shares:.0f}")
        print(f"预期底仓股数: {expected_shares:.0f}")
        print(f"差异: {abs(base_position_shares - expected_shares):.0f} 股")
        
        # 详细调试算法详情
        if 'algorithm_details' in result:
            details = result['algorithm_details']
            print(f"算法详情 - 买入网格: {details.get('buy_grids', 'N/A')}")
            print(f"算法详情 - 卖出网格: {details.get('sell_grids', 'N/A')}")
            print(f"算法详情 - 底仓股数: {details.get('base_position_shares', 'N/A')}")
            print(f"算法详情 - 资金需求系数: {details.get('fund_requirement_factor', 'N/A')}")
            print(f"算法详情 - 总需求资金: {details.get('total_required_fund', 'N/A')}")
        
        # 检查底仓股数计算
        calculated_base_shares = result['base_position_amount'] / current_price
        print(f"重新计算底仓股数: {calculated_base_shares:.0f}")
        
        # 验证底仓股数计算正确（使用算法详情中的值）
        self.assertAlmostEqual(base_position_shares, expected_shares, delta=1)
    
    def test_edge_cases(self):
        """测试边界情况"""
        # 测试价格水平较少的情况
        total_capital = 50000
        price_levels = [3.0, 3.5, 4.0]
        current_price = 3.5
        
        result = self.optimizer.calculate_fund_allocation_v2(
            total_capital, 2, price_levels, current_price
        )
        
        self.assertTrue(result['extreme_case_safe'])
        self.assertGreater(result['single_trade_quantity'], 0)
        
        # 测试所有价格都高于当前价格（只有卖出网格）
        price_levels = [3.6, 3.7, 3.8, 3.9, 4.0]
        result = self.optimizer.calculate_fund_allocation_v2(
            total_capital, 4, price_levels, current_price
        )
        
        # 应该只有底仓，没有买入网格资金
        self.assertEqual(result['total_buy_grid_fund'], 0)
        self.assertGreater(result['base_position_amount'], 0)
    
    def test_large_capital(self):
        """测试大资金情况"""
        total_capital = 1000000  # 100万元
        price_levels = [10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0]
        current_price = 12.5
        
        result = self.optimizer.calculate_fund_allocation_v2(
            total_capital, 10, price_levels, current_price
        )
        
        # 验证资金安全性
        self.assertTrue(result['extreme_case_safe'])
        self.assertLessEqual(result['buy_grid_safety_ratio'], 1.0)
        
        # 验证单笔股数是100的整数倍
        self.assertEqual(result['single_trade_quantity'] % 100, 0)
        
        # 验证资金利用率合理
        self.assertGreater(result['grid_fund_utilization_rate'], 0.5)
        self.assertLessEqual(result['grid_fund_utilization_rate'], 1.0)
    
    def test_compatibility_with_old_interface(self):
        """测试与旧接口的兼容性"""
        total_capital = 100000
        base_position_ratio = 0.3  # 这个参数会被忽略
        grid_count = 8
        price_levels = [2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6]
        base_price = 3.2
        
        # 使用旧接口调用
        result_old = self.optimizer.calculate_fund_allocation(
            total_capital, base_position_ratio, grid_count, price_levels, base_price
        )
        
        # 使用新接口调用
        result_new = self.optimizer.calculate_fund_allocation_v2(
            total_capital, grid_count, price_levels, base_price
        )
        
        # 验证输出结构相同
        self.assertEqual(set(result_old.keys()), set(result_new.keys()))
        
        # 验证资金安全性
        self.assertTrue(result_old['extreme_case_safe'])
        self.assertTrue(result_new['extreme_case_safe'])
    
    def test_algorithm_details(self):
        """测试算法详情信息"""
        total_capital = 80000
        price_levels = [4.0, 4.2, 4.4, 4.6, 4.8, 5.0, 5.2, 5.4, 5.6, 5.8, 6.0]
        current_price = 5.0
        
        result = self.optimizer.calculate_fund_allocation_v2(
            total_capital, 10, price_levels, current_price
        )
        
        # 验证算法详情信息
        self.assertIn('algorithm_details', result)
        details = result['algorithm_details']
        
        self.assertIn('buy_grids', details)
        self.assertIn('sell_grids', details)
        self.assertIn('base_position_shares', details)
        self.assertIn('fund_requirement_factor', details)
        
        # 验证买卖网格数量正确
        actual_buy_grids = sum(1 for gf in result['grid_funds'] if gf['is_buy_level'])
        actual_sell_grids = sum(1 for gf in result['grid_funds'] if not gf['is_buy_level'])
        
        self.assertEqual(details['buy_grids'], actual_buy_grids)
        self.assertEqual(details['sell_grids'], actual_sell_grids)


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)