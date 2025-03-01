<template>
  <div class="create-knowledge">
    <!-- 面包屑导航 -->
    <el-breadcrumb class="breadcrumb">
      <el-breadcrumb-item :to="{ path: '/dashboard' }">工作台</el-breadcrumb-item>
      <el-breadcrumb-item :to="{ path: '/dashboard/knowledge' }">知识库管理</el-breadcrumb-item>
      <el-breadcrumb-item>新建知识库</el-breadcrumb-item>
    </el-breadcrumb>

    <div class="page-container">
      <!-- 步骤条 -->
      <el-steps :active="currentStep" finish-status="success" class="steps">
        <el-step title="选择数据源" />
        <el-step title="文本分段与清洗" />
        <el-step title="处理完成" />
      </el-steps>

      <!-- 主要内容区域 -->
      <div class="content-area">
        <div class="data-source-section">
          <h3>选择数据源</h3>
          <div class="source-options">
            <div class="source-card active">
              <el-icon><Document /></el-icon>
              <span>导入已有文本</span>
            </div>
            <div class="source-card disabled">
              <el-icon><Connection /></el-icon>
              <span>同步自 Notion 内容</span>
            </div>
            <div class="source-card disabled">
              <el-icon><Link /></el-icon>
              <span>同步自 Web 站点</span>
            </div>
          </div>

          <!-- 文件上传区域 -->
          <div class="upload-section">
            <div class="upload-area">
              <el-upload
                class="upload-drop-zone"
                drag
                action="#"
                :auto-upload="false"
                :show-file-list="true"
                :on-change="handleFileChange"
                :on-remove="handleFileRemove"
                :file-list="fileList"
              >
                <el-icon class="upload-icon"><Upload /></el-icon>
                <div class="upload-text">
                  <p>拖拽文件到此处，或者 <em>点击上传</em></p>
                  <p class="upload-tip">
                    已支持 TXT、MARKDOWN、MDX、PDF、HTML、XLSX、XLS、DOCX、CSV、EML、MSG、PPTX、XML、EPUB、PPT、MD、HTM，每个文件不超过 15MB。
                  </p>
                </div>
              </el-upload>
            </div>

            <!-- 已上传文件列表 -->
            <div v-if="fileList.length > 0" class="file-list">
              <div v-for="file in fileList" :key="file.uid" class="file-item">
                <el-icon><Document /></el-icon>
                <span class="file-name">{{ file.name }}</span>
                <span class="file-size">{{ formatFileSize(file.size) }}</span>
                <el-button
                  type="danger"
                  link
                  @click="handleFileRemove(file)"
                >
                  删除
                </el-button>
              </div>
            </div>
          </div>

          <!-- 底部操作按钮 -->
          <div class="bottom-actions">
            <el-button @click="showEmptyKbDialog">创建空知识库</el-button>
            <el-button type="primary" :disabled="!hasFiles" @click="nextStep">
              下一步
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 创建空知识库对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="创建空知识库"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="knowledgeForm"
        :rules="rules"
        label-width="80px"
      >
        <el-form-item label="名称" prop="name">
          <el-input v-model="knowledgeForm.name" placeholder="请输入知识库名称" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="knowledgeForm.description"
            type="textarea"
            placeholder="请输入知识库描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="createEmptyKnowledgeBase">
            创建
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 参数设置对话框 -->
    <el-dialog
      v-model="settingsVisible"
      title="知识库设置"
      width="600px"
    >
      <el-form
        ref="settingsFormRef"
        :model="settingsForm"
        :rules="settingsRules"
        label-width="120px"
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
        <el-form-item label="分段方式" prop="segmentationMethod">
          <el-select v-model="settingsForm.segmentationMethod" placeholder="请选择分段方式">
            <el-option label="按段落" value="paragraph" />
            <el-option label="按句子" value="sentence" />
            <el-option label="按固定长度" value="fixed" />
          </el-select>
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
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="settingsVisible = false">取消</el-button>
          <el-button type="primary" @click="createKnowledgeBaseWithFiles">
            创建
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Document, Connection, Link, Upload } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, UploadFile } from 'element-plus'
import { useKnowledgeStore } from '@/stores/knowledge'

const router = useRouter()
const knowledgeStore = useKnowledgeStore()

const currentStep = ref(1)
const fileList = ref<UploadFile[]>([])
const hasFiles = computed(() => fileList.value.length > 0)

// 空知识库表单相关
const dialogVisible = ref(false)
const formRef = ref<FormInstance>()
const knowledgeForm = ref({
  name: '',
  description: ''
})

