<script setup>
import GenshinNavBar from './components/GenshinNavBar.vue'
</script>

<template>
  <div class="app-container">
    <GenshinNavBar />
    <router-view class="main-content" />
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap');

:root {
  --element-anemo: #74c7b8;
  --element-pyro: #e63946;
  --element-hydro: #42a5f5;
}

body {
  margin: 0;
  background: url('/game_assets/bg/liyue.jpg') no-repeat center center fixed;
  background-size: cover;
  font-family: 'Noto Sans SC', sans-serif;
  min-height: 100vh;
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  padding: 2rem;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);
}
</style>
