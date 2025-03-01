export interface Agent {
  id: string
  name: string
  description: string
  icon?: string
  category: string
  capabilities: string[]
  tags: string[]
  status: 'active' | 'inactive'
  createdAt: string
  updatedAt: string
}

export interface UsageRecord {
  id: string
  agent: Agent
  usedAt: string
  status: 'completed' | 'failed'
} 