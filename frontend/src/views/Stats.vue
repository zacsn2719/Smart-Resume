<template>
  <div v-loading="loading">
    <el-row :gutter="16">
      <el-col :span="8">
        <el-card shadow="never">
          <div class="stat-label">总匹配次数</div>
          <div class="stat-num">{{ data.total }}</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="never">
          <div class="stat-label">平均匹配分</div>
          <div class="stat-num">{{ data.avg_score }}</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="never">
          <div class="stat-label">高度匹配占比</div>
          <div class="stat-num">{{ highRate }}</div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16" style="margin-top: 16px">
      <el-col :span="12">
        <el-card shadow="never">
          <template #header><b>匹配等级分布</b></template>
          <div ref="pieRef" class="chart"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="never">
          <template #header><b>缺失技能 TOP5</b></template>
          <div ref="barRef" class="chart"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row style="margin-top: 16px">
      <el-col :span="24">
        <el-card shadow="never">
          <template #header><b>最近 7 天匹配次数趋势</b></template>
          <div ref="lineRef" class="chart-wide"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'
import * as echarts from 'echarts'
import api from '../api'

const loading = ref(false)
const pieRef = ref(null)
const barRef = ref(null)
const lineRef = ref(null)
const data = reactive({
  total: 0,
  avg_score: 0,
  level_distribution: { 高度匹配: 0, 较匹配: 0, 一般: 0, 不匹配: 0 },
  missing_skill_top5: [],
  trend: []
})

const highRate = computed(() => {
  if (!data.total) return '0%'
  return Math.round((data.level_distribution['高度匹配'] / data.total) * 100) + '%'
})

let charts = []

const renderCharts = () => {
  const pie = echarts.init(pieRef.value)
  pie.setOption({
    tooltip: { trigger: 'item' },
    legend: { bottom: 0 },
    series: [
      {
        name: '匹配等级分布',
        type: 'pie',
        radius: ['40%', '65%'],
        label: { formatter: '{b}: {c}' },
        data: [
          { name: '高度匹配', value: data.level_distribution['高度匹配'] || 0, itemStyle: { color: '#67c23a' } },
          { name: '较匹配', value: data.level_distribution['较匹配'] || 0, itemStyle: { color: '#409eff' } },
          { name: '一般', value: data.level_distribution['一般'] || 0, itemStyle: { color: '#e6a23c' } },
          { name: '不匹配', value: data.level_distribution['不匹配'] || 0, itemStyle: { color: '#f56c6c' } }
        ]
      }
    ]
  })
  charts.push(pie)

  const top5 = data.missing_skill_top5
  const bar = echarts.init(barRef.value)
  bar.setOption({
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    grid: { left: 60, right: 20, bottom: 40, top: 20 },
    xAxis: { type: 'category', data: top5.map((x) => x.skill), axisLabel: { interval: 0, rotate: 20 } },
    yAxis: { type: 'value', minInterval: 1 },
    series: [{ type: 'bar', barMaxWidth: 40, data: top5.map((x) => x.count), itemStyle: { color: '#409eff' } }]
  })
  charts.push(bar)

  const trend = data.trend
  const line = echarts.init(lineRef.value)
  line.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: 60, right: 40, bottom: 40, top: 20 },
    xAxis: { type: 'category', data: trend.map((x) => x.date) },
    yAxis: { type: 'value', minInterval: 1 },
    series: [
      {
        name: '匹配次数',
        type: 'line',
        smooth: true,
        areaStyle: { opacity: 0.15 },
        data: trend.map((x) => x.count),
        itemStyle: { color: '#67c23a' }
      }
    ]
  })
  charts.push(line)
}

const onResize = () => charts.forEach((c) => c.resize())

const load = async () => {
  loading.value = true
  try {
    const res = await api.get('/stats')
    Object.assign(data, res.data)
    await nextTick()
    renderCharts()
    window.addEventListener('resize', onResize)
  } finally {
    loading.value = false
  }
}

onBeforeUnmount(() => {
  window.removeEventListener('resize', onResize)
  charts.forEach((c) => c.dispose())
  charts = []
})

onMounted(load)
</script>

<style scoped>
.stat-label {
  font-size: 14px;
  color: #909399;
}

.stat-num {
  font-size: 32px;
  font-weight: 700;
  margin-top: 8px;
  color: #303133;
}

.chart {
  height: 320px;
}

.chart-wide {
  height: 280px;
}
</style>
