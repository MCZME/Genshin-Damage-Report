<template>
  <nav class="genshin-nav">
    <div class="logo">
      <img src="@/assets/vue.svg" alt="Logo">
      <span>原神伤害分析</span>
    </div>
    
    <div class="nav-links">
      <router-link 
        v-for="link in links" 
        :key="link.path"
        :to="link.path"
        class="nav-item"
        :class="`element-${link.element}`"
      >
        {{ link.name }}
      </router-link>
    </div>

    <!-- 移动端汉堡菜单 -->
    <button class="mobile-menu-btn" @click="toggleMenu">
      <div class="bar"></div>
      <div class="bar"></div>
      <div class="bar"></div>
    </button>
  </nav>
</template>

<script setup>
import { ref } from 'vue';

const links = ref([
  { name: '队伍配置', path: '/team', element: 'anemo' },
  { name: '伤害分析', path: '/damage', element: 'pyro' },
  { name: '角色库', path: '/characters', element: 'hydro' }
]);

const isMenuOpen = ref(false);

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};
</script>

<style scoped>
.genshin-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: rgba(26, 35, 126, 0.8);
  backdrop-filter: blur(5px);
  position: relative;
  z-index: 100;
}

.logo {
  display: flex;
  align-items: center;
  gap: 1rem;
  color: white;
  font-family: 'HYWenHei', sans-serif;
  font-size: 1.5rem;
}

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-item {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: all 0.3s ease;
  position: relative;
  font-family: 'HYWenHei', sans-serif;
}

.nav-item:hover {
  transform: translateY(-3px);
}

.element-anemo {
  background-color: rgba(116, 199, 184, 0.3);
}
.element-pyro {
  background-color: rgba(230, 57, 70, 0.3);
}
.element-hydro {
  background-color: rgba(66, 165, 245, 0.3);
}

.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
}

.bar {
  width: 25px;
  height: 3px;
  background-color: white;
  margin: 5px 0;
  transition: all 0.3s ease;
}

@media (max-width: 768px) {
  .nav-links {
    display: none;
  }
  
  .mobile-menu-btn {
    display: block;
  }
}
</style>
