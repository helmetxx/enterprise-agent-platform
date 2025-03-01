<template>
  <div class="project-settings">
    <div class="page-header">
      <h1>项目设置</h1>
      <el-button-group>
        <el-button 
          type="primary"
          :loading="saving"
          @click="saveSettings"
        >
          保存设置
        </el-button>
        <el-popconfirm
          title="确定要删除该项目吗？"
          @confirm="deleteProject"
        >
          <template #reference>
            <el-button type="danger" :loading="deleting">删除项目</el-button>
          </template>
        </el-popconfirm>
      </el-button-group>
    </div>

    <div class="settings-content">
      <el-row :gutter="20">
        <el-col :span="16">
          <el-card class="settings-card">
            <template #header>
              <div class="card-header">
                <h3>基本设置</h3>
              </div>
            </template>
            
            <el-form 
              ref="formRef"
              :model="formData"
              :rules="rules"
              label-position="top"
            >
              <el-form-item label="项目名称" prop="title">
                <el-input 
                  v-model="formData.title"
                  placeholder="请输入项目名称"
                />
              </el-form-item>

              <el-form-item label="项目描述" prop="description">
                <el-input 
                  v-model="formData.description"
                  type="textarea"
                  :rows="4"
                  placeholder="请输入项目描述"
                />
              </el-form-item>

              <el-form-item label="项目状态">
                <el-select v-model="formData.status">
                  <el-option label="草稿" value="draft" />
                  <el-option label="进行中" value="in_progress" />
                  <el-option label="已完成" value="completed" />
                </el-select>
              </el-form-item>

              <el-form-item label="标签">
                <el-tag
                  v-for="tag in formData.tags"
                  :key="tag"
                  closable
                  @close="handleTagClose(tag)"
                >
                  {{ tag }}
                </el-tag>
                <el-input
                  v-if="inputVisible"
                  ref="tagInputRef"
                  v-model="inputValue"
                  class="tag-input"
                  size="small"
                  @keyup.enter="handleInputConfirm"
                  @blur="handleInputConfirm"
                />
                <el-button 
                  v-else 
                  class="button-new-tag" 
                  size="small" 
                  @click="showInput"
                >
                  + 新标签
                </el-button>
              </el-form-item>
            </el-form>
          </el-card>

          <el-card class="permissions-card">
            <template #header>
              <div class="card-header">
                <h3>权限设置</h3>
              </div>
            </template>
            
            <el-form>
              <el-form-item label="项目成员">
                <el-transfer
                  v-model="formData.members"
                  :data="allMembers"
                  :titles="['可选成员', '已选成员']"
                />
              </el-form-item>

              <el-form-item label="访问权限">
                <el-radio-group v-model="formData.visibility">
                  <el-radio label="private">私有</el-radio>
                  <el-radio label="team">团队可见</el-radio>
                  <el-radio label="public">公开</el-radio>
                </el-radio-group>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>

        <el-col :span="8">
          <el-card class="info-card">
            <template #header>
              <div class="card-header">
                <h3>项目信息</h3>
              </div>
            </template>
            
            <el-descriptions direction="vertical" :column="1" border>
              <el-descriptions-item label="创建时间">
                {{ formatTime(project?.created_at) }}
              </el-descriptions-item>
              <el-descriptions-item label="最后更新">
                {{ formatTime(project?.updated_at) }}
              </el-descriptions-item>
              <el-descriptions-item label="创建者">
                {{ project?.user_id }}
              </el-descriptions-item>
              <el-descriptions-item label="企业">
                {{ project?.enterprise_id }}
              </el-descriptions-item>
            </el-descriptions>

            <div class="project-stats">
              <h4>项目统计</h4>
              <el-row :gutter="20">
                <el-col :span="12">
                  <div class="stat-item">
                    <div class="stat-value">{{ documentAnalyses.length }}</div>
                    <div class="stat-label">文档分析</div>
                  </div>
                </el-col>
                <el-col :span="12">
                  <div class="stat-item">
                    <div class="stat-value">{{ marketAnalyses.length }}</div>
                    <div class="stat-label">市场分析</div>
                  </div>
                </el-col>
                <el-col :span="12">
                  <div class="stat-item">
                    <div class="stat-value">{{ ideas.length }}</div>
                    <div class="stat-label">创意方案</div>
                  </div>
                </el-col>
                <el-col :span="12">
                  <div class="stat-item">
                    <div class="stat-value">{{ images.length }}</div>
                    <div class="stat-label">生成图片</div>
                  </div>
                </el-col>
              </el-row>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus/es/components/form'
