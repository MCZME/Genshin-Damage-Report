<template>
  <svg width="0" height="0" style="position:absolute">
    <filter id="meme-outline">
      <feMorphology operator="dilate" radius="3" in="SourceAlpha" result="thicken" />
      <feFlood flood-color="#F5F5DC" result="color" />
      <feComposite in="color" in2="thicken" operator="in" />
      <feComposite in="SourceGraphic" operator="over" />
    </filter>
  </svg>
  <div class="meme-wall">
    <Loading v-if="loadingE" :isLoading="loadingStatus" />
      <div 
      v-for="meme in memes" 
      :key="meme.id"
      class="meme-item"
      :data-id="meme.id"
      :style="{
        left: meme?.position?.x ?? '50%',
        top: meme?.position?.y ?? '50%',
        transform: `rotate(${meme?.rotation ?? 0}deg) scale(${meme?.scale ?? 1})`,
        backgroundImage: meme?.image ? `url(${meme.image})` : 'none'
      }"
      @click="removeMeme(meme.id)"
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
import Loading from '../components/Loading.vue'
import { useRouter } from 'vue-router'

const loadingStatus = ref(false)
const loadingE = ref(false)
const generatePoints = (numPoints) => {
  const pageWidth = 90
  const pageHeight = 90
  
  const availableHeight = pageHeight
  
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
    const safeOffsetY = Math.min(cellHeight * 0.3, y)
    x += (Math.random() - 0.5) * safeOffsetX * 2
    y += (Math.random() - 0.5) * safeOffsetY * 2
    
    // 确保坐标在有效范围内
    x = Math.max(3, Math.min(pageWidth, x-3))
    y = Math.max(8, Math.min(pageHeight, y-5))
    
    points.push({
      x: x + '%',
      y: y + '%'
    })
  }
  
  return points
}
import config from '../config.js'

const memes = ref([])
const Stickers = ref([])

const fetchStickers = async () => {
  try {
    const response = await fetch(`${config.api.baseUrl}${config.api.endpoints.stickers}/random?count=25`)
    const data = await response.json()
    return data.data.stickers
  } catch (error) {
    console.error('获取表情包失败:', error)
    return []
  }
}

