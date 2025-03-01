<template>
  <div class="agent-market">
    <el-row :gutter="20">
      <el-col :span="6" v-for="agent in agents" :key="agent.id">
        <el-card class="agent-card" :body-style="{ padding: '0px' }">
          <img :src="agent.icon" class="agent-image">
          <div class="agent-info">
            <h3>{{ agent.name }}</h3>
            <p>{{ agent.description }}</p>
            <div class="agent-tags">
              <el-tag 
                v-for="capability in agent.capabilities" 
                :key="capability"
                size="small"
              >
                {{ capability }}
              </el-tag>
            </div>
            <el-button 
              type="primary" 
              @click="startChat(agent.id)"
            >
              开始对话
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAgentStore } from '@/stores/agent'
import type { Agent } from '@/types'

const router = useRouter()
const agentStore = useAgentStore()
const agents = ref<Agent[]>([])

onMounted(async () => {
  try {
    agents.value = await agentStore.fetchAgents()
  } catch (error) {
    console.error('Failed to fetch agents:', error)
  }
})

const startChat = (agentId: string) => {
  router.push(`/chat/${agentId}`)
}
</script>

<style scoped>
.agent-market {
  padding: 20px;
}

.agent-card {
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.agent-card:hover {
  transform: translateY(-5px);
}

.agent-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.agent-info {
  padding: 15px;
}

.agent-tags {
  margin: 10px 0;
}

.agent-tags .el-tag {
  margin-right: 5px;
  margin-bottom: 5px;
}
</style> 