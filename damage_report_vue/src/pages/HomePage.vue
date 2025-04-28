<template>
  <svg width="0" height="0" style="position:absolute">
    <filter id="meme-outline">
      <feMorphology operator="dilate" radius="4" in="SourceAlpha" result="thicken" />
      <feFlood flood-color="#F5F5DC" result="color" />
      <feComposite in="color" in2="thicken" operator="in" />
      <feComposite in="SourceGraphic" operator="over" />
    </filter>
  </svg>
  <div class="meme-wall">
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner"></div>
    </div>
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

const loading = ref(false)
const generatePoints = (numPoints) => {
  // 页面尺寸 (100vw x 100vh)
  const pageWidth = 90
  const pageHeight = 90
  
  // 按钮区域 
  const buttonTop = 60
  const buttonHeight = 10
  const buttonWidth = 20
  const buttonLeft = (pageWidth - buttonWidth) / 2
  
  // 可用区域为顶部70% + 按钮下方20%
  const availableHeight = buttonTop + (100 - buttonTop - buttonHeight)
  
  // 计算可用区域的行列数
  const cols = Math.ceil(Math.sqrt(numPoints * (pageWidth / availableHeight)))
  const rows = Math.ceil(numPoints / cols)
  
  // 计算每个网格单元尺寸
  const cellWidth = pageWidth / cols
  const cellHeight = availableHeight / rows
  
  const points = []
  
  for (let i = 0; i < numPoints; i++) {
    const col = i % cols
    const row = Math.floor(i / cols)
    
    // 计算网格中心点
    let x = col * cellWidth + cellWidth / 2
    let y = row * cellHeight + cellHeight / 2 + 5
    
    // 添加安全随机偏移
    const safeOffsetX = Math.min(cellWidth * 0.3, x, pageWidth - x)
    // 计算y坐标安全偏移
    let maxY
    if (y < buttonTop) {
      maxY = buttonTop - y
    } else {
      maxY = pageHeight - buttonHeight - y
    }
    const safeOffsetY = Math.min(cellHeight * 0.3, y, maxY)
    x += (Math.random() - 0.5) * safeOffsetX * 2
    y += (Math.random() - 0.5) * safeOffsetY * 2
    
    // 确保坐标在有效范围内
    x = Math.max(0, Math.min(pageWidth, x))
    y = Math.max(0, Math.min(pageHeight-5, y-5))
    // 确保不覆盖按钮区域
    if (y > buttonTop && y < buttonTop + buttonHeight && 
        x > buttonLeft && x < buttonLeft + buttonWidth) {
      y = Math.random() * (pageHeight - buttonHeight) + buttonHeight / 2
      x = Math.random() * (pageWidth - buttonWidth) + buttonWidth / 2
    }
    
    points.push({
      x: x + '%',
      y: y + '%'
    })
  }
  
  return points
}
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

const generateMemes = async () => {
  loading.value = true
  memes.value = []
  try {
    const count = Math.floor(Math.random() * 6 + 10) // 10-15个
    const stickers = await fetchStickers()
    let stickerCount = 0
    
    memes.value = []
    for (let i = 0; i < count; i++) {
      if (i === 0) loading.value = false
      await new Promise(resolve => setTimeout(resolve, 300))
      const sticker = stickers[stickerCount] || {}
      let position
      stickerCount++
      const points = generatePoints(count)
      position = points[i]
      
      memes.value = [...memes.value, {
        id: Date.now() + Math.random(),
        position,
        rotation: Math.random() * 30 - 15,
        scale: 0.8 + Math.random() * 0.4,
        image: sticker.file_name ? `http://116.198.207.202:40061${sticker.file_name}` : null
      }]
    }
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
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 5px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #FF3366;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.meme-wall {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  scrollbar-width: none;
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
  filter: url(#meme-outline);
}

.refresh-button {
  position: fixed;
  bottom: 30%;
  left: 50%;
  transform: translateX(-50%);
  padding: 12px 24px;
  background: rgba(255, 51, 102, 0.9);
  border: 2px solid #FFD700;
  border-radius: 30px;
  color: white;
  font-family: 'HYWenHei';
  cursor: pointer;
  z-index: 1000;
  transition: all 0.3s ease;
}

.refresh-button:hover {
  transform: translateX(-50%) scale(1.05);
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
