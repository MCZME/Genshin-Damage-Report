import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import config from './config'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import router from './router'
import App from './App.vue'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    themes: {
      light: {
        colors: {
          primary: '#1a237e',
          secondary: '#0d47a1',
          accent: '#e63946',
          background: '#ffffff'
        }
      },
      dark: {
        colors: {
          primary: '#90caf9',
          secondary: '#64b5f6',
          accent: '#ff8a80',
          background: '#121212'
        }
      }
    }
  }
})

const app = createApp(App)
app.use(vuetify)
app.use(router)
app.config.globalProperties.$config = config
app.mount('#app')
