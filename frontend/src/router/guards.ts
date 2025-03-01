import { Router } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

export function setupRouterGuards(router: Router) {
  router.beforeEach((to, from, next) => {
    const authStore = useAuthStore()
    
    if (to.matched.some(record => record.meta.requiresAuth)) {
      if (!authStore.isAuthenticated) {
        next('/auth/login')
      } else {
        next()
      }
    } else if (to.path === '/auth/login' && authStore.isAuthenticated) {
      next('/dashboard')
    } else {
      next()
    }
  })
} 