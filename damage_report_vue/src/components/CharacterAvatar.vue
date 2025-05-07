<template>
  <div 
    class="avatar-container"
    @mouseenter="handleMouseEnter"
    @mouseleave="handleMouseLeave"
  >
    <!-- 背景层 - 星空 -->
    <v-img
      cover
      :src="'http://116.198.207.202:40061/i/2025/05/01/3e2suj.png'"
      width="100%"
      height="100%"
      class="member-bg"
      :style="{'filter': getElementFilter(element)}"
    ></v-img>
    
    <!-- 中间层 - 元素图标 -->
    <v-img
      :src="getElementImage(element)"
      width="100%"
      height="100%"
      class="member-element"
    ></v-img>
    
    <!-- 上层 - 角色头像 -->
    <v-img
      :src="getCharacterImage()"
      :alt="name"
      width="100%"
      height="100%"
      class="member-avatar"
    ></v-img>

    <!-- 详情卡片 -->
    <div 
      v-if="showCard && data && Object.keys(data).length > 0"
      class="detail-card"
    >
      <div class="card-content">
        <!-- 第一行：角色信息 -->
        <div class="card-row">
          <span class="card-name">{{ data.character.name }}</span>
          <span class="card-level">Lv.{{ data.character.level }}</span>
          <span class="card-constellation">命座{{ data.character.constellation }}</span>
        </div>
        
        <!-- 第二行：武器信息 -->
        <div class="card-row">
          <span class="card-weapon">{{ data.weapon.name }}</span>
          <span class="card-weapon-level">Lv.{{ data.weapon.level }}</span>
          <span class="card-refinement">精{{ data.weapon.refinement }}</span>
        </div>
        
        <!-- 圣遗物信息 -->
        <div class="artifacts-section">
          <div v-for="artifact in data.artifacts" :key="artifact.slot" class="artifact-item">
            <div class="artifact-header">
              <span class="artifact-slot">{{ artifact.slot }}</span>
              <span class="artifact-set">{{ artifact.set_name }}</span>
            </div>
            <div class="artifact-stats">
              <div v-for="(value, stat) in artifact.main_stat" :key="'main-'+stat" class="main-stat">
                {{ stat }}: {{ value }}
              </div>
              <div v-for="(value, stat) in artifact.sub_stats" :key="'sub-'+stat" class="sub-stat">
                {{ stat }}: {{ value }}
              </div>
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
import apiService from '@/api/api'

export default {
  name: 'CharacterAvatar',
  data() {
    return {
      avatarUrls: {},
      debounceTimer: null,
      showCard: false,
      isLoading: false,
      defaultAvatar: '/assets/default-avatar.png',
      hoverZIndex: 1
    }
  },
  props: {
    name: {
      type: String,
      required: true
    },
    element: {
      type: String,
      required: false,
      default: ''
    },
    data: {
      type: Object,
      default: null
    }
  },
  methods: {
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
    debounce(func, delay) {
      clearTimeout(this.debounceTimer);
      this.debounceTimer = setTimeout(func, delay);
    },
    async loadAvatar() {
      if (this.avatarUrls[this.name]) {
        return Promise.resolve();
      }
      
      return new Promise((resolve) => {
        this.debounce(async () => {
          this.avatarUrls[this.name] = await apiService.getAvatar(this.name);
          resolve();
        }, 300);
      });
    },
    getCharacterImage() {
      if (!this.avatarUrls[this.name] && !this.isLoading) {
        this.isLoading = true;
        this.loadAvatar().finally(() => {
          this.isLoading = false;
        });
        return this.defaultAvatar;
      }
      return this.avatarUrls[this.name] || this.defaultAvatar;
    },
    handleMouseEnter() {
      if (this.data && Object.keys(this.data).length > 0) {
        this.showCard = true;
        this.hoverZIndex = 10;
      }
    },
    handleMouseLeave() {
      this.hoverZIndex = 1;
      this.showCard = false;
    }
  }
}
</script>

<style scoped>
.avatar-container {
  position: relative;
  width: 100px;
  height: 100px;
  overflow: visible;
  z-index: v-bind(hoverZIndex);
}

.member-bg,
.member-element,
.member-avatar {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 2;
}

.member-bg{
  object-fit: fill;
  width: 100%;
  height: 100%;
}

.member-element {
  opacity: 0.7;
}

.member-avatar {
  border-radius: 4px;
}

.detail-card {
  position: absolute;
  top: 0;
  left: 0;
  width: 200px;
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  z-index: 1;
  padding: 8px;
  transform: translate(-10px, -10px);
  animation: cardExpand 0.2s ease-out;
}

@keyframes cardExpand {
  from {
    transform: scale(0.5);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.card-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  padding-bottom: 4px;
  border-bottom: 1px solid #eee;
}

.card-name {
  font-weight: bold;
  font-size: 1.1em;
}

.artifacts-section {
  margin-top: 8px;
}

.artifact-item {
  margin-bottom: 8px;
  padding-bottom: 4px;
  border-bottom: 1px dashed #eee;
}

.artifact-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
}

.artifact-slot {
  font-weight: bold;
}

.artifact-set {
  color: #666;
  font-size: 0.9em;
}

.main-stat {
  font-weight: bold;
  color: #4a6baf;
}

.sub-stat {
  color: #666;
  font-size: 0.9em;
}
</style>
