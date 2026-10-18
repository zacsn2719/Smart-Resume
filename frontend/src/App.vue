<template>
  <div class="shell">
    <aside class="app-sidebar">
      <div class="sidebar-top">
        <div class="sidebar-brand">
          <div class="brand-mark">
            <span class="material-symbols-outlined">assignment_turned_in</span>
          </div>
          <div class="brand-text">
            <div class="brand-title-row">
              <span class="brand-title">智配简历</span>
              <span class="brand-pro">PRO</span>
            </div>
            <span class="brand-sub">简历-岗位匹配分析系统</span>
          </div>
        </div>

        <nav class="sidebar-nav">
          <div class="nav-section">WORKSPACE</div>
          <router-link
            v-for="item in workspaceNav"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ active: isActive(item.path) }"
          >
            <span class="material-symbols-outlined">{{ item.icon }}</span>
            <span>{{ item.label }}</span>
          </router-link>

          <div class="nav-section">ANALYTICS &amp; INSIGHTS</div>
          <router-link
            v-for="item in analyticsNav"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ active: isActive(item.path) }"
          >
            <span class="material-symbols-outlined">{{ item.icon }}</span>
            <span>{{ item.label }}</span>
          </router-link>

          <div class="nav-section">SYSTEM</div>
          <router-link
            v-for="item in systemNav"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ active: isActive(item.path) }"
          >
            <span class="material-symbols-outlined">{{ item.icon }}</span>
            <span>{{ item.label }}</span>
          </router-link>
        </nav>
      </div>

      <div class="sidebar-footer">
        <div class="sidebar-user">
          <div class="sidebar-user-left">
            <div class="avatar-square">HR</div>
            <div class="sidebar-user-meta">
              <span class="sidebar-user-name">HR Manager</span>
              <span class="sidebar-user-status">
                <span class="status-dot"></span>在线
              </span>
            </div>
          </div>
          <button class="icon-btn" title="退出登录" type="button">
            <span class="material-symbols-outlined">logout</span>
          </button>
        </div>
      </div>
    </aside>

    <div class="app-main">
      <header class="app-header">
        <div class="breadcrumb">
          <span class="material-symbols-outlined">home</span>
          <span class="t-caption">/</span>
          <span class="t-label-sm" style="color: var(--on-surface)">{{ pageTitle }}</span>
        </div>
        <div class="header-right">
          <div ref="searchBoxRef" class="header-search">
            <span class="material-symbols-outlined">search</span>
            <input
              type="text"
              v-model="keyword"
              placeholder="搜索简历、岗位或匹配记录..."
              @focus="onFocus"
              @keyup.enter="onSearch"
              @keydown.esc.prevent="clearSearch"
            />
            <div v-if="panelVisible" class="header-search-panel">
              <div v-if="!dataLoaded && dataLoading" class="hs-empty">正在加载数据...</div>
              <template v-else>
                <template v-if="results && hasResults">
                  <div v-if="results.resumes.length" class="hs-group">
                    <div class="hs-group-label">简历</div>
                    <button v-for="r in results.resumes" :key="'r' + r.id" type="button" class="hs-item" @click="goResume">
                      <span class="hs-item-title">{{ r.name }}</span>
                      <span class="hs-item-sub">{{ r.skills.join(' / ') || r.education || '暂无技能信息' }}</span>
                    </button>
                  </div>
                  <div v-if="results.jobs.length" class="hs-group">
                    <div class="hs-group-label">岗位</div>
                    <button v-for="j in results.jobs" :key="'j' + j.id" type="button" class="hs-item" @click="goJob">
                      <span class="hs-item-title">{{ j.title }}<em v-if="j.company"> · {{ j.company }}</em></span>
                      <span class="hs-item-sub">{{ j.skills.join(' / ') || '—' }}</span>
                    </button>
                  </div>
                  <div v-if="results.records.length" class="hs-group">
                    <div class="hs-group-label">匹配记录</div>
                    <button v-for="rec in results.records" :key="'c' + rec.id" type="button" class="hs-item" @click="goRecord">
                      <span class="hs-item-title">{{ rec.resume_name }} × {{ rec.job_title }}</span>
                      <span class="hs-item-sub">{{ rec.score }} 分 · {{ rec.level }}</span>
                    </button>
                  </div>
                </template>
                <div v-else class="hs-empty">未找到与「{{ normalizedKw }}」相关的结果</div>
              </template>
            </div>
          </div>
          <button class="header-bell" title="通知" type="button">
            <span class="material-symbols-outlined">notifications</span>
            <span class="header-bell-dot"></span>
          </button>
          <div class="header-user">
            <div class="header-user-avatar">
              <span class="material-symbols-outlined">person</span>
            </div>
            <div class="header-user-meta">
              <span class="header-user-name">招聘专家</span>
              <span class="header-user-sub">人才甄选部</span>
            </div>
          </div>
        </div>
      </header>

      <main class="page-main">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from './api'
