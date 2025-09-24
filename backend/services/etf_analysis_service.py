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
            {'code': '515050', 'name': '5G通信ETF'},
            {'code': '512690', 'name': '酒ETF'},
            {'code': '516160', 'name': '新能源ETF'},
            {'code': '159928', 'name': '消费ETF'},
            {'code': '512170', 'name': '医疗ETF'},
            {'code': '159941', 'name': '纳指ETF'},
            {'code': '513100', 'name': '纳指ETF'},
            {'code': '159920', 'name': '恒生ETF'},
            {'code': '510880', 'name': '红利ETF'},
            {'code': '588000', 'name': '科创50ETF'},
            {'code': '512480', 'name': '半导体ETF'},
            {'code': '159819', 'name': '人工智能ETF'},
            {'code': '159742', 'name': '恒生科技ETF'},
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
                           grid_type: str, risk_preference: str) -> Dict:
        """
        完整的ETF网格交易策略分析
        
        Args:
            etf_code: ETF代码
            total_capital: 总投资资金
            grid_type: 网格类型 ('等差' 或 '等比')
            risk_preference: 风险偏好 ('保守', '稳健', '激进')
            
        Returns:
            完整的策略分析报告
        """
        try:
            logger.info(f"开始ETF策略分析: {etf_code}, 资金{total_capital}, "
                       f"{grid_type}网格, {risk_preference}")
            
            # 1. 获取ETF基础信息
            etf_info = self.get_etf_basic_info(etf_code)
            
            # 2. 获取历史数据（1年）
            df = self.get_historical_data(etf_code, days=365)
            
            # 3. 执性适宜度评估
            suitability_result = self.suitability_analyzer.comprehensive_evaluation(df, etf_info)
            
            # 4. 计算网格策略参数
            atr_analysis = suitability_result['atr_analysis']
            market_indicators = suitability_result['market_indicators']
            
            grid_params = self.grid_strategy.calculate_grid_parameters(
                df=df,
                total_capital=total_capital,
                grid_type=grid_type,
                risk_preference=risk_preference,
                atr_analysis=atr_analysis,
                market_indicators=market_indicators
            )
            
            # 5. 生成策略分析依据
            strategy_rationale = self._generate_strategy_rationale(
                suitability_result, grid_params, risk_preference
            )
            
            # 6. 生成调整建议
            adjustment_suggestions = self._generate_adjustment_suggestions(
                suitability_result, grid_params
            )
            
            # 7. 整合完整报告
            complete_report = {
                'etf_info': etf_info,
                'data_quality': suitability_result['data_quality'],
                'suitability_evaluation': suitability_result,
                'grid_strategy': grid_params,
                'strategy_rationale': strategy_rationale,
                'adjustment_suggestions': adjustment_suggestions,
                'analysis_timestamp': datetime.now().isoformat(),
                'input_parameters': {
                    'etf_code': etf_code,
                    'total_capital': total_capital,
                    'grid_type': grid_type,
                    'risk_preference': risk_preference
                }
            }
            
            logger.info(f"ETF策略分析完成: {etf_code}, 适宜度评分{suitability_result['total_score']}")
            return complete_report
            
        except Exception as e:
            logger.error(f"ETF策略分析失败: {etf_code}, {str(e)}")
            raise
    
    def _generate_strategy_rationale(self, suitability_result: Dict, 
                                   grid_params: Dict, risk_preference: str) -> Dict:
        """
        生成策略分析依据
        
        Args:
            suitability_result: 适宜度评估结果
            grid_params: 网格参数
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
                'grid_count': f"基于ATR智能步长算法设定{grid_params['grid_config']['count']}个网格",
                'fund_allocation': f"底仓比例{grid_params['fund_allocation']['base_position_ratio']:.1%}，"
                                 f"考虑ATR波动、ADX趋势和波动率调整",
                'grid_type': f"{grid_params['grid_config']['type']}网格更适合当前市场特征"
            }
            
            # 收益预测依据
            profit_basis = {
                'parameter_optimization': "基于ATR算法和历史波动率分析",
                'trading_frequency': "根据网格密度和历史波动特征预估",
                'risk_control': "基于ATR波动率和市场趋势指标设定",
                'fund_allocation': "智能资金分配确保风险可控"
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
                                       grid_params: Dict) -> Dict:
        """
        生成调整建议
        
        Args:
            suitability_result: 适宜度评估结果
            grid_params: 网格参数
            
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
            if volatility > 0.4:
                suggestions['risk_control'].append(
                    "波动率较高，建议增加底仓比例或设置止损线"
                )
            
            # 收益增强建议
            grid_count = grid_params['grid_config']['count']
            if grid_count < 20:
                suggestions['profit_enhancement'].append(
                    "网格数量较少，可考虑增加网格密度提高交易机会"
                )
            
            # 资金效率建议
            grid_fund_utilization_rate = grid_params['fund_allocation']['grid_fund_utilization_rate']
            if grid_fund_utilization_rate < 0.8:
                suggestions['profit_enhancement'].append(
                    f"网格资金利用率{grid_fund_utilization_rate:.1%}偏低，可考虑调整网格配置"
                )
            
            return suggestions
            
        except Exception as e:
            logger.error(f"生成调整建议失败: {str(e)}")
            return {}
    
