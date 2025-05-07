<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <ThemeToggle class="theme-toggle" />
    </div>
    <div class="sidebar-content">
      <div v-if="characters" class="character-avatars">
        <CharacterAvatar
          v-for="(value, name) in characters"
          :key="name"
          :name="name"
          :element="value.element"
          :data="value.data"
          class="character-avatar"
        />
      </div>
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
import CharacterAvatar from './CharacterAvatar.vue'
import { useRouter } from 'vue-router'

export default {
  name: 'SideBar',
  components: { ThemeToggle, CharacterAvatar },
  props: {
    characters: {
      type: Object,
      default: null
    }
  },
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
  padding: 10px;
  box-sizing: border-box;
  position: fixed;
  left: 0;
  top: 0;
  display: flex;
  justify-content: space-around;
  flex-direction: column;
}

.sidebar-header {
  padding-bottom: 10px;
  border-bottom: 2px solid rgba(var(--v-theme-accent), 0.8);
  display: flex;
  justify-content: center;
}

.theme-toggle {
  margin-bottom: 15px;
  width: 80px;
  height: 80px;
}

.sidebar-content {
  color: rgba(var(--v-theme-on-primary), 0.9);
  display: flex;
  flex-direction: column;
}

.character-avatars {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  margin: 40px 0;
}

.character-avatar {
  width: 80px;
  height: 80px;
  border: 3px solid rgba(var(--v-theme-primary), 0.8);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  position: relative;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.character-avatar:hover .avatar-img {
  transform: scale(1.05);
}

.home-button {
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 60px;
  border-radius: 4px;
}
</style>
