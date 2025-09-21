import numpy as np
import pandas as pd
import logging
from typing import Dict, List
from datetime import datetime
from .frequency_calculator import FrequencyCalculator

logger = logging.getLogger(__name__)


class TargetReturnConfig:
    """目标收益率配置类"""
    
    def __init__(self, monthly_target_return: float = 0.05):
        """
        初始化目标收益率配置
        
        Args:
            monthly_target_return: 月度目标收益率，默认5%
        """
        self.monthly_target_return = monthly_target_return
        self.min_profit_per_trade = 10.0  # 最小单笔收益（元）
        self.max_single_trade_ratio = 0.1  # 单笔交易最大资金比例
        self.risk_adjustment_factor = 0.8  # 风险调整系数
        self.success_rate = 0.8  # 预期交易成功率
        self.trading_days_per_month = 20  # 每月交易日数
        self.min_shares_unit = 100  # 最小交易股数单位
        self.max_capital_utilization = 0.8  # 最大资金利用率
        self.cash_reserve_ratio = 0.2  # 现金储备比例


class DynamicSharesCalculator:
    """动态股数计算器"""
    
    def __init__(self, target_config: TargetReturnConfig):
        """
        初始化动态股数计算器
        
        Args:
            target_config: 目标收益率配置
        """
        self.config = target_config
        
    def calculate_optimal_shares(self, initial_capital: float, current_price: float,
                               step_size_ratio: float, predicted_daily_triggers: float,
                               transaction_cost: float) -> Dict:
        """
        计算最优交易股数
        
        Args:
            initial_capital: 初始资金
            current_price: 当前价格
            step_size_ratio: 网格步长比例
            predicted_daily_triggers: 预测日交易频次
            transaction_cost: 交易成本比例
            
        Returns:
            Dict: 动态股数分配结果
        """
        try:
            # 1. 计算月度目标收益金额
            target_monthly_profit = initial_capital * self.config.monthly_target_return
            
            # 2. 计算预期月度交易次数
            expected_monthly_trades = (predicted_daily_triggers * 
                                     self.config.trading_days_per_month * 
                                     self.config.success_rate)
            
            # 确保至少有1次交易
            expected_monthly_trades = max(1, expected_monthly_trades)
            
            # 3. 计算每次交易目标收益（考虑交易成本和现实性）
            target_profit_per_trade = target_monthly_profit / expected_monthly_trades
            
            # 考虑双边交易成本和风险调整
            cost_adjustment = 1 + (transaction_cost * 2)
            risk_adjustment = 1.2  # 20%的风险缓冲
            net_target_profit = target_profit_per_trade * cost_adjustment * risk_adjustment
            
            # 设置合理的收益下限和上限
            min_profit_per_trade = self.config.min_profit_per_trade
            max_profit_per_trade = initial_capital * 0.02  # 单次交易收益不超过总资金的2%
            net_target_profit = max(min_profit_per_trade, min(max_profit_per_trade, net_target_profit))
            
            # 4. 计算网格步长金额和所需股数
            grid_step_amount = current_price * step_size_ratio
            
            if grid_step_amount <= 0:
                raise ValueError("网格步长金额必须大于0")
            
            required_shares_per_grid = net_target_profit / grid_step_amount
            
            # 5. 调整到最小交易单位
            optimal_shares = max(self.config.min_shares_unit, 
                               round(required_shares_per_grid / self.config.min_shares_unit) * 
                               self.config.min_shares_unit)
            
            # 6. 应用风险约束
            constrained_shares = self._apply_risk_constraints(
                optimal_shares, current_price, initial_capital
            )
            
            # 7. 计算相关指标
            amount_per_grid = constrained_shares * current_price
            expected_profit_per_trade = constrained_shares * grid_step_amount
            expected_monthly_profit = expected_profit_per_trade * expected_monthly_trades
            actual_monthly_return = expected_monthly_profit / initial_capital
            
            return {
                'shares_per_grid': int(constrained_shares),
                'amount_per_grid': amount_per_grid,
                'expected_profit_per_trade': expected_profit_per_trade,
                'expected_monthly_profit': expected_monthly_profit,
                'actual_monthly_return_rate': actual_monthly_return,
                'target_achievement_ratio': actual_monthly_return / self.config.monthly_target_return,
                'expected_monthly_trades': expected_monthly_trades,
                'capital_per_grid_ratio': amount_per_grid / initial_capital,
                'calculation_details': {
                    'target_monthly_profit': target_monthly_profit,
                    'target_profit_per_trade': target_profit_per_trade,
                    'net_target_profit': net_target_profit,
                    'required_shares_raw': required_shares_per_grid,
                    'optimal_shares_before_constraints': optimal_shares,
                    'cost_adjustment_factor': cost_adjustment
                }
            }
            
        except Exception as e:
            logger.error(f"计算最优股数失败: {str(e)}")
            # 返回保守的默认值
            default_shares = self.config.min_shares_unit
            return {
                'shares_per_grid': default_shares,
                'amount_per_grid': default_shares * current_price,
                'expected_profit_per_trade': default_shares * current_price * step_size_ratio,
                'expected_monthly_profit': 0,
                'actual_monthly_return_rate': 0,
                'target_achievement_ratio': 0,
                'expected_monthly_trades': 0,
                'capital_per_grid_ratio': (default_shares * current_price) / initial_capital,
                'error': str(e)
            }
    
    def _apply_risk_constraints(self, optimal_shares: float, current_price: float, 
                              initial_capital: float) -> float:
        """
        应用风险约束
        
        Args:
            optimal_shares: 最优股数
            current_price: 当前价格
            initial_capital: 初始资金
            
        Returns:
            float: 约束后的股数
        """
        try:
            # 约束1：单笔交易不超过总资金的指定比例
            max_single_trade_amount = initial_capital * self.config.max_single_trade_ratio
            max_shares_by_capital = max(self.config.min_shares_unit,
                                      int(max_single_trade_amount / current_price / 
                                          self.config.min_shares_unit) * self.config.min_shares_unit)
            
            # 约束2：确保最小收益要求（但不能过高）
            min_profit_shares = max(self.config.min_shares_unit,
                                  int(self.config.min_profit_per_trade / 
                                      (current_price * 0.005)))  # 假设0.5%的最小步长
            
            # 约束3：防止过度投资，限制在合理范围内
            reasonable_max_shares = int(initial_capital * 0.15 / current_price / 
                                      self.config.min_shares_unit) * self.config.min_shares_unit
            
            # 应用所有约束 - 取最严格的限制
            constrained_shares = min(optimal_shares, max_shares_by_capital, reasonable_max_shares)
            constrained_shares = max(constrained_shares, min_profit_shares, self.config.min_shares_unit)
            
            # 确保是最小交易单位的倍数
            final_shares = int(constrained_shares / self.config.min_shares_unit) * self.config.min_shares_unit
            
            # 最终安全检查
            final_amount = final_shares * current_price
            if final_amount > initial_capital * self.config.max_single_trade_ratio:
                # 如果仍然超出限制，强制降低到安全水平
                safe_shares = int(initial_capital * self.config.max_single_trade_ratio / 
                                current_price / self.config.min_shares_unit) * self.config.min_shares_unit
                final_shares = max(self.config.min_shares_unit, safe_shares)
            
            return final_shares
            
        except Exception as e:
            logger.error(f"应用风险约束失败: {str(e)}")
            return self.config.min_shares_unit


