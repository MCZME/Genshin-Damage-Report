<template>
  <div class="avatar-container">
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
  </div>
</template>

<script>
import axios from 'axios'
import config from '@/config'

export default {
  name: 'CharacterAvatar',
  data() {
    return {
      avatarUrls: {},
      debounceTimer: null
    }
  },
  props: {
    name: {
      type: String,
      required: true
    },
    element: {
      type: String,
      required: true
    },
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
      if (this.avatarUrls[this.name]) return;
      
      return new Promise((resolve) => {
        this.debounce(async () => {
          try {
            const response = await axios.get(`${config.api.baseUrl}${config.api.endpoints.avatar}`, {
              params: { name: this.name }
            });
            this.avatarUrls[this.name] = `http://116.198.207.202:40061${response.data.file_path}` || '/assets/default-avatar.png';
          } catch (error) {
            console.error('获取头像失败:', error);
            this.avatarUrls[this.name] = '/assets/default-avatar.png';
          }
          resolve();
        }, 300);
      });
    },
    getCharacterImage() {
      if (!this.avatarUrls[this.name]) {
        this.loadAvatar();
        return '';
      }
      return this.avatarUrls[this.name];
    }
  }
}
</script>

<style scoped>
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
</style>
