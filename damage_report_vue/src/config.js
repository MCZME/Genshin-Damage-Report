// 前端应用配置
export default {
  // API配置
  api: {
    baseUrl: 'http://localhost:8000',
    endpoints: {
      damageReport: '/api/damage-reports',
      stickers: '/api/stickers',
      auth: '/api/auth',
      avatar: '/api/avatar',
      weapon: '/api/weapon',
      artifact: '/api/artifact',
    },
    timeout: 10000 // 请求超时时间(毫秒)
  },

  // 主题配置
  theme: {
    primaryColor: '#4a6baf',
    secondaryColor: '#6c757d',
    dangerColor: '#dc3545',
    successColor: '#28a745',
    textColor: '#212529',
    borderRadius: '4px'
  },

  // 应用设置
  app: {
    maxUploadSize: 5 * 1024 * 1024, // 5MB
    defaultPageSize: 10,
    enableAnalytics: false
  }
}
