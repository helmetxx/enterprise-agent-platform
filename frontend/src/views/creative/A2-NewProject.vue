<template>
  <div class="new-project">
    <div class="page-header">
      <h1>创建新项目</h1>
    </div>
    
    <el-form 
      ref="formRef"
      :model="formData"
      :rules="rules"
      label-position="top"
      class="project-form"
    >
      <el-form-item label="项目名称" prop="title">
        <el-input 
          v-model="formData.title"
          placeholder="请输入项目名称"
        />
      </el-form-item>
      
      <el-form-item label="项目描述" prop="description">
        <el-input 
          v-model="formData.description"
          type="textarea"
          :rows="4"
          placeholder="请输入项目描述"
        />
      </el-form-item>
      
      <el-form-item>
        <el-button 
          type="primary"
          :loading="loading"
          @click="handleSubmit"
        >
          创建项目
        </el-button>
        <el-button @click="handleCancel">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormValidateCallback } from 'element-plus/es/components/form'
import { useCreativeStore } from '@/stores/creative'
import type { CreativeProject } from '@/types/creative'

const router = useRouter()
const store = useCreativeStore()
const formRef = ref<FormInstance>()
const loading = ref(false)

const formData = ref({
  title: '',
  description: ''
})

const rules = {
  title: [
    { required: true, message: '请输入项目名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入项目描述', trigger: 'blur' },
    { min: 10, max: 500, message: '长度在 10 到 500 个字符', trigger: 'blur' }
  ]
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    loading.value = true
    const response = await store.createProject({
      ...formData.value,
      status: 'draft' as const
    })
    ElMessage.success('创建成功')
    router.push(`/creative/projects/${response.id}/document`)
  } catch (error) {
    ElMessage.error('创建失败')
  } finally {
    loading.value = false
  }
}

function handleCancel() {
  router.back()
}
</script>

<style lang="scss" scoped>
.new-project {
  padding: var(--spacing-base);
  
  .page-header {
    margin-bottom: var(--spacing-large);
    
    h1 {
      margin: 0;
      color: var(--color-text-primary);
    }
  }
  
  .project-form {
    max-width: 600px;
    margin: 0 auto;
    padding: var(--spacing-large);
    background: var(--color-secondary);
    border-radius: var(--border-radius-large);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
}
</style> 