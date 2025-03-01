<template>
  <div class="image-generation">
    <div class="page-header">
      <h1>图片生成</h1>
      <el-button-group>
        <el-button 
          type="primary"
          :loading="generating"
          @click="generateImage"
        >
          生成图片
        </el-button>
        <el-button @click="nextStep">
          下一步
        </el-button>
      </el-button-group>
    </div>

    <div class="image-content">
      <el-row :gutter="20">
        <el-col :span="8">
          <el-card class="params-card">
            <template #header>
              <div class="card-header">
                <h3>生成参数</h3>
              </div>
            </template>
            <el-form 
              ref="formRef"
              :model="formData"
              label-position="top"
            >
              <el-form-item label="提示词">
                <el-input
                  v-model="formData.prompt"
                  type="textarea"
                  :rows="4"
                  placeholder="描述你想要生成的图片..."
                />
              </el-form-item>

              <el-form-item label="风格">
                <el-select
                  v-model="formData.style"
                  placeholder="选择图片风格"
                >
                  <el-option label="写实风格" value="realistic" />
                  <el-option label="卡通风格" value="cartoon" />
                  <el-option label="水彩风格" value="watercolor" />
                  <el-option label="素描风格" value="sketch" />
                  <el-option label="科技风格" value="tech" />
                </el-select>
              </el-form-item>

              <el-form-item label="尺寸">
                <el-radio-group v-model="formData.size">
                  <el-radio-button label="1:1">正方形</el-radio-button>
                  <el-radio-button label="4:3">横向</el-radio-button>
                  <el-radio-button label="3:4">纵向</el-radio-button>
                </el-radio-group>
              </el-form-item>

              <el-form-item label="高级选项">
                <el-collapse>
                  <el-collapse-item title="详细参数" name="1">
                    <el-form-item label="细节程度">
                      <el-slider 
                        v-model="formData.detail"
                        :step="1"
                        :marks="{
                          1: '简略',
                          2: '标准',
                          3: '精细'
                        }"
                        :min="1"
                        :max="3"
                      />
                    </el-form-item>
                    <el-form-item label="负面提示词">
                      <el-input
                        v-model="formData.negativePrompt"
                        type="textarea"
                        :rows="2"
                        placeholder="不希望出现的元素..."
                      />
                    </el-form-item>
                  </el-collapse-item>
                </el-collapse>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>

        <el-col :span="16">
          <el-card class="gallery-card">
            <template #header>
              <div class="card-header">
                <h3>生成结果</h3>
                <el-button-group>
                  <el-button size="small" @click="downloadSelected">
                    下载选中
                  </el-button>
                  <el-button size="small" @click="regenerate">
                    重新生成
                  </el-button>
                </el-button-group>
              </div>
            </template>
            
            <div v-if="loading" class="gallery-loading">
              <el-skeleton :rows="3" animated />
            </div>
            <div v-else-if="images.length" class="gallery-grid">
              <div 
                v-for="image in images" 
                :key="image.id"
                class="image-item"
                :class="{ selected: selectedImages.includes(image.id) }"
                @click="toggleSelect(image.id)"
              >
                <el-image
                  :src="image.image_url"
                  fit="cover"
                  :preview-src-list="[image.image_url]"
                >
                  <template #placeholder>
                    <div class="image-placeholder">
                      <el-icon><Picture /></el-icon>
                    </div>
                  </template>
                </el-image>
                <div class="image-info">
                  <span class="image-time">{{ formatTime(image.created_at) }}</span>
                  <el-button-group>
                    <el-button 
                      size="small"
                      circle
                      @click.stop="downloadImage(image)"
                    >
                      <el-icon><Download /></el-icon>
                    </el-button>
                    <el-button 
                      size="small"
                      circle
                      @click.stop="showPrompt(image)"
                    >
                      <el-icon><InfoFilled /></el-icon>
                    </el-button>
                  </el-button-group>
                </div>
              </div>
            </div>
            <el-empty v-else description="暂无生成图片" />
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 提示词对话框 -->
    <el-dialog
      v-model="promptDialogVisible"
      title="生成参数"
      width="500px"
    >
      <div v-if="currentImage" class="prompt-detail">
        <h4>提示词</h4>
        <pre>{{ currentImage.prompt_used }}</pre>
        <h4>风格配置</h4>
        <pre>{{ JSON.stringify(currentImage.style_config, null, 2) }}</pre>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Picture, Download, InfoFilled } from '@element-plus/icons-vue'
