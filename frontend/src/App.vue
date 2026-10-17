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
          <div class="header-search">
            <span class="material-symbols-outlined">search</span>
            <input
              type="text"
              v-model="keyword"
              placeholder="搜索简历、岗位或匹配记录..."
              @keyup.enter="onSearch"
            />
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
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const keyword = ref('')

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

function onSearch() {
  /* global search is a presentation placeholder in the design */
}
</script>

<style scoped>
.shell {
  min-height: 100vh;
}
</style>
