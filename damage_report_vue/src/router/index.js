import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../pages/HomePage.vue'
import InfoPage from '../pages/InfoPage.vue'
import TeamDashboardPage from '../pages/TeamDashboardPage.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/info',
    name: 'Info',
    component: InfoPage
  },
  {
    path: '/dashboard/:uuid',
    name: 'Dashboard',
    component: TeamDashboardPage,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
