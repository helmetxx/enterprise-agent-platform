<template>
  <div class="dashboard-layout">
    <!-- 顶部导航栏 -->
    <header class="main-header">
      <div class="header-left">
        <div class="logo">
          <img src="@/assets/logo.svg" alt="Logo">
          <span class="platform-name">企业智能助手平台</span>
        </div>
        <!-- 主导航菜单 -->
        <el-menu 
          mode="horizontal" 
          :default-active="activeMenu"
          class="main-menu"
          router>
          <el-menu-item index="/dashboard">
            <el-icon><Monitor /></el-icon>工作台
          </el-menu-item>
          <el-menu-item index="/dashboard/knowledge">
            <el-icon><Collection /></el-icon>知识库
          </el-menu-item>
          <el-menu-item index="/dashboard/projects">
            <el-icon><Folder /></el-icon>我的项目
          </el-menu-item>
          <el-sub-menu index="more">
            <template #title>
              <el-icon><More /></el-icon>更多
            </template>
            <el-menu-item index="/dashboard/tools">
              <el-icon><Tools /></el-icon>工具
            </el-menu-item>
          </el-sub-menu>
        </el-menu>
      </div>
      
      <div class="header-right">
        <el-dropdown @command="handleCommand">
          <div class="user-profile">
            <common-avatar :src="userStore.user?.avatar" :size="32" />
            <span class="username">{{ userFullName }}</span>
            <el-icon><CaretBottom /></el-icon>
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">
                <el-icon><User /></el-icon>个人中心
              </el-dropdown-item>
              <el-dropdown-item divided command="logout">
                <el-icon><SwitchButton /></el-icon>退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </header>

    <!-- 主内容区 -->
    <div class="main-content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'
import { config } from '@/config'
import CommonAvatar from '@/components/common/Avatar.vue'
import { 
  Monitor, 
  Collection, 
  Folder,
  User,
  CaretBottom,
  SwitchButton,
  More,
  Tools
} from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()
const userStore = useUserStore()

const activeMenu = computed(() => router.currentRoute.value.path)
// 从 authStore 获取用户全名
const userFullName = computed(() => authStore.user?.fullname || '')

const handleCommand = async (command: string) => {
  switch (command) {
    case 'profile':
      ElMessage.info('个人中心功能开发中')
      break
    case 'logout':
      console.log('开始退出登录')
      authStore.logout()
      console.log('状态已清除')
      await router.push('/auth/login')
      console.log('路由已跳转')
      ElMessage.success('已退出登录')
      break
  }
}
</script>

<style lang="scss" scoped>
.dashboard-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-header {
  height: 60px;
  padding: 0 24px;
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 40px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  
  img {
    height: 32px;
  }
  
  .platform-name {
    font-size: 16px;
    font-weight: 500;
    color: #303133;
    white-space: nowrap;
  }
}

.main-menu {
  border-bottom: none;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  
  &:hover {
    background: #f5f7fa;
  }
  
  .username {
    font-size: 14px;
    color: #606266;
  }
}

.main-content {
  flex: 1;
  background: #f5f7fa;
  padding: 24px;
}

:deep(.el-dropdown-menu__item) {
  display: flex;
  align-items: center;
  gap: 8px;
}
</style> 