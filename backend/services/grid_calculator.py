import numpy as np
import pandas as pd
import logging
from typing import Dict, List
from datetime import datetime
from .frequency_calculator import FrequencyCalculator

logger = logging.getLogger(__name__)


class GridCalculator:
    """网格策略计算器"""
    
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
                                historical_data: pd.DataFrame = None) -> Dict:
        """
        计算网格策略参数 - 基于日交易频次的新逻辑
        
        Args:
            current_price: 当前价格
            analysis_result: ETF分析结果
            frequency: 交易频率 ('high', 'medium', 'low')
            initial_capital: 初始资金
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
            
            # 5. 计算资金分配
            capital_allocation = self._calculate_capital_allocation(
                initial_capital, grid_count, current_price
            )
            
            # 6. 计算单笔交易量
            per_trade_amount = capital_allocation['per_grid_amount']
            per_trade_shares = int(per_trade_amount / current_price)
            
            # 确保至少100股
            if per_trade_shares < 100:
                per_trade_shares = 100
                per_trade_amount = per_trade_shares * current_price
            
            # 7. 计算预期收益和风险
            profit_analysis = self._calculate_profit_analysis(
                grid_prices, per_trade_amount, avg_amplitude, self.transaction_cost
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
                
                # 资金配置
                'initial_capital': initial_capital,
                'base_position_amount': capital_allocation['base_position'],
                'grid_position_amount': capital_allocation['grid_position'],
                'per_grid_amount': per_trade_amount,
                'per_grid_shares': per_trade_shares,
                'max_position_amount': capital_allocation['max_position'],
                'min_position_amount': capital_allocation['min_position'],
                
                # 收益分析
                'avg_profit_per_grid': profit_analysis['avg_profit'],
                'avg_profit_rate': profit_analysis['avg_profit_rate'],
                'monthly_profit_estimate': profit_analysis['monthly_estimate'],
                'break_even_amplitude': profit_analysis['break_even_amplitude'],
                
                # 频率预估 - 新的基于日频次的逻辑
                'target_daily_triggers': freq_config['target_daily_triggers'],
                'predicted_daily_triggers': predicted_daily_triggers,
                'estimated_triggers_per_month': monthly_stats['monthly_triggers'],
                'estimated_success_rate': monthly_stats['success_rate'],
                'frequency_match_score': frequency_match_score,
                
                # 风险评估
                'max_drawdown_estimate': profit_analysis['max_drawdown'],
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
        生成动态调整建议
        
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
                'volatility_increase': self._suggest_volatility_increase_adjustment(
                    analysis_result, grid_params
                ),
                'volatility_decrease': self._suggest_volatility_decrease_adjustment(
                    analysis_result, grid_params
                ),
                'trend_market': self._suggest_trend_market_adjustment(
                    analysis_result, grid_params
                ),
                'general_principles': self._get_general_principles()
            }
            
            return suggestions
            
        except Exception as e:
            logger.error(f"生成调整建议失败: {str(e)}")
            return {'error': f'生成调整建议失败: {str(e)}'}
    
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
    
    def _calculate_profit_analysis(self, grid_prices: List[float], per_trade_amount: float,
                                 avg_amplitude: float, transaction_cost: float) -> Dict:
        """计算收益分析"""
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
    
    def _get_general_principles(self) -> List[str]:
        """通用原则"""
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
