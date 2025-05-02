<template>
  <div class="theme-switcher">
      <v-btn
        icon
        @click="menuVisible = !menuVisible"
        :title="'当前主题：' + currentTheme"
        rounded="lg"
        class="theme-toggle-btn"
      >
        <img 
          :src="themeIcons[currentTheme]" 
          class="active-icon"
          alt="current theme icon"
        />
      </v-btn>

    <transition name="slide-fade">
      <div v-if="menuVisible" class="theme-menu">
        <button
          v-for="themeName in themes"
          :key="themeName"
          @click="setTheme(themeName)"
          class="theme-item"
          :data-theme="themeName"
        >
          <img 
            :src="themeIcons[themeName]" 
            :class="[themeName === currentTheme ? 'active-icon' : 'theme-icon']"
            alt="theme icon"
          />
        </button>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { useTheme } from 'vuetify'
import { ref } from 'vue'

const theme = useTheme()
const themes = ['pyro', 'hydro', 'electro', 'cryo', 'anemo', 'geo', 'dendro']
const currentTheme = ref(theme.global.name.value)
const menuVisible = ref(false)

const themeIcons = {
  pyro: 'http://116.198.207.202:40061/i/2025/05/01/2m8zpq.png',
  hydro: 'http://116.198.207.202:40061/i/2025/05/01/2m8zm2.png',
  electro: 'http://116.198.207.202:40061/i/2025/05/01/2m91og.png',
  cryo: 'http://116.198.207.202:40061/i/2025/05/01/2m8yg4.png',
  anemo: 'http://116.198.207.202:40061/i/2025/05/01/2m9093.png',
  geo: 'http://116.198.207.202:40061/i/2025/05/01/2m926v.png',
  dendro: 'http://116.198.207.202:40061/i/2025/05/01/2m90rg.png'
}

const setTheme = (/** @type {string} */ themeName) => {
  const clickedBtn = document.querySelector(`.theme-item[data-theme="${themeName}"]`)
  if (clickedBtn) {
    clickedBtn.classList.add('animate-selection')
    setTimeout(() => {
      clickedBtn.classList.remove('animate-selection')
    }, 1000)
  }
  // 延迟1秒再关闭菜单，确保动画完成
  setTimeout(() => {
    menuVisible.value = false
    currentTheme.value = themeName
    theme.global.name.value = themeName
  }, 800)
}
</script>

<style scoped>
.theme-switcher {
  position: relative;
  display: inline-block;
}

.theme-menu {
  position: absolute;
  left: -8px;
  top: 50%;
  transform: translateY(-50%) translateX(-100%);
  display: flex;
  background: rgba(var(--v-theme-background), 0.9);
  border-radius: 4px;
  padding: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.theme-toggle-btn {
  background: rgba(var(--v-theme-background), 1);
  padding: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.theme-menu .v-btn {
  border: none;
  box-shadow: none;
  min-width: 0;
  padding: 0;
  margin: 0 1px;
}

.active-icon {
  scale: 1.1;
}

.theme-item {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 40px;
  height: 40px;
  transition: all 0.2s;
}

.theme-icon {
  width: 24px;
  height: 24px;
  transition: all 0.2s;
}

.active-icon {
  width: 28px;
  height: 28px;
  opacity: 1;
}

.theme-item:hover .theme-icon {
  transform: scale(1.1);
  opacity: 1;
}

.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.2s ease-in;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-50%) translateX(-80px);
}

.animate-selection {
  animation: floatUp 1s ease-out forwards;
  z-index: 10;
}

.animate-selection img {
  animation: scaleUp 1s ease-out forwards;
}

@keyframes floatUp {
  0% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
  100% {
    transform: translateY(-40px);
    opacity: 0;
  }
}

@keyframes scaleUp {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.5);
  }
  100% {
    transform: scale(1.8);
  }
}
</style>