import { createSearchMatcher, debounce, filterByMatcher, normalizeKeyword } from './utils/search'

const route = useRoute()
const router = useRouter()

const LIMIT_PER_GROUP = 5

const keyword = ref('')
// 防抖后的生效关键词：输入停顿 300ms 后才触发真正的匹配计算
const deferredKeyword = ref('')
const panelOpen = ref(false)
const dataLoading = ref(false)
const dataLoaded = ref(false)
const searchBoxRef = ref(null)

const resumesData = ref([])
const jobsData = ref([])
const recordsData = ref([])

const normalizedKw = computed(() => normalizeKeyword(deferredKeyword.value))
const matcher = computed(() => createSearchMatcher(normalizedKw.value))
const panelVisible = computed(() => panelOpen.value && !!normalizedKw.value)

const results = computed(() => {
  const m = matcher.value
  if (!m) return null
  return {
    resumes: filterByMatcher(resumesData.value, m, (r) => [r.name, r.skills.join(' '), r.education], LIMIT_PER_GROUP),
    jobs: filterByMatcher(jobsData.value, m, (j) => [j.title, j.company, j.skills.join(' ')], LIMIT_PER_GROUP),
    records: filterByMatcher(recordsData.value, m, (r) => [r.resume_name, r.job_title, r.level], LIMIT_PER_GROUP),
  }
})

const hasResults = computed(() => {
  if (!results.value) return false
  return results.value.resumes.length > 0 || results.value.jobs.length > 0 || results.value.records.length > 0
})

// 输入防抖：300ms 内连续输入只执行一次匹配
watch(
  keyword,
  debounce(() => {
    deferredKeyword.value = normalizeKeyword(keyword.value)
  }, 300)
)

// 拉取三类数据供全局搜索匹配（失败时 api 层已统一提示）
const ensureData = async () => {
  if (dataLoading.value || dataLoaded.value) return
  dataLoading.value = true
  try {
    const [r, j, c] = await Promise.all([
      api.get('/resumes', { params: { page: 1, size: 100 } }),
      api.get('/jobs', { params: { page: 1, size: 100 } }),
      api.get('/records', { params: { page: 1, size: 100 } }),
    ])
    resumesData.value = r.data.items
    jobsData.value = j.data.items
    recordsData.value = c.data.items
    dataLoaded.value = true
  } catch (e) {
    /* 忽略，保持已有缓存 */
  } finally {
    dataLoading.value = false
  }
}

function onFocus() {
  panelOpen.value = true
  ensureData()
}

// 回车：跳过防抖立即执行匹配
function onSearch() {
  deferredKeyword.value = normalizeKeyword(keyword.value)
  panelOpen.value = true
  ensureData()
}

function clearSearch() {
  keyword.value = ''
  deferredKeyword.value = ''
  panelOpen.value = false
}

function navTo(path) {
  panelOpen.value = false
  router.push({ path, query: { q: normalizedKw.value } })
}
const goResume = () => navTo('/')
const goJob = () => navTo('/jobs')
const goRecord = () => navTo('/history')

// 点击搜索区域外关闭下拉面板
function onDocPointerDown(e) {
  if (panelOpen.value && searchBoxRef.value && !searchBoxRef.value.contains(e.target)) {
    panelOpen.value = false
  }
}
onMounted(() => document.addEventListener('pointerdown', onDocPointerDown))
onBeforeUnmount(() => document.removeEventListener('pointerdown', onDocPointerDown))

const workspaceNav = [
  { path: '/', label: '简历管理', icon: 'description' },
  { path: '/jobs', label: '岗位管理', icon: 'work' },
]
const analyticsNav = [
  { path: '/match', label: '匹配分析', icon: 'hub' },
  { path: '/history', label: '历史记录', icon: 'history' },
  { path: '/stats', label: '统计看板', icon: 'bar_chart' },
]
const systemNav = [{ path: '/about', label: '关于系统', icon: 'info' }]

const pageTitle = computed(() => route.meta.title || '控制台中心')

function isActive(path) {
  return route.path === path
}
</script>

<style scoped>
.shell {
  min-height: 100vh;
}
</style>
