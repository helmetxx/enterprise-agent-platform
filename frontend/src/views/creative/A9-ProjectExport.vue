<template>
  <div class="project-export">
    <div class="page-header">
      <h1>项目导出</h1>
      <el-button-group>
        <el-button 
          type="primary"
          :loading="exporting"
          @click="exportProject"
        >
          导出项目
        </el-button>
        <el-button @click="nextStep">
          完成
        </el-button>
      </el-button-group>
    </div>

    <div class="export-content">
      <el-row :gutter="20">
        <el-col :span="16">
          <el-card class="export-card">
            <template #header>
              <div class="card-header">
                <h3>导出选项</h3>
              </div>
            </template>
            
            <el-form 
              ref="formRef"
              :model="formData"
              label-position="top"
            >
              <el-form-item label="导出格式">
                <el-radio-group v-model="formData.format">
                  <el-radio-button label="pdf">PDF文档</el-radio-button>
                  <el-radio-button label="word">Word文档</el-radio-button>
                  <el-radio-button label="ppt">PPT演示</el-radio-button>
                </el-radio-group>
              </el-form-item>

              <el-form-item label="内容选择">
                <el-checkbox-group v-model="formData.sections">
                  <el-checkbox label="project_info">项目信息</el-checkbox>
                  <el-checkbox label="document_analysis">文档分析</el-checkbox>
                  <el-checkbox label="market_analysis">市场分析</el-checkbox>
                  <el-checkbox label="ideas">创意方案</el-checkbox>
                  <el-checkbox label="images">生成图片</el-checkbox>
                  <el-checkbox label="solution">技术方案</el-checkbox>
                  <el-checkbox label="evaluation">项目评估</el-checkbox>
                </el-checkbox-group>
              </el-form-item>

              <el-form-item label="模板样式">
                <el-select v-model="formData.template" placeholder="选择模板">
                  <el-option label="简约商务" value="business" />
                  <el-option label="科技创新" value="tech" />
                  <el-option label="创意设计" value="creative" />
                  <el-option label="学术报告" value="academic" />
                </el-select>
              </el-form-item>

              <el-form-item label="高级选项">
                <el-collapse>
                  <el-collapse-item title="导出设置" name="1">
                    <el-form-item label="页面大小">
                      <el-select v-model="formData.pageSize">
                        <el-option label="A4" value="a4" />
                        <el-option label="Letter" value="letter" />
                        <el-option label="自定义" value="custom" />
                      </el-select>
                    </el-form-item>
                    
                    <el-form-item label="图片质量">
                      <el-slider 
                        v-model="formData.imageQuality"
                        :step="10"
                        :marks="{
                          0: '低',
                          50: '中',
                          100: '高'
                        }"
                      />
                    </el-form-item>
                    
                    <el-form-item label="添加水印">
                      <el-switch v-model="formData.watermark" />
                    </el-form-item>
                  </el-collapse-item>
                </el-collapse>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>

        <el-col :span="8">
          <el-card class="preview-card">
            <template #header>
              <div class="card-header">
                <h3>预览</h3>
                <el-button 
                  size="small"
                  @click="refreshPreview"
                  :loading="previewLoading"
                >
                  刷新预览
                </el-button>
              </div>
            </template>
            
            <div v-if="previewLoading" class="preview-loading">
              <el-skeleton :rows="10" animated />
            </div>
            <div v-else-if="previewUrl" class="preview-content">
              <iframe :src="previewUrl" frameborder="0"></iframe>
            </div>
            <el-empty v-else description="暂无预览" />
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useCreativeStore } from '@/stores/creative'
import type { FormInstance } from 'element-plus/es/components/form'

const route = useRoute()
const router = useRouter()
const store = useCreativeStore()
const formRef = ref<FormInstance>()
const exporting = ref(false)
const previewLoading = ref(false)
const previewUrl = ref('')

const projectId = route.params.id as string

const formData = ref({
  format: 'pdf',
  sections: ['project_info', 'document_analysis', 'market_analysis', 'solution', 'evaluation'],
  template: 'business',
  pageSize: 'a4',
  imageQuality: 80,
  watermark: false
})

// 监听表单变化，自动更新预览
watch(
  formData,
  () => {
    refreshPreview()
  },
  { deep: true }
)

async function refreshPreview() {
  previewLoading.value = true
  try {
    const response = await store.getExportPreview(projectId, formData.value)
    previewUrl.value = response.preview_url
  } catch (error) {
    ElMessage.error('获取预览失败')
  } finally {
    previewLoading.value = false
  }
}

async function exportProject() {
  if (!formData.value.sections.length) {
    ElMessage.warning('请选择要导出的内容')
    return
  }

  exporting.value = true
  try {
    const response = await store.exportProject(projectId, formData.value)
    window.open(response.download_url, '_blank')
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
  } finally {
    exporting.value = false
  }
}

function nextStep() {
  router.push(`/creative/projects/${projectId}/settings`)
}
</script>

<style lang="scss" scoped>
.project-export {
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
  
  .export-content {
    .export-card,
    .preview-card {
      height: 100%;
      background: var(--color-secondary);
      border: 1px solid rgba(255, 255, 255, 0.1);
      
      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        
        h3 {
          margin: 0;
          color: var(--color-text-primary);
        }
      }
    }
    
    .preview-content {
      height: 600px;
      
      iframe {
        width: 100%;
        height: 100%;
        background: var(--color-primary);
      }
    }
  }
}
</style> 