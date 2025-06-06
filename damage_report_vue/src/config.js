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
      card_uid: '/api/card-data',
      character: '/api/character',
      sim: '/api/sim-data',
    },
    timeout: 10000 // 请求超时时间(毫秒)s
  },

  // 应用设置
  app: {
    maxUploadSize: 5 * 1024 * 1024, // 5MB
    defaultPageSize: 10,
    enableAnalytics: false
  }
}
