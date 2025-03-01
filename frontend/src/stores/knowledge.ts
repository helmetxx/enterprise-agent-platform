import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '@/utils/api'
import { ElMessage } from 'element-plus'
import type { KnowledgeBase } from '@/types'
import type { UploadFile } from 'element-plus'
import { useRouter } from 'vue-router'

export const useKnowledgeStore = defineStore('knowledge', () => {
  const knowledgeBases = ref<KnowledgeBase[]>([])
  const loading = ref(false)
  const tempFiles = ref<UploadFile[]>([])

  const fetchKnowledgeBases = async () => {
    loading.value = true
    try {
      const response = await api.get('/knowledge')
      knowledgeBases.value = response.data
    } catch (error: any) {
      console.error('Failed to fetch knowledge bases:', error)
      if (error.response?.status === 401) {
        // 重定向到登录页面
        const router = useRouter()
        router.push('/auth/login')
      }
      ElMessage.error(error.response?.data?.detail || '获取知识库列表失败')
    } finally {
      loading.value = false
    }
  }

  const deleteKnowledgeBase = async (id: number) => {
    try {
      await api.delete(`/knowledge/${id}`)
      await fetchKnowledgeBases() // 重新加载列表
      return true
    } catch (error: any) {
      console.error('Failed to delete knowledge base:', error)
      ElMessage.error(error.response?.data?.detail || '删除知识库失败')
      return false
    }
  }

  const createKnowledgeBase = async (data: { name: string; description?: string }) => {
    try {
      const response = await api.post('/knowledge', data)
      await fetchKnowledgeBases() // 重新获取列表
      return response.data
    } catch (error: any) {
      console.error('Failed to create knowledge base:', error)
      ElMessage.error(error.response?.data?.detail || '创建知识库失败')
      throw error
    }
  }

  const uploadDocument = async (knowledgeBaseId: number, file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    try {
      const response = await api.post(
        `/knowledge/${knowledgeBaseId}/documents`, 
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'  // 确保设置正确的 Content-Type
          }
        }
      )
      return response.data
    } catch (error: any) {
      console.error('Failed to upload document:', error)
      ElMessage.error(error.response?.data?.detail || '文件上传失败')
      throw error
    }
  }

  const setTempFiles = (files: UploadFile[]) => {
    tempFiles.value = files
  }

  return {
    knowledgeBases,
    loading,
    tempFiles,
    fetchKnowledgeBases,
    deleteKnowledgeBase,
    createKnowledgeBase,
    uploadDocument,
    setTempFiles
  }
}) 