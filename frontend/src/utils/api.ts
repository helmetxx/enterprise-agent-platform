import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { config } from '@/config'

// 创建 axios 实例
export const api = axios.create({
  baseURL: config.apiBaseUrl,  // 这里应该使用配置
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
      // 添加调试日志
      console.log('Request Headers:', config.headers)
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 响应拦截器
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore()
      authStore.logout()
      const router = useRouter()
      router.push('/auth/login')
      ElMessage.error('登录已过期，请重新登录')
    }
    return Promise.reject(error)
  }
) 