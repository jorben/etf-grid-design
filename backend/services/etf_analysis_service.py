"""
ETF分析服务
整合所有分析模块，提供完整的ETF网格交易策略分析
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging
from datetime import datetime, timedelta
import json

from .data_service import DataService
from .atr_engine import ATREngine
from .suitability_analyzer import SuitabilityAnalyzer
from .grid_strategy import GridStrategy
from .backtest_engine import run_grid_backtest

logger = logging.getLogger(__name__)

class ETFAnalysisService:
    """ETF分析服务主类"""
    
    def __init__(self):
        """初始化分析服务"""
        self.data_service = DataService()
        self.atr_engine = ATREngine()
        self.suitability_analyzer = SuitabilityAnalyzer()
        self.grid_strategy = GridStrategy()
        self.cache = {}  # 简单内存缓存
        
        # 热门ETF列表
        self.popular_etfs = [
            {'code': '510300', 'name': '沪深300ETF'},
            {'code': '510500', 'name': '中证500ETF'},
            {'code': '159919', 'name': '沪深300ETF'},
            {'code': '159915', 'name': '创业板ETF'},
            {'code': '512880', 'name': '证券ETF'},
            {'code': '515050', 'name': '5GETF'},
            {'code': '512690', 'name': '酒ETF'},
            {'code': '516160', 'name': '新能源ETF'},
            {'code': '159928', 'name': '消费ETF'},
            {'code': '512170', 'name': '医疗ETF'},
            {'code': '159941', 'name': '纳斯达克100ETF'},
            {'code': '513100', 'name': '纳斯达克ETF'},
            {'code': '159920', 'name': '恒生ETF'},
            {'code': '510880', 'name': '红利ETF'},
            {'code': '159949', 'name': '创业板50ETF'}
        ]
    
    def get_popular_etfs(self) -> List[Dict]:
        """获取热门ETF列表"""
        return self.popular_etfs
    
    def get_etf_basic_info(self, etf_code: str) -> Dict:
        """
        获取ETF基础信息
        
        Args:
            etf_code: ETF代码
            
        Returns:
            ETF基础信息
        """
        try:
            # 尝试从缓存获取
            cache_key = f"etf_basic_{etf_code}"
            if cache_key in self.cache:
                logger.info(f"从缓存获取ETF基础信息: {etf_code}")
                return self.cache[cache_key]
            
            # 获取基础信息
            basic_info = self.data_service.get_fund_basic(etf_code)
            if not basic_info:
                raise ValueError(f"未找到ETF代码: {etf_code}")
            
            # 获取实时行情
            current_data = self.data_service.get_current_price(etf_code)
            
            # 整合信息
            etf_info = {
                'code': etf_code,
                'name': basic_info.get('name', '未知'),
                'management_company': basic_info.get('management', '未知'),
                'current_price': current_data.get('close', 0),
                'change_pct': current_data.get('pct_chg', 0),
                'volume': current_data.get('vol', 0),
                'amount': current_data.get('amount', 0),
                'setup_date': basic_info.get('setup_date', ''),
                'list_date': basic_info.get('list_date', ''),
                'fund_type': basic_info.get('fund_type', 'ETF'),
                'status': basic_info.get('status', 'L')
            }
            
            # 缓存结果
            self.cache[cache_key] = etf_info
            
            logger.info(f"获取ETF基础信息成功: {etf_code} - {etf_info['name']}")
            return etf_info
            
        except Exception as e:
            logger.error(f"获取ETF基础信息失败: {etf_code}, {str(e)}")
            raise
    
    def get_historical_data(self, etf_code: str, days: int = 365) -> pd.DataFrame:
        """
        获取历史数据
        
        Args:
            etf_code: ETF代码
            days: 获取天数
            
        Returns:
            历史数据DataFrame
        """
        try:
            # 计算日期范围
            end_date = datetime.now().strftime('%Y%m%d')
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
            
            # 尝试从缓存获取
            cache_key = f"etf_daily_{etf_code}_{start_date}_{end_date}"
            if cache_key in self.cache:
                logger.info(f"从缓存获取历史数据: {etf_code}")
                return pd.DataFrame(self.cache[cache_key])
            
            # 获取历史数据
            df = self.data_service.get_daily_data(etf_code, start_date, end_date)
            if df is None or len(df) == 0:
                raise ValueError(f"未获取到历史数据: {etf_code}")
            
            # 数据清洗和验证
            df = df.dropna()
            df = df.sort_values('date')
            
            if len(df) < 30:
                logger.warning(f"历史数据不足30天: {etf_code}, 实际{len(df)}天")
            
            # 缓存结果
            self.cache[cache_key] = df.to_dict('records')
            
            logger.info(f"获取历史数据成功: {etf_code}, {len(df)}条记录")
            return df
            
        except Exception as e:
            logger.error(f"获取历史数据失败: {etf_code}, {str(e)}")
            raise
    
    def analyze_etf_strategy(self, etf_code: str, total_capital: float,
                           grid_type: str, frequency_preference: str,
                           risk_preference: str) -> Dict:
        """
        完整的ETF网格交易策略分析
        
        Args:
            etf_code: ETF代码
            total_capital: 总投资资金
            grid_type: 网格类型 ('等差' 或 '等比')
            frequency_preference: 频率偏好 ('低频', '中频', '高频')
            risk_preference: 风险偏好 ('保守', '稳健', '激进')
            
        Returns:
            完整的策略分析报告
        """
        try:
            logger.info(f"开始ETF策略分析: {etf_code}, 资金{total_capital}, "
                       f"{grid_type}网格, {frequency_preference}, {risk_preference}")
            
            # 1. 获取ETF基础信息
            etf_info = self.get_etf_basic_info(etf_code)
            
            # 2. 获取历史数据（1年）
            df = self.get_historical_data(etf_code, days=365)
            
            # 3. 执行适合度评估
            suitability_result = self.suitability_analyzer.comprehensive_evaluation(df, etf_info)
            
            # 4. 计算网格策略参数
            atr_analysis = suitability_result['atr_analysis']
            market_indicators = suitability_result['market_indicators']
            
            grid_params = self.grid_strategy.calculate_grid_parameters(
                df=df,
                total_capital=total_capital,
                grid_type=grid_type,
                frequency_preference=frequency_preference,
                risk_preference=risk_preference,
                atr_analysis=atr_analysis,
                market_indicators=market_indicators
            )
            
            # 5. 执行简化回测
            # 构建回测所需的网格水平数据
            grid_levels = []
            price_levels = grid_params['price_levels']
            grid_funds = grid_params['fund_allocation']['grid_funds']
            
            # 使用价格水平和资金分配信息构建网格数据
            for i, price in enumerate(price_levels[:-1]):  # 排除最高价格点
                if i < len(grid_funds):
                    fund_info = grid_funds[i]
                    grid_levels.append({
                        'price': price,
                        'allocated_fund': fund_info.get('allocated_fund', fund_info.get('actual_fund', 1000)),
                        'shares': fund_info.get('shares', 100)
                    })
            
            logger.info(f"构建grid_levels完成，数量: {len(grid_levels)}")
            
            backtest_result = run_grid_backtest(
                price_data=df,
                initial_capital=total_capital,
                grid_levels=grid_levels,
                base_position_ratio=grid_params['fund_allocation']['base_position_ratio']
            )
            
            # 6. 生成策略分析依据
            strategy_rationale = self._generate_strategy_rationale(
                suitability_result, grid_params, backtest_result, risk_preference
            )
            
            # 7. 生成调整建议
            adjustment_suggestions = self._generate_adjustment_suggestions(
                suitability_result, grid_params, backtest_result
            )
            
            # 8. 整合完整报告
            complete_report = {
                'etf_info': etf_info,
                'data_quality': suitability_result['data_quality'],
                'suitability_evaluation': suitability_result,
                'grid_strategy': grid_params,
                'backtest_result': backtest_result,
                'strategy_rationale': strategy_rationale,
                'adjustment_suggestions': adjustment_suggestions,
                'analysis_timestamp': datetime.now().isoformat(),
                'input_parameters': {
                    'etf_code': etf_code,
                    'total_capital': total_capital,
                    'grid_type': grid_type,
                    'frequency_preference': frequency_preference,
                    'risk_preference': risk_preference
                }
            }
            
            logger.info(f"ETF策略分析完成: {etf_code}, 适合度评分{suitability_result['total_score']}")
            return complete_report
            
        except Exception as e:
            logger.error(f"ETF策略分析失败: {etf_code}, {str(e)}")
            raise
    
    def _generate_strategy_rationale(self, suitability_result: Dict, 
                                   grid_params: Dict, backtest_result: Dict,
                                   risk_preference: str) -> Dict:
        """
        生成策略分析依据
        
        Args:
            suitability_result: 适合度评估结果
            grid_params: 网格参数
            backtest_result: 回测结果
            risk_preference: 风险偏好
            
        Returns:
            策略分析依据
        """
        try:
            atr_analysis = suitability_result['atr_analysis']
            market_indicators = suitability_result['market_indicators']
            
            # ATR算法优势说明
            atr_advantages = [
                "考虑跳空因素，比传统日振幅更准确",
                "动态适应市场波动特征，避免静态统计方法的滞后性",
                "标准化处理，便于不同标的间的比较",
                "能够捕捉市场波动模式的变化"
            ]
            
            # 参数选择逻辑
            parameter_logic = {
                'price_range': f"基于ATR比率{atr_analysis['current_atr_pct']:.2f}%和{risk_preference}风险偏好计算",
                'grid_count': f"根据{grid_params['frequency_preference']}交易频率设定{grid_params['grid_config']['count']}个网格",
                'fund_allocation': f"底仓比例{grid_params['fund_allocation']['base_position_ratio']:.1%}，"
                                 f"考虑ATR波动、ADX趋势和波动率调整",
                'grid_type': f"{grid_params['grid_config']['type']}网格更适合当前市场特征"
            }
            
            # 收益预测依据
            profit_basis = {
                'historical_performance': f"基于{backtest_result['backtest_period']['total_days']}天回测数据",
                'trading_frequency': f"预期月交易{backtest_result['trading_stats']['expected_monthly_trades']:.1f}次",
                'win_rate': f"历史胜率{backtest_result['performance']['win_rate']:.1%}",
                'risk_control': f"最大回撤预估{backtest_result['performance']['max_drawdown']:.1%}"
            }
            
            return {
                'atr_advantages': atr_advantages,
                'parameter_logic': parameter_logic,
                'profit_basis': profit_basis,
                'market_environment': {
                    'volatility': f"年化波动率{market_indicators['volatility']:.1%}",
                    'trend_characteristic': suitability_result['evaluations']['market_characteristics']['market_type'],
                    'liquidity': suitability_result['evaluations']['liquidity']['level']
                }
            }
            
        except Exception as e:
            logger.error(f"生成策略分析依据失败: {str(e)}")
            return {}
    
    def _generate_adjustment_suggestions(self, suitability_result: Dict,
                                       grid_params: Dict, backtest_result: Dict) -> Dict:
        """
        生成调整建议
        
        Args:
            suitability_result: 适合度评估结果
            grid_params: 网格参数
            backtest_result: 回测结果
            
        Returns:
            调整建议
        """
        try:
            suggestions = {
                'market_environment_changes': [],
                'parameter_optimization': [],
                'risk_control': [],
                'profit_enhancement': []
            }
            
            # 市场环境变化应对
            adx_value = suitability_result['market_indicators']['adx_value']
            if adx_value > 25:
                suggestions['market_environment_changes'].append(
                    "当前处于强趋势环境，建议增加底仓比例，减少网格交易频率"
                )
            elif adx_value < 15:
                suggestions['market_environment_changes'].append(
                    "震荡特征明显，可适当增加网格密度，提高交易频率"
                )
            
            # 参数优化建议
            volatility = suitability_result['market_indicators']['volatility']
            if volatility > 0.4:
                suggestions['parameter_optimization'].append(
                    "波动率较高，建议扩大网格间距，降低交易频率"
                )
            elif volatility < 0.15:
                suggestions['parameter_optimization'].append(
                    "波动率较低，可适当缩小网格间距，增加交易机会"
                )
            
            # 风险控制建议
            max_drawdown = backtest_result['performance']['max_drawdown']
            if max_drawdown > 0.15:
                suggestions['risk_control'].append(
                    "历史最大回撤较大，建议增加底仓比例或设置止损线"
                )
            
            # 收益增强建议
            win_rate = backtest_result['performance']['win_rate']
            if win_rate < 0.6:
                suggestions['profit_enhancement'].append(
                    "胜率偏低，建议优化网格间距或调整交易频率"
                )
            
            # 资金效率建议
            utilization_rate = grid_params['fund_allocation']['utilization_rate']
            if utilization_rate < 0.8:
                suggestions['profit_enhancement'].append(
                    f"资金利用率{utilization_rate:.1%}偏低，可考虑调整网格配置"
                )
            
            return suggestions
            
        except Exception as e:
            logger.error(f"生成调整建议失败: {str(e)}")
            return {}
    
    def generate_report_summary(self, analysis_result: Dict) -> str:
        """
        生成报告摘要文本
        
        Args:
            analysis_result: 分析结果
            
        Returns:
            报告摘要
        """
        try:
            etf_info = analysis_result['etf_info']
            suitability = analysis_result['suitability_evaluation']
            grid_strategy = analysis_result['grid_strategy']
            backtest = analysis_result['backtest_result']
            
            summary = f"""
