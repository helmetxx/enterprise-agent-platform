<template>
  <div class="project-evaluation">
    <div class="page-header">
      <h1>项目评估</h1>
      <el-button-group>
        <el-button 
          type="primary"
          :loading="evaluating"
          @click="startEvaluation"
        >
          开始评估
        </el-button>
        <el-button @click="nextStep">
          下一步
        </el-button>
      </el-button-group>
    </div>

    <div class="evaluation-content">
      <el-row :gutter="20">
        <el-col :span="16">
          <el-card class="evaluation-card">
            <template #header>
              <div class="card-header">
                <h3>评估报告</h3>
              </div>
            </template>
            
            <div v-if="loading" class="evaluation-loading">
              <el-skeleton :rows="10" animated />
            </div>
            <div v-else-if="evaluation" class="evaluation-report">
              <el-descriptions border>
                <el-descriptions-item label="创新性评分">
                  <el-rate
                    v-model="evaluation.innovation_score"
                    disabled
                    show-score
                  />
                </el-descriptions-item>
                <el-descriptions-item label="可行性评分">
                  <el-rate
                    v-model="evaluation.feasibility_score"
                    disabled
                    show-score
                  />
                </el-descriptions-item>
                <el-descriptions-item label="市场潜力评分">
                  <el-rate
                    v-model="evaluation.market_score"
                    disabled
                    show-score
                  />
                </el-descriptions-item>
              </el-descriptions>

              <div class="evaluation-details">
                <h4>创新亮点</h4>
                <ul>
                  <li v-for="(point, index) in evaluation.innovation_points" :key="index">
                    {{ point }}
                  </li>
                </ul>

                <h4>技术挑战</h4>
                <ul>
                  <li v-for="(challenge, index) in evaluation.technical_challenges" :key="index">
                    {{ challenge }}
                  </li>
                </ul>

                <h4>市场机会</h4>
                <ul>
                  <li v-for="(opportunity, index) in evaluation.market_opportunities" :key="index">
                    {{ opportunity }}
                  </li>
                </ul>

                <h4>风险提示</h4>
                <el-alert
                  v-for="(risk, index) in evaluation.risk_alerts"
                  :key="index"
                  :title="risk.title"
                  :type="risk.level"
                  :description="risk.description"
                  show-icon
                  :closable="false"
                  class="risk-alert"
                />
              </div>

              <div class="evaluation-summary">
                <h4>总体评价</h4>
                <div class="summary-content">
                  {{ evaluation.summary }}
                </div>
                
                <h4>建议改进</h4>
                <el-timeline>
                  <el-timeline-item
                    v-for="(suggestion, index) in evaluation.improvement_suggestions"
                    :key="index"
                    :type="suggestion.priority === 'high' ? 'danger' : 'primary'"
                  >
                    <h5>{{ suggestion.title }}</h5>
                    <p>{{ suggestion.content }}</p>
                  </el-timeline-item>
                </el-timeline>
              </div>
            </div>
            <el-empty v-else description="暂无评估报告" />
          </el-card>
        </el-col>

        <el-col :span="8">
          <el-card class="metrics-card">
            <template #header>
              <div class="card-header">
                <h3>关键指标</h3>
              </div>
            </template>
            
            <div v-if="evaluation" class="metrics-list">
              <div 
                v-for="metric in evaluation.key_metrics" 
                :key="metric.name"
                class="metric-item"
              >
                <div class="metric-header">
                  <span class="metric-name">{{ metric.name }}</span>
                  <el-tag :type="getMetricStatus(metric.status)">
                    {{ metric.status }}
                  </el-tag>
                </div>
                <el-progress 
                  :percentage="metric.value" 
                  :status="getProgressStatus(metric.status)"
                />
                <p class="metric-description">{{ metric.description }}</p>
              </div>
            </div>
            <el-empty v-else description="暂无指标数据" />
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

interface EvaluationMetric {
  name: string
  value: number
  status: 'excellent' | 'good' | 'normal' | 'warning' | 'danger'
  description: string
}

interface RiskAlert {
  title: string
  level: 'success' | 'warning' | 'error'
  description: string
}

interface ImprovementSuggestion {
  title: string
  content: string
  priority: 'high' | 'medium' | 'low'
}

interface ProjectEvaluation {
  innovation_score: number
  feasibility_score: number
  market_score: number
  innovation_points: string[]
  technical_challenges: string[]
  market_opportunities: string[]
  risk_alerts: RiskAlert[]
  summary: string
  improvement_suggestions: ImprovementSuggestion[]
  key_metrics: EvaluationMetric[]
}

const route = useRoute()
const router = useRouter()
const store = useCreativeStore()
const loading = ref(false)
const evaluating = ref(false)

const projectId = route.params.id as string
const evaluation = ref<ProjectEvaluation | null>(null)

onMounted(async () => {
  await fetchEvaluation()
})

async function fetchEvaluation() {
  loading.value = true
  try {
    const response = await store.getEvaluation(projectId)
    evaluation.value = response
  } catch (error) {
    ElMessage.error('获取评估报告失败')
  } finally {
    loading.value = false
  }
}

async function startEvaluation() {
  evaluating.value = true
  try {
    const response = await store.createEvaluation(projectId)
    evaluation.value = response
    ElMessage.success('评估完成')
  } catch (error) {
    ElMessage.error('评估失败')
  } finally {
    evaluating.value = false
  }
}

function getMetricStatus(status: string): 'success' | 'warning' | 'danger' {
  const statusMap: Record<string, 'success' | 'warning' | 'danger'> = {
    excellent: 'success',
    good: 'success',
    normal: 'warning',
    warning: 'warning',
    danger: 'danger'
  }
  return statusMap[status] || 'warning'
}

function getProgressStatus(status: string): '' | 'success' | 'warning' | 'exception' {
  const statusMap: Record<string, '' | 'success' | 'warning' | 'exception'> = {
    excellent: 'success',
    good: 'success',
    normal: '',
    warning: 'warning',
    danger: 'exception'
  }
  return statusMap[status] || ''
}

function nextStep() {
  router.push(`/creative/projects/${projectId}/export`)
}
</script>

<style lang="scss" scoped>
.project-evaluation {
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
  
  .evaluation-content {
    .evaluation-card,
    .metrics-card {
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
    
    .evaluation-details {
      margin-top: var(--spacing-large);
      
      h4 {
        color: var(--color-text-primary);
        margin: 20px 0 10px;
        
        &:first-child {
          margin-top: 0;
        }
      }
      
      ul {
        margin: 0;
        padding-left: 20px;
        color: var(--color-text-secondary);
      }
      
      .risk-alert {
        margin-bottom: 10px;
      }
    }
    
    .evaluation-summary {
      margin-top: var(--spacing-large);
      
      h4 {
        color: var(--color-text-primary);
        margin: 20px 0 10px;
      }
      
      .summary-content {
        color: var(--color-text-secondary);
        line-height: 1.6;
      }
      
      h5 {
        color: var(--color-text-primary);
        margin: 0 0 5px;
      }
      
      p {
        color: var(--color-text-secondary);
        margin: 0;
      }
    }
    
    .metrics-list {
      .metric-item {
        margin-bottom: var(--spacing-base);
        
        .metric-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 8px;
          
          .metric-name {
            color: var(--color-text-primary);
            font-weight: 500;
          }
        }
        
        .metric-description {
          margin: 8px 0 0;
          color: var(--color-text-secondary);
          font-size: 12px;
        }
      }
    }
  }
}
</style> 