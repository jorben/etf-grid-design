import React, { useState, useEffect } from 'react';
import { Search, TrendingUp, DollarSign, Settings, Shield, BarChart3, Grid3X3 } from 'lucide-react';
import { usePersistedState } from '../hooks/usePersistedState';
import ETFInfoSkeleton from './ETFInfoSkeleton';

const ParameterForm = ({ onAnalysis, loading }) => {
  // 使用持久化状态
  const [etfCode, setEtfCode] = usePersistedState('etfCode', '510300');
  const [totalCapital, setTotalCapital] = usePersistedState('totalCapital', '100000');
  const [gridType, setGridType] = usePersistedState('gridType', '等比');
  const [frequencyPreference, setFrequencyPreference] = usePersistedState('frequencyPreference', '中频');
  const [riskPreference, setRiskPreference] = usePersistedState('riskPreference', '稳健');

  // 状态管理
  const [popularETFs, setPopularETFs] = useState([]);
  const [capitalPresets, setCapitalPresets] = useState([]);
  const [etfInfo, setEtfInfo] = useState(null);
  const [etfLoading, setEtfLoading] = useState(false);
  const [errors, setErrors] = useState({});

  // 获取热门ETF列表
  useEffect(() => {
    fetch('/api/popular-etfs')
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          setPopularETFs(data.data);
        }
      })
      .catch(err => console.error('获取热门ETF失败:', err));
  }, []);



  // 获取资金预设
  useEffect(() => {
    fetch('/api/capital-presets')
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          setCapitalPresets(data.data);
        }
      })
      .catch(err => console.error('获取资金预设失败:', err));
  }, []);

  // ETF代码变化时获取基础信息
  useEffect(() => {
    if (etfCode && etfCode.length === 6) {
      setEtfLoading(true);
      setEtfInfo(null);
      
      fetch(`/api/etf/basic-info/${etfCode}`)
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            setEtfInfo(data.data);
            setErrors(prev => ({ ...prev, etfCode: '' }));
          } else {
            setEtfInfo(null);
            setErrors(prev => ({ ...prev, etfCode: data.error }));
          }
        })
        .catch(err => {
          setEtfInfo(null);
          setErrors(prev => ({ ...prev, etfCode: '获取ETF信息失败' }));
        })
        .finally(() => {
          setEtfLoading(false);
        });
    } else {
      setEtfInfo(null);
      setEtfLoading(false);
    }
  }, [etfCode]);

  // 表单验证
  const validateForm = () => {
    const newErrors = {};

    if (!etfCode || etfCode.length !== 6 || !/^\d{6}$/.test(etfCode)) {
      newErrors.etfCode = '请输入6位数字ETF代码';
    }

    const capital = parseFloat(totalCapital);
    if (!totalCapital || isNaN(capital) || capital < 100000 || capital > 5000000) {
      newErrors.totalCapital = '投资金额应在10万-500万之间';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // 提交表单
  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateForm()) {
      onAnalysis({
        etfCode,
        totalCapital: parseFloat(totalCapital),
        gridType,
        frequencyPreference,
        riskPreference
      });
    }
  };



  // 选择热门ETF
  const selectPopularETF = (code) => {
    setEtfCode(code);
  };

  // 选择预设资金
  const selectCapitalPreset = (amount) => {
    setTotalCapital(amount.toString());
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 bg-blue-100 rounded-lg">
          <Settings className="w-6 h-6 text-blue-600" />
        </div>
        <div>
          <h2 className="text-xl font-bold text-gray-900">策略参数设置</h2>
          <p className="text-sm text-gray-600">请填写您的投资偏好，系统将为您量身定制网格交易策略</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* ETF标的选择 */}
        <div>
          <div className="flex justify-between items-center mb-3">
            <label className="flex items-center gap-2 text-sm font-medium text-gray-700">
              <Search className="w-4 h-4" />
              ETF标的选择
            </label>
            
            {/* 热门ETF - 靠右对齐 */}
            <div className="flex items-center">
              <span className="text-xs text-gray-500 mr-2">热门ETF：</span>
              <div className="flex flex-wrap gap-2">
                {['510300', '510500', '159915', '588000', '512480', '159819'].map(code => {
                  const etf = popularETFs.find(e => e.code === code);
                  return (
                    <button
                      key={code}
                      type="button"
                      onClick={() => selectPopularETF(code)}
                      className={`px-3 py-1 text-xs rounded-full border transition-colors ${
                        etfCode === code
                          ? 'bg-blue-100 border-blue-300 text-blue-700'
                          : 'bg-gray-50 border-gray-200 text-gray-600 hover:bg-gray-100'
                      }`}
                    >
                      {code} {etf?.name || ''}
                    </button>
                  );
                })}
              </div>
            </div>
          </div>

          <div className="relative">
            <input
              type="text"
              value={etfCode}
              onChange={(e) => setEtfCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
              placeholder="请输入6位ETF代码，如：510300"
              className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                errors.etfCode ? 'border-red-300' : 'border-gray-300'
              }`}
              maxLength={6}
            />
            
            {/* ETF信息区域 - 固定高度避免跳动 */}
            <div className="mt-2" style={{ minHeight: '80px' }}>
              {etfLoading && <ETFInfoSkeleton />}
              
              {!etfLoading && etfInfo && (
                <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
                  <div className="flex items-center gap-2">
                    <TrendingUp className="w-4 h-4 text-blue-600" />
                    <span className="font-medium text-blue-800">{etfInfo.name}</span>
                    <span className="text-sm text-blue-600">
                      ¥{etfInfo.current_price?.toFixed(3)} 
                      <span className={etfInfo.change_pct >= 0 ? 'text-red-600' : 'text-green-600'}>
                        ({etfInfo.change_pct >= 0 ? '+' : ''}{etfInfo.change_pct?.toFixed(2)}%)
                      </span>
                    </span>
                  </div>
                  <p className="text-xs text-blue-600 mt-1">{etfInfo.management_company}</p>
                </div>
              )}
              
              {!etfLoading && errors.etfCode && (
                <p className="mt-1 text-sm text-red-600">{errors.etfCode}</p>
              )}
            </div>
          </div>
        </div>

        {/* 总投资资金量 */}
        <div>
          {/* 标题和常用金额 - 响应式布局 */}
          <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3 mb-3">
            <label className="flex items-center gap-2 text-sm font-medium text-gray-700">
              <DollarSign className="w-4 h-4" />
              总投资资金量
            </label>
            
            {/* 常用金额 - 在小屏幕上换行，大屏幕上靠右对齐 */}
            <div className="flex items-center">
              <span className="text-xs text-gray-500 mr-2">常用金额:</span>
              <div className="flex flex-wrap gap-2">
                {capitalPresets.filter(preset => preset.popular).map(preset => (
                  <button
                    key={preset.value}
                    type="button"
                    onClick={() => selectCapitalPreset(preset.value)}
                    className={`px-2 py-1 text-xs rounded-full border transition-colors ${
                      totalCapital === preset.value.toString()
                        ? 'bg-blue-100 border-blue-300 text-blue-700'
                        : 'bg-gray-50 border-gray-200 text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    {preset.label}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="relative">
            <input
              type="number"
              value={totalCapital}
              onChange={(e) => setTotalCapital(e.target.value)}
              placeholder="请输入投资金额（10万-500万）"
              className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                errors.totalCapital ? 'border-red-300' : 'border-gray-300'
              }`}
              min={100000}
              max={5000000}
              step={10000}
            />
            <div className="absolute right-3 top-3 text-gray-400">
              元
            </div>
            {errors.totalCapital && (
              <p className="mt-1 text-sm text-red-600">{errors.totalCapital}</p>
            )}
          </div>
        </div>

        {/* 开始分析按钮 */}
        <div className="pt-2">
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-4 px-6 rounded-lg font-medium hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? (
              <div className="flex items-center justify-center gap-2">
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                正在分析策略...
              </div>
            ) : (
              '开始分析策略'
            )}
          </button>
        </div>

        {/* 分隔线 */}
        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-300"></div>
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-2 bg-white text-gray-500">更多设置</span>
          </div>
        </div>

        {/* 网格间距类型 */}
        <div>
          <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-3">
            <Grid3X3 className="w-4 h-4" />
            网格间距类型
          </label>
          <div className="grid grid-cols-2 gap-3">
            {[
              { value: '等比', label: '等比网格', desc: '比例间距相等，推荐使用' },
              { value: '等差', label: '等差网格', desc: '价格间距相等，适合新手' }
            ].map(option => (
              <label
                key={option.value}
                className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                  gridType === option.value
                    ? 'border-blue-300 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <input
                  type="radio"
                  name="gridType"
                  value={option.value}
                  checked={gridType === option.value}
                  onChange={(e) => setGridType(e.target.value)}
                  className="sr-only"
                />
                <div className="font-medium text-gray-900">{option.label}</div>
                <div className="text-sm text-gray-600">{option.desc}</div>
              </label>
            ))}
          </div>
        </div>

        {/* 交易频率偏好 */}
        <div>
          <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-3">
            <BarChart3 className="w-4 h-4" />
            交易频率偏好
          </label>
          <div className="grid grid-cols-3 gap-3">
            {[
              { value: '低频', label: '低频交易', desc: '20-30个网格', color: 'green' },
              { value: '中频', label: '中频交易', desc: '40-60个网格', color: 'blue' },
              { value: '高频', label: '高频交易', desc: '80-100个网格', color: 'orange' }
            ].map(option => (
              <label
                key={option.value}
                className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                  frequencyPreference === option.value
                    ? `border-${option.color}-300 bg-${option.color}-50`
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <input
                  type="radio"
                  name="frequencyPreference"
                  value={option.value}
                  checked={frequencyPreference === option.value}
                  onChange={(e) => setFrequencyPreference(e.target.value)}
                  className="sr-only"
                />
                <div className="font-medium text-gray-900">{option.label}</div>
                <div className="text-sm text-gray-600">{option.desc}</div>
              </label>
            ))}
          </div>
        </div>

        {/* 风险偏好 */}
        <div>
          <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-3">
            <Shield className="w-4 h-4" />
            风险偏好
          </label>
          <div className="grid grid-cols-3 gap-3">
            {[
              { value: '保守', label: '保守型', desc: '风险较低，收益稳定', color: 'green' },
              { value: '稳健', label: '稳健型', desc: '平衡风险收益', color: 'blue' },
              { value: '激进', label: '激进型', desc: '追求高收益', color: 'red' }
            ].map(option => (
              <label
                key={option.value}
                className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                  riskPreference === option.value
                    ? `border-${option.color}-300 bg-${option.color}-50`
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <input
                  type="radio"
                  name="riskPreference"
                  value={option.value}
                  checked={riskPreference === option.value}
                  onChange={(e) => setRiskPreference(e.target.value)}
                  className="sr-only"
                />
                <div className="font-medium text-gray-900">{option.label}</div>
                <div className="text-sm text-gray-600">{option.desc}</div>
              </label>
            ))}
          </div>
        </div>


      </form>
    </div>
  );
};

export default ParameterForm;