<template>
  <nav class="navbar">
    <div class="nav-links">
      <router-link to="/">首页</router-link>
      <router-link to="/info">信息页</router-link>
    </div>
    <ThemeToggle />
  </nav>
</template>

<script>
import ThemeToggle from './ThemeToggle.vue'

export default {
  name: 'NavBar',
  components: {
    ThemeToggle
  }
}
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: rgb(var(--v-theme-surface));
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.v-theme--light .navbar {
  background: rgb(var(--v-theme-surface-lighten-1));
  border-bottom: 1px solid rgb(var(--v-theme-border));
}

.nav-links {
  display: flex;
  gap: 1rem;
}

.navbar a {
  text-decoration: none;
  color: rgb(var(--v-theme-on-surface));
}

.navbar a.router-link-active {
  font-weight: bold;
  color: rgb(var(--v-theme-primary));
}
</style>
