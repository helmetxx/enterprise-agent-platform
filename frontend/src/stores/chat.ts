import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { ChatMessage, ChatSession } from '@/types'
import { api } from '@/utils/api'
import { config } from '@/config'

export const useChatStore = defineStore('chat', () => {
  const messages = ref<ChatMessage[]>([])
  const currentSession = ref<ChatSession | null>(null)
  const ws = ref<WebSocket | null>(null)
  
  const isConnected = computed(() => ws.value?.readyState === WebSocket.OPEN)
  
  function initializeWebSocket() {
    ws.value = new WebSocket(config.wsUrl)
    
    ws.value.onmessage = (event) => {
      const message = JSON.parse(event.data)
      messages.value.push(message)
    }
    
    ws.value.onclose = () => {
      setTimeout(initializeWebSocket, 1000)
    }
  }
  
  async function sendMessage(content: string) {
    if (!currentSession.value) return
    
    const message: ChatMessage = {
      content,
      sessionId: currentSession.value.id,
      sender: 'user',
      timestamp: new Date()
    }
    
    messages.value.push(message)
    
    if (ws.value?.readyState === WebSocket.OPEN) {
      ws.value.send(JSON.stringify(message))
    }
    
    await api.post('/chat/messages', message)
  }
  
  return {
    messages,
    currentSession,
    isConnected,
    initializeWebSocket,
    sendMessage
  }
}) 