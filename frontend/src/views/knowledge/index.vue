<template>
  <div class="knowledge-base">
    <!-- 面包屑导航 -->
    <el-breadcrumb class="breadcrumb">
      <el-breadcrumb-item :to="{ path: '/dashboard' }">工作台</el-breadcrumb-item>
      <el-breadcrumb-item>知识库管理</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 页面内容 -->
    <div class="page-container">
      <!-- 页面标题区域 -->
      <div class="page-header">
        <div class="header-content">
          <h2>知识库管理</h2>
          <el-button type="primary" @click="createKnowledgeBase">
            <el-icon><Plus /></el-icon>新建知识库
          </el-button>
        </div>
        <p class="description">管理您的知识库资源，支持文档上传和知识检索</p>
      </div>

      <div class="knowledge-list">
        <el-row :gutter="20">
          <!-- 新建知识库卡片 -->
          <el-col :xs="24" :sm="12" :md="8" :lg="6">
            <div class="create-card" @click="createKnowledgeBase">
              <el-icon><Plus /></el-icon>
              <span>新建知识库</span>
            </div>
          </el-col>
          
          <!-- 知识库卡片列表 -->
          <el-col 
            v-for="kb in knowledgeBases" 
            :key="kb.id" 
            :xs="24" 
            :sm="12" 
            :md="8" 
            :lg="6"
          >
            <el-card class="kb-card" :body-style="{ padding: '0px' }">
              <div class="kb-header">
                <el-icon><Folder /></el-icon>
                <span class="kb-name">{{ kb.name }}</span>
              </div>
              <div class="kb-content">
                <p class="kb-description">{{ kb.description || '暂无描述' }}</p>
                <div class="kb-stats">
                  <div class="stat-item">
                    <span class="label">文档数</span>
                    <span class="value">{{ kb.document_count || 0 }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="label">更新时间</span>
                    <span class="value">{{ formatTime(kb.updated_at) }}</span>
                  </div>
                </div>
              </div>
              <div class="kb-actions">
                <el-button-group>
                  <el-button size="small" @click="viewDetail(kb.id)">查看</el-button>
                  <el-button size="small" @click="uploadDocument(kb.id)">上传</el-button>
                  <el-button size="small" type="danger" @click="deleteKnowledgeBase(kb.id)">删除</el-button>
                </el-button-group>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 创建/编辑知识库对话框 -->
      <el-dialog
        v-model="dialogVisible"
        :title="dialogType === 'create' ? '新建知识库' : '编辑知识库'"
        width="500px"
      >
        <el-form
          ref="formRef"
          :model="knowledgeForm"
          :rules="rules"
          label-width="100px"
        >
          <el-form-item label="名称" prop="name">
            <el-input v-model="knowledgeForm.name" placeholder="请输入知识库名称" />
          </el-form-item>
          <el-form-item label="描述" prop="description">
            <el-input
              v-model="knowledgeForm.description"
              type="textarea"
              placeholder="请输入知识库描述"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useKnowledgeStore } from '@/stores/knowledge'
import { formatTime } from '@/utils/date'
import { Plus, Folder } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'

const router = useRouter()
const knowledgeStore = useKnowledgeStore()
const { knowledgeBases, loading } = knowledgeStore

// 获取知识库列表
onMounted(async () => {
  await knowledgeStore.fetchKnowledgeBases()
})

// 创建知识库
const createKnowledgeBase = () => {
  router.push('/dashboard/knowledge/create')
}

// 查看详情
const viewDetail = (id: number) => {
  router.push(`/knowledge/${id}`)
}

// 上传文档
const uploadDocument = (id: number) => {
  // TODO: 实现文档上传逻辑
  ElMessage.info('文档上传功能开发中...')
}

// 删除知识库
const deleteKnowledgeBase = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除该知识库吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    const success = await knowledgeStore.deleteKnowledgeBase(id)
    if (success) {
      ElMessage.success('删除成功')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Delete failed:', error)
    }
  }
}
</script>

<style lang="scss" scoped>
.knowledge-base {
  .breadcrumb {
    margin-bottom: 16px;
    padding: 16px 20px;
    background-color: var(--el-bg-color);
  }

  .page-container {
    padding: 20px;
    background-color: var(--el-bg-color);
    border-radius: 4px;
    
    .page-header {
      margin-bottom: 24px;

      .header-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;

        h2 {
          margin: 0;
          font-size: 24px;
          color: var(--el-text-color-primary);
        }
      }

      .description {
        color: var(--el-text-color-secondary);
        font-size: 14px;
        margin: 0;
      }
    }

    .knowledge-list {
      .create-card {
        height: 200px;
        border: 2px dashed var(--el-border-color);
        border-radius: 8px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s;

        &:hover {
          border-color: var(--el-color-primary);
          color: var(--el-color-primary);
        }

        .el-icon {
          font-size: 32px;
          margin-bottom: 8px;
        }
      }

      .kb-card {
        margin-bottom: 20px;
        
        .kb-header {
          background-color: var(--el-color-primary-light-9);
          padding: 16px;
          display: flex;
          align-items: center;
          gap: 8px;

          .el-icon {
            font-size: 20px;
            color: var(--el-color-primary);
          }

          .kb-name {
            font-size: 16px;
            font-weight: 500;
          }
        }

        .kb-content {
          padding: 16px;

          .kb-description {
            margin: 0 0 16px;
            color: var(--el-text-color-secondary);
            font-size: 14px;
            min-height: 40px;
          }

          .kb-stats {
            display: flex;
            justify-content: space-between;

            .stat-item {
              display: flex;
              flex-direction: column;

              .label {
                font-size: 12px;
                color: var(--el-text-color-secondary);
              }

              .value {
                font-size: 14px;
                color: var(--el-text-color-primary);
              }
            }
          }
        }

        .kb-actions {
          padding: 12px 16px;
          border-top: 1px solid var(--el-border-color-lighter);
          text-align: right;
        }
      }
    }
  }
}
</style> 