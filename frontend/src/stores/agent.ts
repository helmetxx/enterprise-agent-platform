import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '@/utils/api'
import type { Agent, UsageRecord } from '@/types/agent'
import Logger from '@/utils/logger'

interface AgentQueryParams {
  page: number
  pageSize: number
  search?: string
}

interface AgentResponse {
  items: Agent[]
  total: number
  currentPage: number
  pageSize: number
}

export const useAgentStore = defineStore('agent', () => {
  const agents = ref<Agent[]>([])
  const currentAgent = ref<Agent | null>(null)
  const loading = ref(false)
  const recommendedAgents = ref<Agent[]>([])

  async function getFrequentAgents(): Promise<Agent[]> {
    try {
      const response = await api.get('/agents/frequent')
      return response.data
    } catch (error) {
      console.error('Failed to get frequent agents:', error)
      return []
    }
  }

  async function getRecentUsage(): Promise<UsageRecord[]> {
    try {
      const response = await api.get('/agents/recent-usage')
      return response.data
    } catch (error) {
      Logger.error('Failed to get recent usage:', error)
      return []
    }
  }

  async function getRecommendedAgents(): Promise<Agent[]> {
    try {
      const response = await api.get('/agents/recommended')
      recommendedAgents.value = response.data
      return response.data
    } catch (error) {
      Logger.error('Failed to get recommended agents:', error)
      return []
    }
  }

  async function getAllAgents(): Promise<Agent[]> {
    try {
      loading.value = true
      const response = await api.get('/agents')
      agents.value = response.data
      return response.data
    } catch (error) {
      Logger.error('Failed to get all agents:', error)
      return []
    } finally {
      loading.value = false
    }
  }

  async function getAgent(id: string) {
    try {
      const response = await api.get(`/agents/${id}`)
      currentAgent.value = response
      return response
    } catch (error) {
      console.error('Failed to get agent:', error)
      throw error
    }
  }

  async function getAgents(params: AgentQueryParams): Promise<AgentResponse> {
    try {
      const response = await api.get('/agents', { params })
      return response.data
    } catch (error) {
      console.error('Failed to get agents:', error)
      return {
        items: [],
        total: 0,
        currentPage: 1,
        pageSize: 20
      }
    }
  }

  return {
    agents,
    currentAgent,
    loading,
    recommendedAgents,
    getFrequentAgents,
    getRecentUsage,
    getRecommendedAgents,
    getAllAgents,
    getAgent,
    getAgents
  }
}) 