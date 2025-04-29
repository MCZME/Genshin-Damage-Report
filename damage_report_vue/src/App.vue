<script setup>
import ThemeToggle from './components/ThemeToggle.vue'
</script>

<template>
  <v-app>
    <v-app-bar>
      <v-spacer></v-spacer>
      <ThemeToggle />
    </v-app-bar>
    <v-main>
      <RouterView />
    </v-main>
  </v-app>
</template>
