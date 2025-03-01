<template>
  <div class="document-analysis">
    <div class="page-header">
      <h1>文档分析</h1>
      <el-button-group>
        <el-button 
          type="primary"
          :loading="analyzing"
          @click="startAnalysis"
        >
          开始分析
        </el-button>
        <el-button @click="nextStep">
          下一步
        </el-button>
      </el-button-group>
    </div>
    
    <div class="analysis-content">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card class="upload-card">
            <template #header>
              <div class="card-header">
                <h3>上传文档</h3>
              </div>
            </template>
            <el-upload
              class="document-uploader"
              drag
              action="/api/v1/upload"
              :on-success="handleUploadSuccess"
              :on-error="handleUploadError"
              :before-upload="beforeUpload"
            >
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <div class="el-upload__text">
                将文件拖到此处，或<em>点击上传</em>
              </div>
              <template #tip>
                <div class="el-upload__tip">
                  支持 PDF、Word、TXT 格式文件
                </div>
              </template>
            </el-upload>
          </el-card>
        </el-col>
        
        <el-col :span="12">
          <el-card class="result-card">
            <template #header>
              <div class="card-header">
                <h3>分析结果</h3>
              </div>
            </template>
            <div v-if="loading" class="analysis-loading">
              <el-skeleton :rows="10" animated />
            </div>
            <div v-else-if="analysisResults.length" class="analysis-results">
              <div 
                v-for="result in analysisResults" 
                :key="result.id"
                class="result-item"
              >
                <h4>{{ result.analysis_type }}</h4>
                <pre>{{ JSON.stringify(result.content, null, 2) }}</pre>
              </div>
            </div>
            <el-empty v-else description="暂无分析结果" />
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'
import { useCreativeStore } from '@/stores/creative'
import type { DocumentAnalysis } from '@/types/creative'

const route = useRoute()
const router = useRouter()
const store = useCreativeStore()
const loading = ref(false)
const analyzing = ref(false)
const analysisResults = ref<DocumentAnalysis[]>([])

const projectId = route.params.id as string

onMounted(async () => {
  await fetchAnalysisResults()
})

async function fetchAnalysisResults() {
  loading.value = true
  try {
    const response = await store.getDocumentAnalyses(projectId)
    analysisResults.value = response
  } catch (error) {
    ElMessage.error('获取分析结果失败')
  } finally {
    loading.value = false
  }
}

function handleUploadSuccess(response: any) {
  ElMessage.success('上传成功')
}

function handleUploadError() {
  ElMessage.error('上传失败')
}

function beforeUpload(file: File) {
  const validTypes = ['application/pdf', 'application/msword', 'text/plain']
  if (!validTypes.includes(file.type)) {
    ElMessage.error('只支持 PDF、Word、TXT 格式文件')
    return false
  }
  return true
}

async function startAnalysis() {
  analyzing.value = true
  try {
    await store.createDocumentAnalysis(projectId, {
      analysis_type: 'core_features',
      content: {}
    })
    await fetchAnalysisResults()
    ElMessage.success('分析完成')
  } catch (error) {
    ElMessage.error('分析失败')
  } finally {
    analyzing.value = false
  }
}

function nextStep() {
  router.push(`/creative/projects/${projectId}/market`)
}
</script>

<style lang="scss" scoped>
.document-analysis {
  padding: var(--spacing-base);
  
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-large);
    
    h1 {
      margin: 0;
      color: var(--color-text-primary);
    }
  }
  
  .analysis-content {
    .upload-card,
    .result-card {
      height: 100%;
      background: var(--color-secondary);
      border: 1px solid rgba(255, 255, 255, 0.1);
      
      .card-header {
        h3 {
          margin: 0;
          color: var(--color-text-primary);
        }
      }
    }
    
    .document-uploader {
      :deep(.el-upload-dragger) {
        background: var(--color-primary);
        border-color: var(--color-accent);
      }
    }
    
    .result-item {
      margin-bottom: var(--spacing-base);
      
      h4 {
        color: var(--color-text-primary);
        margin-bottom: 8px;
      }
      
      pre {
        background: var(--color-primary);
        padding: var(--spacing-base);
        border-radius: var(--border-radius-small);
        overflow: auto;
      }
    }
  }
}
</style> 