ETF网格交易策略分析报告: {etf_info['code']} {etf_info['name']}

第一部分：ETF基础信息与数据质量
├── 基本信息: {etf_info['code']} {etf_info['name']} ({etf_info['management_company']})
├── 当前价格: ¥{etf_info['current_price']:.3f} ({etf_info['change_pct']:+.2f}%)
├── 市场表现: 成交量{etf_info['volume']:.0f}万手，成交额{etf_info['amount']:.0f}万元
└── 数据质量: {analysis_result['data_quality']['freshness']}，{analysis_result['data_quality']['completeness']}

第二部分：标的适合度评估 (总分{suitability['total_score']}/100分)
├── 振幅评估: {suitability['evaluations']['amplitude']['score']}/35分 - {suitability['evaluations']['amplitude']['description']}
├── 波动率评估: {suitability['evaluations']['volatility']['score']}/30分 - {suitability['evaluations']['volatility']['description']}
├── 市场特征评估: {suitability['evaluations']['market_characteristics']['score']}/25分 - {suitability['evaluations']['market_characteristics']['description']}
├── 流动性评估: {suitability['evaluations']['liquidity']['score']}/10分 - {suitability['evaluations']['liquidity']['description']}
└── 综合结论: 该标的{suitability['conclusion']}执行网格交易策略

