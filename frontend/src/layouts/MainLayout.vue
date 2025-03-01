<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = () => {
  authStore.logout()
  router.push('/auth/login')
}
</script>

<template>
  <el-container class="layout-container">
    <el-header>
      <div class="header-content">
        <div class="logo">
          <h1>企业智能助手平台</h1>
        </div>
        <div class="user-menu">
          <el-dropdown>
            <span class="el-dropdown-link">
              个人中心<el-icon class="el-icon--right"><arrow-down /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </el-header>
    <el-container>
      <router-view />
    </el-container>
  </el-container>
</template>

<style lang="scss" scoped>
// ... 样式保持不变 ...
</style> 