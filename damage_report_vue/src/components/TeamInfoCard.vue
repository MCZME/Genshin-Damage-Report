<template>
  <v-card class="team-card" :elevation="4">
    <v-card-title class="d-flex justify-space-between">
      <span>{{ team.name }}</span>
      <div class="d-flex align-center" style="gap: 8px">
        <v-chip color="primary" small>
          DPS: {{ team.dps }}
        </v-chip>
        <v-chip color="primary" small>
          模拟时间: {{ team.simulationTime }}s
        </v-chip>
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
              width="100%"
              height="100%"
              class="member-bg"
              :style="{'filter': getElementFilter(member.element)}"
            ></v-img>
            
            <!-- 中间层 - 元素图标 -->
            <v-img
              :src="getElementImage(member.element)"
              width="100%"
              height="100%"
              class="member-element"
            ></v-img>
            
            <!-- 上层 - 角色头像 -->
            <v-img
              :src="getCharacterImage(member.name)"
              :alt="member.name"
              width="100%"
              height="100%"
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
          </div>
          <!-- 天赋 -->
          <div class="talents-badge">
              天赋:{{ member.talentLevels.join('/') }}
          </div>
          <!-- 武器和圣遗物 -->
          <div class="equipment-container">
            <!-- 武器 -->
            <div class="weapon-container">
              <div class="equipment-image-container">
                <v-img
                  :src="getWeaponImage(member.weapon)"
                  class="equipment-image"
                ></v-img>
                <div class="refinement-badge" v-if="member.weapon.refinement">
                  R{{ member.weapon.refinement }}
                </div>
              </div>
            </div>
            
            <!-- 圣遗物 -->
            <div class="artifacts-container">
              <template v-if="!member.artifacts.set1 && !member.artifacts.set2">
                <div class="no-set-effect">无套装效果</div>
              </template>
              <template v-else-if="member.artifacts.set1 === member.artifacts.set2">
                <div class="equipment-image-container">
                  <v-img
                    :src="getArtifactImage(member.artifacts.set1)"
                    class="equipment-image"
                  ></v-img>
                  <div class="set-effect-badge">
                    {{ member.artifacts.set1Count }}
                  </div>
                </div>
              </template>
              <template v-else>
                <div class="equipment-image-container">
                  <v-img
                    :src="getArtifactImage(member.artifacts.set1)"
                    class="equipment-image"
                  ></v-img>
                  <div class="set-effect-badge">2</div>
                </div>
                <div class="equipment-image-container" v-if="member.artifacts.set2">
                  <v-img
                    :src="getArtifactImage(member.artifacts.set2)"
                    class="equipment-image"
                  ></v-img>
                  <div class="set-effect-badge">2</div>
                </div>
              </template>
            </div>
          </div>
        </div>
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
      avatarUrls: {},
      weaponUrls: {},
      artifactUrls: {}
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
    await Promise.all([
      this.loadAvatars(),
      this.loadWeapons(),
      this.loadArtifacts()
    ])
  },
  methods: {
    formatDate(timestamp) {
      return new Date(timestamp).toLocaleDateString()
    },
    getWeaponImage(weaponName) {
      return this.weaponUrls[weaponName] || `https://example.com/weapons/${weaponName}.png`
    },
    getArtifactImage(artifactName) {
      return this.artifactUrls[artifactName] || `https://example.com/artifacts/${artifactName}.png`
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
    },
    async loadWeapons() {
      for (const member of this.team.members) {
        try {
          const response = await axios.get(`${config.api.baseUrl}${config.api.endpoints.weapon}`, {
            params: { name: member.weapon }
          })
          this.weaponUrls[member.weapon] = response.data.file_path || '/assets/default-weapon.png'
        } catch (error) {
          console.error('获取武器图片失败:', error)
          this.weaponUrls[member.weapon] = '/assets/default-weapon.png'
        }
      }
    },
    async loadArtifacts() {
      for (const member of this.team.members) {
        if (member.artifacts.set1) {
          try {
            const response = await axios.get(`${config.api.baseUrl}${config.api.endpoints.artifact}`, {
              params: { name: member.artifacts.set1 }
            })
            this.artifactUrls[member.artifacts.set1] = response.data.file_path || '/assets/default-artifact.png'
          } catch (error) {
            console.error('获取圣遗物图片失败:', error)
            this.artifactUrls[member.artifacts.set1] = '/assets/default-artifact.png'
          }
        }
        if (member.artifacts.set2 && member.artifacts.set2 !== member.artifacts.set1) {
          try {
            const response = await axios.get(`${config.api.baseUrl}${config.api.endpoints.artifact}`, {
              params: { name: member.artifacts.set2 }
            })
            this.artifactUrls[member.artifacts.set2] = response.data.file_path || '/assets/default-artifact.png'
          } catch (error) {
            console.error('获取圣遗物图片失败:', error)
            this.artifactUrls[member.artifacts.set2] = '/assets/default-artifact.png'
          }
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
  width: 100px;
  height: 100px;
}

.member-bg,
.member-element,
.member-avatar {
  position: absolute;
  top: 0;
  left: 0;
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
  top: 0px;
  left: 0;
  background: rgba(0,0,0,0.7);
  color: white;
  padding: 2px 4px;
  font-size: 0.7rem;
  border-radius: 0 0 4px 0;
  z-index: 4;
}

.constellation-badge {
  position: absolute;
  top: 0px;
  right: 0;
  background: rgba(0,0,0,0.7);
  color: gold;
  padding: 2px 4px;
  font-size: 0.7rem;
  border-radius: 0 0 0 4px;
  z-index: 4;
}

.talents-badge {
  position: relative;
  height: 1rem;
  left: 0;
  right: 0;
  background: rgba(0,0,0,0.7);
  color: white;
  font-size: 0.7rem;
  text-align: center;
  z-index: 4;
}

.equipment-container {
  display: flex;
}

.weapon-container {
  flex: 1;
}

.artifacts-container {
  flex: 2;
  display: flex;
  gap: 4px;
}

.equipment-image-container {
  position: relative;
  width: 100%;
  height: 40px;
}

.equipment-image {
  width: 100%;
  height: 100%;
  border-radius: 4px;
}

.refinement-badge,
.set-effect-badge {
  position: absolute;
  top: 0;
  right: 0;
  background: rgba(0,0,0,0.7);
  color: white;
  padding: 1px 3px;
  font-size: 0.6rem;
  border-radius: 0 0 0 4px;
}

.no-set-effect {
  font-size: 0.7rem;
  color: #999;
  text-align: center;
  line-height: 40px;
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