第三部分：为您定制的网格策略 (基于ATR算法)
├── 目标设置: {grid_strategy['risk_preference']}风险偏好，总投资资金¥{analysis_result['input_parameters']['total_capital']:,.0f}
├── 价格区间: ¥{grid_strategy['price_range']['lower']:.3f} - ¥{grid_strategy['price_range']['upper']:.3f} (区间比例{grid_strategy['price_range']['ratio']:.1%})
├── 网格配置: {grid_strategy['grid_config']['count']}个网格，{grid_strategy['grid_config']['type']}类型
├── 网格步长: ¥{grid_strategy['grid_config']['step_size']:.3f} (步长比例{grid_strategy['grid_config']['step_ratio']:.1%})
├── 资金分配: 底仓¥{grid_strategy['fund_allocation']['base_position_amount']:,.0f}，网格资金¥{grid_strategy['fund_allocation']['grid_trading_amount']:,.0f}
└── 资金利用: 预期最大持仓¥{grid_strategy['fund_allocation']['total_actual_fund']:,.0f}，资金利用率{grid_strategy['fund_allocation']['utilization_rate']:.1%}

第四部分：历史回测表现与收益预测
├── 回测时间段: {backtest['backtest_period']['start_date']} 至 {backtest['backtest_period']['end_date']} ({backtest['backtest_period']['total_days']}天)
├── 交易频次: 预期月交易{backtest['trading_stats']['expected_monthly_trades']:.1f}次
├── 收益预测: 预期月收益¥{backtest['trading_stats']['expected_monthly_profit']:,.0f} (年化收益率{backtest['performance']['annual_return']:.1%})
├── 风险指标: 最大回撤{backtest['performance']['max_drawdown']:.1%}，胜率{backtest['performance']['win_rate']:.1%}
└── 总收益: 回测期间总收益¥{backtest['performance']['total_profit']:,.0f}

第五部分：策略分析依据与调整建议
├── ATR算法优势: 动态适应市场波动，考虑跳空因素
├── 参数选择逻辑: 基于ATR比率{suitability['atr_analysis']['current_atr_pct']:.2f}%和{grid_strategy['risk_preference']}风险偏好匹配
├── 市场环境: 年化波动率{suitability['market_indicators']['volatility']:.1%}，{suitability['evaluations']['market_characteristics']['market_type']}特征
└── 风险控制: {suitability['recommendation']}

第六部分：重要声明
└── 免责声明: {backtest['disclaimer']}，本分析仅供参考，不构成投资建议，投资有风险
            """.strip()
            
            return summary
            
        except Exception as e:
            logger.error(f"生成报告摘要失败: {str(e)}")
            return "报告摘要生成失败"