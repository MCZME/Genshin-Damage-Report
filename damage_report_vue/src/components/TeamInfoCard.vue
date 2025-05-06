<template>
  <div v-if="team" class="team-card">
    <div class="team-card-header d-flex justify-space-between">
      <span>{{ team.name }}</span>
      <div class="d-flex align-center" style="gap: 8px">
        <span class="chip">DPS: {{ team.dps }}万</span>
        <span class="chip">模拟时间: {{ team.simulationTime }}s</span>
        <span class="chip">{{ formatDate(team.createdAt) }}</span>
      </div>
    </div>

    <div class="team-card-divider"></div>

    <div class="team-card-content">
      <!-- 成员信息 -->
      <div class="member-grid">
        <div class="member-card" v-for="(member, index) in team.members" :key="index">
          <CharacterAvatar
            :name="member.name"
            :element="member.element">
          </CharacterAvatar>
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
          <!-- 武器和圣遗物 -->
          <div class="equipment-container">
            <!-- 武器 -->
            <div :class="['weapon-container', getArtifactCount(member.artifacts) === 0 ? 'flex-1' : 'flex-1']">
              <div class="equipment-image-container">
                <div class = 'equipment-img'>
                  <img
                  :src="getWeaponImage(member.weapon.name)"
                  class="equipment-image"
                  >
                  <div class="refinement-badge" v-if="member.weapon.refinement">
                    {{ member.weapon.refinement }}
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 圣遗物 -->
            <div :class="['artifacts-container', getArtifactCount(member.artifacts) === 0 ? 'flex-1' : getArtifactCount(member.artifacts) === 1 ? 'flex-1' : 'flex-2']">
              <template v-if="!member.artifacts.set1 && !member.artifacts.set2">
                <div class="no-set-effect">无套装效果</div>
              </template>
              <template v-else-if="member.artifacts.set1 === member.artifacts.set2">
                <div class="equipment-image-container">
                  <img
                    :src="getArtifactImage(member.artifacts.set1)"
                    class="equipment-image"
                  >
                    <div class="set-effect-badge">
                      {{ member.artifacts.set1Count }}
                    </div>
                </div>
              </template>
              <template v-else>
                <div class="equipment-image-container">
                  <img
                    :src="getArtifactImage(member.artifacts.set1)"
                    class="equipment-image"
                  >
                  <div class="set-effect-badge">{{ member.artifacts.set1Count }}</div>
                </div>
                <div class="equipment-image-container" v-if="member.artifacts.set2">
                  <img
                    :src="getArtifactImage(member.artifacts.set2)"
                    class="equipment-image"
                  >
                  <div class="set-effect-badge">{{ member.artifacts.set2Count }}</div>
                </div>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import config from '@/config'
import CharacterAvatar from './CharacterAvatar.vue'

