<template>
  <el-container class="layout">
    <el-aside width="220px" class="aside">
      <div class="logo">
        <div class="logo-title">智配简历</div>
        <div class="logo-sub">简历-岗位匹配分析系统</div>
      </div>
      <el-menu
        :default-active="$route.path"
        router
        background-color="#001529"
        text-color="#bfcbd9"
        active-text-color="#ffffff"
      >
        <el-menu-item index="/">简历管理</el-menu-item>
        <el-menu-item index="/jobs">岗位管理</el-menu-item>
        <el-menu-item index="/match">匹配分析</el-menu-item>
        <el-menu-item index="/history">历史记录</el-menu-item>
        <el-menu-item index="/stats">统计看板</el-menu-item>
        <el-menu-item index="/about">关于</el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <span class="header-title">{{ pageTitle }}</span>
        <span class="header-tip">jieba 分词 · TF-IDF · 余弦相似度</span>
      </el-header>
      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const pageTitle = computed(() => route.meta.title || '智配简历')
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html,
body,
#app {
  height: 100%;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Microsoft YaHei', Arial, sans-serif;
}

.layout {
  height: 100%;
}

.aside {
  background-color: #001529;
}

.logo {
  height: 90px;
  padding: 20px 20px 0;
  color: #fff;
}

.logo-title {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: 2px;
}

.logo-sub {
  margin-top: 6px;
  font-size: 12px;
  color: #8ca0b3;
}

.aside .el-menu {
  border-right: none;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  border-bottom: 1px solid #e6e6e6;
}

.header-title {
  font-size: 18px;
  font-weight: 600;
}

.header-tip {
  font-size: 12px;
  color: #909399;
}

.main {
  background: #f0f2f5;
}
</style>
