<template>
<div v-show="show" :class="['loading-overlay', { 'exiting': isExiting }]">
    <div class="left-panel">
      <div class="left-images">
        <img 
          v-for="(img, index) in images.slice(0, 4)"
          :key="index"
          :src="`/src/assets/img/${img}`"
          :style="{ animationDelay: `${index * 0.2}s` }"
          class="character-img"
        />
      </div>
    </div>
    <div class="right-panel">
      <div class="right-images">
        <img 
          v-for="(img, index) in images.slice(4)"
          :key="index + 4"
          :src="`/src/assets/img/${img}`"
          :style="{ animationDelay: `${(index + 4) * 0.2}s` }"
          class="character-img"
        />
      </div>
    </div>
</div>
</template>

<script setup>
import { defineProps, ref, watch, computed } from 'vue'

const props = defineProps({
  isLoading: Boolean,
})

const show = computed(() => props.isLoading || isExiting.value)

const isExiting = ref(false)
const images = [
  'y2agk-1.png',
  'y2au5-1.png',
  'y2dn5-1.png',
  'y2f6x-1.png',
  'y2gsc-1.png',
  'y2hhj-1.png',
  'y28ht-1.png',
  'y28u5-1.png'
]

watch(() => props.isLoading, (newVal) => {
  if (!newVal) {
    isExiting.value = true
    setTimeout(() => {
      isExiting.value = false
    }, 800)
  }
})
</script>

<style scoped>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: transparent;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  overflow: hidden;
}

.left-panel,
.right-panel {
  position: absolute;
  top: 0;
  transform: translateY(-50%);
  width: 50%;
  height: 100%;
  background: rgb(var(--v-theme-background));
  transition: transform 0.8s ease-out;
  overflow: hidden;
}

.left-panel {
  left: 0;
  transform: translateX(0);
}

.right-panel {
  right: 0;
  transform: translateX(0);
}

.loading-overlay.exiting .left-panel {
  transform: translateX(-100%);
}

.loading-overlay.exiting .right-panel {
  transform: translateX(100%);
}

.left-images,
.right-images {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  align-items: center;
  width: 100%;
  height: 100%;
  padding: 20px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.left-images {
  justify-content: flex-end;
}

.right-images {
  justify-content: flex-start;
}

.character-img {
  width: 80px;
  height: 80px;
  opacity: 0;
  animation: fadeInOut 1.6s infinite;
}

@keyframes fadeInOut {
  0%, 100% {
    opacity: 0;
    transform: scale(0.8);
  }
  50% {
    opacity: 1;
    transform: scale(1.1);
  }
}
</style>