import { useCreativeStore } from '@/stores/creative'
import { formatTime } from '@/utils/date'
import type { GeneratedImage } from '@/types/creative'

const route = useRoute()
const router = useRouter()
const store = useCreativeStore()
const loading = ref(false)
const generating = ref(false)
const promptDialogVisible = ref(false)
const currentImage = ref<GeneratedImage | null>(null)
const selectedImages = ref<string[]>([])

const projectId = route.params.id as string
const ideaId = route.query.ideaId as string

const formData = ref({
  prompt: '',
  style: 'realistic',
  size: '1:1',
  detail: 2,
  negativePrompt: ''
})

const images = ref<GeneratedImage[]>([])

onMounted(async () => {
  if (ideaId) {
    await fetchImages()
  }
})

async function fetchImages() {
  loading.value = true
  try {
    const response = await store.getGeneratedImages(ideaId)
    images.value = response
  } catch (error) {
    ElMessage.error('获取图片列表失败')
  } finally {
    loading.value = false
  }
}

async function generateImage() {
  if (!formData.value.prompt) {
    ElMessage.warning('请输入提示词')
    return
  }

  generating.value = true
  try {
    const response = await store.createGeneratedImage(projectId, ideaId, {
      prompt_used: formData.value.prompt,
      style_config: {
        style: formData.value.style,
        size: formData.value.size,
        detail: formData.value.detail,
        negative_prompt: formData.value.negativePrompt
      }
    })
    images.value.unshift(response)
    ElMessage.success('图片生成成功')
  } catch (error) {
    ElMessage.error('图片生成失败')
  } finally {
    generating.value = false
  }
}

function toggleSelect(imageId: string) {
  const index = selectedImages.value.indexOf(imageId)
  if (index === -1) {
    selectedImages.value.push(imageId)
  } else {
    selectedImages.value.splice(index, 1)
  }
}

function showPrompt(image: GeneratedImage) {
  currentImage.value = image
  promptDialogVisible.value = true
}

async function downloadImage(image: GeneratedImage) {
  try {
    const response = await fetch(image.image_url)
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `image-${image.id}.png`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  } catch (error) {
    ElMessage.error('下载失败')
  }
}

async function downloadSelected() {
  if (!selectedImages.value.length) {
    ElMessage.warning('请选择要下载的图片')
    return
  }

  for (const imageId of selectedImages.value) {
    const image = images.value.find(img => img.id === imageId)
    if (image) {
      await downloadImage(image)
    }
  }
}

function regenerate() {
  if (currentImage.value) {
    formData.value.prompt = currentImage.value.prompt_used
    formData.value = {
      ...formData.value,
      ...currentImage.value.style_config
    }
  }
}

function nextStep() {
  router.push(`/creative/projects/${projectId}/solution`)
}
</script>

<style lang="scss" scoped>
.image-generation {
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
  
  .image-content {
    .params-card,
    .gallery-card {
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
    
    .gallery-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: var(--spacing-base);
      
      .image-item {
        position: relative;
        border-radius: var(--border-radius-small);
        overflow: hidden;
        cursor: pointer;
        
        &.selected {
          outline: 2px solid var(--color-button-primary);
        }
        
        .el-image {
          width: 100%;
          height: 200px;
          background: var(--color-primary);
        }
        
        .image-info {
          position: absolute;
          bottom: 0;
          left: 0;
          right: 0;
          padding: 8px;
          background: rgba(0, 0, 0, 0.7);
          display: flex;
          justify-content: space-between;
          align-items: center;
          
          .image-time {
            color: var(--color-text-secondary);
            font-size: 12px;
          }
        }
      }
    }
  }
  
  .prompt-detail {
    h4 {
      color: var(--color-text-primary);
      margin: 16px 0 8px;
      
      &:first-child {
        margin-top: 0;
      }
    }
    
    pre {
      background: var(--color-primary);
      padding: var(--spacing-base);
      border-radius: var(--border-radius-small);
      overflow: auto;
      margin: 0;
    }
  }
}
</style> 