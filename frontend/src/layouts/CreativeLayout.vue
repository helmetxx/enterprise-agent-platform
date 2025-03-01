<template>
  <div class="creative-layout">
    <!-- 工作区顶部 -->
    <div class="workspace-header">
      <div class="left">
        <h2>产品创意助手</h2>
        <el-menu 
          mode="horizontal" 
          :default-active="activeMenu"
          class="workspace-menu"
          router>
          <el-menu-item index="/creative/new">新产品</el-menu-item>
          <el-menu-item index="/creative/solutions">产品方案</el-menu-item>
          <el-menu-item index="/creative/drafts">创作草稿</el-menu-item>
          <el-menu-item index="/creative/knowledge">知识库</el-menu-item>
        </el-menu>
      </div>
      <div class="right">
        <el-button type="primary">
          <el-icon><Plus /></el-icon>新建
        </el-button>
      </div>
    </div>

    <!-- 工作区内容 -->
    <div class="workspace-content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { Plus, Document, Edit, Collection } from '@element-plus/icons-vue'

const route = useRoute()
const activeMenu = computed(() => route.path)
</script>

<style scoped>
.creative-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.workspace-header {
  background: #fff;
  padding: 16px 24px;
  border-radius: 8px;
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.workspace-header .left {
  display: flex;
  align-items: center;
  gap: 40px;
}

.workspace-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 500;
}

.workspace-menu {
  border-bottom: none;
}

.workspace-content {
  flex: 1;
  background: #fff;
  border-radius: 8px;
  padding: 24px;
}
</style> 