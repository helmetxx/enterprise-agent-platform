<template>
  <div class="new-product">
    <div class="upload-area">
      <div class="input-hint">
        请输入您的产品设计需求,或者上传市场及产品背景知识文件
      </div>
      
      <div class="upload-actions">
        <el-button type="primary" @click="handleFileClick">
          <el-icon><Document /></el-icon>文件
        </el-button>
        <el-button @click="handleVoiceClick">
          <el-icon><Microphone /></el-icon>语音
        </el-button>
        <el-button @click="handleSend">
          <el-icon><Position /></el-icon>
        </el-button>
      </div>
      
      <el-upload
        ref="uploadRef"
        class="upload-drop-area"
        drag
        :action="uploadUrl"
        :show-file-list="false"
        :before-upload="beforeUpload"
        :on-success="handleUploadSuccess"
        :on-error="handleUploadError">
        <div class="upload-hint">
          <el-icon><Upload /></el-icon>
          <div>点击上传或拖入文档</div>
          <div class="upload-limit">
            最多10个文件，单个最大50MB，支持 Word/PDF/TXT/Excel/PPT 格式
          </div>
        </div>
      </el-upload>
    </div>

    <div class="file-tabs">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="最近文件" name="recent">
          <div class="file-list">
            <!-- 最近文件列表 -->
          </div>
        </el-tab-pane>
        <el-tab-pane label="我的知识库" name="knowledge">
          <div class="file-list">
            <!-- 知识库文件列表 -->
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Document, Microphone, Position, Upload } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import type { UploadInstance, UploadProps } from 'element-plus'

const uploadRef = ref<UploadInstance>()
const activeTab = ref('recent')
const uploadUrl = '/api/upload' // 需要替换为实际的上传接口

const handleFileClick = () => {
  uploadRef.value?.handleClick()
}

const handleVoiceClick = () => {
  // 处理语音输入
  ElMessage.info('语音输入功能开发中')
}

const handleSend = () => {
  // 处理发送
  ElMessage.info('发送功能开发中')
}

const beforeUpload: UploadProps['beforeUpload'] = (file) => {
  // 验证文件类型和大小
  const validTypes = ['application/pdf', 'application/msword', 'text/plain', 'application/vnd.ms-excel', 'application/vnd.ms-powerpoint']
  if (!validTypes.includes(file.type)) {
    ElMessage.error('不支持的文件类型')
    return false
  }
  
  const maxSize = 50 * 1024 * 1024 // 50MB
  if (file.size > maxSize) {
    ElMessage.error('文件大小不能超过50MB')
    return false
  }
  
  return true
}

const handleUploadSuccess = (response: any) => {
  ElMessage.success('上传成功')
}

const handleUploadError = () => {
  ElMessage.error('上传失败')
}
</script>

<style scoped>
.new-product {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.upload-area {
  background-color: #fff;
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 24px;
}

.input-hint {
  color: #606266;
  margin-bottom: 16px;
}

.upload-actions {
  margin-bottom: 16px;
  display: flex;
  gap: 12px;
}

.upload-drop-area {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  padding: 20px;
  text-align: center;
}

.upload-hint {
  color: #606266;
}

.upload-limit {
  font-size: 12px;
  color: #909399;
  margin-top: 8px;
}

.file-tabs {
  flex: 1;
  background-color: #fff;
  border-radius: 8px;
  padding: 24px;
}

.file-list {
  min-height: 200px;
}
</style> 