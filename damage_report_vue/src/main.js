import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import config from './config'
import Pyro_theme from '@/assets/theme/Pyro.js'
import Hydro_theme from '@/assets/theme/Hydro.js'
import Electro_theme from '@/assets/theme/Electro.js'
import Cryo_theme from '@/assets/theme/Cryo.js'
import Anemo_theme from '@/assets/theme/Anemo.js'
import Geo_theme from '@/assets/theme/Geo.js'
import Dendro_theme from '@/assets/theme/Dendro.js'
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
      pyro: Pyro_theme,
      hydro: Hydro_theme,
      electro: Electro_theme,
      cryo: Cryo_theme,
      anemo: Anemo_theme,
      geo: Geo_theme,
      dendro: Dendro_theme
    }
  }
})

const app = createApp(App)
app.use(vuetify)
app.use(router)
app.config.globalProperties.$config = config
app.mount('#app')
