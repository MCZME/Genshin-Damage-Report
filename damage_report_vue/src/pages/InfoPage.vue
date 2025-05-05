<template>
  <div class="info-page">
    <NavBar />
    <div class="content">
      <div class="layout-container">
        <div class="left-panel">
          <div class="static-info">
            <h2>队伍信息</h2>
            <p>这里可以显示一些静态信息或统计数据</p>
          </div>
        </div>
        <div class="right-panel">
          <div class="card-header">
            <div class="header-content">
              <h3 class="header-title">队伍列表</h3>
              <div class="header-actions">
                <button class="header-btn" @click="fetchRandomUids">
                  <v-icon icon="mdi-refresh"></v-icon>
                </button>
                <button class="header-btn">
                  <v-icon icon="mdi-filter"></v-icon>
                </button>
                <button class="header-btn">
                  <v-icon icon="mdi-sort"></v-icon>
                </button>
                
              </div>
            </div>
          </div>
            <div class="card-container">
              <v-row>
                <template v-if="loading">
                  <v-col 
                    v-for="n in 4"
                    :key="`skeleton-${n}`"
                    cols="12"
                    sm="6"
                    md="6">
                    <div class="skeleton-card">
                      <div class="skeleton-header">
                        <div class="skeleton-title"></div>
                        <div class="skeleton-chips">
                          <div class="skeleton-chip"></div>
                          <div class="skeleton-chip"></div>
                          <div class="skeleton-chip"></div>
                        </div>
                      </div>
                      <div class="skeleton-divider"></div>
                      <div class="skeleton-content">
                        <div class="skeleton-avatar" v-for="i in 4" :key="i"></div>
                      </div>
                    </div>
                  </v-col>
                </template>
              <template v-else>
                <v-col v-for="(uid, index) in uids"
                    :key="index"
                    cols="12"
                    sm="6"
                    md="6">
                  <TeamInfoCard :uid="uid" />
                </v-col>
              </template>
            </v-row>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import TeamInfoCard from '@/components/TeamInfoCard.vue'
import axios from 'axios'
import config from '@/config'

export default {
  name: 'InfoPage',
  components: {
    NavBar,
    TeamInfoCard
  },
  data() {
    return {
      uids: [],
      loading: false,
      error: null
    }
  },
  async created() {
    await this.fetchRandomUids();
  },
  methods: {
    async fetchRandomUids() {
      // 强制清空当前数据以显示加载状态
      this.uids = [];
      this.loading = true;
      this.error = null;
      
      try {
        // 添加时间戳参数避免缓存
        const timestamp = new Date().getTime();
        const response = await axios.get(`${config.api.baseUrl}${config.api.endpoints.card_uid}/random?t=${timestamp}`);
        this.uids = response.data.data.uids;
      } catch (err) {
        this.error = err.response?.data?.message || '获取UID列表失败';
        console.error('获取UID列表失败:', err);
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.info-page {
  min-height: 100vh;
  background: rgb(var(--v-theme-background));
}

.content {
  padding: 1rem;
  height: 90%;
}

.layout-container {
  display: flex;
  gap: 1rem;
  height: 100%;
}

.left-panel {
  width: 20%;
  background: rgba(var(--v-theme-background_light), 1);
  height: 100%;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.right-panel {
  width: 75%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: rgba(var(--v-theme-background_light), 1);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.card-header {
  border-bottom: 1px solid rgba(var(--v-border-color), 0.12);
  padding: 12px 16px;
  background: rgba(var(--v-theme-surface), 1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 500;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.header-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 8px;
  color: rgba(var(--v-theme-on-surface), 1);
  border-radius: 50%;
  transition: background-color 0.2s ease-in-out;
}

.header-btn:hover {
  background: rgba(var(--v-theme-on-surface), 0.08);
}

.header-btn:active {
  background: rgba(var(--v-theme-on-surface), 0.16);
}

.card-container {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  margin-top: 0;
}

.static-info {
  padding: 1rem;
  /* background: rgba(var(--v-theme-surface), 0.5); */
  border-radius: 8px;
  height: 100%;
}

.skeleton-card {
  background: rgba(var(--v-theme-surface), 1);
  border-radius: 12px;
  margin: 12px;
  box-shadow: 0 1px 2px 0 rgba(0,0,0,0.3), 
              0 1px 3px 1px rgba(0,0,0,0.15);
  overflow: hidden;
}

.skeleton-header {
  padding: 16px 16px 12px;
  display: flex;
  justify-content: space-between;
}

.skeleton-title {
  height: 28px;
  width: 120px;
  background: rgba(var(--v-theme-on-surface), 0.1);
  border-radius: 4px;
  animation: shimmer 1.5s infinite linear;
}

.skeleton-chips {
  display: flex;
  gap: 8px;
}

.skeleton-chip {
  height: 24px;
  width: 60px;
  background: rgba(var(--v-theme-on-surface), 0.1);
  border-radius: 12px;
  animation: shimmer 1.5s infinite linear;
}

.skeleton-divider {
  height: 1px;
  background-color: rgba(var(--v-theme-on-surface), 0.1);
  margin: 0 16px;
}

.skeleton-content {
  padding: 6px 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: center;
}

.skeleton-avatar {
  width: 100px;
  height: 100px;
  background: rgba(var(--v-theme-on-surface), 0.1);
  border-radius: 4px;
  animation: shimmer 1.5s infinite linear;
}

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.skeleton-avatar,
.skeleton-title,
.skeleton-chip,
.skeleton-talents,
.skeleton-weapon,
.skeleton-artifact {
  background: linear-gradient(
    90deg,
    rgba(var(--v-theme-on-surface), 0.1) 25%,
    rgba(var(--v-theme-on-surface), 0.15) 50%,
    rgba(var(--v-theme-on-surface), 0.1) 75%
  );
  background-size: 200% 100%;
}
</style>
