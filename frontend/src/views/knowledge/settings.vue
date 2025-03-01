<template>
  <div class="knowledge-settings">
    <!-- 面包屑导航 -->
    <el-breadcrumb class="breadcrumb">
      <el-breadcrumb-item :to="{ path: '/dashboard' }">工作台</el-breadcrumb-item>
      <el-breadcrumb-item :to="{ path: '/dashboard/knowledge' }">知识库管理</el-breadcrumb-item>
      <el-breadcrumb-item>新建知识库</el-breadcrumb-item>
    </el-breadcrumb>

    <div class="page-container">
      <!-- 步骤条 -->
      <el-steps :active="2" finish-status="success" class="steps">
        <el-step title="选择数据源" />
        <el-step title="文本分段与清洗" />
        <el-step title="处理完成" />
      </el-steps>

      <!-- 主要内容区域 -->
      <div class="content-area">
        <h3>知识库设置</h3>
        
        <el-form
          ref="settingsFormRef"
          :model="settingsForm"
          :rules="settingsRules"
          label-width="120px"
          class="settings-form"
        >
          <el-form-item label="知识库名称" prop="name">
            <el-input v-model="settingsForm.name" placeholder="请输入知识库名称" />
          </el-form-item>
          
          <el-form-item label="描述" prop="description">
            <el-input
              v-model="settingsForm.description"
              type="textarea"
              placeholder="请输入知识库描述"
            />
          </el-form-item>

          <div class="section-title">文本处理设置</div>
          
          <el-form-item label="分段方式" prop="segmentationMethod">
            <el-radio-group v-model="settingsForm.segmentationMethod">
              <el-radio-button value="paragraph">按段落</el-radio-button>
              <el-radio-button value="sentence">按句子</el-radio-button>
              <el-radio-button value="fixed">按固定长度</el-radio-button>
            </el-radio-group>
          </el-form-item>
          
          <el-form-item 
            v-if="settingsForm.segmentationMethod === 'fixed'" 
            label="分段长度" 
            prop="segmentLength"
          >
            <el-input-number 
              v-model="settingsForm.segmentLength" 
              :min="100" 
              :max="1000" 
              :step="50" 
            />
            <span class="form-tip">字符数（建议设置在 100-1000 之间）</span>
          </el-form-item>

          <div class="section-title">文件列表</div>
          <div class="file-list">
            <div v-for="file in files" :key="file.uid" class="file-item">
              <el-icon><Document /></el-icon>
              <span class="file-name">{{ file.name }}</span>
              <span class="file-size">{{ formatFileSize(file.size) }}</span>
              <el-tag size="small" type="info">待处理</el-tag>
            </div>
          </div>

          <div class="form-actions">
            <el-button @click="goBack">上一步</el-button>
            <el-button type="primary" @click="handleSubmit">开始处理</el-button>
          </div>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Document } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { useKnowledgeStore } from '@/stores/knowledge'

const router = useRouter()
const knowledgeStore = useKnowledgeStore()

const settingsFormRef = ref<FormInstance>()
const settingsForm = ref({
  name: '',
  description: '',
  segmentationMethod: 'paragraph',
  segmentLength: 500
})

const settingsRules = {
  name: [{ required: true, message: '请输入知识库名称', trigger: 'blur' }],
  segmentationMethod: [{ required: true, message: '请选择分段方式', trigger: 'change' }]
}

// 从 store 获取文件列表
const files = ref([])
onMounted(() => {
  const storeFiles = knowledgeStore.tempFiles
  console.log('Store files:', storeFiles) // 添加调试日志
  
  if (storeFiles && storeFiles.length > 0) {
    files.value = storeFiles
  } else {
    // 如果没有文件，返回上一步
    ElMessage.warning('请先选择文件')
    router.replace('/dashboard/knowledge/create')
  }
})

const formatFileSize = (size: number) => {
  if (size < 1024) {
    return size + 'B'
  } else if (size < 1024 * 1024) {
    return (size / 1024).toFixed(2) + 'KB'
  } else {
    return (size / (1024 * 1024)).toFixed(2) + 'MB'
  }
}

const goBack = () => {
  router.push('/dashboard/knowledge/create')
}

const handleSubmit = async () => {
  if (!settingsFormRef.value) return
  
  await settingsFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        // 1. 创建知识库
        const kb = await knowledgeStore.createKnowledgeBase({
          name: settingsForm.value.name,
          description: settingsForm.value.description,
          segmentation_method: settingsForm.value.segmentationMethod,
          segment_length: settingsForm.value.segmentLength
        })

        // 2. 上传文件
        const uploadPromises = files.value.map(file => 
          knowledgeStore.uploadDocument(kb.id, file.raw as File)
        )
        
        await Promise.all(uploadPromises)
        
        // 3. 清空临时文件列表
        knowledgeStore.setTempFiles([])
        
        ElMessage.success('知识库创建成功')
        router.push('/dashboard/knowledge')
        
      } catch (error) {
        console.error('Failed to create knowledge base:', error)
        ElMessage.error('创建知识库失败')
      }
    }
  })
}
</script>

<style lang="scss" scoped>
.knowledge-settings {
  .breadcrumb {
    margin-bottom: 16px;
    padding: 16px 20px;
    background-color: var(--el-bg-color);
  }

  .page-container {
    padding: 20px;
    background-color: var(--el-bg-color);
    border-radius: 4px;

    .steps {
      margin-bottom: 40px;
    }

    .content-area {
      max-width: 800px;
      margin: 0 auto;

      h3 {
        margin-bottom: 24px;
        font-size: 18px;
      }

      .settings-form {
        .section-title {
          margin: 24px 0 16px;
          padding-left: 8px;
          border-left: 4px solid var(--el-color-primary);
          font-size: 16px;
          font-weight: 500;
        }

        .form-tip {
          margin-left: 8px;
          color: var(--el-text-color-secondary);
          font-size: 14px;
        }

        .form-actions {
          margin-top: 40px;
          display: flex;
          justify-content: center;
          gap: 16px;
        }
      }
    }
  }
}

.file-list {
  margin: 16px 0;
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 4px;

  .file-item {
    display: flex;
    align-items: center;
    padding: 12px 16px;
    border-bottom: 1px solid var(--el-border-color-lighter);

    &:last-child {
      border-bottom: none;
    }

    .el-icon {
      margin-right: 8px;
      color: var(--el-text-color-secondary);
    }

    .file-name {
      flex: 1;
      margin-right: 16px;
    }

    .file-size {
      color: var(--el-text-color-secondary);
      margin-right: 16px;
    }
  }
}
</style> 