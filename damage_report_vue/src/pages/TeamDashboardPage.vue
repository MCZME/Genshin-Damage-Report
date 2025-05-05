<template>
  <div class="dashboard-container">
    <div class="dashboard">
      <h1>队伍伤害仪表盘</h1>
    </div>
    <SideBar></SideBar>
  </div>
</template>

<script>
import Loading from '../components/Loading.vue'
import SideBar from '../components/SideBar.vue'

export default {
  name: 'TeamDashboardPage',
  components: { SideBar },
  props: {
    uuid: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      loading: true,
      team: null
    }
  },
  async created() {
    try {
      const response = await fetch(`/api/card-data/${this.uuid}`)
      const data = await response.json()
      
      if (data.code === 200) {
        this.team = data.data
      } else {
        throw new Error(data.message)
      }
    } catch (error) {
      console.error('获取队伍数据失败:', error)
    } finally {
      this.loading = false
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  display: flex;
  min-height: 100vh;
}

.dashboard {
  padding: 20px;
  max-width: calc(100% - 280px);
  margin-left: 280px;
  flex-grow: 1;
  min-height: 100vh;
  background: var(--background);
}

.loading {
  display: flex;
  justify-content: center;
  margin-top: 50px;
}

.team-card {
  max-width: 600px;
  margin: 20px auto;
}

.team-card {
  background: var(--card-bg);
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.team-card:hover {
  transform: translateY(-5px);
}

.team-card h3 {
  margin-top: 0;
  color: var(--text-primary);
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 10px;
}

.team-card p {
  margin: 8px 0;
  color: var(--text-secondary);
}
</style>
