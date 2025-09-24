"""
服务接口模块
定义服务层的接口规范，实现依赖注入机制
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import pandas as pd

class AlgorithmInterface(ABC):
    """算法服务接口"""
    
    @abstractmethod
    def calculate_atr(self, df: pd.DataFrame) -> pd.DataFrame:
        """计算ATR指标"""
        pass
    
    @abstractmethod
    def calculate_grid_levels(self, price_lower: float, price_upper: float, 
                            grid_count: int, grid_type: str, base_price: float) -> List[float]:
        """计算网格价格水平"""
        pass
    
    @abstractmethod
    def optimize_grid_parameters(self, df: pd.DataFrame, risk_preference: str) -> Dict:
        """优化网格参数"""
        pass

class DataInterface(ABC):
    """数据服务接口"""
    
    @abstractmethod
    def get_etf_basic_info(self, etf_code: str) -> Dict:
        """获取ETF基础信息"""
        pass
    
    @abstractmethod
    def get_historical_data(self, etf_code: str, days: int) -> pd.DataFrame:
        """获取历史数据"""
        pass
    
    @abstractmethod
    def get_latest_price(self, etf_code: str) -> Dict:
        """获取最新价格"""
        pass

class CacheInterface(ABC):
    """缓存服务接口"""
    
    @abstractmethod
    def get(self, key: str) -> Optional[str]:
        """获取缓存数据"""
        pass
    
    @abstractmethod
    def set(self, key: str, value: str, expire: int = 3600) -> bool:
        """设置缓存数据"""
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        """删除缓存数据"""
        pass

class ServiceContainer:
    """服务容器 - 实现依赖注入"""
    
    def __init__(self):
        self._services = {}
        self._instances = {}
    
    def register(self, service_type: type, implementation: type):
        """注册服务实现"""
        self._services[service_type] = implementation
    
    def register_instance(self, service_type: type, instance: object):
        """注册服务实例"""
        self._instances[service_type] = instance
    
    def get(self, service_type: type):
        """获取服务实例"""
        # 首先检查是否有已注册的实例
        if service_type in self._instances:
            return self._instances[service_type]
        
        # 如果没有实例但有实现类，创建新实例
        if service_type in self._services:
            implementation = self._services[service_type]
            return implementation()
        
        raise ValueError(f"未注册的服务类型: {service_type}")
    
    def create_etf_analysis_service(self):
        """创建ETF分析服务实例"""
        from ..analysis.etf_analysis_service import ETFAnalysisService
        from algorithms.atr.analyzer import ATRAnalyzer
        from algorithms.atr.calculator import ATRCalculator
        from algorithms.grid.arithmetic_grid import ArithmeticGridCalculator
        from algorithms.grid.geometric_grid import GeometricGridCalculator
        from algorithms.grid.optimizer import GridOptimizer
        from ..analysis.suitability_analyzer import SuitabilityAnalyzer
        
        # 创建算法实例
        atr_calculator = ATRCalculator()
        atr_analyzer = ATRAnalyzer(atr_calculator)
        arithmetic_calculator = ArithmeticGridCalculator()
        geometric_calculator = GeometricGridCalculator()
        grid_optimizer = GridOptimizer()
        suitability_analyzer = SuitabilityAnalyzer(atr_analyzer)
        
        # 创建ETF分析服务实例
        return ETFAnalysisService(
            atr_analyzer=atr_analyzer,
            arithmetic_calculator=arithmetic_calculator,
            geometric_calculator=geometric_calculator,
            grid_optimizer=grid_optimizer,
            suitability_analyzer=suitability_analyzer
        )
    
    def create_grid_strategy_service(self):
        """创建网格策略服务实例"""
        from ..analysis.grid_strategy import GridStrategy
        from algorithms.atr.analyzer import ATRAnalyzer
        from algorithms.atr.calculator import ATRCalculator
        from algorithms.grid.arithmetic_grid import ArithmeticGridCalculator
        from algorithms.grid.geometric_grid import GeometricGridCalculator
        from algorithms.grid.optimizer import GridOptimizer
        
        # 创建算法实例
        atr_calculator = ATRCalculator()
        atr_analyzer = ATRAnalyzer(atr_calculator)
        arithmetic_calculator = ArithmeticGridCalculator()
        geometric_calculator = GeometricGridCalculator()
        grid_optimizer = GridOptimizer()
        
        # 创建网格策略服务实例
        return GridStrategy(
            atr_analyzer=atr_analyzer,
            arithmetic_calculator=arithmetic_calculator,
            geometric_calculator=geometric_calculator,
            grid_optimizer=grid_optimizer
        )

# 创建全局服务容器实例
service_container = ServiceContainer()

__all__ = [
    'AlgorithmInterface',
    'DataInterface',
    'CacheInterface',
    'ServiceContainer',
    'service_container'
]
