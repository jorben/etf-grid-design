import { useState, useEffect } from 'react'

/**
 * 自定义Hook：使用localStorage持久化状态
 * @param {string} key - localStorage的键名
 * @param {*} defaultValue - 默认值
 * @returns {[state, setState, clearState]} - 状态值、设置函数、清除函数
 */
export const usePersistedState = (key, defaultValue) => {
  // 从localStorage读取初始值
  const [state, setState] = useState(() => {
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : defaultValue
    } catch (error) {
      console.warn(`Error reading localStorage key "${key}":`, error)
      return defaultValue
    }
  })

  // 当状态改变时，保存到localStorage
  useEffect(() => {
    try {
      window.localStorage.setItem(key, JSON.stringify(state))
    } catch (error) {
      console.warn(`Error setting localStorage key "${key}":`, error)
    }
  }, [key, state])

  // 清除状态的函数
  const clearState = () => {
    try {
      window.localStorage.removeItem(key)
      setState(defaultValue)
    } catch (error) {
      console.warn(`Error removing localStorage key "${key}":`, error)
    }
  }

  return [state, setState, clearState]
}

/**
 * 专门用于表单数据的持久化Hook
 * @param {Object} defaultFormData - 默认表单数据
 * @returns {[formData, setFormData, clearFormData, updateField]} 
 */
export const usePersistedFormData = (defaultFormData) => {
  const [formData, setFormData, clearFormData] = usePersistedState('etf-trading-form', defaultFormData)

  // 更新单个字段的便捷函数
  const updateField = (name, value) => {
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  return [formData, setFormData, clearFormData, updateField]
}