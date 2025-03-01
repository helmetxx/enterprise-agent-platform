<template>
  <div class="idea-generation">
    <div class="page-header">
      <h1>创意生成</h1>
      <el-button-group>
        <el-button 
          type="primary"
          :loading="generating"
          @click="generateIdea"
        >
          生成创意
        </el-button>
        <el-button @click="nextStep">
          下一步
        </el-button>
      </el-button-group>
    </div>

    <div class="idea-content">
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
              <el-form-item label="创新程度">
                <el-rate 
                  v-model="formData.innovationLevel"
                  :max="5"
                  :texts="['保守', '谨慎', '平衡', '创新', '颠覆']"
                  show-text
                />
              </el-form-item>

              <el-form-item label="关键词">
                <el-select
                  v-model="formData.keywords"
                  multiple
                  filterable
                  allow-create
                  default-first-option
                  placeholder="输入关键词"
                >
                  <el-option
                    v-for="item in suggestedKeywords"
                    :key="item"
                    :label="item"
                    :value="item"
                  />
                </el-select>
              </el-form-item>

              <el-form-item label="约束条件">
                <el-checkbox-group v-model="formData.constraints">
                  <el-checkbox label="cost">成本控制</el-checkbox>
                  <el-checkbox label="time">时间限制</el-checkbox>
                  <el-checkbox label="tech">技术可行</el-checkbox>
                  <el-checkbox label="market">市场需求</el-checkbox>
                </el-checkbox-group>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>

        <el-col :span="16">
          <el-card class="ideas-card">
            <template #header>
              <div class="card-header">
                <h3>创意列表</h3>
                <el-button-group>
                  <el-button size="small" @click="sortByScore">
                    按评分排序
                  </el-button>
                  <el-button size="small" @click="filterHighScore">
                    筛选高分
                  </el-button>
                </el-button-group>
              </div>
            </template>
            
            <div v-if="loading" class="ideas-loading">
              <el-skeleton :rows="10" animated />
            </div>
            <div v-else-if="ideas.length" class="ideas-list">
              <el-collapse v-model="activeIdeas">
                <el-collapse-item
                  v-for="idea in displayIdeas"
                  :key="idea.id"
                  :title="getIdeaTitle(idea)"
                  :name="idea.id"
                >
                  <div class="idea-detail">
                    <div class="idea-score">
                      <el-rate
                        v-model="idea.evaluation_score"
                        disabled
                        show-score
                        text-color="#ff9900"
                      />
                    </div>
                    <div class="idea-content">
                      <pre>{{ JSON.stringify(idea.idea_content, null, 2) }}</pre>
                    </div>
                    <div class="idea-actions">
                      <el-button-group>
                        <el-button 
                          type="primary" 
                          size="small"
                          @click="selectIdea(idea)"
                        >
                          选择此创意
                        </el-button>
                        <el-button 
                          size="small"
                          @click="generateImage(idea.id)"
                        >
                          生成图片
                        </el-button>
                      </el-button-group>
                    </div>
                  </div>
                </el-collapse-item>
              </el-collapse>
            </div>
            <el-empty v-else description="暂无创意" />
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useCreativeStore } from '@/stores/creative'
import type { IdeaGeneration } from '@/types/creative'

const route = useRoute()
const router = useRouter()
const store = useCreativeStore()
const loading = ref(false)
const generating = ref(false)
const activeIdeas = ref<string[]>([])

const projectId = route.params.id as string

const formData = ref({
  innovationLevel: 3,
  keywords: [] as string[],
  constraints: [] as string[]
})

const suggestedKeywords = ref([
  '智能化',
  '可持续',
  '用户体验',
  '成本效益',
  '创新设计'
])

const ideas = ref<IdeaGeneration[]>([])
const displayIdeas = computed(() => ideas.value)

onMounted(async () => {
  await fetchIdeas()
})

async function fetchIdeas() {
  loading.value = true
  try {
    const response = await store.getIdeas(projectId)
    ideas.value = response
  } catch (error) {
    ElMessage.error('获取创意列表失败')
  } finally {
    loading.value = false
  }
}

function getIdeaTitle(idea: IdeaGeneration): string {
  return idea.idea_content.title || `创意 ${idea.id.slice(0, 8)}`
}

async function generateIdea() {
  if (!formData.value.keywords.length) {
    ElMessage.warning('请至少输入一个关键词')
    return
  }

  generating.value = true
  try {
    const response = await store.createIdea(projectId, {
      idea_content: {
        ...formData.value
      }
    })
    ideas.value.unshift(response)
    activeIdeas.value = [response.id]
    ElMessage.success('创意生成成功')
  } catch (error) {
    ElMessage.error('创意生成失败')
  } finally {
    generating.value = false
  }
}

function sortByScore() {
  ideas.value.sort((a, b) => b.evaluation_score - a.evaluation_score)
}

function filterHighScore() {
  ideas.value = ideas.value.filter(idea => idea.evaluation_score >= 4)
}

function selectIdea(idea: IdeaGeneration) {
  store.setCurrentIdea(idea)
  ElMessage.success('已选择创意')
}

function generateImage(ideaId: string) {
  router.push(`/creative/projects/${projectId}/images?ideaId=${ideaId}`)
}

function nextStep() {
  router.push(`/creative/projects/${projectId}/images`)
}
</script>

<style lang="scss" scoped>
.idea-generation {
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
  
  .idea-content {
    .params-card,
    .ideas-card {
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
    
    .idea-detail {
      .idea-score {
        margin-bottom: var(--spacing-base);
      }
      
      .idea-content {
        pre {
          background: var(--color-primary);
          padding: var(--spacing-base);
          border-radius: var(--border-radius-small);
          overflow: auto;
        }
      }
      
      .idea-actions {
        margin-top: var(--spacing-base);
        text-align: right;
      }
    }
  }
}
</style> 