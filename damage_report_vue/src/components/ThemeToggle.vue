<template>
  <div class="theme-switcher">
      <v-btn
        icon
        @click="menuVisible = !menuVisible"
        :title="'当前主题：' + currentTheme"
        rounded="sm"
      >
        <img 
          :src="themeIcons[currentTheme]" 
          class="active-icon"
          alt="current theme icon"
        />
      </v-btn>

    <transition name="slide-fade">
      <div v-if="menuVisible" class="theme-menu">
        <v-btn
          v-for="themeName in themes"
          :key="themeName"
          icon
          @click="setTheme(themeName)"
          class="theme-item"
          rounded="sm"
        >
          <img 
            :src="themeIcons[themeName]" 
            :class="[themeName === currentTheme ? 'active-icon' : 'theme-icon']"
            alt="theme icon"
          />
        </v-btn>
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

const setTheme = (themeName) => {
  currentTheme.value = themeName
  theme.global.name.value = themeName
  menuVisible.value = false
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

.theme-menu .v-btn {
  border: none !important;
  box-shadow: none !important;
  background: rgba(var(--v-theme-primary), 0.1) !important;
  min-width: 0 !important;
  padding: 0 !important;
  margin: 0 1px !important;
}

.theme-menu .v-btn:hover {
  background: rgba(var(--v-theme-primary), 0.2) !important;
}

.theme-menu .active-icon {
  filter: drop-shadow(0 0 2px rgba(0, 0, 0, 0.3));
}

.theme-item {
  transition: all 0.2s;
}

.theme-icon {
  width: 24px;
  height: 24px;
  opacity: 0.7;
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
</style>
