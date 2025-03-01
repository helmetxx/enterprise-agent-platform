<template>
  <div class="dashboard">
    <div class="welcome-section">
      <h2>欢迎使用企业智能助手平台</h2>
      <p>这里是您的个人工作空间</p>
    </div>

    <el-row :gutter="20" class="section">
      <el-col :span="24">
        <h3 class="section-title">
          <el-icon><Timer /></el-icon>
          最近使用
        </h3>
      </el-col>
      <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="record in recentUsage" :key="record.id">
        <el-card class="usage-card">
          <div class="usage-info">
            <img :src="record.agent.icon || defaultAgentIcon" :alt="record.agent.name">
            <div class="usage-details">
              <h4>{{ record.agent.name }}</h4>
              <p>{{ formatTime(record.usedAt) }}</p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="section">
      <el-col :span="24">
        <div class="section-header">
          <h3 class="section-title">
            <el-icon><Connection /></el-icon>
            推荐智能体
          </h3>
          <router-link to="/dashboard/market" class="view-more">
            查看更多
          </router-link>
        </div>
      </el-col>
      <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="agent in recommendedAgents" :key="agent.id">
        <el-card class="agent-card" @click="navigateToAgent(agent)">
          <div class="agent-icon">
            <img :src="agent.icon || defaultAgentIcon" :alt="agent.name">
          </div>
          <div class="agent-info">
            <h4>{{ agent.name }}</h4>
            <p>{{ agent.description }}</p>
            <div class="agent-tags">
              <el-tag size="small" v-for="tag in agent.tags" :key="tag">{{ tag }}</el-tag>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Timer, Connection } from '@element-plus/icons-vue'
import { formatTime } from '@/utils/date'
import { useAgentStore } from '@/stores/agent'
import type { Agent, UsageRecord } from '@/types/agent'
import Logger from '@/utils/logger'

const router = useRouter()
const agentStore = useAgentStore()
const defaultAgentIcon = '/assets/default-agent-icon.png'

const recentUsage = ref<UsageRecord[]>([])
const recommendedAgents = ref<Agent[]>([])

onMounted(async () => {
  try {
    // 获取最近使用记录
    recentUsage.value = await agentStore.getRecentUsage()
    // 获取推荐智能体
    recommendedAgents.value = await agentStore.getRecommendedAgents()
  } catch (error) {
    Logger.error('Failed to load dashboard data:', error)
  }
})

const navigateToAgent = (agent: Agent) => {
  // 根据不同的 agent.id 跳转到对应的智能应用
  switch(agent.id) {
    case 'agent-001':
      router.push('/dashboard/creative')
      break
    // 后续其他智能应用的路由
    default:
      router.push(`/agent/${agent.id}`)
  }
}

const navigateToMarket = () => {
  router.push('/market')
}
</script>

<style lang="scss" scoped>
.dashboard {
  padding: 20px;

  .welcome-section {
    margin-bottom: 40px;
    
    h2 {
      font-size: 24px;
      color: var(--el-text-color-primary);
      margin-bottom: 8px;
    }
    
    p {
      color: var(--el-text-color-secondary);
    }
  }

  .section {
    margin-bottom: 40px;

    .section-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;

      .view-more {
        text-decoration: none;
        color: var(--el-color-primary);
        &:hover {
          text-decoration: underline;
        }
      }
    }

    .section-title {
      display: flex;
      align-items: center;
      font-size: 18px;
      margin-bottom: 20px;

      .el-icon {
        margin-right: 8px;
        font-size: 20px;
      }
    }
  }

  .agent-card {
    height: 100%;
    cursor: pointer;
    transition: all 0.3s;

    &:hover {
      transform: translateY(-5px);
      box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
    }

    .agent-icon {
      width: 60px;
      height: 60px;
      margin-bottom: 16px;

      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 8px;
      }
    }

    .agent-info {
      h4 {
        margin: 0 0 8px;
        font-size: 16px;
      }

      p {
        margin: 0 0 12px;
        color: var(--el-text-color-secondary);
        font-size: 14px;
      }

      .agent-tags {
        .el-tag {
          margin-right: 8px;
          margin-bottom: 8px;
        }
      }
    }
  }

  .usage-card {
    .usage-info {
      display: flex;
      align-items: center;

      img {
        width: 40px;
        height: 40px;
        border-radius: 4px;
        margin-right: 12px;
      }

      .usage-details {
        h4 {
          margin: 0 0 4px;
          font-size: 14px;
        }

        p {
          margin: 0;
          color: var(--el-text-color-secondary);
          font-size: 12px;
        }
      }
    }
  }
}
</style> 