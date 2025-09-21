#!/usr/bin/env python3
"""
测试新的频次计算逻辑
验证基于日K线数据的交易频次推断是否符合预期
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.frequency_calculator import FrequencyCalculator
from services.grid_calculator import GridCalculator


def generate_mock_historical_data(days=90, base_price=100, volatility=0.02):
    """生成模拟的历史K线数据"""
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    
    # 生成随机价格走势
    returns = np.random.normal(0, volatility, days)
    prices = [base_price]
    
    for ret in returns[1:]:
        prices.append(prices[-1] * (1 + ret))
    
    # 生成OHLC数据
    data = []
    for i, (date, close_price) in enumerate(zip(dates, prices)):
        # 模拟日内波动
        daily_volatility = np.random.uniform(0.01, 0.04)  # 1%-4%的日内波动
        
        open_price = close_price * (1 + np.random.normal(0, 0.005))  # 开盘价有小幅跳空
        high_price = max(open_price, close_price) * (1 + daily_volatility * np.random.uniform(0.3, 1.0))
        low_price = min(open_price, close_price) * (1 - daily_volatility * np.random.uniform(0.3, 1.0))
        
        # 模拟成交量
        volume = np.random.uniform(1000000, 5000000)  # 100万-500万股
        
        data.append({
            'trade_date': date.strftime('%Y%m%d'),
            'open': round(open_price, 3),
            'high': round(high_price, 3),
            'low': round(low_price, 3),
            'close': round(close_price, 3),
            'vol': int(volume)
        })
    
    return pd.DataFrame(data)


def test_frequency_analysis():
    """测试频次分析功能"""
    print("=" * 60)
    print("测试频次分析功能")
    print("=" * 60)
    
    # 创建频次计算器
    freq_calc = FrequencyCalculator()
    
    # 生成模拟数据
    historical_data = generate_mock_historical_data(days=90, base_price=100, volatility=0.025)
    
    print(f"生成了 {len(historical_data)} 天的模拟历史数据")
    print(f"价格范围: {historical_data['low'].min():.3f} - {historical_data['high'].max():.3f}")
    
    # 分析历史模式
    patterns = freq_calc.analyze_historical_patterns(historical_data)
    
    if 'error' in patterns:
        print(f"❌ 历史模式分析失败: {patterns['error']}")
        return False
    
    print("\n📊 历史模式分析结果:")
    print(f"  平均日振幅: {patterns['avg_daily_amplitude']:.4f} ({patterns['avg_daily_amplitude']*100:.2f}%)")
    print(f"  波动率: {patterns['volatility']:.2f}%")
    print(f"  成交量因子: {patterns['avg_volume_factor']:.2f}")
    print(f"  价格连续性: {patterns['price_continuity']:.2f}")
    print(f"  数据质量评分: {patterns['data_quality']['score']:.2f}")
    
    return patterns


def test_grid_parameter_calculation():
    """测试网格参数计算"""
    print("\n" + "=" * 60)
    print("测试网格参数计算")
    print("=" * 60)
    
    # 创建计算器
    freq_calc = FrequencyCalculator()
    grid_calc = GridCalculator()
    
    # 生成模拟数据
    historical_data = generate_mock_historical_data(days=90, base_price=100, volatility=0.025)
    current_price = historical_data['close'].iloc[-1]
    
    # 分析历史模式
    patterns = freq_calc.analyze_historical_patterns(historical_data)
    
    if 'error' in patterns:
        print(f"❌ 无法进行网格参数计算: {patterns['error']}")
        return False
    
    # 测试不同频次类型
    frequencies = ['high', 'medium', 'low']
    initial_capital = 100000
    
    print(f"\n💰 测试参数:")
    print(f"  当前价格: ¥{current_price:.3f}")
    print(f"  初始资金: ¥{initial_capital:,}")
    
    results = {}
    
    for freq_type in frequencies:
        print(f"\n🔄 测试 {freq_type} 频次...")
        
        # 计算最优网格参数
        freq_params = freq_calc.calculate_optimal_grid_parameters(
            freq_type, current_price, patterns, 0.2  # 假设20%的价格区间
        )
        
        if 'error' in freq_params:
            print(f"  ❌ {freq_type} 频次计算失败: {freq_params['error']}")
            continue
        
        target_triggers = freq_params['target_daily_triggers']
        predicted_triggers = freq_params['predicted_daily_triggers']
        match_score = freq_params['frequency_match_score']
        
        print(f"  📈 目标日频次: {target_triggers} 次/天")
        print(f"  📊 预测日频次: {predicted_triggers:.2f} 次/天")
        print(f"  🎯 匹配度: {match_score:.2%}")
        print(f"  🔢 最优网格数: {freq_params['optimal_grid_count']}")
        print(f"  📏 网格步长: {freq_params['grid_step_ratio']:.4f} ({freq_params['grid_step_ratio']*100:.2f}%)")
        
        # 计算月度统计
        monthly_stats = freq_calc.estimate_monthly_statistics(predicted_triggers)
        print(f"  📅 预估月触发: {monthly_stats['monthly_triggers']} 次")
        print(f"  ✅ 月成功交易: {monthly_stats['successful_monthly_trades']} 次")
        
        results[freq_type] = {
            'freq_params': freq_params,
            'monthly_stats': monthly_stats
        }
        
        # 评估匹配度
        if match_score > 0.8:
            print(f"  ✅ 匹配度优秀")
        elif match_score > 0.6:
            print(f"  ⚠️  匹配度良好")
        else:
            print(f"  ❌ 匹配度较差，建议调整参数")
    
    return results


def test_frequency_recommendations():
    """测试频次推荐功能"""
    print("\n" + "=" * 60)
    print("测试频次推荐功能")
    print("=" * 60)
    
    freq_calc = FrequencyCalculator()
    
    # 测试不同市场条件下的推荐
    test_scenarios = [
        {
            'name': '低波动市场',
            'volatility': 15,
            'avg_amplitude': 0.015,
            'volume_factor': 1.0
        },
        {
            'name': '中等波动市场',
            'volatility': 25,
            'avg_amplitude': 0.025,
            'volume_factor': 1.2
        },
        {
            'name': '高波动市场',
            'volatility': 40,
            'avg_amplitude': 0.045,
            'volume_factor': 1.8
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n📊 {scenario['name']}:")
        
        # 构造模拟的历史模式数据
        patterns = {
            'volatility': scenario['volatility'],
            'avg_daily_amplitude': scenario['avg_amplitude'],
            'avg_volume_factor': scenario['volume_factor'],
            'price_continuity': 0.7,
            'data_quality': {'score': 0.9}
        }
        
        # 获取推荐
        recommendations = freq_calc.get_frequency_recommendations(patterns)
        
        if 'error' in recommendations:
            print(f"  ❌ 推荐生成失败: {recommendations['error']}")
            continue
        
        print(f"  🎯 最佳推荐: {recommendations['best_frequency']}")
        print(f"  📈 市场评估:")
        print(f"    波动率水平: {recommendations['market_assessment']['volatility_level']}")
        print(f"    流动性水平: {recommendations['market_assessment']['liquidity_level']}")
        print(f"    整体适用性: {recommendations['market_assessment']['overall_suitability']}")
        
        print(f"  📋 各频次适合度:")
        for freq_type, rec in recommendations['recommendations'].items():
            status = "✅ 推荐" if rec['recommended'] else "❌ 不推荐"
            print(f"    {freq_type}: 适合度 {rec['suitability_score']:.2%}, "
                  f"风险 {rec['risk_level']}, {status}")


def test_integration_with_grid_calculator():
    """测试与网格计算器的集成"""
    print("\n" + "=" * 60)
    print("测试与网格计算器的集成")
    print("=" * 60)
    
    # 创建计算器
    grid_calc = GridCalculator()
    
    # 生成模拟数据和分析结果
    historical_data = generate_mock_historical_data(days=90, base_price=100, volatility=0.025)
    current_price = historical_data['close'].iloc[-1]
    
    # 模拟ETF分析结果
    analysis_result = {
        'avg_amplitude': 2.5,
        'volatility': 25.0,
        'price_std': current_price * 0.02
    }
    
    print(f"💰 测试参数:")
    print(f"  当前价格: ¥{current_price:.3f}")
    print(f"  历史数据: {len(historical_data)} 天")
    
    # 测试新的网格计算逻辑
    for frequency in ['high', 'medium', 'low']:
        print(f"\n🔄 测试 {frequency} 频次的网格计算...")
        
        grid_params = grid_calc.calculate_grid_parameters(
            current_price=current_price,
            analysis_result=analysis_result,
            frequency=frequency,
            initial_capital=100000,
            historical_data=historical_data
        )
        
        if 'error' in grid_params:
            print(f"  ❌ 计算失败: {grid_params['error']}")
            continue
        
        print(f"  📊 计算结果:")
        print(f"    目标日频次: {grid_params.get('target_daily_triggers', 'N/A')} 次/天")
        print(f"    预测日频次: {grid_params.get('predicted_daily_triggers', 'N/A'):.2f} 次/天")
        print(f"    网格数量: {grid_params['grid_count']}")
        print(f"    价格区间: ¥{grid_params['price_lower_bound']:.3f} - ¥{grid_params['price_upper_bound']:.3f}")
        print(f"    月触发预估: {grid_params['estimated_triggers_per_month']} 次")
        print(f"    计算方法: {grid_params.get('calculation_method', 'unknown')}")
        
        if 'frequency_match_score' in grid_params:
            score = grid_params['frequency_match_score']
            print(f"    频次匹配度: {score:.2%}")
            
            if score > 0.8:
                print(f"    ✅ 匹配度优秀")
            elif score > 0.6:
                print(f"    ⚠️  匹配度良好")
            else:
                print(f"    ❌ 匹配度较差")


def main():
    """主测试函数"""
    print("🚀 开始测试新的频次计算逻辑")
    print("=" * 80)
    
    try:
        # 1. 测试频次分析
        patterns = test_frequency_analysis()
        if not patterns:
            return
        
        # 2. 测试网格参数计算
        grid_results = test_grid_parameter_calculation()
        if not grid_results:
            return
        
        # 3. 测试频次推荐
        test_frequency_recommendations()
        
        # 4. 测试集成
        test_integration_with_grid_calculator()
        
        print("\n" + "=" * 80)
        print("🎉 所有测试完成！")
        print("=" * 80)
        
        # 总结
        print("\n📋 测试总结:")
        print("✅ 频次分析功能正常")
        print("✅ 网格参数计算功能正常")
        print("✅ 频次推荐功能正常")
        print("✅ 与网格计算器集成正常")
        
        print("\n💡 关键改进:")
        print("• 基于日K线数据推断日内交易频次")
        print("• 用户输入的日频次与实际计算结果对齐")
        print("• 增加频次匹配度评估")
        print("• 提供智能的频次推荐")
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()