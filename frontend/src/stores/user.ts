import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '@/utils/api'
import { config } from '@/config'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)

  function setDefaultUserData(userData: any) {
    if (userData && !userData.avatar) {
      userData.avatar = config.defaultAvatar
    }
    return userData
  }
  
  async function fetchUserProfile() {
    try {
      const response = await api.get('/users/me')
      const userData = setDefaultUserData(response.data)
      user.value = userData
      return userData
    } catch (error) {
      console.error('Failed to fetch user profile:', error)
      return null
    }
  }

  return {
    user,
    fetchUserProfile,
  }
}) 