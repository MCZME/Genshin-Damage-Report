<template>
  <div class="dashboard-container">
    <div class="dashboard">
      <h1>队伍伤害仪表盘</h1>
    </div>
    <SideBar :characters="this.avatarUrls"></SideBar>
  </div>
</template>

<script>
import axios from 'axios'
import config from '@/config'
import SideBar from '../components/SideBar.vue'

export default {
  name: 'TeamDashboardPage',
  components: { SideBar },
  props: {
    uuid: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      team: null,
      avatarUrls: {}
    }
  },
  methods: {
    async getCharacterAvatar(team_data) {
      const avatar = []
      const newAvatars = {}
      team_data.map(char => {
        if (!char?.error) {
          avatar.push(char.character.name)
          newAvatars[char.character.name] = {
            data: char,
            element: this.avatarUrls[char.character.name]?.element || ''
          }
        }
      })
      this.avatarUrls = Object.assign({}, this.avatarUrls, newAvatars)
      await this.getCharacterElement(avatar)
    },
    async getCharacterElement(avatar) {
      try {
        const response = await axios.get(`${config.api.baseUrl}${config.api.endpoints.character}/element`, {
          params: { 
            teamMember: avatar 
          },
          paramsSerializer: params => {
            return Object.entries(params)
              .flatMap(([key, values]) => 
                Array.isArray(values) 
                  ? values.map(v => `${key}=${encodeURIComponent(v)}`)
                  : `${key}=${encodeURIComponent(values)}`
              )
              .join('&');
          }
        });
        
        // 更新缓存
        response.data.data.forEach(item => {
          this.avatarUrls[item.name].element = item.element || '';
        });
      
      } catch (error) {
        console.error('获取角色元素类型失败:', error);
      }
    }
  },
  async created() {
    try {
      const response = await axios.get(
        `${this.$config.api.baseUrl}${this.$config.api.endpoints.sim}/${this.uuid}`
      )
      if (response.data.code === 200) {
        this.team = response.data.data
        // 预加载角色头像
        if (this.team?.team_data) {
          await this.getCharacterAvatar(this.team.team_data)
        }
      } else {
        console.error('获取队伍数据失败:', response.data.message)
      }
    } catch (error) {
      console.error('获取队伍数据失败:', error)
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  display: flex;
  min-height: 100vh;
}

.dashboard {
  padding: 20px;
  max-width: calc(100% - 280px);
  margin-left: 280px;
  flex-grow: 1;
  min-height: 100vh;
  background: var(--background);
}

.loading {
  display: flex;
  justify-content: center;
  margin-top: 50px;
}

.team-card {
  max-width: 600px;
  margin: 20px auto;
}

.team-card {
  background: var(--card-bg);
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.team-card:hover {
  transform: translateY(-5px);
}

.team-card h3 {
  margin-top: 0;
  color: var(--text-primary);
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 10px;
}

.team-card p {
  margin: 8px 0;
  color: var(--text-secondary);
}
</style>
