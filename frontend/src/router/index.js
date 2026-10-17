import { createRouter, createWebHistory } from 'vue-router'
import Resumes from '../views/Resumes.vue'
import Jobs from '../views/Jobs.vue'
import Match from '../views/Match.vue'
import History from '../views/History.vue'
import Stats from '../views/Stats.vue'
import About from '../views/About.vue'

const routes = [
  { path: '/', name: 'Resumes', component: Resumes, meta: { title: '简历管理' } },
  { path: '/jobs', name: 'Jobs', component: Jobs, meta: { title: '岗位管理' } },
  { path: '/match', name: 'Match', component: Match, meta: { title: '匹配分析' } },
  { path: '/history', name: 'History', component: History, meta: { title: '历史记录' } },
  { path: '/stats', name: 'Stats', component: Stats, meta: { title: '统计看板' } },
  { path: '/about', name: 'About', component: About, meta: { title: '关于' } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
