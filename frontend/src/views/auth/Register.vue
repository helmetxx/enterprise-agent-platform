<template>
  <div class="register-container">
    <el-card class="register-card">
      <h2>注册</h2>
      <el-form 
        ref="formRef"
        :model="registerForm" 
        :rules="rules"
        @submit.prevent="handleRegister"
      >
        <el-form-item prop="email">
          <el-input v-model="registerForm.email" placeholder="邮箱" />
        </el-form-item>
        <el-form-item prop="full_name">
          <el-input v-model="registerForm.full_name" placeholder="姓名" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="registerForm.password" type="password" placeholder="密码" />
        </el-form-item>
        <el-form-item prop="confirmPassword">
          <el-input v-model="registerForm.confirmPassword" type="password" placeholder="确认密码" />
        </el-form-item>
        <el-form-item>
          <el-button 
            type="primary" 
            native-type="submit"
            :loading="loading" 
            block
          >
            注册
          </el-button>
        </el-form-item>
        <div class="form-footer">
          <router-link to="/auth/login">已有账号？立即登录</router-link>
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
import { api } from '@/utils/api'

const router = useRouter()
const loading = ref(false)
const formRef = ref<FormInstance>()

const registerForm = ref({
  email: '',
  full_name: '',
  password: '',
  confirmPassword: ''
})

const validatePass2 = (rule: any, value: string, callback: any) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== registerForm.value.password) {
    callback(new Error('两次输入密码不一致!'))
  } else {
    callback()
  }
}

const rules: FormRules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  full_name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validatePass2, trigger: 'blur' }
  ]
}

const handleRegister = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    loading.value = true
    
    const requestData = {
      email: registerForm.value.email,
      full_name: registerForm.value.full_name,
      password: registerForm.value.password
    }
    
    const response = await api.post('/auth/register', requestData)
    console.log('Register response:', response)
    
    ElMessage.success('注册成功，请登录')
    await router.push('/auth/login')
  } catch (error: any) {
    console.error('Register error:', {
      error,
      config: error.config,
      response: error.response
    })
    if (error.response) {
      ElMessage.error(error.response.data.message || '注册失败，请稍后重试')
    } else {
      ElMessage.error('注册失败，请稍后重试')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.register-container {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f7fa;
}

.register-card {
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