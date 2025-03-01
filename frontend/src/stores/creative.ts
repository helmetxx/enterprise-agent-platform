import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '@/utils/api'
import type { 
  CreativeProject,
  DocumentAnalysis,
  MarketAnalysis,
  IdeaGeneration,
  GeneratedImage,
  SolutionDesign 
} from '@/types'

export const useCreativeStore = defineStore('creative', () => {
  // 状态
  const currentProject = ref<CreativeProject | null>(null)
  const documentAnalyses = ref<DocumentAnalysis[]>([])
  const marketAnalyses = ref<MarketAnalysis[]>([])
  const ideas = ref<IdeaGeneration[]>([])
  const images = ref<GeneratedImage[]>([])
  const solution = ref<SolutionDesign | null>(null)
  const loading = ref(false)
  const currentIdea = ref<IdeaGeneration | null>(null)

  // Getters
  const projectStatus = computed(() => currentProject.value?.status || 'draft')
  const hasDocumentAnalysis = computed(() => documentAnalyses.value.length > 0)
  const hasMarketAnalysis = computed(() => marketAnalyses.value.length > 0)

  // Actions
  async function fetchProject(projectId: string) {
    loading.value = true
    try {
      const response = await api.get(`/api/v1/creative/projects/${projectId}`)
      currentProject.value = response.data
    } catch (error) {
      console.error('Failed to fetch project:', error)
    } finally {
      loading.value = false
    }
  }

  async function createDocumentAnalysis(projectId: string, data: any) {
    loading.value = true
    try {
      const response = await api.post(
        `/api/v1/creative/projects/${projectId}/document-analysis/`,
        data
      )
      documentAnalyses.value.push(response.data)
      return response.data
    } catch (error) {
      console.error('Failed to create document analysis:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  async function createProject(data: Partial<CreativeProject>) {
    loading.value = true
    try {
      const response = await api.post('/api/v1/creative/projects/', data)
      return response.data
    } catch (error) {
      console.error('Failed to create project:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  async function getMarketAnalyses(projectId: string) {
    loading.value = true
    try {
      const response = await api.get(`/api/v1/creative/projects/${projectId}/market-analysis`)
      return response.data
    } catch (error) {
      console.error('Failed to get market analyses:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  async function createMarketAnalysis(projectId: string, data: any) {
    loading.value = true
    try {
      const response = await api.post(
        `/api/v1/creative/projects/${projectId}/market-analysis/`,
        data
      )
      marketAnalyses.value.push(response.data)
      return response.data
    } catch (error) {
      console.error('Failed to create market analysis:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  async function getIdeas(projectId: string) {
    loading.value = true
    try {
      const response = await api.get(`/api/v1/creative/projects/${projectId}/ideas`)
      return response.data
    } catch (error) {
      console.error('Failed to get ideas:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  async function createIdea(projectId: string, data: any) {
    loading.value = true
    try {
      const response = await api.post(
        `/api/v1/creative/projects/${projectId}/idea-generation/`,
        data
      )
      ideas.value.push(response.data)
      return response.data
    } catch (error) {
      console.error('Failed to create idea:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  function setCurrentIdea(idea: IdeaGeneration) {
    currentIdea.value = idea
  }

  async function getGeneratedImages(ideaId: string) {
    loading.value = true
    try {
      const response = await api.get(`/api/v1/creative/ideas/${ideaId}/images`)
      return response.data
    } catch (error) {
      console.error('Failed to get generated images:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  async function createGeneratedImage(projectId: string, ideaId: string, data: any) {
    loading.value = true
    try {
      const response = await api.post(
        `/api/v1/creative/ideas/${ideaId}/images/`,
        data
      )
      images.value.push(response.data)
      return response.data
    } catch (error) {
      console.error('Failed to create generated image:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  async function getSolution(projectId: string) {
    loading.value = true
    try {
      const response = await api.get(`/api/v1/creative/projects/${projectId}/solution`)
      return response.data
    } catch (error) {
      console.error('Failed to get solution:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  async function createSolution(projectId: string, data: any) {
    loading.value = true
    try {
      const response = await api.post(
        `/api/v1/creative/projects/${projectId}/solution/`,
        data
      )
      solution.value = response.data
      return response.data
    } catch (error) {
      console.error('Failed to create solution:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  async function getEvaluation(projectId: string) {
    loading.value = true
    try {
      const response = await api.get(`/api/v1/creative/projects/${projectId}/evaluation`)
      return response.data
    } catch (error) {
      console.error('Failed to get evaluation:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  async function createEvaluation(projectId: string) {
    loading.value = true
    try {
      const response = await api.post(
        `/api/v1/creative/projects/${projectId}/evaluation/`
      )
      return response.data
    } catch (error) {
      console.error('Failed to create evaluation:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  async function getExportPreview(projectId: string, options: any) {
    loading.value = true
    try {
      const response = await api.post(
        `/api/v1/creative/projects/${projectId}/export/preview`,
        options
      )
      return response.data
    } catch (error) {
      console.error('Failed to get export preview:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  async function exportProject(projectId: string, options: any) {
    loading.value = true
    try {
      const response = await api.post(
        `/api/v1/creative/projects/${projectId}/export`,
        options
      )
      return response.data
    } catch (error) {
      console.error('Failed to export project:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  async function updateProject(projectId: string, data: Partial<CreativeProject>) {
    loading.value = true
    try {
      const response = await api.put(
        `/api/v1/creative/projects/${projectId}`,
        data
      )
      currentProject.value = response.data
      return response.data
    } catch (error) {
      console.error('Failed to update project:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  async function deleteProject(projectId: string) {
    loading.value = true
    try {
      await api.delete(`/api/v1/creative/projects/${projectId}`)
    } catch (error) {
      console.error('Failed to delete project:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  return {
    currentProject,
    documentAnalyses,
    marketAnalyses,
    ideas,
    images,
    solution,
    loading,
    projectStatus,
    hasDocumentAnalysis,
    hasMarketAnalysis,
    fetchProject,
    createDocumentAnalysis,
    createProject,
    getMarketAnalyses,
    createMarketAnalysis,
    getIdeas,
    createIdea,
    setCurrentIdea,
    getGeneratedImages,
    createGeneratedImage,
    getSolution,
    createSolution,
    getEvaluation,
    createEvaluation,
    getExportPreview,
    exportProject,
    updateProject,
    deleteProject,
  }
}) 