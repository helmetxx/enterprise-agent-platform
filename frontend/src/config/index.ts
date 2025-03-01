export const config = {
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  wsUrl: import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws',
  pageSize: 20,
  uploadMaxSize: 5 * 1024 * 1024, // 5MB
  supportedFileTypes: ['image/jpeg', 'image/png', 'image/gif', 'application/pdf'],
  defaultAvatar: '/assets/default-avatar.png',
  defaultAgentIcon: '/assets/default-agent-icon.png'
}

export const errorMessages = {
  network: '网络错误，请检查网络连接',
  server: '服务器错误，请稍后重试',
  unauthorized: '请先登录',
  forbidden: '没有权限进行此操作',
  validation: '输入数据有误，请检查'
} 