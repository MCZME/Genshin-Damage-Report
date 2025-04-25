import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Pages from 'vite-plugin-pages'
import Layouts from 'vite-plugin-vue-layouts'
import vuetify from 'vite-plugin-vuetify'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    Layouts(),
    Pages({
      dirs: 'src/pages',
      exclude: ['**/components/*.vue']
    }),
    vuetify({
      autoImport: true,
      styles: { configFile: 'src/style.css' }
    })
  ],
  resolve: {
    alias: {
      '@': '/src'
    }
  },
  server: {
    fs: {
      allow: [
        'E:/project/Genshin Damage Report/damage_report_vue',
        'E:/project/Genshin Damage Report/node_modules'
      ]
    }
  }
})
