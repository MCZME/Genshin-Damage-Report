<template>
  <div class="meme-wall">
    <div 
      v-for="meme in memes" 
      :key="meme.id"
      class="meme-item"
      :style="{
        left: meme.position.x,
        top: meme.position.y,
        transform: `rotate(${meme.rotation}deg) scale(${meme.scale})`,
        backgroundColor: meme.color
      }"
    ></div>

    <button 
      class="refresh-button"
      @click="refreshWall"
    >
      <div class="pyro-effect"></div>
      <span>全屏刷新</span>
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'

const ELEMENT_COLORS = [
  '#FF3366', // 火
  '#00B4D8', // 水
  '#70E000', // 草
  '#FFD700', // 岩
  '#9D4EDD', // 雷
  '#FF914D', // 冰
  '#6A4C93'  // 风
]

const memes = ref([])

const getRandomElementColor = () => {
  return ELEMENT_COLORS[Math.floor(Math.random() * ELEMENT_COLORS.length)]
}

const generateMeme = () => ({
  id: Date.now() + Math.random(),
  color: getRandomElementColor(),
  position: {
    x: Math.random() * 90 + '%',
    y: Math.random() * 90 + '%'
  },
  rotation: Math.random() * 30 - 15,
  scale: 0.8 + Math.random() * 0.4
})

const generateMemes = () => {
  const count = Math.floor(Math.random() * 6 + 10) // 10-15个
  memes.value = Array.from({ length: count }, generateMeme)
}

const refreshWall = () => {
  memes.value = []
  nextTick(() => generateMemes())
}

onMounted(() => {
  generateMemes()
})
</script>

<style scoped>
.meme-wall {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: url('http://116.198.207.202:40061/i/2025/04/28/pmkq4n.png') 0 0/100% 100% no-repeat;
}

.meme-item {
  position: absolute;
  width: 120px;
  height: 120px;
  border-radius: 20px;
  box-shadow: 0 8px 15px rgba(0,0,0,0.3);
  transition: all 1.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.refresh-button {
  position: fixed;
  bottom: 30px;
  right: 30px;
  padding: 12px 24px;
  background: rgba(255, 51, 102, 0.9);
  border: 2px solid #FFD700;
  border-radius: 30px;
  color: white;
  font-family: 'HYWenHei';
  cursor: pointer;
  z-index: 1000;
  transition: transform 0.3s ease;
}

.refresh-button:hover {
  transform: scale(1.05);
}

.pyro-effect {
  position: absolute;
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, 
    transparent 25%, 
    rgba(255, 215, 0, 0.4) 50%, 
    transparent 75%);
  animation: pyro-flow 1.5s infinite;
  border-radius: 30px;
}

@keyframes pyro-flow {
  from { transform: translateX(-100%); }
  to { transform: translateX(100%); }
}
</style>
