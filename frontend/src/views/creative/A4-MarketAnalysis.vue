<template>
  <div class="market-analysis">
    <div class="page-header">
      <h1>市场分析</h1>
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
          <el-card class="input-card">
            <template #header>
              <div class="card-header">
                <h3>分析参数</h3>
              </div>
            </template>
            <el-form 
              ref="formRef"
              :model="formData"
              label-position="top"
            >
              <el-form-item label="目标市场">
                <el-select 
                  v-model="formData.targetMarket"
                  multiple
                  placeholder="选择目标市场"
                >
                  <el-option label="消费者市场" value="consumer" />
                  <el-option label="企业市场" value="business" />
                  <el-option label="政府市场" value="government" />
                </el-select>
              </el-form-item>

              <el-form-item label="竞品分析维度">
                <el-checkbox-group v-model="formData.competitorDimensions">
                  <el-checkbox label="产品功能">功能对比</el-checkbox>
                  <el-checkbox label="价格策略">价格分析</el-checkbox>
                  <el-checkbox label="市场份额">市场份额</el-checkbox>
                  <el-checkbox label="用户评价">用户反馈</el-checkbox>
                </el-checkbox-group>
              </el-form-item>

              <el-form-item label="分析深度">
                <el-slider 
                  v-model="formData.analysisDepth"
                  :step="1"
                  :marks="{
                    1: '基础',
                    2: '标准',
                    3: '深入'
                  }"
                  :min="1"
                  :max="3"
                />
              </el-form-item>
            </el-form>
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
                <h4>{{ getAnalysisTitle(result) }}</h4>
                <div class="analysis-charts">
                  <!-- 这里可以添加图表组件 -->
                </div>
                <pre>{{ JSON.stringify(result.analysis_data, null, 2) }}</pre>
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
import { useCreativeStore } from '@/stores/creative'
import type { MarketAnalysis } from '@/types/creative'

const route = useRoute()
const router = useRouter()
const store = useCreativeStore()
const loading = ref(false)
const analyzing = ref(false)
const analysisResults = ref<MarketAnalysis[]>([])

const projectId = route.params.id as string

const formData = ref({
  targetMarket: [] as string[],
  competitorDimensions: [] as string[],
  analysisDepth: 2
})

onMounted(async () => {
  await fetchAnalysisResults()
})

async function fetchAnalysisResults() {
  loading.value = true
  try {
    const response = await store.getMarketAnalyses(projectId)
    analysisResults.value = response
  } catch (error) {
    ElMessage.error('获取分析结果失败')
  } finally {
    loading.value = false
  }
}

function getAnalysisTitle(result: MarketAnalysis): string {
  const titles: Record<string, string> = {
    market_size: '市场规模分析',
    competitor: '竞品分析',
    trend: '市场趋势分析'
  }
  return titles[result.analysis_type] || '分析结果'
}

async function startAnalysis() {
  if (!formData.value.targetMarket.length || !formData.value.competitorDimensions.length) {
    ElMessage.warning('请选择目标市场和分析维度')
    return
  }

  analyzing.value = true
  try {
    await store.createMarketAnalysis(projectId, {
      analysis_data: {
        ...formData.value
      }
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
  router.push(`/creative/projects/${projectId}/ideas`)
}
</script>

<style lang="scss" scoped>
.market-analysis {
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
    .input-card,
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