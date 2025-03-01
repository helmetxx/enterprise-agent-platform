<template>
  <div class="chat-window">
    <div class="messages" ref="messagesContainer">
      <div v-for="message in messages" :key="message.id" 
           :class="['message', message.sender === 'user' ? 'user' : 'agent']">
        <div class="message-content">
          {{ message.content }}
        </div>
        <div class="message-time">
          {{ formatTime(message.timestamp) }}
        </div>
      </div>
    </div>
    
    <div class="input-area">
      <el-input
        v-model="newMessage"
        type="textarea"
        :rows="3"
        placeholder="输入消息..."
        @keyup.enter.prevent="sendMessage"
      />
      <el-button type="primary" @click="sendMessage">发送</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useChatStore } from '@/stores/chat'
import { formatTime } from '@/utils/date'

const chatStore = useChatStore()
const messages = ref([])
const newMessage = ref('')
const messagesContainer = ref(null)

const sendMessage = async () => {
  if (!newMessage.value.trim()) return
  
  await chatStore.sendMessage({
    content: newMessage.value,
    type: 'text'
  })
  
  newMessage.value = ''
}

onMounted(() => {
  chatStore.initializeWebSocket()
})

watch(() => chatStore.messages, (newMessages) => {
  messages.value = newMessages
  scrollToBottom()
}, { deep: true })

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}
</script>

<style scoped>
.chat-window {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #f5f7fa;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.message {
  margin-bottom: 12px;
  max-width: 70%;
}

.message.user {
  margin-left: auto;
}

.message-content {
  padding: 10px;
  border-radius: 8px;
  background: #fff;
}

.message.user .message-content {
  background: #409eff;
  color: white;
}

.message-time {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.input-area {
  padding: 20px;
  background: white;
  border-top: 1px solid #eee;
}
</style> 