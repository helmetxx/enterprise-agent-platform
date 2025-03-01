<template>
  <div class="register-container">
    <div class="space-background">
      <div class="stars"></div>
      <div class="rocket"></div>
      <div class="planet"></div>
    </div>
    
    <el-card class="register-card">
      <template #header>
        <h2 class="card-title">注册账号</h2>
      </template>
      
      <el-form 
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-position="top"
      >
        <el-form-item label="用户名" prop="username">
          <el-input 
            v-model="formData.username"
            placeholder="请输入用户名"
          />
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input 
            v-model="formData.email"
            placeholder="请输入邮箱"
          />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input 
            v-model="formData.password"
            type="password"
            placeholder="请输入密码"
          />
        </el-form-item>
        
        <el-button 
          type="primary" 
          :loading="loading"
          @click="handleRegister"
        >
          注册
        </el-button>
      </el-form>
      
      <div class="form-footer">
        <router-link to="/login" class="login-link">
          已有账号？立即登录
        </router-link>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import api from '../utils/axios'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loading = ref(false)
const formRef = ref()

const formData = reactive({
  username: '',
  email: '',
  password: ''
})

const rules = {
  username: [{ required: true, message: 'Please input username', trigger: 'blur' }],
  email: [
    { required: true, message: 'Please input email', trigger: 'blur' },
    { type: 'email', message: 'Please input valid email', trigger: 'blur' }
  ],
  password: [{ required: true, message: 'Please input password', trigger: 'blur' }]
}

const handleRegister = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    loading.value = true
    
    console.log('Sending registration request:', formData)
    const response = await api.post('/api/v1/auth/register', formData)
    console.log('Registration response:', response)
    
    ElMessage.success('Registration successful')
    router.push('/login')
  } catch (error: any) {
    console.error('Registration error:', error)
    ElMessage.error(
      error.response?.data?.detail || 
      error.message || 
      'Registration failed'
    )
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

.space-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  
  .stars {
    position: absolute;
    width: 100%;
    height: 100%;
    background-image: radial-gradient(circle, #ffffff 1px, transparent 1px);
    background-size: 50px 50px;
    animation: twinkle 3s infinite;
  }
  
  .rocket {
    position: absolute;
    width: 100px;
    height: 100px;
    background: url('/assets/rocket.svg') no-repeat center;
    background-size: contain;
    left: 10%;  // 与登录页面相反的位置
    top: 20%;
    animation: float 6s infinite ease-in-out;
  }
  
  .planet {
    position: absolute;
    width: 200px;
    height: 200px;
    background: url('/assets/planet.svg') no-repeat center;
    background-size: contain;
    right: 10%;  // 与登录页面相反的位置
    bottom: 10%;
    opacity: 0.6;
  }
}

.register-card {
  width: 400px;
  background: rgba(45, 45, 45, 0.7);
  backdrop-filter: blur(10px);
  border-radius: var(--border-radius-large);
  border: 1px solid rgba(255, 255, 255, 0.1);
  z-index: 1;
  
  :deep(.el-card__header) {
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .card-title {
    color: var(--color-text-primary);
    text-align: center;
    margin: 0;
    font-size: 24px;
  }
}

:deep(.el-input) {
  .el-input__wrapper {
    background: var(--color-secondary);
    border: 1px solid var(--color-accent);
    
    input {
      color: var(--color-text-primary);
      
      &::placeholder {
        color: var(--color-text-secondary);
      }
    }
  }
}

:deep(.el-button) {
  width: 100%;
  height: 40px;
  background: var(--color-button-primary);
  border: none;
  
  &:hover {
    background: var(--color-button-primary-hover);
  }
}

.form-footer {
  text-align: center;
  margin-top: var(--spacing-large);
  
  .login-link {
    color: var(--color-text-secondary);
    text-decoration: none;
    
    &:hover {
      color: var(--color-button-primary);
    }
  }
}
</style> 