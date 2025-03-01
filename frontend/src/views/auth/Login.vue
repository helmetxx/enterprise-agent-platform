<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2>登录</h2>
      <el-form 
        ref="formRef"
        :model="loginForm" 
        :rules="rules"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="email">
          <el-input v-model="loginForm.email" placeholder="邮箱" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="loginForm.password" type="password" placeholder="密码" />
        </el-form-item>
        <el-form-item>
          <el-button 
            type="primary" 
            native-type="submit" 
            :loading="loading"
            block
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
        <div class="form-footer">
          <router-link to="/auth/register">没有账号？立即注册</router-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import Logger from '@/utils/logger'

const router = useRouter()
const authStore = useAuthStore()
const loading = ref(false)
const formRef = ref<FormInstance>()

const loginForm = ref({
  email: '',
  password: ''
})

const rules: FormRules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    loading.value = true
    
    Logger.info('Starting login process...')
    await authStore.login({
      email: loginForm.value.email,
      password: loginForm.value.password
    })
    
    Logger.info('Login successful:')
    ElMessage.success('登录成功')
    await router.push('/')
  } catch (error: any) {
    Logger.error('Login error:', error)
    ElMessage.error(typeof error === 'string' ? error : '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.login-container {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f7fa;
}

.login-card {
  width: 400px;
  padding: 20px;

  h2 {
    text-align: center;
    margin-bottom: 20px;
  }

  .form-footer {
    text-align: center;
    margin-top: 16px;
  }
}
</style> 