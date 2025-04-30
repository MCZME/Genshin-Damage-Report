<template>
  <v-card class="team-card" :elevation="4">
    <v-card-title class="d-flex justify-space-between">
      <span>{{ team.name }}</span>
      <div class="d-flex align-center">
        <div class="text-center mr-4">
          <div class="text-caption">DPS</div>
          <div class="text-h6">{{ team.dps }}</div>
        </div>
        <div class="text-center mr-4">
          <div class="text-caption">模拟时间</div>
          <div class="text-h6">{{ team.simulationTime }}s</div>
        </div>
        <v-chip color="primary" small>
          {{ formatDate(team.createdAt) }}
        </v-chip>
      </div>
    </v-card-title>

    <v-divider></v-divider>

    <v-card-text>
      <!-- 成员信息 -->
      <div class="member-grid">
        <div class="member-card" v-for="(member, index) in team.members" :key="index">
          <div class="avatar-container">
            <!-- 背景层 - 星空 -->
            <v-img
              cover
              :src="'http://116.198.207.202:40061/i/2025/05/01/3e2suj.png'"
              width="80"
              height="80"
              class="member-bg"
              :style="{'filter': getElementFilter(member.element)}"
            ></v-img>
            
            <!-- 中间层 - 元素图标 -->
            <v-img
              :src="getElementImage(member.element)"
              width="80"
              height="80"
              class="member-element"
            ></v-img>
            
            <!-- 上层 - 角色头像 -->
            <v-img
              :src="getCharacterImage(member.name)"
              :alt="member.name"
              width="80"
              height="80"
              class="member-avatar"
            ></v-img>
            
            <!-- 等级 -->
            <div class="level-badge">
              Lv{{ member.level }}
            </div>
            
            <!-- 命座 -->
            <div class="constellation-badge">
              {{ member.constellation }}
            </div>
            
            <!-- 天赋 -->
            <div class="talents-badge">
              天赋:{{ member.talentLevels.join('/') }}
            </div>
          </div>
        </div>
      </div>

      <!-- 文本介绍 -->
      <div class="description mt-4">
        <p class="text-body-2">{{ team.description }}</p>
      </div>

    </v-card-text>
  </v-card>
</template>

<script>
import axios from 'axios'
import config from '@/config'

export default {
  name: 'TeamInfoCard',
  data() {
    return {
      avatarUrls: {}
    }
  },
  props: {
    team: {
      type: Object,
      required: true,
      validator: (value) => {
        return (
          value.name &&
          Array.isArray(value.members) &&
          value.members.length <= 4 &&
          value.dps &&
          value.simulationTime &&
          value.createdAt
        )
      }
    }
  },
  async created() {
    await this.loadAvatars()
  },
  methods: {
    formatDate(timestamp) {
      return new Date(timestamp).toLocaleDateString()
    },
    getWeaponImage(weaponName) {
      return `https://example.com/weapons/${weaponName}.png`
    },
    getArtifactImage(artifactName) {
      return `https://example.com/artifacts/${artifactName}.png`
    },
    getCharacterImage(characterName) {
      return this.avatarUrls[characterName] || '/assets/default-avatar.png'
    },
    getElementImage(element) {
      const elementImages = {
        '岩': 'http://116.198.207.202:40061/i/2025/05/01/2m926v.png',
        '水': 'http://116.198.207.202:40061/i/2025/05/01/2m8zm2.png',
        '雷': 'http://116.198.207.202:40061/i/2025/05/01/2m91og.png',
        '草': 'http://116.198.207.202:40061/i/2025/05/01/2m90rg.png',
        '风': 'http://116.198.207.202:40061/i/2025/05/01/2m9093.png',
        '火': 'http://116.198.207.202:40061/i/2025/05/01/2m8zpq.png',
        '冰': 'http://116.198.207.202:40061/i/2025/05/01/2m8yg4.png'
      }
      return elementImages[element] || ''
    },
    getElementFilter(element) {
      const elementColors = {
        '岩': 'sepia(100%) saturate(300%) hue-rotate(30deg)',
        '水': 'sepia(100%) saturate(300%) hue-rotate(180deg)',
        '雷': 'sepia(100%) saturate(300%) hue-rotate(270deg)',
        '草': 'sepia(100%) saturate(300%) hue-rotate(90deg)',
        '风': 'sepia(100%) saturate(300%) hue-rotate(150deg)',
        '火': 'sepia(100%) saturate(400%) hue-rotate(-30deg)',
        '冰': 'sepia(100%) saturate(300%) hue-rotate(210deg)'
      }
      return elementColors[element] || ''
    },
    async loadAvatars() {
      for (const member of this.team.members) {
        try {
          const response = await axios.get(`${config.api.baseUrl}${config.api.endpoints.avatar}`, {
            params: { name: member.name }
          })
          this.avatarUrls[member.name] = `http://116.198.207.202:40061${response.data.file_path}` || '/assets/default-avatar.png'
        } catch (error) {
          console.error('获取头像失败:', error)
          this.avatarUrls[member.name] = '/assets/default-avatar.png'
        }
      }
    }
  }
}
</script>

<style scoped>
.team-card {
  margin: 12px;
  max-width: 500px;
}

.member-grid {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  justify-content: center;
}

.member-card {
  position: relative;
}

.avatar-container {
  position: relative;
  width: 80px;
  height: 100px;
}

.member-bg,
.member-element,
.member-avatar {
  position: absolute;
  top: 0;
  left: 0;
  border-radius: 4px;
}

.member-bg{
  z-index: 1;
  object-fit: fill;
  width: 100%;
  height: 100%;
}

.member-element {
  z-index: 2;
  opacity: 0.7;
}

.member-avatar {
  z-index: 3;
}

.member-avatar {
  border-radius: 4px;
}

.level-badge {
  position: absolute;
  top: 0;
  left: 0;
  background: rgba(0,0,0,0.7);
  color: white;
  padding: 2px 4px;
  font-size: 0.7rem;
  border-radius: 0 0 4px 0;
}

.constellation-badge {
  position: absolute;
  top: 0;
  right: 0;
  background: rgba(0,0,0,0.7);
  color: gold;
  padding: 2px 4px;
  font-size: 0.7rem;
  border-radius: 0 0 0 4px;
}

.talents-badge {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0,0,0,0.7);
  color: white;
  padding: 2px;
  font-size: 0.7rem;
  text-align: center;
  border-radius: 0 0 4px 4px;
}

.description {
  white-space: pre-line;
}

.member-stats {
  padding: 8px;
}

.basic-stats {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.equipment {
  display: flex;
  align-items: center;
  gap: 12px;
}

.artifacts {
  display: flex;
  gap: 4px;
}
</style>
