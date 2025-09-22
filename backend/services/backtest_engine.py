"""
简化回测引擎
基于日线数据的网格交易策略回测
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any

class GridBacktestEngine:
    """网格交易回测引擎"""
    
    def __init__(self, initial_capital: float, grid_levels: List[Dict], base_position_ratio: float = 0.2):
        """
        初始化回测引擎
        
        Args:
            initial_capital: 初始资金
            grid_levels: 网格价位列表
            base_position_ratio: 底仓比例
        """
        self.initial_capital = initial_capital
        self.grid_levels = sorted(grid_levels, key=lambda x: x['price'])
        self.base_position_ratio = base_position_ratio
        
        # 回测状态
        self.cash = initial_capital * (1 - base_position_ratio)  # 可用现金
        self.base_position_value = initial_capital * base_position_ratio  # 底仓价值
        self.positions = {}  # 网格持仓 {price: shares}
        self.trades = []  # 交易记录
        self.equity_curve = []  # 权益曲线
        
        # 初始化网格状态
        for level in self.grid_levels:
            self.positions[level['price']] = 0
    
    def run_backtest(self, price_data: pd.DataFrame) -> Dict[str, Any]:
        """
        执行回测
        
        Args:
            price_data: 价格数据，包含 trade_date, open, high, low, close, vol
            
        Returns:
            回测结果字典
        """
        if price_data.empty:
            return self._generate_empty_result()
        
        # 确保数据按日期排序
        price_data = price_data.sort_values('date').reset_index(drop=True)
        
        # 计算底仓股数（基于第一天收盘价）
        first_price = price_data.iloc[0]['close']
        base_shares = int(self.base_position_value / first_price)
        
        # 执行逐日回测
        for idx, row in price_data.iterrows():
            self._process_daily_trading(row, idx)
        
        # 计算最终结果
        final_price = price_data.iloc[-1]['close']
        return self._calculate_results(price_data, base_shares, final_price)
    
    def _process_daily_trading(self, price_row: pd.Series, day_idx: int):
        """处理单日交易"""
        date = price_row['date']
        high = price_row['high']
        low = price_row['low']
        close = price_row['close']
        
        # 检查每个网格点位是否被触发
        for level in self.grid_levels:
            # 安全地获取价格和资金信息
            if isinstance(level, dict):
                grid_price = level.get('price', 0)
                allocated_fund = level.get('allocated_fund', level.get('actual_fund', 1000))
            else:
                # 如果level不是字典，跳过这个网格点
                continue
            
            # 买入条件：价格跌到网格点位且有资金
            if low <= grid_price and self.cash >= allocated_fund and self.positions[grid_price] == 0:
                shares = int(allocated_fund / grid_price)
                if shares > 0:
                    cost = shares * grid_price
                    self.cash -= cost
                    self.positions[grid_price] = shares
                    
                    self.trades.append({
                        'date': date,
                        'type': 'buy',
                        'price': grid_price,
                        'shares': shares,
                        'amount': cost,
                        'profit': 0
                    })
            
            # 卖出条件：价格涨到网格点位且有持仓
            elif high >= grid_price and self.positions[grid_price] > 0:
                shares = self.positions[grid_price]
                revenue = shares * grid_price
                
                # 计算盈利（找到对应的买入价格）
                buy_price = self._find_buy_price(grid_price)
                profit = (grid_price - buy_price) * shares if buy_price else 0
                
                self.cash += revenue
                self.positions[grid_price] = 0
                
                self.trades.append({
                    'date': date,
                    'type': 'sell',
                    'price': grid_price,
                    'shares': shares,
                    'amount': revenue,
                    'profit': profit
                })
        
        # 记录当日权益
        total_equity = self._calculate_current_equity(close)
        self.equity_curve.append({
            'date': date,
            'equity': total_equity,
            'cash': self.cash,
            'position_value': total_equity - self.cash
        })
    
    def _find_buy_price(self, sell_price: float) -> float:
        """找到对应的买入价格（简化处理，假设就是下一个更低的网格价位）"""
        lower_levels = [level['price'] for level in self.grid_levels if level['price'] < sell_price]
        return max(lower_levels) if lower_levels else sell_price * 0.95
    
    def _calculate_current_equity(self, current_price: float) -> float:
        """计算当前总权益"""
        # 现金
        total_equity = self.cash
        
        # 底仓价值
        base_shares = int(self.base_position_value / self.grid_levels[0]['price'])
        total_equity += base_shares * current_price
        
        # 网格持仓价值
        for grid_price, shares in self.positions.items():
            total_equity += shares * current_price
        
        return total_equity
    
    def _calculate_results(self, price_data: pd.DataFrame, base_shares: int, final_price: float) -> Dict[str, Any]:
        """计算回测结果"""
        if not self.trades:
            return self._generate_empty_result()
        
        # 基本统计
        total_trades = len(self.trades)
        buy_trades = [t for t in self.trades if t['type'] == 'buy']
        sell_trades = [t for t in self.trades if t['type'] == 'sell']
        profitable_trades = [t for t in sell_trades if t['profit'] > 0]
        
        # 收益计算
        total_profit = sum(t['profit'] for t in sell_trades)
        final_equity = self._calculate_current_equity(final_price)
        total_return = (final_equity - self.initial_capital) / self.initial_capital
        
        # 时间计算
        start_date = price_data.iloc[0]['date']
        end_date = price_data.iloc[-1]['date']
        total_days = len(price_data)
        
        # 年化收益率
        years = total_days / 252  # 假设252个交易日为一年
        annual_return = (1 + total_return) ** (1/years) - 1 if years > 0 else 0
        
        # 最大回撤计算
        max_drawdown = self._calculate_max_drawdown()
        
        # 交易频率
        avg_trades_per_day = total_trades / total_days if total_days > 0 else 0
        expected_monthly_trades = avg_trades_per_day * 21  # 21个交易日为一个月
        expected_monthly_profit = total_profit * (21 / total_days) if total_days > 0 else 0
        
        return {
            'backtest_period': {
                'start_date': start_date,
                'end_date': end_date,
                'total_days': total_days
            },
            'performance': {
                'total_profit': total_profit,
                'total_return': total_return,
                'annual_return': annual_return,
                'max_drawdown': max_drawdown,
                'win_rate': len(profitable_trades) / len(sell_trades) if sell_trades else 0
            },
            'trading_stats': {
                'total_trades': total_trades,
                'profitable_trades': len(profitable_trades),
                'avg_trades_per_day': avg_trades_per_day,
                'expected_monthly_trades': expected_monthly_trades,
                'expected_monthly_profit': expected_monthly_profit
            },
            'final_equity': final_equity,
            'trades': self.trades[-10:],  # 最近10笔交易
            'equity_curve': self.equity_curve[-30:],  # 最近30天权益曲线
            'disclaimer': "本回测基于历史日线数据估算，实际交易效果可能存在差异。投资有风险，请谨慎决策。"
        }
    
    def _calculate_max_drawdown(self) -> float:
        """计算最大回撤"""
        if not self.equity_curve:
            return 0.0
        
        equity_values = [point['equity'] for point in self.equity_curve]
        peak = equity_values[0]
        max_dd = 0.0
        
        for equity in equity_values:
            if equity > peak:
                peak = equity
            drawdown = (peak - equity) / peak
            max_dd = max(max_dd, drawdown)
        
        return max_dd
    
    def _generate_empty_result(self) -> Dict[str, Any]:
        """生成空结果"""
        return {
            'backtest_period': {
                'start_date': '',
                'end_date': '',
                'total_days': 0
            },
            'performance': {
                'total_profit': 0,
                'total_return': 0,
                'annual_return': 0,
                'max_drawdown': 0,
                'win_rate': 0
            },
            'trading_stats': {
                'total_trades': 0,
                'profitable_trades': 0,
                'avg_trades_per_day': 0,
                'expected_monthly_trades': 0,
                'expected_monthly_profit': 0
            },
            'final_equity': self.initial_capital,
            'trades': [],
            'equity_curve': [],
            'disclaimer': "数据不足，无法进行有效回测。"
        }

def run_grid_backtest(
    price_data: pd.DataFrame,
    initial_capital: float,
    grid_levels: List[Dict],
    base_position_ratio: float = 0.2
) -> Dict[str, Any]:
    """
    运行网格交易回测
    
    Args:
        price_data: 价格数据
        initial_capital: 初始资金
        grid_levels: 网格价位配置
        base_position_ratio: 底仓比例
        
    Returns:
        回测结果
    """
    engine = GridBacktestEngine(initial_capital, grid_levels, base_position_ratio)
    return engine.run_backtest(price_data)