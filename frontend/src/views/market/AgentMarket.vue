<template>
  <div class="agent-market">
    <el-breadcrumb class="breadcrumb">
      <el-breadcrumb-item :to="{ path: '/dashboard' }">工作台</el-breadcrumb-item>
      <el-breadcrumb-item>应用集市</el-breadcrumb-item>
    </el-breadcrumb>

    <div class="search-box">
      <el-input
        v-model="searchQuery"
        placeholder="搜索智能体名称或描述"
        clearable
        @input="handleSearch"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </div>

    <div class="agent-grid">
      <el-row :gutter="20">
        <el-col 
          v-for="agent in agents" 
          :key="agent.id" 
          :xs="24" 
          :sm="12" 
          :md="8" 
          :lg="6"
        >
          <agent-card :agent="agent" />
        </el-col>
      </el-row>
    </div>

    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[20, 40, 60]"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Search } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import AgentCard from '@/components/AgentCard.vue'
import { useAgentStore } from '@/stores/agent'
import type { Agent } from '@/types/agent'

const agentStore = useAgentStore()
const agents = ref<Agent[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const searchQuery = ref('')

const loadAgents = async () => {
  try {
    const response = await agentStore.getAgents({
      page: currentPage.value,
      pageSize: pageSize.value,
      search: searchQuery.value || undefined
    })
    agents.value = response.items || []
    total.value = response.total || 0
  } catch (error) {
    console.error('Failed to load agents:', error)
    ElMessage.error('加载智能体列表失败')
  }
}

const handleSearch = () => {
  currentPage.value = 1
  loadAgents()
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  loadAgents()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  loadAgents()
}

onMounted(() => {
  loadAgents()
})
</script>

<style lang="scss" scoped>
.agent-market {
  padding: 20px;

  .breadcrumb {
    margin-bottom: 20px;
  }

  .search-box {
    margin-bottom: 20px;
    max-width: 400px;
  }

  .agent-grid {
    margin-bottom: 20px;
  }

  .pagination {
    display: flex;
    justify-content: center;
    margin-top: 20px;
  }
}
</style> 