const generateMemes = async () => {
  loadingStatus.value = true
  loadingE.value = true
  memes.value = []
  try {
    const count = Math.floor(Math.random() * 6 + 10)
    let stickerCount = 0
    const stickers = await fetchStickers()
    Stickers.value = stickers
    memes.value = []    
    for (let i = 0; i < count; i++) {
      if (i === 0) setTimeout(() => {
        loadingStatus.value = false 
        setTimeout(() => {
          loadingE.value = false
        }, 10000);
      }, 1000)
      await new Promise(resolve => setTimeout(resolve, 300))
      const sticker = stickers[stickerCount] || {}
      let position
      stickerCount++
      const points = generatePoints(count)
      position = points[i]
      
      memes.value = [...memes.value, {
        id: Date.now() + Math.random(),
        position,
        rotation: Math.random() * 60 - 15,
        scale: 0.8 + Math.random() * 0.4,
        image: sticker.file_name ? `http://116.198.207.202:40061${sticker.file_name}` : null
      }]
    }
  } catch (error) {
    console.error('生成表情包失败:', error)
    // 返回默认meme数据
    const count = Math.floor(Math.random() * 6 + 15)
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

const router = useRouter()

const refreshWall = async () => {
  loadingStatus.value = true
  loadingE.value = true
  await nextTick()
  
  // 显示Loading动画1秒
  await new Promise(resolve => setTimeout(resolve, 1000))
  
  // 跳转到信息页
  router.push('/info')
  loadingStatus.value = false
  loadingE.value = false
}

const removeMeme = (id) => {
  const meme = memes.value.find(m => m.id === id)
  if (meme) {
    const memeElement = document.querySelector(`.meme-item[data-id="${id}"]`)
    if (memeElement) {
      // 添加tearing类触发完整动画
      memeElement.classList.add('tearing')
      // 动画结束后移除元素和类
      setTimeout(() => {
        memes.value = memes.value.filter(m => m.id !== id)
        memeElement.classList.remove('tearing')
      }, 2000)
    } else {
      memes.value = memes.value.filter(m => m.id !== id)
    }
  }
}

const handleWallClick = (e) => {
  if (e.target.classList.contains('meme-wall')) {
    const randomSticker = Stickers.value[Math.floor(Math.random() * Stickers.value.length)]
    const newMeme = {
      id: Date.now() + Math.random(),
      position: {
        x: ((Math.max(160, Math.min(e.clientX, window.innerWidth - 80)) - 80) / window.innerWidth * 100) + '%',
        y: ((Math.max(160, Math.min(e.clientY, window.innerHeight - 80)) - 80) / window.innerHeight * 100) + '%'
      },
      rotation: Math.random() * 30 - 15,
      scale: 0.8 + Math.random() * 0.4,
      image: `http://116.198.207.202:40061${randomSticker.file_name}`
    }
    memes.value = [...memes.value, newMeme]
  }
}

onMounted(async () => {
  if (!localStorage.getItem('hasVisited')) {
    loadingStatus.value = true
    localStorage.setItem('hasVisited', 'true')
    setTimeout(async () => {
      await generateMemes()
      loadingStatus.value = false
    }, 3000)
  } else {
    await generateMemes()
  }
  document.querySelector('.meme-wall').addEventListener('click', handleWallClick)
})
</script>

<style scoped>
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
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  filter: url(#meme-outline);
  transition: transform 0.2s ease;
  cursor: pointer;
  animation: popIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
}

.meme-item:hover {
  animation: shake 0.5s ease;
}

@keyframes popIn {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  80% {
    transform: scale(1.2);
    opacity: 1;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes shake {
  0%, 100% {
    transform: translateX(0) rotate(0deg);
  }
  20% {
    transform: translateX(-2px) rotate(-2deg);
  }
  40% {
    transform: translateX(2px) rotate(2deg);
  }
  60% {
    transform: translateX(-2px) rotate(-1deg);
  }
  80% {
    transform: translateX(2px) rotate(1deg);
  }
}

@keyframes tearOff {
  0% {
      transform: 
        translate3d(0, 0, 500px)
        scale(1.05)
        rotate3d(0,0,1,-3deg);
    }
    3% {
      transform: 
        translate3d(0, 0, 500px)
        scale(1.05)
        rotate3d(0,0,1,3deg);
    }
    5% {
      transform: 
        translate3d(0, 0, 500px)
        scale(1.1)
        rotate3d(0.5,0.2,0.1,15deg);
    }
    7% {
      transform: 
        translate3d(5vw, 2vh, 500px)
        scale(1.1)
        rotate3d(0.6,0.3,0.2,20deg);
    }
    10% {
      transform: 
        translate3d(10vw, 5vh, 500px)
        scale(1.1)
        rotate3d(0.8,0.3,0.2,30deg);
    }
    20% {
      transform: 
        translate3d(20vw, 15vh, 500px)
        scale(1.05)
        rotate3d(0.7,0.4,0.3,45deg);
    }
    35% {
      transform: 
        translate3d(35vw, 30vh, 500px)
        scale(1)
        rotate3d(0.6,0.5,0.4,60deg)
        skew(3deg, 2deg);
    }
    50% {
      transform: 
        translate3d(50vw, 45vh, 500px)
        scale(0.95)
        rotate3d(0.5,0.4,0.3,75deg)
        skew(5deg, 3deg);
    }
    65% {
      transform: 
        translate3d(65vw, 60vh, 500px)
        scale(0.9)
        rotate3d(0.4,0.3,0.2,85deg)
        skew(7deg, 5deg);
    }
    80% {
      transform: 
        translate3d(80vw, 75vh, 500px)
        scale(0.85)
        rotate3d(0.3,0.2,0.1,90deg)
        skew(9deg, 6deg);
        opacity: 1;
    }
    95% {
      transform: 
        translate3d(95vw, 90vh, 500px)
        scale(0.8)
        rotate3d(0.2,0.1,0.05,95deg)
        skew(11deg, 7deg);
        opacity: 0.5;
    }
    100% {
      transform:
        translate3d(110vw, 105vh, 500px)
        rotate3d(0.1,0.05,0,100deg)
        scale(0.75)
        skew(12deg, 8deg);
        opacity: 0.2;
    }
}

.meme-item.tearing {
  animation: tearOff 2s linear forwards;
  transform-style: preserve-3d;
  will-change: transform, opacity;
  backface-visibility: hidden;
  perspective: 500px;
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
