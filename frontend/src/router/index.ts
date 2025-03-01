import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import CreativeLayout from '@/layouts/CreativeLayout.vue'
import NewProduct from '@/views/creative/NewProduct.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/auth',
    component: () => import('@/layouts/AuthLayout.vue'),
    children: [
      {
        path: 'login',
        name: 'Login',
        component: () => import('@/views/auth/Login.vue')
      },
      {
        path: 'register',
        name: 'Register',
        component: () => import('@/views/auth/Register.vue')
      }
    ]
  },
  {
    path: '/dashboard',
    component: () => import('@/layouts/DashboardLayout.vue'),
    meta: { 
      requiresAuth: true,
      noCache: true
    },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue')
      },
      {
        path: 'market',
        name: 'AgentMarket',
        component: () => import('@/views/market/AgentMarket.vue'),
        meta: {
          title: '应用集市',
          breadcrumb: ['工作台', '应用集市']
        }
      },
      {
        path: 'creative',
        component: () => import('@/layouts/CreativeLayout.vue'),
        children: [
          {
            path: '',
            name: 'ProductAssistant',
            component: () => import('@/views/creative/ProductAssistant.vue'),
            meta: {
              title: '产品创意助手'
            }
          },
          {
            path: 'new',
            name: 'NewProduct',
            component: () => import('@/views/creative/NewProduct.vue'),
            meta: {
              title: '新产品'
            }
          }
        ]
      },
      {
        path: 'knowledge',
        name: 'KnowledgeBase',
        component: () => import('@/views/knowledge/index.vue'),
        meta: {
          title: '知识库管理',
          breadcrumb: ['工作台', '知识库管理']
        }
      },
      {
        path: 'knowledge/create',
        name: 'CreateKnowledgeBase',
        component: () => import('@/views/knowledge/create.vue'),
        meta: {
          title: '新建知识库',
          breadcrumb: ['工作台', '知识库管理', '新建知识库']
        }
      },
      {
        path: 'knowledge/:id',
        name: 'KnowledgeBaseDetail',
        component: () => import('@/views/knowledge/detail.vue'),
        meta: {
          title: '知识库详情',
          breadcrumb: ['工作台', '知识库管理', '知识库详情']
        }
      },
      {
        path: 'knowledge/settings',
        name: 'KnowledgeSettings',
        component: () => import('@/views/knowledge/settings.vue'),
        meta: {
          requiresAuth: true,
          title: '知识库设置'
        }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // 如果要访问的是需要认证的页面，且用户未登录
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/auth/login')
  } else if (to.path === '/auth/login' && authStore.isAuthenticated) {
    // 如果已登录用户访问登录页，重定向到首页
    next('/')
  } else {
    next()
  }
})

export default router 