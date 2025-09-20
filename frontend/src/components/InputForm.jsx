import React, { useState } from 'react'
import { Search, DollarSign, Zap, Info } from 'lucide-react'
import { popularETFsWithNames, getETFName, extractETFCode } from '../config/etfNames'

const InputForm = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    etf_code: '',
    frequency: 'medium',
    initial_capital: '100000'
  })
  
  const [errors, setErrors] = useState({})
  const [isSubmitting, setIsSubmitting] = useState(false)

  const validateForm = () => {
    const newErrors = {}
    
    // 验证ETF代码
    if (!formData.etf_code.trim()) {
      newErrors.etf_code = '请输入ETF代码'
    } else if (!/^\d{6}$/.test(formData.etf_code.trim())) {
      newErrors.etf_code = 'ETF代码应为6位数字'
    }
    
    // 验证初始资金
    const capital = parseFloat(formData.initial_capital)
    if (!formData.initial_capital || isNaN(capital)) {
      newErrors.initial_capital = '请输入有效的资金数额'
    } else if (capital < 10000) {
      newErrors.initial_capital = '初始资金应不少于1万元'
    } else if (capital > 10000000) {
      newErrors.initial_capital = '初始资金不能超过1000万元'
    }
    
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleInputChange = (e) => {
    const { name, value } = e.target
    
    // 如果是ETF代码输入，提取纯数字编号
    let processedValue = value
    if (name === 'etf_code') {
      processedValue = extractETFCode(value)
    }
    
    setFormData(prev => ({
      ...prev,
      [name]: processedValue
    }))
    
    // 清除对应字段的错误
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }))
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!validateForm()) {
      return
    }
    
    setIsSubmitting(true)
    
    try {
      await onSubmit({
        etf_code: formData.etf_code.trim(),
        frequency: formData.frequency,
        initial_capital: parseFloat(formData.initial_capital)
      })
    } catch (error) {
      console.error('提交失败:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  const frequencyOptions = [
    { value: 'high', label: '高频', description: '约8次买卖/天', icon: Zap },
    { value: 'medium', label: '中频', description: '约4次买卖/天', icon: Zap },
    { value: 'low', label: '低频', description: '约1次买卖/天', icon: Zap }
  ]


  return (
    <div className="card">
      <div className="card-header">
        <h3 className="card-title">策略参数设置</h3>
        <div className="flex items-center text-sm text-gray-500">
          <Info className="w-4 h-4 mr-1" />
          请填写以下参数以生成网格交易策略
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* ETF代码输入 */}
        <div>
          <label htmlFor="etf_code" className="label">
            ETF代码
          </label>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              id="etf_code"
              name="etf_code"
              value={formData.etf_code}
              onChange={handleInputChange}
              placeholder="请输入6位ETF代码，如：510300"
              className={`input pl-10 ${errors.etf_code ? 'border-danger-500' : ''}`}
              maxLength="6"
            />
          </div>
          {errors.etf_code && (
            <p className="mt-1 text-sm text-danger-600">{errors.etf_code}</p>
          )}
          {/* 显示ETF名称 */}
          {formData.etf_code && formData.etf_code.length === 6 && !errors.etf_code && (
            <p className="mt-1 text-sm text-success-600">
              {getETFName(formData.etf_code)}
            </p>
          )}
          
          {/* ETF输入框下方的按钮 - 放在热门ETF列表上方 */}
          <div className="flex justify-center space-x-4 pt-4 pb-3">
            <button
              type="button"
              onClick={() => {
                setFormData({
                  etf_code: '',
                  frequency: 'medium',
                  initial_capital: '100000'
                })
                setErrors({})
              }}
              className="btn-secondary"
            >
              重置
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="btn-primary"
            >
              {isSubmitting ? (
                <>
                  <div className="loading-spinner mr-2"></div>
                  分析中...
                </>
              ) : (
                '开始分析'
              )}
            </button>
          </div>
          
          <div className="mt-2">
            <p className="text-xs text-gray-500 mb-2">热门ETF：</p>
            <div className="flex flex-wrap gap-2">
              {popularETFsWithNames.map(etf => (
                <button
                  key={etf.code}
                  type="button"
                  onClick={() => handleInputChange({ target: { name: 'etf_code', value: etf.code } })}
                  className={`px-2 py-1 text-xs rounded border transition-colors ${
                    formData.etf_code === etf.code
                      ? 'bg-primary-100 border-primary-300 text-primary-700'
                      : 'bg-gray-50 border-gray-200 text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  {etf.code} {etf.name}
                </button>
              ))}
            </div>
          </div>
          
          {/* 分割线和更多设置标题 */}
          <div className="relative flex items-center justify-center mt-6 mb-4">
            <div className="flex-grow border-t border-gray-300"></div>
            <span className="mx-4 text-sm text-gray-500 bg-white px-2">更多设置</span>
            <div className="flex-grow border-t border-gray-300"></div>
          </div>
        </div>

        {/* 交易频率选择 */}
        <div>
          <label className="label">交易频率</label>
          <div className="grid grid-cols-1 gap-3">
            {frequencyOptions.map(option => {
              const Icon = option.icon
              return (
                <label
                  key={option.value}
                  className={`relative flex items-center p-4 border rounded-lg cursor-pointer transition-all ${
                    formData.frequency === option.value
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <input
                    type="radio"
                    name="frequency"
                    value={option.value}
                    checked={formData.frequency === option.value}
                    onChange={handleInputChange}
                    className="sr-only"
                  />
                  <div className="flex items-center flex-1">
                    <Icon className={`w-5 h-5 mr-3 ${
                      formData.frequency === option.value ? 'text-primary-600' : 'text-gray-400'
                    }`} />
                    <div>
                      <div className={`font-medium ${
                        formData.frequency === option.value ? 'text-primary-900' : 'text-gray-900'
                      }`}>
                        {option.label}
                      </div>
                      <div className="text-sm text-gray-500">{option.description}</div>
                    </div>
                  </div>
                  {formData.frequency === option.value && (
                    <div className="w-5 h-5 rounded-full bg-primary-600 flex items-center justify-center">
                      <div className="w-2 h-2 bg-white rounded-full"></div>
                    </div>
                  )}
                </label>
              )
            })}
          </div>
        </div>

        {/* 初始资金输入 */}
        <div>
          <label htmlFor="initial_capital" className="label">
            初始资金（元）
          </label>
          <div className="relative">
            <DollarSign className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="number"
              id="initial_capital"
              name="initial_capital"
              value={formData.initial_capital}
              onChange={handleInputChange}
              placeholder="请输入初始资金"
              min="10000"
              max="10000000"
              step="1000"
              className={`input pl-10 ${errors.initial_capital ? 'border-danger-500' : ''}`}
            />
          </div>
          {errors.initial_capital && (
            <p className="mt-1 text-sm text-danger-600">{errors.initial_capital}</p>
          )}
          <div className="mt-2">
            <div className="flex flex-wrap gap-2">
              {['50000', '100000', '200000', '500000'].map(amount => (
                <button
                  key={amount}
                  type="button"
                  onClick={() => handleInputChange({ target: { name: 'initial_capital', value: amount } })}
                  className={`px-3 py-1 text-xs rounded border transition-colors ${
                    formData.initial_capital === amount
                      ? 'bg-primary-100 border-primary-300 text-primary-700'
                      : 'bg-gray-50 border-gray-200 text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  ¥{(parseInt(amount) / 10000).toFixed(0)}万
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* 提示信息 */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex">
            <Info className="w-5 h-5 text-blue-400 mt-0.5" />
            <div className="ml-3">
              <h3 className="text-sm font-medium text-blue-800">使用提示</h3>
              <div className="mt-2 text-sm text-blue-700">
                <ul className="list-disc list-inside space-y-1">
                  <li>ETF代码为6位数字，如510300（沪深300ETF）</li>
                  <li>高频交易适合波动较大的市场，但需要更多精力监控</li>
                  <li>建议初始资金不少于10万元，以获得更好的资金利用效率</li>
                  <li>分析结果基于历史数据，不构成投资建议</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

      </form>
    </div>
  )
}

export default InputForm
