<template>
  <nav class="navbar">
    <div class="nav-links">
      <router-link to="/">首页</router-link>
      <div class="center-links">
        <router-link to="/info">首页</router-link>
        <div class="dropdown">
          <button class="dropbtn">排列</button>
          <div class="dropdown-content">
            <router-link to="/arrange/character">角色</router-link>
            <router-link to="/arrange/team">队伍</router-link>
          </div>
        </div>
        <div class="dropdown">
          <button class="dropbtn">分析</button>
          <div class="dropdown-content">
            <router-link to="/analyze/query">查询</router-link>
            <router-link to="/analyze/compare">对比</router-link>
          </div>
        </div>
        <div class="dropdown">
          <button class="dropbtn">关于</button>
          <div class="dropdown-content">
            <router-link to="/about/faq">常见问题</router-link>
            <router-link to="/about/updates">更新</router-link>
          </div>
        </div>
      </div>
    </div>
    <ThemeToggle class="theme-size" />
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
  width: 100%;
  height: 3rem;
  padding: 0 1rem;
  background: rgb(var(--v-theme-secondary));
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-links {
  display: flex;
  justify-content: space-between;
  width: 100%;
  height: 100%;
  gap: 1rem;
}

.center-links {
  display: flex;
  gap: 1.5rem;
  flex-grow: 1;
  justify-content: flex-end;
  padding-right: 1rem;
}

.navbar a {
  display: inline-flex;
  align-items: center;
  text-decoration: none;
  color: rgb(var(--v-theme-on-surface));
}

.navbar a.router-link-active {
  font-weight: bold;
}

.dropdown {
  position: relative;
  display: inline-block;
  display: inline-flex;
  align-items: center;
}

.dropbtn {
  background: none;
  border: none;
  color: rgb(var(--v-theme-on-surface));
  font-size: inherit;
  cursor: pointer;
  padding: 0;
  margin: 0;
  position: relative;
  padding-right: 15px;
}

.dropbtn::after {
  content: "▼";
  font-size: 0.6em;
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%) rotate(0deg);
  transition: transform 0.3s ease;
}

.dropdown:hover .dropbtn::after {
  transform: translateY(-50%) rotate(90deg);
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: rgb(var(--v-theme-surface));
  opacity: 1;
  min-width: 120px;
  box-shadow: 0px 4px 8px 0px rgba(0,0,0,0.2);
  z-index: 1;
  top: 100%;
  right: 0%;
  border-radius: 0 0 10% 10%;
}

.dropdown-content a {
  color: rgb(var(--v-theme-on-surface));
  padding: 8px 12px;
  text-decoration: none;
  display: block;
  text-align: left;
  font-size: 0.875rem;
}

.dropdown-content a:hover {
  color: rgb(var(--v-theme-secondary));
}

.dropdown:hover .dropdown-content {
  display: block;
}

.theme-size {
  position: relative;
  margin-left: 1rem;
}

.theme-size::before {
  content: "";
  position: absolute;
  left: -0.75rem;
  top: 50%;
  transform: translateY(-50%);
  height: 1.5rem;
  width: 1px;
  background-color: rgb(var(--v-theme-on-surface));
  opacity: 0.5;
}

.theme-size {
  width: 34px;
  height: 34px;
}
</style>
