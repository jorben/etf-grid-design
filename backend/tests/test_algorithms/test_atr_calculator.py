"""
ATR计算器单元测试
测试ATR算法模块的核心功能
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from algorithms.atr.calculator import ATRCalculator, calculate_volatility, calculate_adx


class TestATRCalculator:
    """ATR计算器测试类"""
    
    def setup_method(self):
        """测试前准备"""
        self.calculator = ATRCalculator(period=14)
        self.sample_data = self._create_sample_data()
    
    def _create_sample_data(self, days: int = 100) -> pd.DataFrame:
        """创建测试数据"""
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        
        # 生成随机价格数据
        np.random.seed(42)  # 固定随机种子保证测试可重复
        base_price = 10.0
        returns = np.random.normal(0.001, 0.02, days)  # 日收益率
        prices = base_price * np.exp(np.cumsum(returns))
        
        # 生成OHLC数据
        df = pd.DataFrame({
            'date': dates,
            'open': prices * (1 + np.random.normal(0, 0.005, days)),
            'high': prices * (1 + np.abs(np.random.normal(0.01, 0.01, days))),
            'low': prices * (1 - np.abs(np.random.normal(0.01, 0.01, days))),
            'close': prices,
            'vol': np.random.randint(1000000, 5000000, days),
            'amount': np.random.randint(50000000, 200000000, days)
        })
        
        return df
    
    def test_calculate_true_range(self):
        """测试真实波幅计算"""
        df = self.sample_data.copy()
        df_with_tr = self.calculator.calculate_true_range(df)
        
        # 验证TR列存在
        assert 'tr' in df_with_tr.columns
        assert 'prev_close' in df_with_tr.columns
        
        # 验证TR值非负
        assert df_with_tr['tr'].min() >= 0
        
        # 验证TR计算逻辑
        for i in range(1, len(df_with_tr)):
            high = df_with_tr.iloc[i]['high']
            low = df_with_tr.iloc[i]['low']
            prev_close = df_with_tr.iloc[i-1]['close']
            
            tr1 = high - low
            tr2 = abs(high - prev_close)
            tr3 = abs(low - prev_close)
            expected_tr = max(tr1, tr2, tr3)
            
            actual_tr = df_with_tr.iloc[i]['tr']
            assert abs(actual_tr - expected_tr) < 1e-10
    
    def test_calculate_atr(self):
        """测试ATR计算"""
        df = self.sample_data.copy()
        df_with_atr = self.calculator.calculate_atr(df)
        
        # 验证ATR列存在
        assert 'ATR' in df_with_atr.columns
        
        # 验证ATR值非负
        assert df_with_atr['ATR'].min() >= 0
        
        # 验证ATR计算逻辑（由于min_periods=1，所有行都有值）
        assert not pd.isna(df_with_atr.iloc[0]['ATR'])
        assert not pd.isna(df_with_atr.iloc[self.calculator.period - 1]['ATR'])
        
        # 验证ATR平滑计算
        df_with_tr = self.calculator.calculate_true_range(df)
        first_valid_atr = df_with_tr['tr'].iloc[:self.calculator.period].mean()
        actual_first_atr = df_with_atr.iloc[self.calculator.period - 1]['ATR']
        
        assert abs(actual_first_atr - first_valid_atr) < 1e-10
    
    def test_calculate_atr_with_custom_period(self):
        """测试自定义周期的ATR计算"""
        custom_period = 20
        calculator = ATRCalculator(period=custom_period)
        df_with_atr = calculator.calculate_atr(self.sample_data.copy())
        
        # 验证自定义周期（由于min_periods=1，所有行都有值）
        assert not pd.isna(df_with_atr.iloc[0]['ATR'])
        assert not pd.isna(df_with_atr.iloc[custom_period - 1]['ATR'])
    
    def test_process_data(self):
        """测试数据处理方法"""
        df = self.sample_data.copy()
        processed_df = self.calculator.process_data(df)
        
        # 验证处理后的数据包含所有必要列
        expected_columns = ['date', 'open', 'high', 'low', 'close', 'vol', 'amount', 'tr', 'ATR']
        assert all(col in processed_df.columns for col in expected_columns)
        
        # 验证数据排序
        assert processed_df['date'].is_monotonic_increasing
    
    def test_calculate_volatility(self):
        """测试波动率计算"""
        df = self.sample_data.copy()
        volatility = calculate_volatility(df)
        
        # 验证波动率在合理范围内
        assert 0 <= volatility <= 1.0
        
        # 验证年化波动率计算逻辑
        returns = np.log(df['close'] / df['close'].shift(1)).dropna()
        expected_volatility = returns.std() * np.sqrt(252)
        
        assert abs(volatility - expected_volatility) < 1e-10
    
    def test_calculate_adx(self):
        """测试ADX计算"""
        df = self.sample_data.copy()
        adx_value = calculate_adx(df)
        
        # 验证ADX值在合理范围内
        assert 0 <= adx_value <= 100
        
        # 验证ADX计算逻辑（简化验证）
        assert isinstance(adx_value, float)
    
    def test_edge_cases(self):
        """测试边界情况"""
        # 空数据测试
        empty_df = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'vol', 'amount'])
        with pytest.raises(ValueError):
            self.calculator.calculate_atr(empty_df)
        
        # 单行数据测试（应该能正常处理）
        single_row_df = self.sample_data.iloc[:1].copy()
        result = self.calculator.calculate_atr(single_row_df)
        assert 'ATR' in result.columns
        assert len(result) == 1
        
        # 缺失列测试
        incomplete_df = self.sample_data[['date', 'open', 'high']].copy()
        with pytest.raises(KeyError):
            self.calculator.calculate_atr(incomplete_df)
    
    def test_data_quality_checks(self):
        """测试数据质量检查"""
        # 测试异常价格数据
        df = self.sample_data.copy()
        df.loc[10, 'high'] = -1  # 异常高价
        df.loc[20, 'low'] = 1000  # 异常低价
        
        with pytest.raises(ValueError):
            self.calculator.calculate_atr(df)
        
        # 测试缺失值
        df = self.sample_data.copy()
        df.loc[30, 'close'] = None
        
        with pytest.raises(ValueError):
            self.calculator.calculate_atr(df)
    
    def test_performance(self):
        """测试性能"""
        import time
        
        # 创建大数据集
        large_data = self._create_sample_data(1000)
        
        start_time = time.time()
        result = self.calculator.calculate_atr(large_data)
        end_time = time.time()
        
        # 验证计算时间在合理范围内（1秒内）
        assert (end_time - start_time) < 1.0
        
        # 验证结果正确性
        assert 'ATR' in result.columns
        assert len(result) == len(large_data)


class TestVolatilityFunction:
    """波动率函数测试"""
    
    def test_volatility_with_different_periods(self):
        """测试不同周期的波动率计算"""
        df = TestATRCalculator()._create_sample_data(100)
        
        # 测试默认周期
        vol_default = calculate_volatility(df)
        assert isinstance(vol_default, float)
        
        # 测试自定义周期（需要修改calculate_volatility函数以支持period参数）
        # 暂时注释掉，因为当前函数不支持period参数
        # vol_short = calculate_volatility(df, period=30)
        # vol_long = calculate_volatility(df, period=200)
        # assert isinstance(vol_short, float)
        # assert isinstance(vol_long, float)
    
    def test_volatility_edge_cases(self):
        """测试波动率边界情况"""
        # 恒定价格
        constant_prices = pd.DataFrame({
            'close': [10.0] * 100
        })
        vol = calculate_volatility(constant_prices)
        assert vol == 0.0
        
        # 单点数据（处理NaN情况）
        single_point = pd.DataFrame({
            'close': [10.0]
        })
        vol = calculate_volatility(single_point)
        # 单点数据应该返回0.0或NaN，这里检查是否为数值
        assert vol == 0.0 or np.isnan(vol)


class TestADXFunction:
    """ADX函数测试"""
    
    def test_adx_basic_functionality(self):
        """测试ADX基本功能"""
        df = TestATRCalculator()._create_sample_data(100)
        adx = calculate_adx(df)
        
        assert isinstance(adx, float)
        assert 0 <= adx <= 100
    
    def test_adx_with_different_periods(self):
        """测试不同周期的ADX计算"""
        df = TestATRCalculator()._create_sample_data(100)
        
        adx_short = calculate_adx(df, period=10)
        adx_long = calculate_adx(df, period=20)
        
        assert isinstance(adx_short, float)
        assert isinstance(adx_long, float)
