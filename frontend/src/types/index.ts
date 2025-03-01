export interface User {
  id: string
  username: string
  email: string
  is_active: boolean
  created_at: string
}

export interface LoginForm {
  email: string
  password: string
}

export interface Agent {
  id: string
  name: string
  description: string
  category: string
  capabilities: string[]
  icon: string
  created_at: string
}

export interface ChatMessage {
  id?: string
  content: string
  sender: 'user' | 'agent'
  sessionId: string
  timestamp: Date
  type?: 'text' | 'image' | 'file'
  metadata?: any
}

export interface ChatSession {
  id: string
  agentId: string
  messages: ChatMessage[]
  createdAt: Date
  updatedAt: Date
}

export interface KnowledgeBase {
  id: number
  name: string
  description: string
  created_by: number
  created_at: string
  updated_at: string
  document_count: number
}

export interface Document {
  id: number
  knowledge_base_id: number
  filename: string
  file_type: string
  status: string
  created_at: string
} 