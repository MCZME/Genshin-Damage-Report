import axios from 'axios'
import config from '../config.js'

// 缓存对象
const cache = {
  weaponUrls: {},
  artifactUrls: {},
  elementCache: {},
  avatarUrls: {}
}

const apiService = {
  /**
   * 获取角色头像
   * @param {string} name 角色名称
   * @returns {Promise<string>} 头像URL
   */
  async getAvatar(name) {
    if (cache.avatarUrls[name]) {
      return cache.avatarUrls[name]
    }
    
    try {
      const response = await axios.get(`${config.api.baseUrl}${config.api.endpoints.avatar}`, {
        params: { name }
      })
      cache.avatarUrls[name] = `http://116.198.207.202:40061${response.data.file_path}` || '/assets/default-avatar.png'
      return cache.avatarUrls[name]
    } catch (error) {
      console.error('获取头像失败:', error)
      cache.avatarUrls[name] = '/assets/default-avatar.png'
      return cache.avatarUrls[name]
    }
  },

  /**
   * 获取武器图片
   * @param {string} name 武器名称
   * @returns {Promise<string>} 武器图片URL
   */
  async getWeaponImage(name) {
    if (cache.weaponUrls[name]) {
      return cache.weaponUrls[name]
    }
    
    try {
      const response = await axios.get(`${config.api.baseUrl}${config.api.endpoints.weapon}`, {
        params: { name }
      })
      cache.weaponUrls[name] = response.data.file_path || '/assets/default-weapon.png'
      return cache.weaponUrls[name]
    } catch (error) {
      console.error('获取武器图片失败:', error)
      cache.weaponUrls[name] = '/assets/default-weapon.png'
      return cache.weaponUrls[name]
    }
  },

  /**
   * 获取角色元素类型
   * @param {Array<string>} names 角色名称数组
   * @returns {Promise<Object>} 角色元素类型映射
   */
  async getCharacterElements(names) {
    // 过滤已缓存的角色
    const uncachedNames = names.filter(name => !cache.elementCache[name])
    
    if (uncachedNames.length > 0) {
      try {
        const response = await axios.get(`${config.api.baseUrl}${config.api.endpoints.character}/element`, {
          params: { teamMember: uncachedNames },
          paramsSerializer: params => {
            return Object.entries(params)
              .flatMap(([key, values]) => 
                Array.isArray(values) 
                  ? values.map(v => `${key}=${encodeURIComponent(v)}`)
                  : `${key}=${encodeURIComponent(values)}`
              )
              .join('&')
          }
        })
        
        // 更新缓存
        response.data.data.forEach(item => {
          cache.elementCache[item.name] = item.element
        })
      } catch (error) {
        console.error('获取角色元素类型失败:', error)
      }
    }
    
    // 返回所有请求角色的元素类型
    return names.reduce((result, name) => {
      result[name] = cache.elementCache[name]
      return result
    }, {})
  },

  /**
   * 获取圣遗物图片
   * @param {string} name 圣遗物名称
   * @returns {Promise<string>} 圣遗物图片URL
   */
  async getArtifactImage(name) {
    if (cache.artifactUrls[name]) {
      return cache.artifactUrls[name]
    }
    
    try {
      const response = await axios.get(`${config.api.baseUrl}${config.api.endpoints.artifact}`, {
        params: { name }
      })
      cache.artifactUrls[name] = response.data.file_path || '/assets/default-artifact.png'
      return cache.artifactUrls[name]
    } catch (error) {
      console.error('获取圣遗物图片失败:', error)
      cache.artifactUrls[name] = '/assets/default-artifact.png'
      return cache.artifactUrls[name]
    }
  },

  /**
   * 获取队伍数据
   * @param {string} uid 用户UID
   * @returns {Promise<Object>} 队伍数据
   */
  async getTeamData(uid) {
    try {
      const response = await axios.get(`${config.api.baseUrl}${config.api.endpoints.card_uid}/${uid}`)
      return response.data
    } catch (error) {
      console.error('获取队伍数据失败:', error)
      throw error
    }
  }
}

export default apiService
