<template>
  <div class="damage-page">
    <!-- 原神风格标题 -->
    <div class="genshin-header">
      <h1 class="text-h3 mb-2">伤害分析</h1>
      <div class="element-divider pyro"></div>
    </div>
    
    <div class="data-grid">
      <!-- DPS仪表盘 -->
      <v-card class="dashboard-card element-card">
        <v-card-title class="card-title">
          <v-icon color="pyro" class="mr-2">mdi-sword-cross</v-icon>
          实时DPS
        </v-card-title>
        <div class="dps-display">
          <span class="dps-value">42,568</span>
          <span class="dps-unit">/秒</span>
        </div>
        <v-progress-linear
          color="pyro"
          height="8"
          :value="85"
          striped
        ></v-progress-linear>
      </v-card>

      <!-- 元素反应统计 -->
      <v-card class="dashboard-card element-card">
        <v-card-title class="card-title">
          <v-icon color="anemo" class="mr-2">mdi-wind-power</v-icon>
          元素反应
        </v-card-title>
        <div class="reaction-chart">
          <div 
            class="reaction-item" 
            v-for="item in reactions" 
            :key="item.name"
            :style="{borderLeft: `4px solid var(--element-${item.element})`}"
          >
            <div class="reaction-icon" :class="`element-${item.element}`">
              <v-icon>{{ item.icon }}</v-icon>
            </div>
            <div class="reaction-info">
              <div class="reaction-name">{{ item.name }}</div>
              <v-progress-linear
                :color="item.element"
                height="6"
                :value="item.count * 4"
                rounded
              ></v-progress-linear>
              <div class="reaction-count">{{ item.count }}次触发</div>
            </div>
          </div>
        </div>
      </v-card>

      <!-- 队伍角色展示 -->
      <v-card class="dashboard-card team-card">
        <v-card-title class="card-title">
          <v-icon color="electro" class="mr-2">mdi-account-group</v-icon>
          当前队伍
        </v-card-title>
        <div class="team-members">
          <div 
            class="character" 
            v-for="char in characters" 
            :key="char.name"
            :style="{background: `linear-gradient(to right, rgba(0,0,0,0.3), var(--element-${char.element}-light))`}"
          >
            <div class="char-icon">
              <v-avatar size="60">
                <v-img :src="`/game_assets/characters/${char.img}`"></v-img>
              </v-avatar>
            </div>
            <div class="char-info">
              <div class="char-name">{{ char.name }}</div>
              <div class="char-dps">{{ char.dps }} DPS</div>
            </div>
          </div>
        </div>
      </v-card>
    </div>
  </div>
</template>

<script setup>
const reactions = [
  { name: '蒸发', element: 'pyro', icon: 'mdi-fire', count: 24 },
  { name: '融化', element: 'cryo', icon: 'mdi-snowflake', count: 18 },
  { name: '超载', element: 'electro', icon: 'mdi-lightning-bolt', count: 12 }
]

const characters = [
  { name: '胡桃', element: 'pyro', img: 'hutao.png', dps: '24,568' },
  { name: '行秋', element: 'hydro', img: 'xingqiu.png', dps: '8,742' },
  { name: '钟离', element: 'geo', img: 'zhongli.png', dps: '5,321' },
  { name: '夜兰', element: 'hydro', img: 'yelan.png', dps: '9,937' }
]
</script>

<style scoped>
.damage-page {
  color: white;
  padding: 20px;
  font-family: 'HYWenHei', sans-serif;
}

.genshin-header {
  text-align: center;
  margin-bottom: 2rem;
}

.genshin-header h1 {
  color: #fff;
  text-shadow: 0 0 10px rgba(230, 57, 70, 0.5);
  letter-spacing: 2px;
}

.element-divider {
  height: 4px;
  width: 120px;
  margin: 0 auto;
  border-radius: 2px;
}

.element-divider.pyro {
  background: linear-gradient(to right, transparent, var(--element-pyro), transparent);
}

.data-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: auto 1fr;
  gap: 30px;
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.dashboard-card {
  min-height: 300px;
}

.dps-display {
  padding: 40px 20px;
}

.dps-value {
  font-size: 4.5rem;
}

.team-card {
  grid-column: span 1;
  grid-row: span 2;
}

.reaction-chart {
  padding: 20px;
}

.dashboard-card {
  background: rgba(26, 26, 46, 0.7) !important;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.3s ease;
}

.dashboard-card:hover {
  transform: translateY(-5px);
}

.card-title {
  color: white !important;
  font-family: 'HYWenHei', sans-serif;
  padding: 16px !important;
  background: rgba(0, 0, 0, 0.2);
}

.dps-display {
  display: flex;
  align-items: baseline;
  justify-content: center;
  padding: 20px;
  flex-direction: column;
  align-items: center;
}

.dps-value {
  font-size: 3.5rem;
  font-weight: bold;
  color: var(--element-pyro);
  line-height: 1;
  text-shadow: 0 0 8px rgba(230, 57, 70, 0.5);
}

.dps-unit {
  font-size: 1.2rem;
  opacity: 0.8;
  margin-top: -10px;
}

.reaction-chart {
  padding: 10px 15px;
}

.reaction-item {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  padding: 8px 12px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  transition: all 0.3s ease;
}

.reaction-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.reaction-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  font-size: 1rem;
}

.reaction-info {
  flex: 1;
}

.reaction-name {
  font-weight: 600;
  margin-bottom: 4px;
}

.reaction-count {
  opacity: 0.7;
  font-size: 0.8rem;
  margin-top: 2px;
}

.team-members {
  padding: 10px;
}

.character {
  display: flex;
  align-items: center;
  padding: 12px;
  margin-bottom: 10px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.character:hover {
  transform: translateX(5px);
}

.char-icon {
  margin-right: 15px;
}

.char-info {
  flex: 1;
}

.char-name {
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 4px;
}

.char-dps {
  font-size: 0.9rem;
  opacity: 0.8;
}

/* 元素颜色变量 */
:root {
  --element-pyro: #e63946;
  --element-pyro-light: rgba(230, 57, 70, 0.2);
  --element-hydro: #42a5f5;
  --element-hydro-light: rgba(66, 165, 245, 0.2);
  --element-anemo: #74c7b8;
  --element-anemo-light: rgba(116, 199, 184, 0.2);
  --element-electro: #ab47bc;
  --element-electro-light: rgba(171, 71, 188, 0.2);
  --element-cryo: #90caf9;
  --element-cryo-light: rgba(144, 202, 249, 0.2);
  --element-geo: #ffb74d;
  --element-geo-light: rgba(255, 183, 77, 0.2);
  --element-dendro: #81c784;
  --element-dendro-light: rgba(129, 199, 132, 0.2);
}
</style>