export default {
  name: 'TeamInfoCard',
  components: {
    CharacterAvatar
  },
  props: {
    uid: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      team: null,
      loading: false,
      error: null,
      weaponUrls: {},
      artifactUrls: {},
      // 缓存元素类型
      elementCache: {},
      // 防抖计时器
      debounceTimer: null
    }
  },
  async created() {
    await this.fetchTeamData();
  },
  watch: {
    uid: {
      immediate: true,
      handler: 'fetchTeamData'
    }
  },
  methods: {
    formatDate(timestamp) {
      return new Date(timestamp).toLocaleDateString()
    },
    getWeaponImage(weaponName) {
      return this.weaponUrls[weaponName] || ``
    },
    getArtifactImage(artifactName) {
      return this.artifactUrls[artifactName] || ``
    },
    // 简单防抖函数
    debounce(func, delay) {
      clearTimeout(this.debounceTimer);
      this.debounceTimer = setTimeout(func, delay);
    },

    async fetchTeamData() {
      // 使用防抖包装实际请求
      return new Promise((resolve) => {
        this.debounce(async () => {
          this.loading = true;
          this.error = null;
          
          try {
            // 1. 获取原始队伍数据
            const response = await axios.get(`${config.api.baseUrl}${config.api.endpoints.card_uid}/${this.uid}`);
            const data = response.data.data;
            
            // 2. 处理成员数据
            const memberNames = data.team_data
              .filter(member => !member.error)
              .map(member => member.character.name);
            
            // 批量获取元素类型
            await this.getCharacterElement(memberNames);
            
            const processedMembers = data.team_data
              .filter(member => !member.error)
              .map((member, index) => {
                const [talentAttack, talentSkill, talentBurst] = 
                  member.character.talents.split('/').map(Number);
                
                // 统计圣遗物套装数量
                const artifactCounts = {};
                member.artifacts.forEach(artifact => {
                  artifactCounts[artifact.set_name] = (artifactCounts[artifact.set_name] || 0) + 1;
                });
                
                // 确定圣遗物套装效果
                let set1 = null, set1Count = 0;
                let set2 = null, set2Count = 0;
                
                Object.entries(artifactCounts).forEach(([setName, count]) => {
                  if (count >= 4) {
                    set1 = setName;
                    set1Count = 4;
                  } else if (count >= 2) {
                    if (!set1) {
                      set1 = setName;
                      set1Count = 2;
                    } else if (!set2) {
                      set2 = setName;
                      set2Count = 2;
                    }
                  }
                });

                return {
                  name: member.character.name,
                  level: member.character.level,
                  element: this.elementCache[member.character.name],
                  constellation: member.character.constellation,
                  talentLevels: [talentAttack, talentSkill, talentBurst],
                  weapon: {
                    name: member.weapon.name,
                    refinement: member.weapon.refinement
                  },
                  artifacts: {
                    set1,
                    set1Count,
                    set2,
                    set2Count
                  }
                };
              });

            // 3. 设置队伍数据
            this.team = {
              name: data.name,
              dps: (data.dps / 10000).toFixed(2),
              simulationTime: (data.simulation_duration / 60).toFixed(2),
              createdAt: new Date(data.created_at).getTime(),
              members: processedMembers
            };

            // 4. 并行加载所有图片
            await Promise.all([
              this.loadWeapons(),
              this.loadArtifacts()
            ]);
          } catch (err) {
            this.error = err.response?.data?.message || '获取队伍数据失败';
            console.error('获取队伍数据失败:', err);
          } finally {
            this.loading = false;
            resolve();
          }
        }, 300); // 防抖延迟300ms
      });
    },
    getArtifactCount(artifacts) {
      let count = 0;
      if (artifacts.set1) count++;
      if (artifacts.set2 && artifacts.set1 !== artifacts.set2) count++;
      return count;
    },
    async loadWeapons() {
      await Promise.all(this.team.members.map(async member => {
        // 如果已有缓存则跳过
        if (this.weaponUrls[member.weapon.name]) return;
        
        try {
          const response = await axios.get(`${config.api.baseUrl}${config.api.endpoints.weapon}`, {
            params: { name: member.weapon.name }
          });
          this.weaponUrls[member.weapon.name] = response.data.file_path || '/assets/default-weapon.png';
        } catch (error) {
          console.error('获取武器图片失败:', error);
          this.weaponUrls[member.weapon.name] = '/assets/default-weapon.png';
        }
      }));
    },
    async getCharacterElement(teamMember) {
      // 检查缓存是否已包含所有需要的元素
      const uncachedMembers = teamMember.filter(name => !this.elementCache[name]);
      
      if (uncachedMembers.length === 0) {
        return teamMember.map(name => this.elementCache[name]);
      }
      
      try {
        const response = await axios.get(`${config.api.baseUrl}${config.api.endpoints.character}/element`, {
          params: { 
            teamMember: uncachedMembers 
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
          this.elementCache[item.name] = item.element;
        });
      
      } catch (error) {
        console.error('获取角色元素类型失败:', error);
      }
    },
    async loadArtifacts() {
      const artifactRequests = [];
      
      this.team.members.forEach(member => {
        if (member.artifacts.set1 && !this.artifactUrls[member.artifacts.set1]) {
          artifactRequests.push(
            axios.get(`${config.api.baseUrl}${config.api.endpoints.artifact}`, {
              params: { name: member.artifacts.set1 }
            })
            .then(response => {
              this.artifactUrls[member.artifacts.set1] = response.data.file_path || '/assets/default-artifact.png';
            })
            .catch(error => {
              console.error('获取圣遗物图片失败:', error);
              this.artifactUrls[member.artifacts.set1] = '/assets/default-artifact.png';
            })
          );
        }
        
        if (member.artifacts.set2 && !this.artifactUrls[member.artifacts.set2]) {
          artifactRequests.push(
            axios.get(`${config.api.baseUrl}${config.api.endpoints.artifact}`, {
              params: { name: member.artifacts.set2 }
            })
            .then(response => {
              this.artifactUrls[member.artifacts.set2] = response.data.file_path || '/assets/default-artifact.png';
            })
            .catch(error => {
              console.error('获取圣遗物图片失败:', error);
              this.artifactUrls[member.artifacts.set2] = '/assets/default-artifact.png';
            })
          );
        }
      });
      
      await Promise.all(artifactRequests);
    }
  }
}
</script>

<style scoped>
.team-card {
  margin: 12px;
  max-width: 500px;
  background: rgba(var(--v-theme-surface), 1);
  border-radius: 12px;
  box-shadow: 0 1px 2px 0 rgba(0,0,0,0.3), 
              0 1px 3px 1px rgba(0,0,0,0.15);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.team-card:hover {
  box-shadow: 0 2px 4px 0 rgba(0,0,0,0.3), 
              0 4px 8px 3px rgba(0,0,0,0.15);
}

.team-card-header {
  padding: 16px 16px 12px;
  font-size: 1.25rem;
  font-weight: 500;
  letter-spacing: 0.00625em;
}

.team-card-divider {
  height: 1px;
  background-color: rgba(var(--v-theme-accent), 1);
  margin: 0 16px;
}

.team-card-content {
  padding: 6px 8px 6px;
}

.chip {
  background: rgba(var(--v-theme-secondary), 1);
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 0.875rem;
  font-weight: 500;
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
  display: flex;
}

.artifacts-container {
  display: flex;
  gap: 4px;
  justify-content: end;
}

.flex-1 {
  flex: 1;
}

.flex-2 {
  flex: 2;
}

.equipment-image-container {
  position: relative;
  width: 100%;
  height: 40px;
  display: flex;
  justify-content: start;
}

.equipment-img {
  height: 100%;
  width: fit-content;
}

.equipment-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.refinement-badge,
.set-effect-badge {
  position: absolute;
  top: 0;
  right: 0;
  background: rgba(0,0,0,0.5);
  color: rgb(255, 162, 0);
  padding: 1px 1px;
  font-size: 0.6rem;
  border-radius: 0 0 0 6px;
}

.refinement-badge {
  transform: translateX(calc(-100% - 2px));
}

.set-effect-badge {
  transform: translateX(calc(-100% + 2px));
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
