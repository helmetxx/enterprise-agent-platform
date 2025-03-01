<template>
  <div class="solution-design">
    <div class="page-header">
      <h1>方案设计</h1>
      <el-button-group>
        <el-button 
          type="primary"
          :loading="generating"
          @click="generateSolution"
        >
          生成方案
        </el-button>
        <el-button @click="nextStep">
          下一步
        </el-button>
      </el-button-group>
    </div>

    <div class="solution-content">
      <el-row :gutter="20">
        <el-col :span="8">
          <el-card class="params-card">
            <template #header>
              <div class="card-header">
                <h3>设计参数</h3>
              </div>
            </template>
            <el-form 
              ref="formRef"
              :model="formData"
              label-position="top"
            >
              <el-form-item label="技术路线">
                <el-select
                  v-model="formData.techStack"
                  multiple
                  placeholder="选择技术路线"
                >
                  <el-option label="Web技术" value="web" />
                  <el-option label="移动端" value="mobile" />
                  <el-option label="人工智能" value="ai" />
                  <el-option label="物联网" value="iot" />
                  <el-option label="区块链" value="blockchain" />
                </el-select>
              </el-form-item>

              <el-form-item label="实现难度">
                <el-rate 
                  v-model="formData.difficulty"
                  :max="5"
                  :texts="['简单', '较易', '适中', '较难', '复杂']"
                  show-text
                />
              </el-form-item>

              <el-form-item label="开发周期">
                <el-select
                  v-model="formData.timeline"
                  placeholder="选择开发周期"
                >
                  <el-option label="1-3个月" value="short" />
                  <el-option label="3-6个月" value="medium" />
                  <el-option label="6-12个月" value="long" />
                  <el-option label="1年以上" value="very_long" />
                </el-select>
              </el-form-item>

              <el-form-item label="资源需求">
                <el-checkbox-group v-model="formData.resources">
                  <el-checkbox label="frontend">前端开发</el-checkbox>
                  <el-checkbox label="backend">后端开发</el-checkbox>
                  <el-checkbox label="devops">运维支持</el-checkbox>
                  <el-checkbox label="ai">AI工程师</el-checkbox>
                  <el-checkbox label="pm">项目经理</el-checkbox>
                </el-checkbox-group>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>

        <el-col :span="16">
          <el-card v-loading="loading" class="solution-card">
            <template #header>
              <div class="card-header">
                <h3>方案详情</h3>
              </div>
            </template>
            
            <div v-if="solution" class="solution-detail">
              <h4>技术架构</h4>
              <pre>{{ JSON.stringify(solution.technical_solution, null, 2) }}</pre>

              <h4>可行性分析</h4>
              <pre>{{ JSON.stringify(solution.feasibility_study, null, 2) }}</pre>

              <h4>实施路径</h4>
              <el-timeline>
                <el-timeline-item
                  v-for="phase in solution.implementation_path.phases"
                  :key="phase.name"
                  :type="getTimelineItemType(phase.status)"
                >
                  <h5>{{ phase.name }}</h5>
                  <p>{{ phase.time }}</p>
                  <ul>
                    <li v-for="task in phase.tasks" :key="task">
                      {{ task }}
                    </li>
                  </ul>
                </el-timeline-item>
              </el-timeline>
            </div>
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
import { useCreativeStore } from '@/stores/creative'
import type { SolutionDesign, TimelineStatus } from '@/types/creative'

const route = useRoute()
const router = useRouter()
const store = useCreativeStore()
const loading = ref(false)
const generating = ref(false)

const projectId = route.params.id as string

const formData = ref({
  techStack: [] as string[],
  difficulty: 3,
  timeline: 'medium',
  resources: [] as string[]
})

const solution = ref<SolutionDesign | null>(null)

onMounted(async () => {
  await fetchSolution()
})

async function fetchSolution() {
  loading.value = true
  try {
    const response = await store.getSolution(projectId)
    solution.value = response
  } catch (error) {
    ElMessage.error('获取方案失败')
  } finally {
    loading.value = false
  }
}

async function generateSolution() {
  if (!formData.value.techStack.length || !formData.value.resources.length) {
    ElMessage.warning('请选择技术路线和资源需求')
    return
  }

  generating.value = true
  try {
    const response = await store.createSolution(projectId, {
      technical_solution: {
        tech_stack: formData.value.techStack,
        difficulty: formData.value.difficulty
      },
      feasibility_study: {
        timeline: formData.value.timeline
      },
      implementation_path: {
        resources: formData.value.resources
      }
    })
    solution.value = response
    ElMessage.success('方案生成成功')
  } catch (error) {
    ElMessage.error('方案生成失败')
  } finally {
    generating.value = false
  }
}

function getTimelineItemType(status: TimelineStatus): 'primary' | 'success' | 'warning' | 'danger' {
  const types: Record<TimelineStatus, 'primary' | 'success' | 'warning' | 'danger'> = {
    pending: 'primary',
    completed: 'success',
    in_progress: 'warning',
    blocked: 'danger'
  }
  return types[status]
}

function nextStep() {
  router.push(`/creative/projects/${projectId}/evaluation`)
}
</script>

<style lang="scss" scoped>
.solution-design {
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
  
  .solution-content {
    .params-card,
    .solution-card {
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
    
    .solution-detail {
      h4 {
        color: var(--color-text-primary);
        margin: 20px 0 10px;
        
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
      
      h5 {
        color: var(--color-text-primary);
        margin: 0 0 5px;
      }
      
      p {
        color: var(--color-text-secondary);
        margin: 0;
      }
      
      ul {
        margin: 10px 0 0;
        padding-left: 20px;
        
        li {
          color: var(--color-text-secondary);
        }
      }
    }
  }
}
</style>