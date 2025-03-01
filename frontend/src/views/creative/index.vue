<template>
  <div class="creative-home">
    <!-- 面包屑导航 -->
    <el-breadcrumb class="breadcrumb">
      <el-breadcrumb-item :to="{ path: '/dashboard' }">工作台</el-breadcrumb-item>
      <el-breadcrumb-item>产品创意助手</el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 欢迎区域 -->
    <div class="welcome-section">
      <h2>欢迎使用产品创意助手</h2>
      <p>这里是您的产品创意工作空间，让我们开始激发创意吧！</p>
    </div>

    <!-- 功能模块卡片 -->
    <el-row :gutter="20" class="feature-section">
      <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="feature in features" :key="feature.path">
        <el-card class="feature-card" @click="navigateToFeature(feature.path)">
          <div class="feature-icon">
            <el-icon>
              <component :is="feature.icon"></component>
            </el-icon>
          </div>
          <div class="feature-info">
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.description }}</p>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 最近项目 -->
    <div class="recent-section">
      <h3 class="section-title">最近项目</h3>
      <el-empty v-if="!recentProjects.length" description="暂无最近项目"></el-empty>
      <el-row v-else :gutter="20">
        <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="project in recentProjects" :key="project.id">
          <el-card class="project-card">
            <h4>{{ project.name }}</h4>
            <p>{{ project.description }}</p>
            <div class="project-meta">
              <span>{{ formatTime(project.updatedAt) }}</span>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Lightning,
  DataAnalysis,
  CircleCheck,
  EditPen,
  Picture,
  Document,
  TrendCharts,
  Share,
  Setting
} from '@element-plus/icons-vue'
import { formatTime } from '@/utils/date'

const router = useRouter()
const recentProjects = ref([])

const features = [
  {
    title: '创意发散',
    description: '通过AI助手激发创意灵感',
    icon: Lightning,
    path: '/dashboard/creative/ideation'
  },
  {
    title: '创意分析',
    description: '深入分析创意可行性',
    icon: DataAnalysis,
    path: '/dashboard/creative/analysis'
  },
  {
    title: '创意验证',
    description: '验证创意的可行性',
    icon: CircleCheck,
    path: '/dashboard/creative/validation'
  },
  {
    title: '创意优化',
    description: '优化和完善创意',
    icon: EditPen,
    path: '/dashboard/creative/refinement'
  },
  {
    title: '图片生成',
    description: '生成创意相关的图片',
    icon: Picture,
    path: '/dashboard/creative/visualization'
  },
  {
    title: '文档生成',
    description: '生成创意文档',
    icon: Document,
    path: '/dashboard/creative/documentation'
  },
  {
    title: '项目评估',
    description: '评估项目进展',
    icon: TrendCharts,
    path: '/dashboard/creative/evaluation'
  },
  {
    title: '团队协作',
    description: '与团队成员协作',
    icon: Share,
    path: '/dashboard/creative/collaboration'
  },
  {
    title: '项目设置',
    description: '管理项目配置',
    icon: Setting,
    path: '/dashboard/creative/settings'
  }
]

const navigateToFeature = (path: string) => {
  router.push(path)
}
</script>

<style lang="scss" scoped>
.creative-home {
  .breadcrumb {
    margin-bottom: 20px;
  }

  .welcome-section {
    margin-bottom: 40px;
    
    h2 {
      font-size: 24px;
      margin-bottom: 8px;
    }
    
    p {
      color: var(--el-text-color-secondary);
    }
  }

  .feature-section {
    margin-bottom: 40px;
  }

  .feature-card {
    height: 100%;
    cursor: pointer;
    transition: all 0.3s;

    &:hover {
      transform: translateY(-5px);
    }

    .feature-icon {
      font-size: 32px;
      margin-bottom: 16px;
      color: var(--el-color-primary);
    }

    .feature-info {
      h3 {
        margin: 0 0 8px;
      }

      p {
        margin: 0;
        color: var(--el-text-color-secondary);
        font-size: 14px;
      }
    }
  }

  .section-title {
    margin-bottom: 20px;
    font-size: 18px;
  }

  .project-card {
    h4 {
      margin: 0 0 8px;
    }

    p {
      margin: 0 0 12px;
      color: var(--el-text-color-secondary);
      font-size: 14px;
    }

    .project-meta {
      color: var(--el-text-color-secondary);
      font-size: 12px;
    }
  }
}
</style> 