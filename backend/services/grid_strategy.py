"""
网格策略计算模块
基于ATR算法的智能网格参数计算和资金分配
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
from .atr_engine import ATREngine

logger = logging.getLogger(__name__)

class GridStrategy:
    """网格策略计算器"""
    
    def __init__(self):
        """初始化策略计算器"""
        self.atr_engine = ATREngine()
    
    def calculate_base_position_ratio(self, atr_ratio: float, risk_preference: str, 
                                    adx_value: float, volatility: float) -> float:
        """
        智能底仓比例计算
        
        Args:
            atr_ratio: ATR比率
            risk_preference: 风险偏好
            adx_value: ADX指数
            volatility: 年化波动率
            
        Returns:
            底仓比例
        """
        try:
            # 基础比例（根据风险偏好）
            base_ratios = {
                '保守': 0.30,  # 35%底仓，65%网格
                '稳健': 0.20,  # 25%底仓，75%网格
                '激进': 0.10   # 15%底仓，85%网格
            }
            
            base_ratio = base_ratios.get(risk_preference, 0.25)
            
            # ATR波动调整（波动越大，底仓比例越高）
            atr_adjustment = min(atr_ratio * 5, 0.15)  # 最大调整15%
            
            # 市场趋势调整（基于ADX指数）
            if adx_value < 20:      # 震荡市
                trend_adjustment = -0.05  # 减少底仓，增加网格资金
            elif adx_value < 25:    # 弱趋势
                trend_adjustment = 0.05   # 适中调整
            else:                   # 强趋势
                trend_adjustment = 0.1    # 增加底仓比例
            
            # 波动率调整
            if volatility > 0.4:    # 高波动
                volatility_adjustment = 0.05
            elif volatility < 0.15: # 低波动
                volatility_adjustment = -0.05
            else:                   # 正常波动
                volatility_adjustment = 0
            
            # 计算最终底仓比例
            final_ratio = (base_ratio + atr_adjustment + 
                          trend_adjustment + volatility_adjustment)
            
            # 限制在10%-70%之间
            final_ratio = max(0.1, min(0.7, final_ratio))
            
            logger.info(f"底仓比例计算: 基础{base_ratio:.1%} + ATR调整{atr_adjustment:.1%} + "
                       f"趋势调整{trend_adjustment:.1%} + 波动率调整{volatility_adjustment:.1%} = {final_ratio:.1%}")
            
            return final_ratio
            
        except Exception as e:
            logger.error(f"底仓比例计算失败: {str(e)}")
            return 0.25  # 默认25%
    
    def calculate_optimal_step_size(self, atr_ratio: float, current_price: float, 
                                   risk_preference: str) -> Tuple[float, float]:
        """
        基于ATR计算最优步长
        
        Args:
            atr_ratio: ATR比率
            current_price: 当前价格
            risk_preference: 风险偏好
            
        Returns:
            (step_size, step_ratio)
        """
        try:
            # ATR 基础步长系数（根据风险偏好）
            risk_multipliers = {
                '保守': 1.0,   # 1.0倍ATR作为步长，步长较大，交易频次较低
                '稳健': 0.8,   # 0.8倍ATR作为步长，平衡交易频次
                '激进': 0.6    # 0.6倍ATR作为步长，步长较小，交易频次较高
            }
            
            risk_multiplier = risk_multipliers.get(risk_preference, 1)
            
            # 计算基于ATR的步长
            atr_value = atr_ratio * current_price
            optimal_step_size = atr_value * risk_multiplier
            optimal_step_ratio = optimal_step_size / current_price
            
            # 确保步长在合理范围内（0.5% - 5%）
            min_step_ratio = 0.005  # 0.2%
            max_step_ratio = 0.05   # 5%
            optimal_step_ratio = max(min_step_ratio, min(max_step_ratio, optimal_step_ratio))
            optimal_step_size = optimal_step_ratio * current_price
            
            logger.info(f"ATR步长计算: ATR比率{atr_ratio:.1%}, 风险系数{risk_multiplier}, "
                       f"最优步长{optimal_step_size:.3f}({optimal_step_ratio:.1%})")
            
            return optimal_step_size, optimal_step_ratio
            
        except Exception as e:
            logger.error(f"ATR步长计算失败: {str(e)}")
            # 返回默认步长（1%）
            default_step_ratio = 0.01
            return current_price * default_step_ratio, default_step_ratio
    
    def calculate_grid_count_from_step(self, price_lower: float, price_upper: float, 
                                      step_size: float, grid_type: str) -> int:
        """
        基于步长计算网格数量
        
        Args:
            price_lower: 价格下边界
            price_upper: 价格上边界
            step_size: 网格步长
            grid_type: 网格类型
            
        Returns:
            网格数量
        """
        try:
            if grid_type == '等差':
                # 等差网格：网格数量 = 价格区间 / 步长
                grid_count = int((price_upper - price_lower) / step_size)
            else:
                # 等比网格：基于步长比例计算
                avg_price = (price_lower + price_upper) / 2
                step_ratio = step_size / avg_price
                grid_count = int(np.log(price_upper / price_lower) / np.log(1 + step_ratio))
            
            # 限制网格数量在合理范围内（10-150个）
            grid_count = max(10, min(150, grid_count))
            
            logger.info(f"基于步长计算网格数量: {grid_type}网格, 步长{step_size:.3f}, 数量{grid_count}个")
            
            return grid_count
            
        except Exception as e:
            logger.error(f"基于步长计算网格数量失败: {str(e)}")
            return 50  # 默认50个
    
    
    def calculate_price_levels(self, price_lower: float, price_upper: float, 
                             grid_count: int, grid_type: str) -> List[float]:
        """
        计算网格价格水平
        
        Args:
            price_lower: 价格下边界
            price_upper: 价格上边界
            grid_count: 网格数量
            grid_type: 网格类型 ('等差' 或 '等比')
            
        Returns:
            价格水平列表
        """
        try:
            if grid_type == '等差':
                # 等差网格
                step = (price_upper - price_lower) / grid_count
                price_levels = [price_lower + i * step for i in range(grid_count + 1)]
            else:
                # 等比网格（推荐）
                ratio = (price_upper / price_lower) ** (1 / grid_count)
                price_levels = [price_lower * (ratio ** i) for i in range(grid_count + 1)]
            
            logger.info(f"价格水平计算完成: {grid_type}网格，{len(price_levels)}个价格点")
            return price_levels
            
        except Exception as e:
            logger.error(f"价格水平计算失败: {str(e)}")
            return []
    
    def calculate_fund_allocation(self, total_capital: float, base_position_ratio: float, 
                                grid_count: int, price_levels: List[float]) -> Dict:
        """
        智能资金分配计算
        
        Args:
            total_capital: 总投资资金
            base_position_ratio: 底仓比例
            grid_count: 网格数量
            price_levels: 价格水平列表
            
        Returns:
            资金分配结果
        """
        try:
            # 1. 底仓资金计算
            base_position_amount = total_capital * base_position_ratio
            
            # 2. 网格交易资金
            grid_trading_amount = total_capital - base_position_amount
            
            # 3. 预留机动资金（5%）
            reserve_amount = total_capital * 0.05
            available_grid_amount = grid_trading_amount - reserve_amount
            
            # 4. 计算单笔数量（基于网格资金平均分配）
            single_trade_quantity = self._calculate_single_trade_quantity(
                available_grid_amount, grid_count, price_levels
            )
            
            # 5. 每格资金分配（使用统一的单笔数量）
            grid_funds = []
            total_required_fund = 0
            
            if price_levels and single_trade_quantity > 0:
                # 只计算买入网格（价格低于当前价格的网格）
                current_price = sum(price_levels) / len(price_levels)  # 使用平均价格作为参考
                buy_levels = [p for p in price_levels[:-1] if p <= current_price]
                
                for i, price in enumerate(price_levels[:-1]):
                    # 使用统一的单笔数量
                    shares = single_trade_quantity
                    actual_fund = shares * price
                    total_required_fund += actual_fund
                    
                    grid_funds.append({
                        'level': i + 1,
                        'price': round(price, 3),
                        'allocated_fund': round(actual_fund, 2),
                        'shares': shares,
                        'actual_fund': round(actual_fund, 2),
                        'is_buy_level': price <= current_price
                    })
                
                # 验证极端情况：所有买入网格成交时的资金需求
                buy_grid_total_fund = sum(gf['actual_fund'] for gf in grid_funds if gf['is_buy_level'])
                
                # 如果买入网格总资金超出可用资金，重新计算单笔数量
                if buy_grid_total_fund > available_grid_amount:
                    logger.warning(f"买入网格总资金{buy_grid_total_fund:.0f}超出可用资金{available_grid_amount:.0f}，重新计算单笔数量")
                    single_trade_quantity = self._recalculate_safe_quantity(
                        available_grid_amount, buy_levels
                    )
                    
                    # 重新计算网格资金分配
                    grid_funds = []
                    for i, price in enumerate(price_levels[:-1]):
                        shares = single_trade_quantity
                        actual_fund = shares * price
                        
                        grid_funds.append({
                            'level': i + 1,
                            'price': round(price, 3),
                            'allocated_fund': round(actual_fund, 2),
                            'shares': shares,
                            'actual_fund': round(actual_fund, 2),
                            'is_buy_level': price <= current_price
                        })
            
            # 6. 计算资金利用率
            total_actual_fund = sum(gf['actual_fund'] for gf in grid_funds)
            utilization_rate = total_actual_fund / total_capital
            
            # 7. 计算买入网格资金占用（极端情况验证）
            buy_grid_fund = sum(gf['actual_fund'] for gf in grid_funds if gf.get('is_buy_level', False))
            buy_grid_safety_ratio = buy_grid_fund / available_grid_amount if available_grid_amount > 0 else 0
            
            # 8. 计算预期单笔收益（基于平均网格间距）
            if len(price_levels) > 1:
                avg_price = sum(price_levels) / len(price_levels)
                avg_step = (price_levels[-1] - price_levels[0]) / len(price_levels)
                expected_profit_per_trade = single_trade_quantity * avg_step
            else:
                expected_profit_per_trade = 0
            
            result = {
                'base_position_amount': round(base_position_amount, 2),
                'grid_trading_amount': round(available_grid_amount, 2),
                'reserve_amount': round(reserve_amount, 2),
                'grid_funds': grid_funds,
                'total_actual_fund': round(total_actual_fund, 2),
                'utilization_rate': round(utilization_rate, 4),
                'expected_profit_per_trade': round(expected_profit_per_trade, 2),
                'grid_count': len(grid_funds),
                'base_position_ratio': base_position_ratio,
                # 新增单笔数量相关字段
                'single_trade_quantity': single_trade_quantity,
                'buy_grid_fund': round(buy_grid_fund, 2),
                'buy_grid_safety_ratio': round(buy_grid_safety_ratio, 4),
                'extreme_case_safe': buy_grid_safety_ratio <= 1.0
            }
            
            logger.info(f"资金分配完成: 底仓{base_position_amount:.0f}, "
                       f"网格{available_grid_amount:.0f}, 单笔数量{single_trade_quantity}股, "
                       f"买入网格资金{buy_grid_fund:.0f}, 安全比例{buy_grid_safety_ratio:.1%}")
            
            return result
            
        except Exception as e:
            logger.error(f"资金分配计算失败: {str(e)}")
            raise
    
    def _calculate_single_trade_quantity(self, available_grid_amount: float, 
                                       grid_count: int, price_levels: List[float]) -> int:
        """
        计算单笔交易数量（基于网格资金平均分配）
        
        公式：单笔数量 = 网格金额 ÷ 网格数量 × 2 ÷ 标的价格，结果100整数倍向下取整
        
        Args:
            available_grid_amount: 可用网格资金
            grid_count: 网格数量
            price_levels: 价格水平列表
            
        Returns:
            单笔交易数量（100股的整数倍）
        """
        try:
            if not price_levels or grid_count <= 0:
                return 100  # 默认最小交易单位
            
            # 计算平均价格（作为标的价格）
            avg_price = sum(price_levels) / len(price_levels)
            
            # 正确的计算公式：网格金额 ÷ 网格数量 × 2 ÷ 标的价格
            # 乘以2是因为只需考虑单边网格（买入网格）
            theoretical_shares = available_grid_amount / grid_count * 2 / avg_price
            
            # 向下取整到100股的整数倍
            shares_per_100 = int(theoretical_shares / 100)
            single_trade_quantity = max(1, shares_per_100) * 100  # 至少100股
            
            logger.debug(f"单笔数量计算: 网格资金{available_grid_amount:.0f}, "
                        f"网格数{grid_count}, 标的价格{avg_price:.3f}, "
                        f"理论股数{theoretical_shares:.0f}, 单笔数量{single_trade_quantity}股")
            
            return single_trade_quantity
            
        except Exception as e:
            logger.error(f"计算单笔数量失败: {str(e)}")
            return 100  # 返回默认值
    
    def _recalculate_safe_quantity(self, available_grid_amount: float, 
                                 buy_levels: List[float]) -> int:
        """
        重新计算安全的单笔数量（确保极端情况下资金充足）
        
        使用相同的计算公式：网格金额 ÷ 网格数量 × 2 ÷ 标的价格
        但针对极端情况进行安全调整
        
        Args:
            available_grid_amount: 可用网格资金
            buy_levels: 买入价格水平列表
            
        Returns:
            安全的单笔交易数量
        """
        try:
            if not buy_levels:
                return 100
            
            # 计算买入网格的平均价格
            avg_buy_price = sum(buy_levels) / len(buy_levels)
            buy_grid_count = len(buy_levels)
            
            # 使用相同的计算公式，但加入安全系数
            # 公式：网格金额 ÷ 买入网格数量 × 2 ÷ 平均买入价格 × 安全系数
            safety_factor = 0.9  # 90%的资金利用率，保留10%安全边际
            safe_theoretical_shares = (available_grid_amount / buy_grid_count * 2 / avg_buy_price) * safety_factor
            
            # 向下取整到100股的整数倍
            safe_shares_per_100 = int(safe_theoretical_shares / 100)
            safe_quantity = max(1, safe_shares_per_100) * 100
            
            logger.info(f"重新计算安全单笔数量: 买入网格数{buy_grid_count}, "
                       f"平均买入价格{avg_buy_price:.3f}, "
                       f"安全理论股数{safe_theoretical_shares:.0f}, "
                       f"最终安全数量{safe_quantity}股")
            
            return safe_quantity
            
        except Exception as e:
            logger.error(f"重新计算安全数量失败: {str(e)}")
            return 100
    
    def calculate_grid_parameters(self, df: pd.DataFrame, total_capital: float,
                                grid_type: str, risk_preference: str, 
                                atr_analysis: Dict, market_indicators: Dict) -> Dict:
        """
        计算完整的网格策略参数（基于ATR智能步长）
        
        Args:
            df: 历史数据
            total_capital: 总投资资金
            grid_type: 网格类型
            risk_preference: 风险偏好
            atr_analysis: ATR分析结果
            market_indicators: 市场指标
            
        Returns:
            完整的网格策略参数
        """
        try:
            current_price = float(df.iloc[-1]['close'])
            atr_ratio = atr_analysis['current_atr_ratio']
            
            # 1. 计算价格区间（基于ATR和风险偏好）
            price_lower, price_upper = self.atr_engine.calculate_price_range(
                current_price, atr_ratio, risk_preference
            )
            
            # 2. 基于ATR计算最优步长（核心改进）
            step_size, step_ratio = self.calculate_optimal_step_size(
                atr_ratio, current_price, risk_preference
            )
            
            # 3. 基于步长计算网格数量（而不是先定义数量）
            grid_count = self.calculate_grid_count_from_step(
                price_lower, price_upper, step_size, grid_type
            )
            
            # 4. 根据实际步长和网格数量重新调整价格区间（确保一致性）
            if grid_type == '等差':
                # 等差网格：确保价格区间与步长*数量一致
                total_range = step_size * grid_count
                price_center = current_price
                price_lower = price_center - total_range / 2
                price_upper = price_center + total_range / 2
            else:
                # 等比网格：基于步长比例调整
                total_ratio = step_ratio * grid_count
                price_lower = current_price * (1 - total_ratio / 2)
                price_upper = current_price * (1 + total_ratio / 2)
            
            # 5. 计算价格水平
            price_levels = self.calculate_price_levels(
                price_lower, price_upper, grid_count, grid_type
            )
            
            # 6. 计算底仓比例
            base_position_ratio = self.calculate_base_position_ratio(
                atr_ratio, risk_preference, 
                market_indicators['adx_value'], 
                market_indicators['volatility']
            )
            
            # 7. 计算资金分配
            fund_allocation = self.calculate_fund_allocation(
                total_capital, base_position_ratio, grid_count, price_levels
            )
            
            # 8. 计算价格区间比例
            price_range_ratio = (price_upper - price_lower) / current_price
            
            # 9. ATR评分
            atr_score, atr_description = self.atr_engine.get_atr_score(atr_ratio)
            
            result = {
                'current_price': current_price,
                'price_range': {
                    'lower': round(price_lower, 3),
                    'upper': round(price_upper, 3),
                    'ratio': round(price_range_ratio, 4)
                },
                'grid_config': {
                    'count': grid_count,
                    'type': grid_type,
                    'step_size': round(step_size, 3),
                    'step_ratio': round(step_ratio, 4)
                },
                'price_levels': [round(p, 3) for p in price_levels],
                'fund_allocation': fund_allocation,
                'risk_preference': risk_preference,
                'atr_based': True,
                'atr_score': atr_score,
                'atr_description': atr_description,
                'calculation_method': 'ATR智能步长算法',
                'calculation_logic': {
                    'step1': f'ATR比率: {atr_ratio:.1%}',
                    'step2': f'基于ATR和风险偏好计算最优步长: {step_size:.3f} ({step_ratio:.1%})',
                    'step3': f'基于步长计算网格数量: {grid_count}个',
                    'step4': f'调整价格区间: [{price_lower:.3f}, {price_upper:.3f}]',
                    'step5': f'生成{len(price_levels)}个价格水平'
                }
            }
            
            logger.info(f"ATR智能网格策略计算完成: ATR步长{step_size:.3f}({step_ratio:.1%}), "
                       f"{grid_count}个{grid_type}网格, 区间[{price_lower:.3f}, {price_upper:.3f}]")
            
            return result
            
        except Exception as e:
            logger.error(f"网格策略参数计算失败: {str(e)}")
            raise

class GridBacktester:
    """简化版网格回测引擎"""
    
    def __init__(self):
        """初始化回测引擎"""
        pass
    
    def run_backtest(self, df: pd.DataFrame, grid_params: Dict, 
                    start_date: str = None, end_date: str = None) -> Dict:
        """
        运行简化版回测
        
        Args:
            df: 历史数据
            grid_params: 网格参数
            start_date: 回测开始日期
            end_date: 回测结束日期
            
        Returns:
            回测结果
        """
        try:
            # 筛选回测时间范围
            if start_date:
                df = df[df['trade_date'] >= start_date.replace('-', '')]
            if end_date:
                df = df[df['trade_date'] <= end_date.replace('-', '')]
            
            if len(df) < 30:
                logger.warning("回测数据不足30天，结果可能不准确")
            
            price_levels = grid_params['price_levels']
            fund_allocation = grid_params['fund_allocation']
            
            # 初始化回测状态
            positions = {}  # 持仓记录 {price_level: shares}
            trades = []     # 交易记录
            total_profit = 0
            max_drawdown = 0
            equity_curve = []
            
            # 初始底仓
            base_shares = int(fund_allocation['base_position_amount'] / grid_params['current_price'])
            current_equity = fund_allocation['base_position_amount']
            
            # 遍历历史数据进行回测
            for idx, row in df.iterrows():
                current_price = float(row['close'])
                date = row['trade_date']
                
                # 检查网格触发
                for i, grid_price in enumerate(price_levels[:-1]):  # 排除最高价格点
                    grid_fund = fund_allocation['grid_funds'][i]
                    
                    # 买入条件：价格跌破网格点且未持仓
                    if (current_price <= grid_price and 
                        grid_price not in positions and 
                        current_price >= price_levels[0]):  # 不低于最低网格
                        
                        shares = grid_fund['shares']
                        if shares > 0:
                            positions[grid_price] = shares
                            trades.append({
                                'date': date,
                                'type': 'buy',
                                'price': grid_price,
                                'shares': shares,
                                'amount': shares * grid_price
                            })
                    
                    # 卖出条件：价格突破网格点且有对应低价位持仓
                    elif current_price >= grid_price and grid_price in positions:
                        shares = positions[grid_price]
                        profit = shares * (current_price - grid_price)
                        total_profit += profit
                        
                        trades.append({
                            'date': date,
                            'type': 'sell',
                            'price': current_price,
                            'shares': shares,
                            'amount': shares * current_price,
                            'profit': profit
                        })
                        
                        del positions[grid_price]
                
                # 计算当前权益
                position_value = sum(shares * current_price for shares in positions.values())
                current_equity = (fund_allocation['base_position_amount'] + 
                                base_shares * current_price + position_value + total_profit)
                
                equity_curve.append({
                    'date': date,
                    'equity': current_equity,
                    'price': current_price
                })
                
                # 计算最大回撤
                if equity_curve:
                    peak_equity = max(eq['equity'] for eq in equity_curve)
                    drawdown = (peak_equity - current_equity) / peak_equity
                    max_drawdown = max(max_drawdown, drawdown)
            
            # 计算回测统计
            total_trades = len(trades)
            profitable_trades = len([t for t in trades if t.get('profit', 0) > 0])
            win_rate = profitable_trades / max(total_trades, 1)
            
            # 计算收益率
            initial_capital = fund_allocation['base_position_amount'] + fund_allocation['grid_trading_amount']
            total_return = (current_equity - initial_capital) / initial_capital
            
            # 计算年化收益率
            days = len(df)
            annual_return = (1 + total_return) ** (252 / max(days, 1)) - 1
            
            # 预测交易频次
            avg_trades_per_day = total_trades / max(days, 1)
            expected_monthly_trades = avg_trades_per_day * 21  # 21个交易日/月
            
            # 预期月收益
            if days > 0:
                daily_profit = total_profit / days
                expected_monthly_profit = daily_profit * 21
            else:
                expected_monthly_profit = 0
            
            result = {
                'backtest_period': {
                    'start_date': df.iloc[0]['trade_date'],
                    'end_date': df.iloc[-1]['trade_date'],
                    'total_days': days
                },
                'performance': {
                    'total_return': round(total_return, 4),
                    'annual_return': round(annual_return, 4),
                    'total_profit': round(total_profit, 2),
                    'max_drawdown': round(max_drawdown, 4),
                    'win_rate': round(win_rate, 4)
                },
                'trading_stats': {
                    'total_trades': total_trades,
                    'profitable_trades': profitable_trades,
                    'avg_trades_per_day': round(avg_trades_per_day, 2),
                    'expected_monthly_trades': round(expected_monthly_trades, 1),
                    'expected_monthly_profit': round(expected_monthly_profit, 2)
                },
                'final_equity': round(current_equity, 2),
                'trades': trades[-10:] if trades else [],  # 最近10笔交易
                'equity_curve': equity_curve[-60:] if equity_curve else [],  # 最近60天权益曲线
                'disclaimer': "基于日线数据估算，实际效果可能有差异"
            }
            
            logger.info(f"回测完成: {days}天, {total_trades}笔交易, "
                       f"总收益{total_profit:.2f}, 年化收益率{annual_return:.1%}")
            
            return result
            
        except Exception as e:
            logger.error(f"回测失败: {str(e)}")
            raise