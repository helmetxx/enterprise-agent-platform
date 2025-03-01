<template>
  <div class="product-assistant-container">
    <!-- 左侧菜单 -->
    <div class="sidebar">
      <el-menu
        class="sidebar-menu"
        :default-active="activeMenu"
        background-color="#f4f6f8"
        text-color="#333"
      >
        <el-menu-item index="new-product" class="new-product-item">
          <el-icon><Plus /></el-icon>
          <span>新产品</span>
        </el-menu-item>
        <el-menu-item index="product-plan">
          <el-icon><Document /></el-icon>
          <span>产品方案</span>
        </el-menu-item>
        <el-menu-item index="drafts">
          <el-icon><Edit /></el-icon>
          <span>创作草稿</span>
        </el-menu-item>
        <el-menu-item index="knowledge-base">
          <el-icon><Collection /></el-icon>
          <span>知识库</span>
        </el-menu-item>
      </el-menu>
    </div>

    <!-- 右侧内容区 -->
    <div class="main-content">
      <div class="content-header">
        <h2>产品创意助手-输入新产品的市场洞察文件</h2>
      </div>
      
      <div class="upload-section">
        <div class="upload-area">
          <el-input
            type="textarea"
            v-model="inputContent"
            placeholder="请输入您的产品设计需求,或者上传市场及产品背景知识文件"
            :rows="6"
          />
          <div class="upload-actions">
            <el-button type="primary" class="upload-btn">
              <el-icon><Document /></el-icon>
              文件
            </el-button>
            <el-button type="primary" class="upload-btn">
              <el-icon><Microphone /></el-icon>
              语音
            </el-button>
            <el-button type="primary" class="send-btn">
              <el-icon><Position /></el-icon>
            </el-button>
          </div>
        </div>

        <div class="file-list">
          <el-tabs v-model="activeTab">
            <el-tab-pane label="最近文件" name="recent">
              <!-- 最近文件列表 -->
            </el-tab-pane>
            <el-tab-pane label="我的知识库" name="knowledge">
              <!-- 知识库文件列表 -->
            </el-tab-pane>
          </el-tabs>
          
          <div class="upload-box">
            <el-upload
              class="upload-demo"
              drag
              action="/api/upload"
              multiple
            >
              <div class="upload-content">
                <p>点击上传或拖入文档</p>
                <p class="upload-tip">最多10个文件，单个最大50MB，支持 Word/PDF/TXT/Excel/PPT 格式</p>
              </div>
            </el-upload>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Plus, Document, Edit, Collection, Microphone, Position } from '@element-plus/icons-vue'

const activeMenu = ref('new-product')
const inputContent = ref('')
const activeTab = ref('recent')
</script>

<style scoped lang="scss">
.product-assistant-container {
  display: flex;
  height: 100vh;
  background-color: #fff;
}

.sidebar {
  width: 200px;
  border-right: 1px solid #e6e6e6;
  
  .sidebar-menu {
    height: 100%;
    border-right: none;
  }

  .new-product-item {
    color: #409EFF;
    font-weight: bold;
  }
}

.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;

  .content-header {
    margin-bottom: 20px;
    
    h2 {
      font-size: 20px;
      color: #333;
    }
  }
}

.upload-section {
  .upload-area {
    margin-bottom: 20px;
    
    .upload-actions {
      display: flex;
      gap: 10px;
      margin-top: 10px;
    }

    .upload-btn {
      display: flex;
      align-items: center;
      gap: 5px;
    }

    .send-btn {
      margin-left: auto;
    }
  }
}

.file-list {
  background-color: #f8f9fa;
  border-radius: 4px;
  padding: 20px;

  .upload-box {
    margin-top: 20px;
    border: 2px dashed #e6e6e6;
    border-radius: 4px;
    
    .upload-content {
      text-align: center;
      padding: 20px;
      
      .upload-tip {
        font-size: 12px;
        color: #999;
        margin-top: 10px;
      }
    }
  }
}
</style> 