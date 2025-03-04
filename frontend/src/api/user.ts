import { api } from '@/utils/api'
import { config } from '@/config'

export const userApi = {
  async getProfile() {
    try {
      const response = await api.get('/users/me')
      // 确保用户头像使用正确的默认值
      if (response.data && (!response.data.avatar || response.data.avatar === 'avatar-default.png')) {
        response.data.avatar = config.defaultAvatar
      }
      return response.data
    } catch (error) {
      console.error('Failed to fetch user profile:', error)
      throw error
    }
  },
  
  async updateProfile(userData: any) {
    // 如果头像是默认的，不要发送到服务器
    if (userData.avatar === config.defaultAvatar) {
      delete userData.avatar
    }
    return api.put('/users/me', userData)
  },
  
  // 其他用户相关 API 方法...
} 