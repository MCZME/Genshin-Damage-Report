<template>
  <div class="meme-wall">
    <div 
      v-for="meme in memes" 
      :key="meme.id"
      class="meme-item"
      :style="{
        left: meme?.position?.x ?? '50%',
        top: meme?.position?.y ?? '50%',
        transform: `rotate(${meme?.rotation ?? 0}deg) scale(${meme?.scale ?? 1})`,
        backgroundImage: meme?.image ? `url(${meme.image})` : 'none'
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
import config from '../config.js'

const memes = ref([])

const fetchStickers = async () => {
  try {
    const response = await fetch(`${config.api.baseUrl}${config.api.endpoints.stickers}/random?count=15`)
    const data = await response.json()
    return data.data.stickers
  } catch (error) {
    console.error('获取表情包失败:', error)
    return []
  }
}

const checkPositionOverlap = (position, memes, minDistance = 20) => {
  for (const meme of memes) {
    const dx = Math.abs(parseFloat(position.x) - parseFloat(meme.position.x))
    const dy = Math.abs(parseFloat(position.y) - parseFloat(meme.position.y))
    if (dx < minDistance && dy < minDistance) {
      return true
    }
  }
  return false
}

const generateMemes = async () => {
  try {
    const count = Math.floor(Math.random() * 6 + 10) // 10-15个
    const stickers = await fetchStickers()
    const newMemes = []
    let stickerCount = 0
    
    for (let i = 0; i < count; i++) {
      const sticker = stickers[stickerCount] || {}
      let position, attempts = 0
      stickerCount ++
      do {
        position = {
          x: 5 + Math.random() * 80 + '%',
          y: 10 + Math.random() * 70 + '%'
        }
        attempts++
      } while (attempts < 10 && checkPositionOverlap(position, newMemes))
      
      newMemes.push({
        id: Date.now() + Math.random(),
        position,
        rotation: Math.random() * 30 - 15,
        scale: 0.8 + Math.random() * 0.4,
        image: sticker.file_name ? `http://116.198.207.202:40061${sticker.file_name}` : null
      })
    }
    
    memes.value = newMemes
  } catch (error) {
    console.error('生成表情包失败:', error)
    // 返回默认meme数据
    const count = Math.floor(Math.random() * 6 + 10)
    memes.value = Array.from({ length: count }, () => ({
      id: Date.now() + Math.random(),
      position: {
        x: Math.random() * 90 + '%',
        y: Math.random() * 90 + '%'
      },
      rotation: Math.random() * 30 - 15,
      scale: 0.8 + Math.random() * 0.4,
      image: null
    }))
  }
}

const refreshWall = async () => {
  memes.value = []
  await nextTick()
  await generateMemes()
}

onMounted(async () => {
  await generateMemes()
})
</script>

<style scoped>
.meme-wall {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: url('http://116.198.207.202:40061/i/2025/04/28/txohxa.png') 0 0/100% 100% no-repeat;
}

.meme-item {
  position: absolute;
  width: 120px;
  height: 120px;
  border-radius: 20px;
  transition: all 1.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
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