const rules = {
  name: [
    { required: true, message: '请输入知识库名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ]
}

// 文件上传相关
const handleFileChange = (file: UploadFile) => {
  console.log('File changed:', file)
  if (!validateFile(file)) {
    return false
  }
  // 检查是否已存在相同文件
  const exists = fileList.value.some(f => f.name === file.name)
  if (!exists) {
    fileList.value.push(file)
    console.log('Current file list:', fileList.value)
  }
  return false // 阻止自动上传
}

const handleFileRemove = (file: UploadFile) => {
  const index = fileList.value.indexOf(file)
  if (index > -1) {
    fileList.value.splice(index, 1)
  }
}

// 文件验证
const validateFile = (file: UploadFile) => {
  const allowedTypes = [
    'text/plain', 'text/markdown', 'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/msword'
  ]
  
  if (!allowedTypes.includes(file.raw?.type || '')) {
    ElMessage.error('不支持的文件类型')
    return false
  }
  
  const maxSize = 15 * 1024 * 1024 // 15MB
  if (file.size > maxSize) {
    ElMessage.error('文件大小不能超过15MB')
    return false
  }
  
  return true
}

// 格式化文件大小
const formatFileSize = (size: number) => {
  if (size < 1024) {
    return size + 'B'
  } else if (size < 1024 * 1024) {
    return (size / 1024).toFixed(2) + 'KB'
  } else {
    return (size / (1024 * 1024)).toFixed(2) + 'MB'
  }
}

// 参数设置相关
const settingsVisible = ref(false)
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

// 下一步
const nextStep = () => {
  if (!hasFiles.value) {
    ElMessage.warning('请先选择要上传的文件')
    return
  }
  // 将文件列表保存到 store 中
  knowledgeStore.setTempFiles(fileList.value)
  router.push('/dashboard/knowledge/settings')
}

// 显示创建空知识库对话框
const showEmptyKbDialog = () => {
  dialogVisible.value = true
}

// 创建空知识库
const createEmptyKnowledgeBase = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await knowledgeStore.createKnowledgeBase({
          name: knowledgeForm.value.name,
          description: knowledgeForm.value.description
        })
        ElMessage.success('创建成功')
        router.push('/dashboard/knowledge')
      } catch (error) {
        console.error('Failed to create knowledge base:', error)
        ElMessage.error('创建失败')
      }
    }
  })
}

// 创建知识库并上传文件
const createKnowledgeBaseWithFiles = async () => {
  if (!settingsFormRef.value) return
  
  await settingsFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        // 1. 创建知识库
        const kb = await knowledgeStore.createKnowledgeBase({
          name: settingsForm.value.name,
          description: settingsForm.value.description
        })

        // 2. 上传文件
        const uploadPromises = fileList.value.map(file => 
          knowledgeStore.uploadDocument(kb.id, file.raw as File)
        )
        
        await Promise.all(uploadPromises)
        
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
.create-knowledge {
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

      .data-source-section {
        h3 {
          margin-bottom: 20px;
          font-size: 18px;
        }

        .source-options {
          display: flex;
          gap: 20px;
          margin-bottom: 30px;

          .source-card {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
            border: 1px solid var(--el-border-color);
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;

            &.active {
              border-color: var(--el-color-primary);
              color: var(--el-color-primary);
            }

            &.disabled {
              opacity: 0.5;
              cursor: not-allowed;
            }

            .el-icon {
              font-size: 24px;
              margin-bottom: 8px;
            }
          }
        }

        .upload-section {
          margin-bottom: 30px;

          .upload-area {
            border: 2px dashed var(--el-border-color);
            border-radius: 8px;
            padding: 20px;

            .upload-drop-zone {
              width: 100%;
              
              :deep(.el-upload-dragger) {
                width: 100%;
                height: 200px;
              }
            }

            .upload-icon {
              font-size: 48px;
              color: var(--el-text-color-secondary);
            }

            .upload-text {
              color: var(--el-text-color-regular);
              
              em {
                color: var(--el-color-primary);
                font-style: normal;
                cursor: pointer;
              }

              .upload-tip {
                font-size: 12px;
                color: var(--el-text-color-secondary);
                margin-top: 8px;
              }
            }
          }
        }

        .bottom-actions {
          display: flex;
          justify-content: space-between;
          padding-top: 20px;
          border-top: 1px solid var(--el-border-color-lighter);
        }
      }
    }
  }
}

.file-list {
  margin-top: 20px;
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