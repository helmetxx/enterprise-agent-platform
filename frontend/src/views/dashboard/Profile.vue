<template>
  <div class="profile-page">
    <el-card class="profile-card">
      <div class="profile-header">
        <div class="avatar-container">
          <el-avatar :size="100" :src="userStore.user?.avatar || config.defaultAvatar" />
          <el-button class="change-avatar-btn" size="small" @click="handleChangeAvatar">
            <el-icon><Edit /></el-icon>
            更换头像
          </el-button>
        </div>
        <div class="user-info">
          <h2>{{ userStore.user?.name }}</h2>
          <p>{{ userStore.user?.email }}</p>
        </div>
      </div>
      
      <el-divider />
      
      <el-form :model="profileForm" label-width="100px">
        <el-form-item label="姓名">
          <el-input v-model="profileForm.name" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="profileForm.email" disabled />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="profileForm.phone" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="saveProfile">保存修改</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Edit } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { config } from '@/config'

const userStore = useUserStore()
const profileForm = ref({
  name: '',
  email: '',
  phone: '',
  avatar: ''
})

onMounted(async () => {
  if (!userStore.user) {
    await userStore.fetchUserProfile()
  }
  
  if (userStore.user) {
    profileForm.value = {
      name: userStore.user.name || '',
      email: userStore.user.email || '',
      phone: userStore.user.phone || '',
      avatar: userStore.user.avatar || config.defaultAvatar
    }
  }
})

const handleChangeAvatar = () => {
  ElMessage.info('头像上传功能开发中')
}

const saveProfile = async () => {
  try {
    // 保存逻辑
    ElMessage.success('个人资料已更新')
  } catch (error) {
    ElMessage.error('更新失败，请重试')
  }
}
</script>

<style scoped>
.profile-page {
  max-width: 800px;
  margin: 0 auto;
}

.profile-header {
  display: flex;
  margin-bottom: 24px;
}

.avatar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-right: 32px;
}

.change-avatar-btn {
  margin-top: 8px;
}

.user-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.user-info h2 {
  margin: 0 0 8px;
}

.user-info p {
  margin: 0;
  color: #909399;
}
</style> 