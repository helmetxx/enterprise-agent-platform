<template>
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
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { Agent } from '@/types/agent'

const props = defineProps<{
  agent: Agent
}>()

const router = useRouter()
const defaultAgentIcon = '/assets/default-agent-icon.png'

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
</script>

<style lang="scss" scoped>
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
</style> 