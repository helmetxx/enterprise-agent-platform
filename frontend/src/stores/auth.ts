import { defineStore } from 'pinia'
import { api } from '@/utils/api'
import Logger from '@/utils/logger'
import { useRouter } from 'vue-router'

interface LoginCredentials {
  email: string
  password: string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
  }),
  
  getters: {
    isAuthenticated: (state) => {
      console.log('检查认证状态:', !!state.token)
      return !!state.token
    },
  },
  
  actions: {
    async login(credentials: { email: string; password: string }) {
      try {
        Logger.info('Login attempt:', { email: credentials.email })

        // 使用 form-urlencoded 格式
        const formData = new URLSearchParams()
        formData.append('username', credentials.email)
        formData.append('password', credentials.password)
        
        const response = await api.post('/auth/login', formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        })

        const { access_token, token_type } = response.data
        if (!access_token) {
          throw new Error('登录响应中没有找到 token')
        }

        // 保存认证信息
        this.token = access_token
        localStorage.setItem('token', access_token)
        // 设置全局请求头
        api.defaults.headers.common['Authorization'] = `${token_type} ${access_token}`

        Logger.info('Login successful, token saved')
        return response.data
      } catch (error: any) {
        Logger.error('Login failed:', error)
        throw error.response?.data?.detail || error.message || '登录失败'
      }
    },

    // 注册仍然使用 JSON 格式
    async register(userData: { email: string; password: string; full_name: string }) {
      const response = await api.post('/auth/register', userData)
      return response
    },

    logout() {
      Logger.info('Logging out')
      this.token = null
      localStorage.removeItem('token')
      delete api.defaults.headers.common['Authorization']
    }
  }
}) 