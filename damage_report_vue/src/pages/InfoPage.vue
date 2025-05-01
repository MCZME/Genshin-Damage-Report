<template>
  <div class="info-page">
    <NavBar />
    <div class="content">
      <v-container>
        <TeamInfoCard v-for="(team, index) in teams"
            :key="index"
            cols="12"
            sm="6"
            md="4"
            :team="team" />
      </v-container>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import TeamInfoCard from '@/components/TeamInfoCard.vue'

export default {
  name: 'InfoPage',
  components: {
    NavBar,
    TeamInfoCard
  },
  data() {
    return {
      teams: [
        {
          name: '雷神国家队',
          members: [
            {
              name: '雷电将军',
              avatar: 'https://example.com/raiden.png',
              level: 90,
              element: '雷',
              constellation: 2,
              talentLevels: [9, 9, 10],
              weapon: '薙草之稻光',
              artifacts: ['绝缘之旗印4件']
            },
            {
              name: '行秋',
              avatar: 'https://example.com/xingqiu.png',
              level: 80,
              element: '水',
              constellation: 6,
              talentLevels: [1, 9, 9],
              weapon: '祭礼剑',
              artifacts: ['沉沦之心2件', '宗室2件']
            },
            {
              name: '香菱',
              avatar: 'https://example.com/xiangling.png',
              level: 80,
              element: '火',
              constellation: 4,
              talentLevels: [1, 8, 8],
              weapon: '「渔获」',
              artifacts: ['绝缘之旗印']
            },
            {
              name: '班尼特',
              avatar: 'https://example.com/bennett.png',
              level: 80,
              element: '火',
              constellation: 1,
              talentLevels: [1, 8, 8],
              weapon: '天空之刃',
              artifacts: ['宗室4件']
            }
          ],
          description: '经典雷神国家队配置，通过元素反应打出高额伤害',
          dps: 45000,
          simulationTime: 90,
          createdAt: Date.now()
        }
      ]
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
}
</style>
