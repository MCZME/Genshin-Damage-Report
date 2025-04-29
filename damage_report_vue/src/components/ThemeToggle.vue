<template>
  <v-btn
    icon
    @click="toggleTheme"
    :title="theme.global.current.value.dark ? '切换到亮色主题' : '切换到暗色主题'"
  >
    <v-icon>
      {{ theme.global.current.value.dark ? 'mdi-weather-sunny' : 'mdi-weather-night' }}
    </v-icon>
  </v-btn>
</template>

<script setup>
import { useTheme } from 'vuetify'

const theme = useTheme()

const toggleTheme = () => {
  theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark'
}
</script>