import { useCreativeStore } from '@/stores/creative'
import { formatTime } from '@/utils/date'
import type { CreativeProject } from '@/types/creative'

const route = useRoute()
const router = useRouter()
const store = useCreativeStore()
const formRef = ref<FormInstance>()
const tagInputRef = ref<HTMLInputElement>()

const saving = ref(false)
const deleting = ref(false)
const inputVisible = ref(false)
const inputValue = ref('')

const projectId = route.params.id as string
const project = ref<CreativeProject | null>(null)

const formData = ref({
  title: '',
  description: '',
  status: 'draft',
  tags: [] as string[],
  members: [] as string[],
  visibility: 'private'
})

const rules = {
  title: [
    { required: true, message: '请输入项目名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入项目描述', trigger: 'blur' },
    { min: 10, max: 500, message: '长度在 10 到 500 个字符', trigger: 'blur' }
  ]
}

const allMembers = [
  { key: 'user1', label: '用户1' },
  { key: 'user2', label: '用户2' },
  { key: 'user3', label: '用户3' },
  { key: 'user4', label: '用户4' }
]

onMounted(async () => {
  await fetchProject()
})

async function fetchProject() {
  try {
    const response = await store.fetchProject(projectId)
    project.value = response
    formData.value = {
      title: project.value?.title || '',
      description: project.value?.description || '',
      status: project.value?.status || 'draft',
      tags: project.value?.tags || [],
      members: project.value?.members || [],
      visibility: project.value?.visibility || 'private'
    }
  } catch (error) {
    ElMessage.error('获取项目失败')
  }
}

async function saveSettings() {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      saving.value = true
      try {
        await store.updateProject(projectId, formData.value)
        ElMessage.success('保存成功')
      } catch (error) {
        ElMessage.error('保存失败')
      } finally {
        saving.value = false
      }
    }
  })
}

async function deleteProject() {
  deleting.value = true
  try {
    await store.deleteProject(projectId)
    ElMessage.success('删除成功')
    router.push('/creative/projects')
  } catch (error) {
    ElMessage.error('删除失败')
  } finally {
    deleting.value = false
  }
}

function handleTagClose(tag: string) {
  formData.value.tags = formData.value.tags.filter(t => t !== tag)
}

function showInput() {
  inputVisible.value = true
  nextTick(() => {
    tagInputRef.value?.focus()
  })
}

function handleInputConfirm() {
  if (inputValue.value) {
    if (!formData.value.tags.includes(inputValue.value)) {
      formData.value.tags.push(inputValue.value)
    }
  }
  inputVisible.value = false
  inputValue.value = ''
}
</script>

<style lang="scss" scoped>
.project-settings {
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
  
  .settings-content {
    .settings-card,
    .permissions-card,
    .info-card {
      margin-bottom: var(--spacing-large);
      background: var(--color-secondary);
      border: 1px solid rgba(255, 255, 255, 0.1);
      
      .card-header {
        h3 {
          margin: 0;
          color: var(--color-text-primary);
        }
      }
      
      &:last-child {
        margin-bottom: 0;
      }
    }
    
    .tag-input {
      width: 90px;
      margin-left: 8px;
      vertical-align: bottom;
    }
    
    .button-new-tag {
      margin-left: 8px;
    }
    
    .project-stats {
      margin-top: var(--spacing-large);
      
      h4 {
        margin: 0 0 16px;
        color: var(--color-text-primary);
      }
      
      .stat-item {
        text-align: center;
        padding: 16px;
        margin-bottom: 16px;
        background: var(--color-primary);
        border-radius: var(--border-radius-small);
        
        .stat-value {
          font-size: 24px;
          font-weight: bold;
          color: var(--color-text-primary);
        }
        
        .stat-label {
          margin-top: 4px;
          color: var(--color-text-secondary);
        }
      }
    }
  }
}
</style> 