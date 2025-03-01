<template>
  <div class="project-list">
    <div class="page-header">
      <h1>我的项目</h1>
      <el-button type="primary" @click="createNewProject">
        创建新项目
      </el-button>
    </div>

    <el-table 
      v-loading="loading"
      :data="projects"
      style="width: 100%"
    >
      <el-table-column prop="title" label="项目名称">
        <template #default="{ row }">
          <router-link :to="`/creative/projects/${row.id}/document`">
            {{ row.title }}
          </router-link>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ getStatusText(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间">
        <template #default="{ row }">
          {{ formatTime(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button-group>
            <el-button 
              size="small"
              @click="viewProject(row.id)"
            >
              查看
            </el-button>
            <el-button 
              size="small"
              type="danger"
              @click="deleteProject(row.id)"
            >
              删除
            </el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useCreativeStore } from '@/stores/creative'
import { formatTime } from '@/utils/date'
import { api } from '@/utils/api'
import type { CreativeProject } from '@/types/creative'

const router = useRouter()
const store = useCreativeStore()
const loading = ref(false)
const projects = ref<CreativeProject[]>([])

// 更新状态处理函数的类型
type StatusType = 'draft' | 'in_progress' | 'completed'
type StatusTypes = Record<StatusType, string>

// 获取项目列表
async function fetchProjects() {
  loading.value = true
  try {
    const response = await api.get('/api/v1/creative/projects/')
    projects.value = response.data
  } catch (error) {
    ElMessage.error('获取项目列表失败')
  } finally {
    loading.value = false
  }
}

// 创建新项目
function createNewProject() {
  router.push('/creative/projects/new')
}

// 查看项目
function viewProject(id: string) {
  router.push(`/creative/projects/${id}/document`)
}

// 删除项目
async function deleteProject(id: string) {
  try {
    await ElMessageBox.confirm('确定要删除该项目吗？', '提示', {
      type: 'warning'
    })
    await api.delete(`/api/v1/creative/projects/${id}`)
    ElMessage.success('删除成功')
    fetchProjects()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 状态处理
function getStatusType(status: StatusType) {
  const types: StatusTypes = {
    draft: 'info',
    in_progress: 'warning',
    completed: 'success'
  }
  return types[status] || 'info'
}

function getStatusText(status: StatusType) {
  const texts: StatusTypes = {
    draft: '草稿',
    in_progress: '进行中',
    completed: '已完成'
  }
  return texts[status] || status
}

onMounted(() => {
  fetchProjects()
})
</script>

<style lang="scss" scoped>
.project-list {
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
}
</style> 