class GridCalculator:
    """网格策略计算器 - 增强版，支持目标收益率导向"""
    
    def __init__(self):
        """初始化网格计算器"""
        # 初始化频次计算器
        self.frequency_calculator = FrequencyCalculator()
        
        # 频率配置 - 针对低价ETF优化的频次设计
        self.frequency_config = {
            'high': {
                'target_daily_triggers': 5.5,    # 5-6次/天（优化后）
                'min_grids': 10,
                'max_grids': 25,
                'min_range_ratio': 0.10,
                'max_range_ratio': 0.35
            },
            'medium': {
                'target_daily_triggers': 2.5,   # 2-3次/天（优化后）
                'min_grids': 6,
                'max_grids': 15,
                'min_range_ratio': 0.08,
                'max_range_ratio': 0.25
            },
            'low': {
                'target_daily_triggers': 1,   # 1次/天（保持不变）
                'min_grids': 3,
                'max_grids': 10,
                'min_range_ratio': 0.05,
                'max_range_ratio': 0.20
            }
        }
        
        # 交易成本假设 (双边)
        self.transaction_cost = 0.001  # 0.1%
        
        logger.info("网格策略计算器初始化成功")
    
    def calculate_grid_parameters(self, current_price: float, analysis_result: Dict, 
                                frequency: str, initial_capital: float, 
                                target_monthly_return: float = 0.05,
                                historical_data: pd.DataFrame = None) -> Dict:
        """
        计算网格策略参数 - 基于目标收益率和日交易频次的新逻辑
        
        Args:
            current_price: 当前价格
            analysis_result: ETF分析结果
            frequency: 交易频率 ('high', 'medium', 'low')
            initial_capital: 初始资金
            target_monthly_return: 月度目标收益率，默认5%
            historical_data: 历史K线数据（用于频次分析）
            
        Returns:
            Dict: 网格策略参数
        """
        try:
            if 'error' in analysis_result:
                return {'error': analysis_result['error']}
            
            # 获取频率配置
            freq_config = self.frequency_config.get(frequency)
            if not freq_config:
                return {'error': f'不支持的频率类型: {frequency}'}
            
            # 基础参数
            avg_amplitude = analysis_result.get('avg_amplitude', 2.0)
            volatility = analysis_result.get('volatility', 25.0)
            price_std = analysis_result.get('price_std', current_price * 0.02)
            
            # 1. 分析历史交易模式（如果有历史数据）
            historical_patterns = None
            if historical_data is not None and not historical_data.empty:
                historical_patterns = self.frequency_calculator.analyze_historical_patterns(historical_data)
                if 'error' in historical_patterns:
                    logger.warning(f"历史模式分析失败: {historical_patterns['error']}")
                    historical_patterns = None
            
            # 2. 计算价格区间
            price_range = self._calculate_price_range(
                current_price, avg_amplitude, volatility, price_std, freq_config
            )
            
            # 3. 基于目标日交易频次计算最优网格参数
            if historical_patterns:
                frequency_params = self.frequency_calculator.calculate_optimal_grid_parameters(
                    frequency, current_price, historical_patterns, price_range['range_ratio']
                )
                
                if 'error' not in frequency_params:
                    # 使用频次计算器的结果
                    grid_count = frequency_params['optimal_grid_count']
                    actual_step_ratio = frequency_params['grid_step_ratio']
                    predicted_daily_triggers = frequency_params['predicted_daily_triggers']
                    frequency_match_score = frequency_params['frequency_match_score']
                    
                    # 重新计算价格区间以匹配网格数量
                    price_range['range_ratio'] = actual_step_ratio * grid_count
                    price_range['range_amount'] = current_price * price_range['range_ratio']
                    price_range['upper'] = current_price + price_range['range_amount'] / 2
                    price_range['lower'] = current_price - price_range['range_amount'] / 2
                else:
                    # 回退到传统方法
                    grid_count = self._calculate_grid_count(
                        price_range, avg_amplitude, frequency, freq_config
                    )
                    predicted_daily_triggers = freq_config['target_daily_triggers']
                    frequency_match_score = 0.5
            else:
                # 没有历史数据时使用传统方法
                grid_count = self._calculate_grid_count(
                    price_range, avg_amplitude, frequency, freq_config
                )
                predicted_daily_triggers = freq_config['target_daily_triggers']
                frequency_match_score = 0.5
            
            # 4. 计算网格价格
            grid_prices = self._calculate_grid_prices(
                price_range['lower'], price_range['upper'], grid_count
            )
            
            # 5. 初始化目标收益率配置和动态股数计算器
            target_config = TargetReturnConfig(target_monthly_return)
            shares_calculator = DynamicSharesCalculator(target_config)
            
            # 6. 计算动态股数分配（新的核心逻辑）
            dynamic_allocation = shares_calculator.calculate_optimal_shares(
                initial_capital=initial_capital,
                current_price=current_price,
                step_size_ratio=price_range['range_ratio'] / grid_count,
                predicted_daily_triggers=predicted_daily_triggers,
                transaction_cost=self.transaction_cost
            )
            
            # 7. 获取动态计算的交易参数
            per_trade_shares = dynamic_allocation['shares_per_grid']
            per_trade_amount = dynamic_allocation['amount_per_grid']
            
            # 8. 计算传统资金分配（用于对比和兼容性）
            traditional_allocation = self._calculate_capital_allocation(
                initial_capital, grid_count, current_price
            )
            
            # 9. 计算增强的收益分析
            profit_analysis = self._calculate_enhanced_profit_analysis(
                dynamic_allocation, predicted_daily_triggers, 
                price_range['range_ratio'] / grid_count, current_price
            )
            
            # 8. 计算基于日频次的月度统计
            monthly_stats = self.frequency_calculator.estimate_monthly_statistics(
                predicted_daily_triggers, 0.8  # 假设80%成功率
            )
            
            grid_params = {
                # 基础参数
                'current_price': current_price,
                'frequency': frequency,
                'frequency_name': self._get_frequency_name(frequency),
                
                # 目标收益率配置（新增）
                'target_monthly_return': target_monthly_return,
                'target_monthly_profit': initial_capital * target_monthly_return,
                
                # 价格区间
                'price_lower_bound': price_range['lower'],
                'price_upper_bound': price_range['upper'],
                'price_range_ratio': price_range['range_ratio'],
                'price_range_amount': price_range['range_amount'],
                
                # 网格设置
                'grid_count': grid_count,
                'grid_prices': grid_prices,
                'step_size_ratio': price_range['range_ratio'] / grid_count,
                'step_size_amount': price_range['range_amount'] / grid_count,
                
                # 动态股数配置（新的核心参数）
                'per_grid_shares': per_trade_shares,
                'per_grid_amount': per_trade_amount,
                'expected_profit_per_trade': dynamic_allocation['expected_profit_per_trade'],
                'expected_monthly_trades': dynamic_allocation['expected_monthly_trades'],
                'expected_monthly_profit': dynamic_allocation['expected_monthly_profit'],
                'actual_monthly_return_rate': dynamic_allocation['actual_monthly_return_rate'],
                'target_achievement_ratio': dynamic_allocation['target_achievement_ratio'],
                'capital_per_grid_ratio': dynamic_allocation['capital_per_grid_ratio'],
                
                # 资金配置（兼容传统字段名）
                'initial_capital': initial_capital,
                'base_position_amount': traditional_allocation['base_position'],
                'grid_position_amount': traditional_allocation['grid_position'],
                'max_position_amount': traditional_allocation['max_position'],
                'min_position_amount': traditional_allocation['min_position'],
                
                # 传统资金配置（保留用于对比）
                'traditional_base_position': traditional_allocation['base_position'],
                'traditional_grid_position': traditional_allocation['grid_position'],
                'traditional_per_grid_amount': traditional_allocation['per_grid_amount'],
                'traditional_max_position': traditional_allocation['max_position'],
                'traditional_min_position': traditional_allocation['min_position'],
                
                # 收益分析（兼容传统字段名）
                'avg_profit_per_grid': profit_analysis['profit_per_trade'],
                'avg_profit_rate': profit_analysis['profit_rate_per_trade'],
                'monthly_profit_estimate': profit_analysis['monthly_profit_estimate'],
                'break_even_amplitude': profit_analysis['break_even_amplitude'],
                
                # 增强收益分析
                'profit_per_trade': profit_analysis['profit_per_trade'],
                'profit_rate_per_trade': profit_analysis['profit_rate_per_trade'],
                'monthly_return_rate': profit_analysis['monthly_return_rate'],
                'annualized_return_rate': profit_analysis['annualized_return_rate'],
                
                # 频率预估 - 新的基于日频次的逻辑
                'target_daily_triggers': freq_config['target_daily_triggers'],
                'predicted_daily_triggers': predicted_daily_triggers,
                'estimated_triggers_per_month': monthly_stats['monthly_triggers'],
                'estimated_success_rate': monthly_stats['success_rate'],
                'frequency_match_score': frequency_match_score,
                
                # 风险评估
                'max_drawdown_estimate': profit_analysis.get('max_drawdown_estimate', 0.05),
                'risk_level': self._assess_risk_level(volatility, price_range['range_ratio']),
                
                # 计算方法标识
                'calculation_method': 'frequency_based' if historical_patterns else 'traditional',
                'historical_data_available': historical_patterns is not None,
                'calculation_date': datetime.now().isoformat()
            }
            
            logger.info(f"网格参数计算完成 - 频率: {frequency}, 网格数: {grid_count}, "
                       f"价格区间: [{price_range['lower']:.3f}, {price_range['upper']:.3f}], "
                       f"目标日频次: {freq_config['target_daily_triggers']}, "
                       f"预测日频次: {predicted_daily_triggers:.2f}")
            
            return grid_params
            
        except Exception as e:
            logger.error(f"计算网格参数失败: {str(e)}")
            return {'error': f'计算网格参数失败: {str(e)}'}
    
    def generate_adjustment_suggestions(self, analysis_result: Dict, grid_params: Dict) -> Dict:
        """
        生成动态调整建议 - 增强版，包含目标收益率相关建议
        
        Args:
            analysis_result: 分析结果
            grid_params: 网格参数
            
        Returns:
            Dict: 调整建议
        """
        try:
            if 'error' in analysis_result or 'error' in grid_params:
                return {'error': '无法生成调整建议'}
            
            suggestions = {
                'target_return_optimization': self._suggest_target_return_optimization(
                    analysis_result, grid_params
                ),
                'volatility_increase': self._suggest_volatility_increase_adjustment(
                    analysis_result, grid_params
                ),
                'volatility_decrease': self._suggest_volatility_decrease_adjustment(
                    analysis_result, grid_params
                ),
                'trend_market': self._suggest_trend_market_adjustment(
                    analysis_result, grid_params
                ),
                'capital_efficiency': self._suggest_capital_efficiency_improvement(
                    grid_params
                ),
                'general_principles': self._get_enhanced_general_principles()
            }
            
            return suggestions
            
        except Exception as e:
            logger.error(f"生成调整建议失败: {str(e)}")
            return {'error': f'生成调整建议失败: {str(e)}'}
    
    def _suggest_target_return_optimization(self, analysis_result: Dict, grid_params: Dict) -> Dict:
        """
        目标收益率优化建议
        
        Args:
            analysis_result: 分析结果
            grid_params: 网格参数
            
        Returns:
            Dict: 目标收益率优化建议
        """
        try:
            target_achievement_ratio = grid_params.get('target_achievement_ratio', 0)
            actual_monthly_return = grid_params.get('actual_monthly_return_rate', 0)
            target_monthly_return = grid_params.get('target_monthly_return', 0.05)
            
            if target_achievement_ratio >= 0.9:
                situation = '目标收益率可达成'
                suggestions = [
                    f'当前配置预期可实现月收益率 {actual_monthly_return:.2%}，接近目标 {target_monthly_return:.2%}',
                    '可以考虑适当提高目标收益率或降低风险',
                    '建议保持当前股数配置，定期监控实际表现',
                    '可以考虑将部分资金投入其他策略以分散风险'
                ]
                adjustments = {
                    'action': '维持当前配置',
                    'risk_level': '可接受',
                    'optimization_potential': '低'
                }
            elif target_achievement_ratio >= 0.7:
                situation = '目标收益率基本可达成'
                suggestions = [
                    f'当前配置预期实现月收益率 {actual_monthly_return:.2%}，略低于目标 {target_monthly_return:.2%}',
                    '可以适当增加每网格的交易股数',
                    '考虑优化网格密度以提高交易频次',
                    '监控市场波动性，适时调整参数'
                ]
                adjustments = {
                    'shares_adjustment': '增加10-20%',
                    'grid_density': '可适当增加',
                    'risk_level': '中等'
                }
            elif target_achievement_ratio >= 0.5:
                situation = '目标收益率存在缺口'
                suggestions = [
                    f'当前配置预期月收益率 {actual_monthly_return:.2%}，明显低于目标 {target_monthly_return:.2%}',
                    '建议显著增加每网格的交易股数',
                    '考虑缩小网格区间以提高交易频次',
                    '评估是否需要降低目标收益率预期',
                    '考虑增加初始投入资金'
                ]
                adjustments = {
                    'shares_adjustment': '增加30-50%',
                    'grid_range': '缩小10-15%',
                    'target_return': '可考虑降低至3-4%',
                    'capital_increase': '建议考虑'
                }
            else:
                situation = '目标收益率难以达成'
                suggestions = [
                    f'当前配置预期月收益率 {actual_monthly_return:.2%}，远低于目标 {target_monthly_return:.2%}',
                    '建议重新评估目标收益率的合理性',
                    '考虑大幅增加交易股数（注意风险控制）',
                    '评估切换到更高频的交易策略',
                    '考虑组合多种策略以提高整体收益'
                ]
                adjustments = {
                    'target_return': f'建议降低至 {actual_monthly_return * 1.5:.1%}',
                    'strategy_review': '需要重新评估',
                    'risk_warning': '大幅调整股数存在高风险'
                }
            
            return {
                'situation': situation,
                'target_achievement_ratio': f'{target_achievement_ratio:.1%}',
                'suggestions': suggestions,
                'parameter_adjustments': adjustments
            }
            
        except Exception as e:
            logger.error(f"生成目标收益率优化建议失败: {str(e)}")
            return {
                'situation': '无法分析',
                'suggestions': ['建议检查参数配置'],
                'error': str(e)
            }
    
    def _suggest_capital_efficiency_improvement(self, grid_params: Dict) -> Dict:
        """
        资金效率改进建议
        
        Args:
            grid_params: 网格参数
            
        Returns:
            Dict: 资金效率改进建议
        """
        try:
            capital_per_grid_ratio = grid_params.get('capital_per_grid_ratio', 0)
            grid_count = grid_params.get('grid_count', 0)
            
            # 修正：网格交易中，通常只有一半的网格会同时持仓
            # 因为买入网格和卖出网格是交替的
            effective_grid_ratio = 0.5  # 假设50%的网格同时持仓
            total_capital_usage = capital_per_grid_ratio * grid_count * effective_grid_ratio
            
            if total_capital_usage > 0.8:
                situation = '资金利用率过高'
                suggestions = [
                    f'当前资金利用率 {total_capital_usage:.1%}，存在流动性风险',
                    '建议减少每网格的交易股数',
                    '保留更多现金应对市场突发情况',
                    '考虑降低网格数量以减少资金占用'
                ]
                risk_level = '高风险'
            elif total_capital_usage > 0.6:
                situation = '资金利用率适中'
                suggestions = [
                    f'当前资金利用率 {total_capital_usage:.1%}，处于合理范围',
                    '可以根据市场情况微调股数配置',
                    '保持当前的风险控制水平',
                    '定期评估资金使用效率'
                ]
                risk_level = '中等风险'
            else:
                situation = '资金利用率偏低'
                suggestions = [
                    f'当前资金利用率 {total_capital_usage:.1%}，存在提升空间',
                    '可以适当增加每网格的交易股数',
                    '考虑增加网格数量以提高覆盖范围',
                    '评估是否可以提高目标收益率'
                ]
                risk_level = '低风险'
            
            return {
                'situation': situation,
                'capital_utilization': f'{total_capital_usage:.1%}',
                'risk_level': risk_level,
                'suggestions': suggestions,
                'optimization_recommendations': {
                    'ideal_utilization_range': '60%-75%',
                    'current_status': 'high' if total_capital_usage > 0.75 else 'low' if total_capital_usage < 0.5 else 'optimal'
                }
            }
            
        except Exception as e:
            logger.error(f"生成资金效率建议失败: {str(e)}")
            return {
                'situation': '无法分析资金效率',
                'suggestions': ['建议检查资金配置参数'],
                'error': str(e)
            }
    
    def _calculate_price_range(self, current_price: float, avg_amplitude: float, 
                             volatility: float, price_std: float, freq_config: Dict) -> Dict:
        """计算价格区间"""
        try:
            # 基础范围：基于历史波动率和振幅
            base_range_ratio = max(
                avg_amplitude * 15,  # 振幅倍数
                volatility * 0.8,    # 波动率倍数
                price_std / current_price * 8  # 标准差倍数
            ) / 100
            
            # 应用频率配置约束
            min_range = freq_config['min_range_ratio']
            max_range = freq_config['max_range_ratio']
            
            # 调整范围比例
            range_ratio = np.clip(base_range_ratio, min_range, max_range)
            
            # 计算具体价格边界
            range_amount = current_price * range_ratio
            lower_bound = current_price - range_amount / 2
            upper_bound = current_price + range_amount / 2
            
            # 确保下边界为正数
            if lower_bound <= 0:
                lower_bound = current_price * 0.1
                range_ratio = (upper_bound - lower_bound) / current_price
            
            return {
                'lower': lower_bound,
                'upper': upper_bound,
                'range_ratio': range_ratio,
                'range_amount': range_amount
            }
            
        except Exception as e:
            logger.error(f"计算价格区间失败: {str(e)}")
            # 使用默认范围
            default_ratio = (freq_config['min_range_ratio'] + freq_config['max_range_ratio']) / 2
            return {
                'lower': current_price * (1 - default_ratio / 2),
                'upper': current_price * (1 + default_ratio / 2),
                'range_ratio': default_ratio,
                'range_amount': current_price * default_ratio
            }
    
    def _calculate_grid_count(self, price_range: Dict, avg_amplitude: float, 
                            frequency: str, freq_config: Dict) -> int:
        """计算网格数量 - 传统方法（当没有历史数据时使用）"""
        try:
            range_amount = price_range['range_amount']
            target_daily_triggers = freq_config['target_daily_triggers']
            
            # 基于目标日交易频次估算网格数量
            # 假设每个网格步长应该能在日振幅范围内被触发
            estimated_daily_amplitude_ratio = avg_amplitude / 100  # 转换为比例
            
            # 理论上需要的网格步长来达到目标频次
            target_step_ratio = estimated_daily_amplitude_ratio / target_daily_triggers * 2
            
            # 计算网格数量
            base_grid_count = int(price_range['range_ratio'] / target_step_ratio)
            
            # 应用频率配置约束
            min_grids = freq_config['min_grids']
            max_grids = freq_config['max_grids']
            
            # 调整网格数量
            grid_count = np.clip(base_grid_count, min_grids, max_grids)
            
            # 确保为整数
            grid_count = int(grid_count)
            
            logger.debug(f"传统方法计算网格数量: 目标频次={target_daily_triggers}, "
                        f"估算振幅={estimated_daily_amplitude_ratio:.4f}, "
                        f"网格数={grid_count}")
            
            return grid_count
            
        except Exception as e:
            logger.error(f"计算网格数量失败: {str(e)}")
            return freq_config['min_grids']
    
    def _calculate_grid_prices(self, lower_bound: float, upper_bound: float, 
                             grid_count: int) -> List[float]:
        """计算网格价格"""
        try:
            # 等差数列生成网格价格
            step_size = (upper_bound - lower_bound) / grid_count
            
            grid_prices = []
            for i in range(grid_count + 1):  # 包含边界
                price = lower_bound + i * step_size
                grid_prices.append(round(price, 3))
            
            return grid_prices
            
        except Exception as e:
            logger.error(f"计算网格价格失败: {str(e)}")
            return [lower_bound, upper_bound]
    
    def _calculate_capital_allocation(self, initial_capital: float, 
                                    grid_count: int, current_price: float) -> Dict:
        """计算资金分配"""
        try:
            # 基础仓位：30-50%的资金
            base_position_ratio = 0.4
            base_position = initial_capital * base_position_ratio
            
            # 网格仓位：剩余资金
            grid_position = initial_capital - base_position
            
            # 每个网格的资金量
            per_grid_amount = grid_position / grid_count
            
            # 计算最大最小持仓
            max_position = base_position + grid_position  # 全部投入
            min_position = base_position * 0.3  # 基础仓位的30%
            
            return {
                'base_position': base_position,
                'grid_position': grid_position,
                'per_grid_amount': per_grid_amount,
                'max_position': max_position,
                'min_position': min_position
            }
            
        except Exception as e:
            logger.error(f"计算资金分配失败: {str(e)}")
            return {
                'base_position': initial_capital * 0.4,
                'grid_position': initial_capital * 0.6,
                'per_grid_amount': initial_capital * 0.6 / grid_count,
                'max_position': initial_capital,
                'min_position': initial_capital * 0.1
            }
    
    def _calculate_enhanced_profit_analysis(self, dynamic_allocation: Dict, 
                                          predicted_daily_triggers: float,
                                          step_size_ratio: float, current_price: float) -> Dict:
        """
        增强的收益分析 - 基于动态股数分配
        
        Args:
            dynamic_allocation: 动态股数分配结果
            predicted_daily_triggers: 预测日交易频次
            step_size_ratio: 网格步长比例
            current_price: 当前价格
            
        Returns:
            Dict: 增强的收益分析结果
        """
        try:
            shares_per_grid = dynamic_allocation['shares_per_grid']
            amount_per_grid = dynamic_allocation['amount_per_grid']
            
            # 单次交易收益（基于股数和步长）
            profit_per_trade = shares_per_grid * current_price * step_size_ratio
            
            # 单次交易收益率（相对于投入金额）
            profit_rate_per_trade = step_size_ratio
            
            # 月度收益预估
            monthly_trades = predicted_daily_triggers * 20 * 0.8  # 20个交易日，80%成功率
            monthly_profit_estimate = profit_per_trade * monthly_trades
            
            # 月度收益率（相对于单网格投入）
            monthly_return_rate = monthly_profit_estimate / amount_per_grid if amount_per_grid > 0 else 0
            
            # 年化收益率
            annualized_return_rate = monthly_return_rate * 12
            
            # 盈亏平衡振幅（考虑交易成本）
            break_even_amplitude = (self.transaction_cost * 2) * 100  # 双边成本转换为百分比
            
            # 最大回撤预估
            max_drawdown_estimate = self._estimate_max_drawdown(step_size_ratio, monthly_trades)
            
            # 风险收益比
            risk_return_ratio = monthly_return_rate / max_drawdown_estimate if max_drawdown_estimate > 0 else 0
            
            return {
                'profit_per_trade': profit_per_trade,
                'profit_rate_per_trade': profit_rate_per_trade,
                'monthly_profit_estimate': monthly_profit_estimate,
                'monthly_return_rate': monthly_return_rate,
                'annualized_return_rate': annualized_return_rate,
                'break_even_amplitude': break_even_amplitude,
                'max_drawdown_estimate': max_drawdown_estimate,
                'risk_return_ratio': risk_return_ratio,
                'monthly_trades_estimate': monthly_trades
            }
            
        except Exception as e:
            logger.error(f"计算增强收益分析失败: {str(e)}")
            return {
                'profit_per_trade': 0,
                'profit_rate_per_trade': step_size_ratio,
                'monthly_profit_estimate': 0,
                'monthly_return_rate': 0,
                'annualized_return_rate': 0,
                'break_even_amplitude': 0.2,
                'max_drawdown_estimate': 0.05,
                'risk_return_ratio': 0,
                'error': str(e)
            }
    
    def _estimate_max_drawdown(self, step_size_ratio: float, monthly_trades: float) -> float:
        """
        估算最大回撤
        
        Args:
            step_size_ratio: 网格步长比例
            monthly_trades: 月度交易次数
            
        Returns:
            float: 最大回撤估算（百分比）
        """
        try:
            # 基于步长和交易频次的回撤模型
            # 假设最坏情况下连续亏损的网格数
            max_consecutive_losses = min(5, max(2, monthly_trades * 0.1))
            
            # 单次最大亏损（步长 + 交易成本）
            single_loss_ratio = step_size_ratio + (self.transaction_cost * 2)
            
            # 最大回撤 = 连续亏损次数 × 单次亏损比例 × 风险系数
            risk_multiplier = 1.2  # 20%的风险缓冲
            max_drawdown = max_consecutive_losses * single_loss_ratio * risk_multiplier
            
            # 限制在合理范围内（1%-20%）
            return max(0.01, min(0.20, max_drawdown))
            
        except Exception as e:
            logger.error(f"估算最大回撤失败: {str(e)}")
            return 0.05  # 默认5%回撤
    
    def _calculate_profit_analysis(self, grid_prices: List[float], per_trade_amount: float,
                                 avg_amplitude: float, transaction_cost: float) -> Dict:
        """计算收益分析（传统方法，保留用于兼容性）"""
        try:
            step_size = (grid_prices[-1] - grid_prices[0]) / (len(grid_prices) - 1)
            
            # 平均每网格收益
            avg_profit = step_size * per_trade_amount
            
            # 收益率
            avg_profit_rate = step_size / grid_prices[len(grid_prices) // 2]
            
            # 月度收益预估
            monthly_estimate = avg_profit * 20  # 假设每月触发20次
            
            # 盈亏平衡振幅
            break_even_amplitude = (transaction_cost * 2) * 100  # 双边成本
            
            # 最大回撤预估（百分比）
            current_price = grid_prices[len(grid_prices) // 2]  # 取中间价格作为当前价格
            max_drawdown_amount = step_size * 3  # 假设连续3个网格亏损
            max_drawdown = max_drawdown_amount / current_price  # 转换为百分比
            
            return {
                'avg_profit': avg_profit,
                'avg_profit_rate': avg_profit_rate,
                'monthly_estimate': monthly_estimate,
                'break_even_amplitude': break_even_amplitude,
                'max_drawdown': max_drawdown
            }
            
        except Exception as e:
            logger.error(f"计算收益分析失败: {str(e)}")
            return {
                'avg_profit': per_trade_amount * 0.01,
                'avg_profit_rate': 0.01,
                'monthly_estimate': per_trade_amount * 0.2,
                'break_even_amplitude': 0.2,
                'max_drawdown': 0.05  # 默认5%回撤
            }
    
    def _estimate_trigger_frequency_legacy(self, avg_amplitude: float, grid_count: int, 
                                         range_ratio: float) -> Dict:
        """估算触发频率 - 传统方法（已弃用，保留用于兼容性）"""
        try:
            # 每个网格的步长比例
            step_ratio = range_ratio / grid_count
            
            # 触发概率：日均振幅能覆盖网格步长的概率
            trigger_probability = min(1.0, avg_amplitude / (step_ratio * 100))
            
            # 日触发次数预估
            daily_triggers = trigger_probability * 2  # 假设每日可能有2次机会
            
            # 月触发次数预估
            triggers_per_month = daily_triggers * 20  # 20个交易日
            
            # 成功率预估
            success_rate = min(0.9, trigger_probability * 1.2)
            
            return {
                'daily_triggers': daily_triggers,
                'triggers_per_month': int(triggers_per_month),
                'success_rate': success_rate
            }
            
        except Exception as e:
            logger.error(f"估算触发频率失败: {str(e)}")
            return {
                'daily_triggers': 1.0,
                'triggers_per_month': 20,
                'success_rate': 0.7
            }
    
    def _assess_risk_level(self, volatility: float, range_ratio: float) -> str:
        """评估风险等级"""
        try:
            risk_score = volatility / 50 + range_ratio / 0.5
            
            if risk_score < 0.8:
                return '低风险'
            elif risk_score < 1.2:
                return '中等风险'
            elif risk_score < 1.6:
                return '高风险'
            else:
                return '极高风险'
            
        except:
            return '中等风险'
    
    def _suggest_volatility_increase_adjustment(self, analysis_result: Dict, 
                                               grid_params: Dict) -> Dict:
        """波动率上升时的调整建议"""
        return {
            'situation': '波动率上升',
            'suggestions': [
                '适当扩大网格区间，增加价格覆盖范围',
                '减少网格数量，增大单个网格的步长',
                '降低仓位比例，控制风险暴露',
                '设置更严格的止损条件',
                '考虑暂停交易，等待波动率稳定'
            ],
            'parameter_adjustments': {
                'price_range_ratio': '增加10-20%',
                'grid_count': '减少20-30%',
                'position_ratio': '降低至30-40%',
                'stop_loss': '设置5-8%的止损线'
            }
        }
    
    def _suggest_volatility_decrease_adjustment(self, analysis_result: Dict, 
                                               grid_params: Dict) -> Dict:
        """波动率下降时的调整建议"""
        return {
            'situation': '波动率下降',
            'suggestions': [
                '缩小网格区间，提高资金利用效率',
                '增加网格数量，捕捉更小的价格波动',
                '适当提高仓位比例',
                '降低对收益的期望值',
                '考虑切换到更高频的交易策略'
            ],
            'parameter_adjustments': {
                'price_range_ratio': '减少10-15%',
                'grid_count': '增加15-25%',
                'position_ratio': '提高至50-60%',
                'profit_expectation': '降低20-30%'
            }
        }
    
    def _suggest_trend_market_adjustment(self, analysis_result: Dict, 
                                        grid_params: Dict) -> Dict:
        """趋势市场下的调整建议"""
        trend_direction = analysis_result.get('trend_direction', '震荡')
        
        if '上涨' in trend_direction:
            situation = '上涨趋势市场'
            suggestions = [
                '将网格中心适当上移',
                '在下方设置更密集的网格',
                '减少上方网格的仓位配置',
                '考虑加入趋势跟踪策略',
                '设置移动止盈条件'
            ]
        elif '下跌' in trend_direction:
            situation = '下跌趋势市场'
            suggestions = [
                '将网格中心适当下移',
                '在上方设置更密集的网格',
                '减少下方网格的仓位配置',
                '考虑暂停网格交易',
                '设置更严格的止损条件'
            ]
        else:
            situation = '趋势性市场'
            suggestions = [
                '重新评估网格策略的适用性',
                '考虑使用动态网格策略',
                '结合趋势指标进行优化',
                '适当降低仓位和预期收益',
                '密切关注市场变化'
            ]
        
        return {
            'situation': situation,
            'suggestions': suggestions,
            'parameter_adjustments': {
                'grid_center': '根据趋势方向调整',
                'position_allocation': '趋势方向减少配置',
                'risk_management': '加强风险管理'
            }
        }
    
    def _get_enhanced_general_principles(self) -> List[str]:
        """增强的通用原则 - 适用于目标收益率导向策略"""
        return [
            '以目标收益率为导向，定期评估实际表现与预期的差距',
            '动态调整交易股数，平衡收益目标与风险控制',
            '严格控制单笔交易金额，避免过度集中风险',
            '保持20%以上的现金储备，确保流动性安全',
            '定期回顾网格参数，根据市场变化及时调整',
            '关注交易成本对收益的影响，确保净收益为正',
            '监控资金利用率，维持在60%-75%的合理范围',
            '分散投资时间和标的，降低单一策略风险',
            '建立止损机制，设定最大可接受亏损限额',
            '跟踪市场波动性变化，适时调整风险敞口',
            '记录交易数据，持续优化策略参数',
            '在高波动期间降低仓位，在低波动期间适度加仓'
        ]
    
    def _get_general_principles(self) -> List[str]:
        """通用原则（保留用于兼容性）"""
        return [
            '定期回顾和调整网格参数，适应市场变化',
            '严格控制风险，设置合理的止损线',
            '分散投资，不要将所有资金投入单一策略',
            '关注交易成本，确保网格收益能覆盖成本',
            '保持充足的现金储备，应对突发情况',
            '监控市场流动性，避免在流动性不足时交易',
            '根据市场波动性动态调整网格密度',
            '定期评估策略有效性，必要时及时调整'
        ]
    
    def _get_frequency_name(self, frequency: str) -> str:
        """获取频率中文名称"""
        frequency_names = {
            'high': '高频',
            'medium': '中频',
            'low': '低频'
        }
        return frequency_names.get(frequency, '未知')
