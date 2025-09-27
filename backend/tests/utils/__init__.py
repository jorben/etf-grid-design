"""
测试工具模块
提供测试辅助函数和工具
"""

from typing import Any, Dict, List, Optional
import json
import tempfile
import os


class TestDataGenerator:
    """测试数据生成器"""
    
    @staticmethod
    def generate_etf_data(etf_code: str = "510300") -> Dict[str, Any]:
        """生成ETF测试数据"""
        return {
            "code": etf_code,
            "name": f"测试ETF{etf_code}",
            "current_price": 3.85,
            "change_pct": 0.52,
            "volume": 15000000,
            "amount": 57750000.0,
            "setup_date": "2012-05-28",
            "list_date": "2012-05-28",
            "fund_type": "ETF",
            "status": "L",
            "trade_date": "2024-01-15",
            "data_age_days": 1
        }
    
    @staticmethod
    def generate_price_series(
        start_price: float = 3.80,
        days: int = 30,
        volatility: float = 0.02
    ) -> List[Dict[str, Any]]:
        """生成价格序列测试数据"""
        import random
        from datetime import datetime, timedelta
        
        prices = []
        current_price = start_price
        base_date = datetime(2024, 1, 1)
        
        for i in range(days):
            date = base_date + timedelta(days=i)
            # 模拟价格波动
            change = random.uniform(-volatility, volatility)
            current_price = current_price * (1 + change)
            
            prices.append({
                "date": date.strftime("%Y-%m-%d"),
                "open": current_price * (1 + random.uniform(-0.01, 0.01)),
                "high": current_price * (1 + random.uniform(0, 0.02)),
                "low": current_price * (1 + random.uniform(-0.02, 0)),
                "close": current_price,
                "volume": random.randint(1000000, 20000000),
                "amount": current_price * random.randint(1000000, 20000000)
            })
        
        return prices
    
    @staticmethod
    def generate_analysis_input(
        etf_code: str = "510300",
        total_capital: float = 1000000.0
    ) -> Dict[str, Any]:
        """生成分析输入参数测试数据"""
        return {
            "etf_code": etf_code,
            "total_capital": total_capital,
            "grid_type": "等差",
            "risk_preference": "均衡",
            "analysis_days": 365
        }


class TestFileHelper:
    """测试文件辅助类"""
    
    @staticmethod
    def create_temp_json_file(data: Dict[str, Any]) -> str:
        """创建临时JSON文件"""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(data, temp_file, indent=2, ensure_ascii=False)
        temp_file.close()
        return temp_file.name
    
    @staticmethod
    def create_temp_csv_file(data: List[Dict[str, Any]]) -> str:
        """创建临时CSV文件"""
        import csv
        
        if not data:
            return ""
        
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='')
        writer = csv.DictWriter(temp_file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        temp_file.close()
        return temp_file.name
    
    @staticmethod
    def cleanup_temp_files(file_paths: List[str]):
        """清理临时文件"""
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.unlink(file_path)
            except Exception:
                pass  # 忽略清理错误


class MockHelper:
    """模拟对象辅助类"""
    
    @staticmethod
    def create_mock_function(return_value: Any = None, side_effect: Any = None):
        """创建模拟函数"""
        class MockFunction:
            def __init__(self):
                self.calls = []
                self.return_value = return_value
                self.side_effect = side_effect
            
            def __call__(self, *args, **kwargs):
                self.calls.append((args, kwargs))
                
                if self.side_effect is not None:
                    if callable(self.side_effect):
                        return self.side_effect(*args, **kwargs)
                    elif isinstance(self.side_effect, Exception):
                        raise self.side_effect
                    else:
                        return self.side_effect
                
                return self.return_value
        
        return MockFunction()
    
    @staticmethod
    def create_mock_class(**methods):
        """创建模拟类"""
        class MockClass:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)
                
                # 添加方法调用记录
                self.method_calls = {}
                for method_name in methods.keys():
                    self.method_calls[method_name] = []
        
        # 添加方法
        for method_name, return_value in methods.items():
            def create_method(method_name, return_value):
                def method(self, *args, **kwargs):
                    self.method_calls[method_name].append((args, kwargs))
                    if callable(return_value):
                        return return_value(*args, **kwargs)
                    return return_value
                return method
            
            setattr(MockClass, method_name, create_method(method_name, return_value))
        
        return MockClass


class PerformanceTestHelper:
    """性能测试辅助类"""
    
    @staticmethod
    def measure_execution_time(func, *args, **kwargs) -> float:
        """测量函数执行时间"""
        import time
        
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        
        return end_time - start_time
    
    @staticmethod
    def run_performance_test(
        func, 
        iterations: int = 1000,
        *args, **kwargs
    ) -> Dict[str, Any]:
        """运行性能测试"""
        import time
        import statistics
        
        execution_times = []
        
        for _ in range(iterations):
            start_time = time.time()
            func(*args, **kwargs)
            end_time = time.time()
            execution_times.append(end_time - start_time)
        
        return {
            "iterations": iterations,
            "total_time": sum(execution_times),
            "average_time": statistics.mean(execution_times),
            "min_time": min(execution_times),
            "max_time": max(execution_times),
            "std_dev": statistics.stdev(execution_times) if len(execution_times) > 1 else 0
        }
    
    @staticmethod
    def assert_performance_threshold(
        func, 
        max_time: float,
        iterations: int = 100,
        *args, **kwargs
    ):
        """断言性能阈值"""
        result = PerformanceTestHelper.run_performance_test(
            func, iterations, *args, **kwargs
        )
        
        assert result["average_time"] <= max_time, (
            f"性能测试失败: 平均执行时间 {result['average_time']:.6f}s "
            f"超过阈值 {max_time}s"
        )


class AsyncTestHelper:
    """异步测试辅助类"""
    
    @staticmethod
    async def run_async_function(func, *args, **kwargs):
        """运行异步函数"""
        import asyncio
        return await func(*args, **kwargs)
    
    @staticmethod
    def create_async_mock(return_value: Any = None):
        """创建异步模拟函数"""
        async def async_mock(*args, **kwargs):
            return return_value
        return async_mock


# 导出工具类
test_data_generator = TestDataGenerator()
test_file_helper = TestFileHelper()
mock_helper = MockHelper()
performance_test_helper = PerformanceTestHelper()
async_test_helper = AsyncTestHelper()


__all__ = [
    'TestDataGenerator',
    'TestFileHelper', 
    'MockHelper',
    'PerformanceTestHelper',
    'AsyncTestHelper',
    'test_data_generator',
    'test_file_helper',
    'mock_helper',
    'performance_test_helper',
    'async_test_helper'
]
