<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <ThemeToggle class="theme-toggle" />
    </div>
    <div class="sidebar-content">
      <slot></slot>
    </div>
    <v-btn 
      class="home-button"
      color="primary"
      variant="flat"
      @click="goToInfo"
      icon
    >
      <v-icon>mdi-home</v-icon>
    </v-btn>
  </aside>
</template>

<script>
import ThemeToggle from './ThemeToggle.vue'
import { useRouter } from 'vue-router'

export default {
  name: 'SideBar',
  components: { ThemeToggle },
  setup() {
    const router = useRouter()
    
    const goToInfo = () => {
      router.push('/info')
    }

    return {
      goToInfo
    }
  }
}
</script>

<style scoped>
.sidebar {
  width: 160px;
  height: 100vh;
  background: rgba(var(--v-theme-secondary), 1);
  padding: 20px;
  box-sizing: border-box;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 100;
  overflow-y: auto;
  display: flex;
  justify-content: center;
}

.sidebar-header {
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(var(--v-theme-on-primary), 0.2);
}

.theme-toggle {
  margin-bottom: 15px;
  width: 80px;
  height: 80px;
}

.sidebar-header h3 {
  margin: 0;
  color: rgba(var(--v-theme-on-primary), 1);
  font-size: 1.2rem;
}

.sidebar-content {
  color: rgba(var(--v-theme-on-primary), 0.9);
}

.sidebar-content h4 {
  color: rgba(var(--v-theme-on-primary), 1);
  margin-top: 20px;
  margin-bottom: 10px;
}

.home-button {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 60px;
  border-radius: 4px;
}
</style>
