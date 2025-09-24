import React from 'react';
import { 
  BarChart3, 
  TrendingUp, 
  TrendingDown,
  Calendar, 
  DollarSign, 
  Percent,
  Activity,
  Target,
  AlertTriangle,
  CheckCircle,
  Info,
  Lightbulb,
  Shield,
  Zap
} from 'lucide-react';

const BacktestResultCard = ({ backtestResult, strategyRationale, adjustmentSuggestions, showDetailed = false }) => {
  if (!backtestResult) return null;

  const {
    backtest_period,
    performance,
    trading_stats,
    final_equity,
    trades,
    disclaimer
  } = backtestResult;

  // 格式化金额
  const formatAmount = (amount) => {
    return new Intl.NumberFormat('zh-CN', {
      style: 'currency',
      currency: 'CNY',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  // 格式化百分比
  const formatPercent = (value) => {
    return (value * 100).toFixed(2) + '%';
  };

  // 格式化日期为 YYYY-MM-DD 格式
  const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return dateString; // 如果无法解析，返回原字符串
    
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    
    return `${year}-${month}-${day}`;
  };

  // 获取收益率颜色
  const getReturnColor = (value) => {
    if (value > 0) return 'text-red-600';
    if (value < 0) return 'text-green-600';
    return 'text-gray-600';
  };

  return (
    <div className="space-y-6">
      {/* 重要提示 */}
      <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-lg">
        <div className="flex items-start gap-2">
          <AlertTriangle className="w-5 h-5 text-yellow-600 mt-0.5 flex-shrink-0" />
          <div className="text-sm text-yellow-800">
            <p className="font-medium mb-1">重要提示</p>
            <p>{disclaimer}</p>
          </div>
        </div>
      </div>

      {/* 回测概览 */}
      <div className="bg-gradient-to-r from-green-50 to-emerald-50 p-6 rounded-lg border border-green-200">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 bg-green-200 rounded-lg">
            <BarChart3 className="w-6 h-6 text-green-700" />
          </div>
          <div>
            <h3 className="text-xl font-bold text-green-900">历史回测表现与收益预测</h3>
            <p className="text-green-700">基于历史数据的策略效果分析</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-white p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <Calendar className="w-4 h-4 text-blue-600" />
              <span className="text-sm font-medium text-gray-700">回测期间</span>
            </div>
            <div className="text-lg font-bold text-gray-900">{backtest_period.total_days}天</div>
            <div className="text-xs text-gray-600">
              {formatDate(backtest_period.start_date)} - {formatDate(backtest_period.end_date)}
            </div>
          </div>

          <div className="bg-white p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <Activity className="w-4 h-4 text-purple-600" />
              <span className="text-sm font-medium text-gray-700">交易次数</span>
            </div>
            <div className="text-lg font-bold text-gray-900">{trading_stats.total_trades}笔</div>
            <div className="text-xs text-gray-600">
              胜率 {formatPercent(performance.win_rate)}
            </div>
          </div>

          <div className="bg-white p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <DollarSign className="w-4 h-4 text-green-600" />
              <span className="text-sm font-medium text-gray-700">总收益</span>
            </div>
            <div className={`text-lg font-bold ${getReturnColor(performance.total_profit)}`}>
              {performance.total_profit >= 0 ? '+' : ''}{formatAmount(performance.total_profit)}
            </div>
            <div className="text-xs text-gray-600">
              收益率 {formatPercent(performance.total_return)}
            </div>
          </div>

          <div className="bg-white p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <TrendingUp className="w-4 h-4 text-orange-600" />
              <span className="text-sm font-medium text-gray-700">年化收益</span>
            </div>
            <div className={`text-lg font-bold ${getReturnColor(performance.annual_return)}`}>
              {performance.annual_return >= 0 ? '+' : ''}{formatPercent(performance.annual_return)}
            </div>
            <div className="text-xs text-gray-600">
              预期年化表现
            </div>
          </div>
        </div>
      </div>

      {/* 详细性能指标 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* 收益指标 */}
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-green-100 rounded-lg">
              <TrendingUp className="w-5 h-5 text-green-600" />
            </div>
            <div>
              <h4 className="font-semibold text-gray-900">收益指标</h4>
              <p className="text-sm text-gray-600">策略盈利能力分析</p>
            </div>
          </div>

          <div className="space-y-4">
            <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span className="text-sm text-gray-700">总收益</span>
              <span className={`font-semibold ${getReturnColor(performance.total_profit)}`}>
                {performance.total_profit >= 0 ? '+' : ''}{formatAmount(performance.total_profit)}
              </span>
            </div>

            <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span className="text-sm text-gray-700">总收益率</span>
              <span className={`font-semibold ${getReturnColor(performance.total_return)}`}>
                {performance.total_return >= 0 ? '+' : ''}{formatPercent(performance.total_return)}
              </span>
            </div>

            <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span className="text-sm text-gray-700">年化收益率</span>
              <span className={`font-semibold ${getReturnColor(performance.annual_return)}`}>
                {performance.annual_return >= 0 ? '+' : ''}{formatPercent(performance.annual_return)}
              </span>
            </div>

            <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span className="text-sm text-gray-700">预期月收益</span>
              <span className={`font-semibold ${getReturnColor(trading_stats.expected_monthly_profit)}`}>
                {trading_stats.expected_monthly_profit >= 0 ? '+' : ''}{formatAmount(trading_stats.expected_monthly_profit)}
              </span>
            </div>
          </div>
        </div>

        {/* 风险指标 */}
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-red-100 rounded-lg">
              <Shield className="w-5 h-5 text-red-600" />
            </div>
            <div>
              <h4 className="font-semibold text-gray-900">风险指标</h4>
              <p className="text-sm text-gray-600">策略风险控制分析</p>
            </div>
          </div>

          <div className="space-y-4">
            <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span className="text-sm text-gray-700">最大回撤</span>
              <span className={`font-semibold ${
                performance.max_drawdown > 0.15 ? 'text-red-600' : 
                performance.max_drawdown > 0.08 ? 'text-yellow-600' : 'text-green-600'
              }`}>
                {formatPercent(performance.max_drawdown)}
              </span>
            </div>

            <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span className="text-sm text-gray-700">交易胜率</span>
              <span className={`font-semibold ${
                performance.win_rate >= 0.7 ? 'text-green-600' : 
                performance.win_rate >= 0.5 ? 'text-yellow-600' : 'text-red-600'
              }`}>
                {formatPercent(performance.win_rate)}
              </span>
            </div>

            <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span className="text-sm text-gray-700">盈利交易</span>
              <span className="font-semibold text-gray-900">
                {trading_stats.profitable_trades}/{trading_stats.total_trades}笔
              </span>
            </div>

            <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
              <span className="text-sm text-gray-700">最终权益</span>
              <span className="font-semibold text-gray-900">
                {formatAmount(final_equity)}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* 交易频次分析 */}
      <div className="bg-white border border-gray-200 rounded-lg p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 bg-purple-100 rounded-lg">
            <Activity className="w-5 h-5 text-purple-600" />
          </div>
          <div>
            <h4 className="font-semibold text-gray-900">交易频次分析</h4>
            <p className="text-sm text-gray-600">预期交易活跃度和收益频率</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <div className="text-2xl font-bold text-blue-600 mb-1">
              {trading_stats.avg_trades_per_day.toFixed(1)}
            </div>
            <div className="text-sm text-blue-700 font-medium">日均交易</div>
            <div className="text-xs text-gray-600 mt-1">次/天</div>
          </div>

          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-2xl font-bold text-green-600 mb-1">
              {trading_stats.expected_monthly_trades.toFixed(1)}
            </div>
            <div className="text-sm text-green-700 font-medium">预期月交易</div>
            <div className="text-xs text-gray-600 mt-1">次/月</div>
          </div>

          <div className="text-center p-4 bg-orange-50 rounded-lg">
            <div className="text-2xl font-bold text-orange-600 mb-1">
              {trading_stats.total_trades}
            </div>
            <div className="text-sm text-orange-700 font-medium">历史总交易</div>
            <div className="text-xs text-gray-600 mt-1">回测期间</div>
          </div>

          <div className="text-center p-4 bg-purple-50 rounded-lg">
            <div className="text-2xl font-bold text-purple-600 mb-1">
              {formatAmount(trading_stats.expected_monthly_profit)}
            </div>
            <div className="text-sm text-purple-700 font-medium">预期月收益</div>
            <div className="text-xs text-gray-600 mt-1">基于历史</div>
          </div>
        </div>
      </div>



      {/* 最近交易记录 */}
      {showDetailed && trades && trades.length > 0 && (
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-gray-100 rounded-lg">
              <BarChart3 className="w-5 h-5 text-gray-600" />
            </div>
            <div>
              <h4 className="font-semibold text-gray-900">最近交易记录</h4>
              <p className="text-sm text-gray-600">回测期间的交易明细（最近10笔）</p>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-2 px-3">日期</th>
                  <th className="text-left py-2 px-3">类型</th>
                  <th className="text-right py-2 px-3">价格</th>
                  <th className="text-right py-2 px-3">数量</th>
                  <th className="text-right py-2 px-3">金额</th>
                  <th className="text-right py-2 px-3">盈亏</th>
                </tr>
              </thead>
              <tbody>
                {trades.map((trade, index) => (
                  <tr key={index} className="border-b border-gray-100">
                    <td className="py-2 px-3">{trade.date}</td>
                    <td className="py-2 px-3">
                      <span className={`px-2 py-1 rounded text-xs ${
                        trade.type === 'buy' 
                          ? 'bg-red-100 text-red-700' 
                          : 'bg-green-100 text-green-700'
                      }`}>
                        {trade.type === 'buy' ? '买入' : '卖出'}
                      </span>
                    </td>
                    <td className="text-right py-2 px-3">¥{trade.price.toFixed(3)}</td>
                    <td className="text-right py-2 px-3">{trade.shares}</td>
                    <td className="text-right py-2 px-3">{formatAmount(trade.amount)}</td>
                    <td className={`text-right py-2 px-3 ${
                      trade.profit > 0 ? 'text-red-600' : 
                      trade.profit < 0 ? 'text-green-600' : 'text-gray-600'
                    }`}>
                      {trade.profit ? 
                        (trade.profit >= 0 ? '+' : '') + formatAmount(trade.profit) : 
                        '-'
                      }
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

    </div>
  );
};

export default BacktestResultCard;
