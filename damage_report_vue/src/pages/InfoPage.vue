<template>
  <div class="info-page">
    <NavBar />
    <div class="content">
      <div class="layout-container">
        <div class="left-panel">
          <div class="static-info">
            <h2>队伍信息</h2>
            <p>这里可以显示一些静态信息或统计数据</p>
          </div>
        </div>
        <div class="right-panel">
          <div class="card-header">
            <div class="header-content">
              <h3 class="header-title">队伍列表</h3>
              <div class="header-actions">
                <button class="header-btn">
                  <v-icon icon="mdi-refresh"></v-icon>
                </button>
                <button class="header-btn">
                  <v-icon icon="mdi-filter"></v-icon>
                </button>
                <button class="header-btn">
                  <v-icon icon="mdi-sort"></v-icon>
                </button>
                
              </div>
            </div>
          </div>
          <div class="card-container">
            <v-row>
              <v-col v-for="(team, index) in teams"
                  :key="index"
                  cols="12"
                  sm="6"
                  md="6">
                <TeamInfoCard :team="team" />
              </v-col>
            </v-row>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import TeamInfoCard from '@/components/TeamInfoCard.vue'

export default {
  name: 'InfoPage',
  components: {
    NavBar,
    TeamInfoCard
  },
  data() {
    return {
      teams: [
        {
          name: '雷神国家队',
          members: [
            {
              name: '雷电将军',
              avatar: 'https://example.com/raiden.png',
              level: 90,
              element: '雷',
              constellation: 2,
              talentLevels: [9, 9, 10],
              weapon: '薙草之稻光',
              artifacts: ['绝缘之旗印4件']
            },
            {
              name: '行秋',
              avatar: 'https://example.com/xingqiu.png',
              level: 80,
              element: '水',
              constellation: 6,
              talentLevels: [1, 9, 9],
              weapon: '祭礼剑',
              artifacts: ['沉沦之心2件', '宗室2件']
            },
            {
              name: '香菱',
              avatar: 'https://example.com/xiangling.png',
              level: 80,
              element: '火',
              constellation: 4,
              talentLevels: [1, 8, 8],
              weapon: '「渔获」',
              artifacts: ['绝缘之旗印']
            },
            {
              name: '班尼特',
              avatar: 'https://example.com/bennett.png',
              level: 80,
              element: '火',
              constellation: 1,
              talentLevels: [1, 8, 8],
              weapon: '天空之刃',
              artifacts: ['宗室4件']
            }
          ],
          description: '经典雷神国家队配置，通过元素反应打出高额伤害',
          dps: 45000,
          simulationTime: 90,
          createdAt: Date.now()
        }
      ]
    }
  }
}
</script>

<style scoped>
.info-page {
  min-height: 100vh;
  background: rgb(var(--v-theme-background));
}

.content {
  padding: 1rem;
  height: 90%;
}

.layout-container {
  display: flex;
  gap: 1rem;
  height: 100%;
}

.left-panel {
  width: 20%;
  background: rgba(var(--v-theme-background_light), 1);
  height: 100%;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.right-panel {
  width: 75%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: rgba(var(--v-theme-background_light), 1);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.card-header {
  border-bottom: 1px solid rgba(var(--v-border-color), 0.12);
  padding: 12px 16px;
  background: rgba(var(--v-theme-surface), 1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 500;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.header-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 8px;
  color: rgba(var(--v-theme-on-surface), 1);
  border-radius: 50%;
  transition: background-color 0.2s ease-in-out;
}

.header-btn:hover {
  background: rgba(var(--v-theme-on-surface), 0.08);
}

.header-btn:active {
  background: rgba(var(--v-theme-on-surface), 0.16);
}

.card-container {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  margin-top: 0;
}

.static-info {
  padding: 1rem;
  /* background: rgba(var(--v-theme-surface), 0.5); */
  border-radius: 8px;
  height: 100%;
}
</style>
