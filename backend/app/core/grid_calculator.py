"""
网格计算器模块

基于ATR分析结果计算网格交易策略参数
"""

import logging
from typing import List, Dict, Any, Tuple
from decimal import Decimal, ROUND_HALF_UP
import math

from ..models.etf_models import ETFPriceData
from ..models.analysis_models import ATRAnalysis, AnalysisResult
from ..models.strategy_models import StrategyConfig, GridLevel
from ..utils.calculators import calculate_compound_return
from ..utils.formatters import format_currency, format_percentage

logger = logging.getLogger(__name__)


class GridCalculator:
    """网格计算器"""
    
    def __init__(self):
        """初始化网格计算器"""
        # 网格策略配置
        self.min_grid_spacing = 0.005  # 最小网格间距 0.5%
        self.max_grid_spacing = 0.1    # 最大网格间距 10%
        self.default_grid_count = 10   # 默认网格数量
        
        # 资金分配策略
        self.reserve_ratio = 0.1       # 预留资金比例 10%
        self.max_single_position = 0.2 # 单个网格最大仓位 20%
    
    def calculate_grid_strategy(self, config: StrategyConfig, 
                              current_data: ETFPriceData,
                              atr_result: ATRAnalysis) -> AnalysisResult:
        """
        计算网格策略
        
        Args:
            config: 网格策略配置
            current_data: 当前价格数据
            atr_result: ATR分析结果
            
        Returns:
            AnalysisResult: 网格策略分析结果
        """
        try:
            # 计算网格参数
            grid_params = self._calculate_grid_parameters(config, atr_result)
            
            # 生成网格价位
            grid_levels = self._generate_grid_levels(
                config.current_price, grid_params['spacing'], config.grid_count
            )
            
            # 计算资金分配
            fund_allocation = self._calculate_fund_allocation(
                config.investment_amount, config.grid_count
            )
            
            # 生成交易信号
            trading_signals = self._generate_trading_signals(
                grid_levels, config.current_price, fund_allocation
            )
            
            # 计算预期收益
            expected_returns = self._calculate_expected_returns(
                grid_levels, fund_allocation, atr_result
            )
            
            # 风险评估
            risk_assessment = self._assess_strategy_risk(
                config, grid_params, atr_result
            )
            
            # 返回字典格式的分析结果，而不是 AnalysisResult 对象
            return {
                'etf_code': config.etf_code,
                'strategy_type': "ATR网格策略",
                'grid_count': config.grid_count,
                'current_price': config.current_price,
                'grid_spacing': grid_params['spacing'],
                'price_range': grid_params['price_range'],
                'investment_amount': config.investment_amount,
                'grid_levels': grid_levels,
                'fund_allocation': fund_allocation,
                'trading_signals': trading_signals,
                'expected_returns': expected_returns,
                'risk_assessment': risk_assessment,
                'atr_based_params': grid_params,
                'trading_parameters': self._create_trading_parameters(config, grid_params)
            }
            
        except Exception as e:
            logger.error(f"网格策略计算失败: {e}")
            raise
    
    def _calculate_grid_parameters(self, config: StrategyConfig, 
                                 atr_result: ATRAnalysis) -> Dict[str, Any]:
        """
        计算网格参数
        
        Args:
            config: 网格策略配置
            atr_result: ATR分析结果
            
        Returns:
            dict: 网格参数
        """
        # 基于ATR计算建议网格间距
        atr_percentage = atr_result['current_atr_pct'] / 100  # 转换为小数
        atr_spacing = atr_percentage * 0.8  # ATR的80%作为网格间距
        
        # 应用用户设定的价格范围
        user_spacing = config.price_range_percent / config.grid_count
        
        # 取两者的平均值，并限制在合理范围内
        suggested_spacing = (atr_spacing + user_spacing) / 2
        grid_spacing = max(self.min_grid_spacing, 
                          min(self.max_grid_spacing, suggested_spacing))
        
        # 计算价格范围
        price_range = {
            'upper': config.current_price * (1 + config.price_range_percent / 2),
            'lower': config.current_price * (1 - config.price_range_percent / 2),
            'total_range_percent': config.price_range_percent
        }
        
        return {
            'spacing': grid_spacing,
            'spacing_percent': grid_spacing * 100,
            'atr_based_spacing': atr_spacing,
            'user_defined_spacing': user_spacing,
            'price_range': price_range,
            'atr_influence': 0.5,  # ATR影响权重
            'volatility_adjustment': self._calculate_volatility_adjustment(atr_result)
        }
    
    def _generate_grid_levels(self, current_price: float, spacing: float, 
                            grid_count: int) -> List[Dict[str, Any]]:
        """
        生成网格价位
        
        Args:
            current_price: 当前价格
            spacing: 网格间距
            grid_count: 网格数量
            
        Returns:
            List[dict]: 网格价位列表
        """
        grid_levels = []
        
        # 计算网格中心（当前价格附近）
        center_index = grid_count // 2
        
        for i in range(grid_count):
            # 计算相对于中心的偏移
            offset = (i - center_index) * spacing
            
            # 计算网格价格
            grid_price = current_price * (1 + offset)
            
            # 确定网格类型
            if grid_price < current_price:
                grid_type = "买入网格"
                action = "buy"
            elif grid_price > current_price:
                grid_type = "卖出网格"
                action = "sell"
            else:
                grid_type = "当前价格"
                action = "hold"
            
            grid_level = {
                'level': i + 1,
                'price': round(grid_price, 3),
                'type': grid_type,
                'action': action,
                'distance_from_current': abs(grid_price - current_price),
                'distance_percent': abs(offset) * 100,
                'is_active': abs(grid_price - current_price) / current_price <= 0.1  # 10%范围内为活跃网格
            }
            
            grid_levels.append(grid_level)
        
        # 按价格排序
        grid_levels.sort(key=lambda x: x['price'])
        
        return grid_levels
    
    def _calculate_fund_allocation(self, total_amount: float, 
                                 grid_count: int) -> Dict[str, Any]:
        """
        计算资金分配
        
        Args:
            total_amount: 总投资金额
            grid_count: 网格数量
            
        Returns:
            dict: 资金分配方案
        """
        # 预留资金
        reserve_amount = total_amount * self.reserve_ratio
        available_amount = total_amount - reserve_amount
        
        # 计算每个网格的基础资金
        base_amount_per_grid = available_amount / grid_count
        
        # 限制单个网格最大资金
        max_amount_per_grid = total_amount * self.max_single_position
        amount_per_grid = min(base_amount_per_grid, max_amount_per_grid)
        
        # 计算实际使用的资金
        actual_used_amount = amount_per_grid * grid_count
        actual_reserve = total_amount - actual_used_amount
        
        return {
            'total_amount': total_amount,
            'amount_per_grid': amount_per_grid,
            'reserve_amount': actual_reserve,
            'reserve_ratio': actual_reserve / total_amount,
            'grid_count': grid_count,
            'max_single_position_ratio': self.max_single_position,
            'allocation_strategy': "均匀分配" if base_amount_per_grid <= max_amount_per_grid else "限额分配"
        }
    
    def _generate_trading_signals(self, grid_levels: List[Dict[str, Any]], 
                                current_price: float,
                                fund_allocation: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        生成交易信号
        
        Args:
            grid_levels: 网格价位
            current_price: 当前价格
            fund_allocation: 资金分配
            
        Returns:
            List[dict]: 交易信号列表
        """
        trading_signals = []
        amount_per_grid = fund_allocation['amount_per_grid']
        
        for grid in grid_levels:
            if not grid['is_active']:
                continue
            
            signal = {
                'grid_level': grid['level'],
                'price': grid['price'],
                'action': grid['action'],
                'amount': amount_per_grid,
                'priority': self._calculate_signal_priority(grid, current_price),
                'expected_shares': int(amount_per_grid / grid['price']) if grid['price'] > 0 else 0,
                'trigger_condition': f"价格{'跌至' if grid['action'] == 'buy' else '涨至'}{grid['price']}时执行",
                'stop_condition': self._generate_stop_condition(grid, grid_levels)
            }
            
            trading_signals.append(signal)
        
        # 按优先级排序
        trading_signals.sort(key=lambda x: x['priority'], reverse=True)
        
        return trading_signals
    
    def _calculate_expected_returns(self, grid_levels: List[Dict[str, Any]], 
                                  fund_allocation: Dict[str, Any],
                                  atr_result: ATRAnalysis) -> Dict[str, Any]:
        """
        计算预期收益
        
        Args:
            grid_levels: 网格价位
            fund_allocation: 资金分配
            atr_result: ATR分析结果
            
        Returns:
            dict: 预期收益分析
        """
        # 基于ATR计算预期波动次数
        daily_volatility = atr_result['current_atr_pct'] / 100  # 转换为小数
        expected_daily_trades = daily_volatility / (grid_levels[1]['price'] - grid_levels[0]['price']) * grid_levels[0]['price']
        
        # 计算单次交易预期收益
        avg_grid_spacing = sum(abs(g['distance_percent']) for g in grid_levels) / len(grid_levels)
        single_trade_return = avg_grid_spacing / 100 * 0.8  # 考虑手续费
        
        # 计算预期收益
        daily_expected_return = expected_daily_trades * single_trade_return * fund_allocation['amount_per_grid']
        monthly_expected_return = daily_expected_return * 22  # 22个交易日
        annual_expected_return = daily_expected_return * 252  # 252个交易日
        
        return {
            'daily_expected_return': daily_expected_return,
            'monthly_expected_return': monthly_expected_return,
            'annual_expected_return': annual_expected_return,
            'annual_return_rate': annual_expected_return / fund_allocation['total_amount'],
            'expected_trade_frequency': expected_daily_trades,
            'single_trade_profit_rate': single_trade_return,
            'risk_adjusted_return': annual_expected_return / max(daily_volatility, 0.01),
            'assumptions': {
                'market_efficiency': 0.8,
                'transaction_cost': 0.002,
                'slippage': 0.001
            }
        }
    
    def _assess_strategy_risk(self, config: StrategyConfig, 
                            grid_params: Dict[str, Any],
                            atr_result: ATRAnalysis) -> Dict[str, Any]:
        """
        评估策略风险
        
        Args:
            config: 网格策略配置
            grid_params: 网格参数
            atr_result: ATR分析结果
            
        Returns:
            dict: 风险评估结果
        """
        # 计算最大可能损失
        max_price_drop = config.price_range_percent / 2
        max_loss = config.investment_amount * max_price_drop
        
        # 计算资金利用率风险
        fund_utilization = (config.investment_amount - config.investment_amount * self.reserve_ratio) / config.investment_amount
        
        # 流动性风险评估
        liquidity_risk = "低" if atr_result['current_atr'] > config.current_price * 0.01 else "中"
        
        # 市场风险评估
        market_risk = self._assess_market_risk(atr_result)
        
        # 计算波动率风险
        atr_pct = atr_result['current_atr_pct'] / 100  # 转换为小数
        volatility_risk = "高" if atr_pct > 0.03 else "中" if atr_pct > 0.015 else "低"
        
        return {
            'max_potential_loss': max_loss,
            'max_loss_percentage': max_price_drop * 100,
            'fund_utilization_rate': fund_utilization * 100,
            'liquidity_risk': liquidity_risk,
            'market_risk': market_risk,
            'volatility_risk': volatility_risk,
            'strategy_risk_level': self._calculate_overall_risk_level(atr_result, fund_utilization),
            'risk_mitigation': [
                "设置止损位",
                "分批建仓",
                "定期调整网格",
                "关注市场趋势"
            ]
        }
    
    def _create_trading_parameters(self, config: StrategyConfig, 
                                 grid_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建交易参数
        
        Args:
            config: 网格策略配置
            grid_params: 网格参数
            
        Returns:
            Dict: 交易参数字典
        """
        return {
            'etf_code': config.etf_code,
            'strategy_type': "ATR网格策略",
            'entry_price': config.current_price,
            'stop_loss_price': config.current_price * (1 - config.price_range_percent / 2),
            'take_profit_price': config.current_price * (1 + config.price_range_percent / 2),
            'position_size': config.investment_amount,
            'max_position_ratio': self.max_single_position,
            'grid_spacing': grid_params['spacing'],
            'rebalance_threshold': grid_params['spacing'] * 0.5,
            'risk_level': self._calculate_overall_risk_level(None, 0.9)
        }
    
    def _calculate_volatility_adjustment(self, atr_result: ATRAnalysis) -> float:
        """
        计算波动率调整系数
        
        Args:
            atr_result: ATR分析结果
            
        Returns:
            float: 调整系数
        """
        # 基于ATR百分比调整网格间距
        atr_pct = atr_result['current_atr_pct'] / 100  # 转换为小数
        if atr_pct > 0.05:  # 高波动
            return 1.2
        elif atr_pct > 0.02:  # 中等波动
            return 1.0
        else:  # 低波动
            return 0.8
    
    def _calculate_signal_priority(self, grid: Dict[str, Any], current_price: float) -> int:
        """
        计算交易信号优先级
        
        Args:
            grid: 网格信息
            current_price: 当前价格
            
        Returns:
            int: 优先级分数
        """
        distance = abs(grid['price'] - current_price) / current_price
        
        # 距离当前价格越近，优先级越高
        if distance < 0.02:  # 2%以内
            return 100
        elif distance < 0.05:  # 5%以内
            return 80
        elif distance < 0.1:  # 10%以内
            return 60
        else:
            return 40
    
    def _generate_stop_condition(self, current_grid: Dict[str, Any], 
                               all_grids: List[Dict[str, Any]]) -> str:
        """
        生成止损条件
        
        Args:
            current_grid: 当前网格
            all_grids: 所有网格
            
        Returns:
            str: 止损条件描述
        """
        if current_grid['action'] == 'buy':
            # 买入网格的止损条件
            lower_grids = [g for g in all_grids if g['price'] < current_grid['price']]
            if lower_grids:
                stop_price = min(g['price'] for g in lower_grids)
                return f"价格跌破{stop_price}时止损"
            else:
                return f"价格跌破{current_grid['price'] * 0.95}时止损"
        else:
            # 卖出网格的止损条件
            return "持有至目标价位或止损"
    
    def _assess_market_risk(self, atr_result: ATRAnalysis) -> str:
        """
        评估市场风险
        
        Args:
            atr_result: ATR分析结果
            
        Returns:
            str: 市场风险等级
        """
        atr_pct = atr_result['current_atr_pct'] / 100  # 转换为小数
        if atr_pct > 0.04:
            return "高"
        elif atr_pct > 0.02:
            return "中"
        else:
            return "低"
    
    def _calculate_overall_risk_level(self, atr_result: ATRAnalysis = None, 
                                    fund_utilization: float = 0.9) -> str:
        """
        计算整体风险等级
        
        Args:
            atr_result: ATR分析结果
            fund_utilization: 资金利用率
            
        Returns:
            str: 整体风险等级
        """
        risk_score = 0
        
        # 波动率风险
        if atr_result:
            atr_pct = atr_result['current_atr_pct'] / 100  # 转换为小数
            if atr_pct > 0.03:
                risk_score += 3
            elif atr_pct > 0.015:
                risk_score += 2
            else:
                risk_score += 1
        
        # 资金利用率风险
        if fund_utilization > 0.9:
            risk_score += 2
        elif fund_utilization > 0.8:
            risk_score += 1
        
        # 综合评级
        if risk_score >= 4:
            return "高风险"
        elif risk_score >= 3:
            return "中高风险"
        elif risk_score >= 2:
            return "中等风险"
        else:
            return "低风险"