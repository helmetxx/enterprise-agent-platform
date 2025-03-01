<template>
  <div class="home-container">
    <!-- 侧边栏 -->
    <div class="sidebar">
      <div class="logo">
        <img src="/assets/logo.svg" alt="Logo" />
      </div>
      <el-menu
        class="sidebar-menu"
        :default-active="activeMenu"
        background-color="transparent"
        text-color="var(--color-text-secondary)"
        active-text-color="var(--color-text-primary)"
      >
        <el-menu-item index="dashboard">
          <el-icon><Monitor /></el-icon>
          <span>工作台</span>
        </el-menu-item>
        <el-menu-item index="agents">
          <el-icon><Magic /></el-icon>
          <span>智能体市场</span>
        </el-menu-item>
        <el-menu-item index="history">
          <el-icon><Timer /></el-icon>
          <span>使用记录</span>
        </el-menu-item>
      </el-menu>
    </div>

    <!-- 主内容区 -->
    <div class="main-content">
      <!-- 顶部栏 -->
      <div class="top-bar">
        <div class="search-bar">
          <el-input
            v-model="searchQuery"
            placeholder="搜索智能体..."
            prefix-icon="Search"
          />
        </div>
        <div class="user-info">
          <el-dropdown trigger="click">
            <el-avatar :size="40" :src="defaultAvatar" />
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>个人设置</el-dropdown-item>
                <el-dropdown-item divided @click="handleLogout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>

      <!-- 内容区 -->
      <div class="content">
        <!-- 快捷操作区 -->
        <section class="quick-actions">
          <h2>快捷操作</h2>
          <div class="action-cards">
            <el-card v-for="action in quickActions" :key="action.id" class="action-card">
              <div class="action-icon">
                <el-icon><component :is="action.icon" /></el-icon>
              </div>
              <h3>{{ action.title }}</h3>
              <p>{{ action.description }}</p>
            </el-card>
          </div>
        </section>

        <!-- 推荐智能体 -->
        <section class="recommended-agents">
          <h2>推荐智能体</h2>
          <div class="agent-cards">
            <el-card v-for="agent in recommendedAgents" :key="agent.id" class="agent-card">
              <img :src="agent.icon" :alt="agent.name" class="agent-icon">
              <h3>{{ agent.name }}</h3>
              <p>{{ agent.description }}</p>
              <div class="agent-tags">
                <el-tag v-for="tag in agent.tags" :key="tag" size="small">{{ tag }}</el-tag>
              </div>
              <el-button type="primary" @click="startChat(agent.id)">开始对话</el-button>
            </el-card>
          </div>
        </section>

        <!-- 最近使用 -->
        <section class="recent-usage">
          <h2>最近使用</h2>
          <el-table :data="recentUsage" style="width: 100%">
            <el-table-column prop="agentName" label="智能体" />
            <el-table-column prop="lastUsed" label="最后使用时间" />
            <el-table-column prop="status" label="状态" />
            <el-table-column fixed="right" label="操作">
              <template #default="scope">
                <el-button link type="primary" @click="continueChat(scope.row.id)">
                  继续对话
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Monitor, Magic, Timer, Search } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const router = useRouter()
const activeMenu = ref('dashboard')
const searchQuery = ref('')
const defaultAvatar = '/avatar-default.svg'

// 快捷操作数据
const quickActions = ref([
  {
    id: 1,
    title: '创建项目',
    description: '开始一个新的创意项目',
    icon: 'Plus'
  },
  {
    id: 2,
    title: '智能助手',
    description: '获取AI帮助和建议',
    icon: 'ChatDotRound'
  }
])

// 推荐智能体数据
const recommendedAgents = ref([
  {
    id: 1,
    name: '产品创意助手',
    description: '帮助你发现和优化产品创意',
    icon: '/assets/agent-icons/creative.svg',
    tags: ['创意', '产品']
  },
  {
    id: 2,
    name: '营销文案助手',
    description: '生成专业的营销文案',
    icon: '/assets/agent-icons/marketing.svg',
    tags: ['营销', '文案']
  }
])

// 最近使用记录
const recentUsage = ref([
  {
    id: 1,
    agentName: '产品创意助手',
    lastUsed: '2024-01-22 14:30',
    status: '进行中'
  }
])

// 处理函数
const handleLogout = () => {
  // 实现登出逻辑
  router.push('/login')
  ElMessage.success('已退出登录')
}

const startChat = (agentId: number) => {
  router.push(`/chat/${agentId}`)
}

const continueChat = (chatId: number) => {
  router.push(`/chat/${chatId}`)
}
</script>

<style scoped lang="scss">
.home-container {
  display: flex;
  min-height: 100vh;
  background: var(--color-primary);
}

.sidebar {
  width: 240px;
  background: rgba(45, 45, 45, 0.7);
  backdrop-filter: blur(10px);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  padding: 20px 0;
  
  .logo {
    padding: 0 20px;
    margin-bottom: 30px;
    img {
      height: 40px;
    }
  }
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.top-bar {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 30px;
  background: rgba(45, 45, 45, 0.7);
  backdrop-filter: blur(10px);
  
  .search-bar {
    width: 300px;
  }
}

.content {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
  
  section {
    margin-bottom: 40px;
    
    h2 {
      color: var(--color-text-primary);
      margin-bottom: 20px;
    }
  }
}

.action-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  
  .action-card {
    background: rgba(45, 45, 45, 0.7);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: transform 0.3s;
    
    &:hover {
      transform: translateY(-5px);
    }
    
    .action-icon {
      font-size: 24px;
      margin-bottom: 10px;
      color: var(--color-button-primary);
    }
  }
}

.agent-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  
  .agent-card {
    background: rgba(45, 45, 45, 0.7);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: transform 0.3s;
    
    &:hover {
      transform: translateY(-5px);
    }
    
    .agent-icon {
      width: 60px;
      height: 60px;
      margin-bottom: 15px;
    }
    
    .agent-tags {
      margin: 10px 0;
      .el-tag {
        margin-right: 8px;
        margin-bottom: 8px;
      }
    }
  }
}

:deep(.el-table) {
  background: transparent;
  
  th, td {
    background: rgba(45, 45, 45, 0.7);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  th {
    color: var(--color-text-secondary);
  }
  
  td {
    color: var(--color-text-primary);
  }
}
</style> 