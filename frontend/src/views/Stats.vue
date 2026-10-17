<template>
  <div class="page-inner" style="padding:1rem 1.5rem">
    <!-- 页头 -->
    <div class="page-head">
      <div>
        <div class="row-gap-xs">
          <span class="t-headline-md">统计看板</span>
          <span class="pill secondary">实时同步</span>
        </div>
        <p class="page-head-sub">算法引擎：jieba 分词 · TF-IDF 逆文档频 · 余弦文本相似度模型</p>
      </div>
      <div class="page-head-actions">
        <div class="segmented">
          <button :class="{ active: range === '7d' }" @click="range = '7d'">最近 7 天</button>
          <button :class="{ active: range === 'month' }" @click="range = 'month'">本月</button>
          <button :class="{ active: range === 'custom' }" @click="range = 'custom'">自定义</button>
        </div>
        <button class="btn btn-surface" @click="exportReport">
          <span class="material-symbols-outlined">download</span><span>导出看板报表</span>
        </button>
        <button class="btn btn-primary" :disabled="loading" @click="recompute">
          <span class="material-symbols-outlined">{{ loading ? 'sync' : 'bolt' }}</span><span>执行全量重算</span>
        </button>
      </div>
    </div>

    <!-- KPI -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-top">
          <div class="kpi-top-left">
            <div class="kpi-icon primary"><span class="material-symbols-outlined">hub</span></div>
            <span class="kpi-label">总匹配次数</span>
          </div>
          <span class="pill primary">+{{ todayCount }} 今日</span>
        </div>
        <div class="kpi-value-row"><span class="kpi-value">{{ data.total }}</span><span class="kpi-unit">次评测</span></div>
        <div class="kpi-foot"><span>待匹配候选池 {{ resumeCount }} 份</span><span style="color:var(--tertiary)">覆盖率 {{ data.total ? 100 : 0 }}%</span></div>
      </div>

      <div class="kpi-card">
        <div class="kpi-top">
          <div class="kpi-top-left">
            <div class="kpi-icon secondary"><span class="material-symbols-outlined">speed</span></div>
            <span class="kpi-label">平均匹配分</span>
          </div>
          <span class="pill neutral">基准 60.0</span>
        </div>
        <div class="kpi-value-row"><span class="kpi-value">{{ data.avg_score }}</span><span class="kpi-unit">/ 100 分</span></div>
        <div class="kpi-foot"><span>最高得分 {{ maxScore }}</span><span class="c-secondary">波动 ±{{ fluctuation }}</span></div>
      </div>

      <div class="kpi-card">
        <div class="kpi-top">
          <div class="kpi-top-left">
            <div class="kpi-icon error"><span class="material-symbols-outlined">warning</span></div>
            <span class="kpi-label">高度匹配占比</span>
          </div>
          <span class="pill" :class="highCount ? 'tertiary' : 'error'">{{ highCount ? '质量达标' : '需关注' }}</span>
        </div>
        <div class="kpi-value-row">
          <span class="kpi-value" :style="{ color: highCount ? 'var(--tertiary)' : 'var(--error)' }">{{ highRate }}%</span>
          <span class="kpi-unit">{{ highCount }} 份达标</span>
        </div>
        <div class="kpi-foot"><span>跨专业投递占多数</span><span :style="{ color: highCount ? 'var(--tertiary)' : 'var(--error)' }">{{ highCount ? '技能断层已修复' : '技能断层明显' }}</span></div>
      </div>

      <div class="kpi-card">
        <div class="kpi-top">
          <div class="kpi-top-left">
            <div class="kpi-icon tertiary"><span class="material-symbols-outlined">psychology</span></div>
            <span class="kpi-label">覆盖技能词库</span>
          </div>
          <span class="pill tertiary">+{{ skillVocab.length }} 关键词</span>
        </div>
        <div class="kpi-value-row"><span class="kpi-value">{{ skillVocab.length }}</span><span class="kpi-unit">项核心标签</span></div>
        <div class="kpi-foot"><span>NLP 标准词典已生效</span><span style="color:var(--tertiary)">候选/岗位已并入</span></div>
      </div>
    </div>

    <!-- 双图网格 -->
    <div class="grid-2col">
      <!-- 匹配等级分布 -->
      <div class="card" style="display:flex;flex-direction:column;justify-content:space-between">
        <div class="card-head">
          <div class="row-gap-xs">
            <span class="section-title">匹配等级分布</span>
            <span class="material-symbols-outlined c-secondary" style="font-size:18px" title="根据余弦文本匹配度区间划分等级">help</span>
          </div>
          <span class="t-caption c-secondary">总基数: {{ data.total }}</span>
        </div>

        <div class="chart-box donut-wrap" style="height:15rem;position:relative">
          <div ref="pieRef" style="width:100%;height:100%"></div>
          <div class="donut-center">
            <span class="t-caption c-secondary" style="text-transform:uppercase;letter-spacing:0.06em">{{ dominantLabel }} 占比</span>
            <span class="t-headline-xl" style="font-weight:700">{{ dominantRate }}%</span>
            <span class="t-caption" :style="{ color: dominantColor }">样本量 {{ data.total }} 份</span>
          </div>
        </div>

        <div class="legend-grid">
          <div v-for="l in levelLegend" :key="l.name" class="legend-card" :class="{ danger: l.name === '不匹配' && l.count }">
            <div class="legend-card-left">
              <span class="dot" :style="{ background: l.color }"></span>
              <span class="legend-text">{{ l.name }} ({{ l.range }})</span>
            </div>
            <span class="legend-val">{{ l.count }} 份</span>
          </div>
        </div>

        <div class="tips" style="display:flex;margin-top:0.75rem">
          <span class="material-symbols-outlined">tips_and_updates</span>
          <span>诊断提示：当前被测样本偏向跨领域投递，在工程基础设施架构要求上出现明显技术栈断层。建议检查初筛 JD 的技术硬指标权重。</span>
        </div>
      </div>

      <!-- 缺失技能 TOP5 -->
      <div class="card" style="display:flex;flex-direction:column;justify-content:space-between">
        <div class="card-head" style="align-items:flex-start">
          <div>
            <div class="row-gap-xs">
              <span class="section-title">缺失技能 TOP 5</span>
              <span class="pill primary">硬性技术门槛</span>
            </div>
            <p class="t-caption c-secondary" style="margin:4px 0 0">候选人与岗位要求对照中，出现频率最高的缺失知识点</p>
          </div>
          <button class="icon-btn" title="更多技能筛选"><span class="material-symbols-outlined">filter_list</span></button>
        </div>

        <div class="chart-box tall" ref="barRef"></div>

        <div class="row-between wrap" style="gap:0.5rem;padding-top:0.75rem">
          <div class="row-gap-sm wrap t-caption c-secondary">
            <span class="row-gap-xs"><span class="dot" style="width:10px;height:10px;border-radius:2px;background:var(--primary-container)"></span>核心容器化技术 (权重 × 1.5)</span>
            <span class="row-gap-xs"><span class="dot" style="width:10px;height:10px;border-radius:2px;background:var(--secondary-container)"></span>自动化交付链 (权重 × 1.0)</span>
          </div>
          <a class="link-primary" href="javascript:;">配置缺失技能预警策略<span class="material-symbols-outlined" style="font-size:14px">arrow_forward</span></a>
        </div>
      </div>
    </div>

    <!-- 趋势 -->
    <div class="card" style="display:flex;flex-direction:column;gap:0.75rem">
      <div class="row-between wrap" style="gap:0.75rem">
        <div>
          <div class="row-gap-xs">
            <span class="section-title">最近 7 天匹配次数趋势与效率</span>
            <span class="pill tertiary">高敏监测</span>
          </div>
          <p class="t-caption c-secondary" style="margin:4px 0 0">记录每日触发岗位简历协同分析的模型任务总数及处理耗时</p>
        </div>
        <div class="row-gap-md wrap t-caption c-secondary">
          <span class="row-gap-xs"><span class="dot" style="width:12px;height:3px;border-radius:2px;background:var(--primary-container)"></span>匹配次数 (次)</span>
          <span class="row-gap-xs"><span class="dot" style="width:12px;height:3px;border-radius:2px;background:var(--secondary-fixed-dim)"></span>基线均值</span>
          <span class="row-gap-xs"><span class="dot" style="width:8px;height:8px;background:var(--tertiary-container)"></span>峰值记录点</span>
        </div>
      </div>

      <div class="chart-box tall" ref="lineRef"></div>

      <div class="row-between wrap" style="gap:0.75rem;padding-top:0.5rem;background:var(--surface-container-low);border-radius:0.5rem;padding:0.75rem">
        <div class="row-gap-sm" style="align-items:flex-start">
          <div class="kpi-icon primary" style="width:1.75rem;height:1.75rem;border-radius:9999px;flex-shrink:0"><span class="material-symbols-outlined" style="font-size:16px">insights</span></div>
          <div>
            <span class="t-label-md">系统分析结论：</span>
            <span class="t-body-sm c-secondary">近期整体匹配量 {{ data.total ? '平稳' : '为零' }}，算法词频库已并入微服务与云原生标签；当前初筛候选人多因容器编排经历不足被评定为「{{ bottomLevel }}」。</span>
          </div>
        </div>
        <button class="btn-text">优化岗位画像关键词<span class="material-symbols-outlined" style="font-size:16px">chevron_right</span></button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'
import * as echarts from 'echarts'
import { ElMessage } from 'element-plus'
import api from '../api'

const loading = ref(false)
const range = ref('7d')
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

const resumeCount = ref(0)
const jobCount = ref(0)
const skillVocab = ref([])
const maxScore = ref(0)
const minScore = ref(0)
const todayCount = ref(0)
let charts = []

const highCount = computed(() => data.level_distribution['高度匹配'] || 0)
const highRate = computed(() => (data.total ? Math.round((highCount.value / data.total) * 100) : 0))
const fluctuation = computed(() => (maxScore.value || minScore.value ? Math.abs(maxScore.value - minScore.value).toFixed(1) : '0.0'))
const bottomLevel = computed(() => {
  const entries = Object.entries(data.level_distribution)
  if (!entries.length) return '—'
  entries.sort((a, b) => a[1] - b[1])
  return entries[entries.length - 1][0]
})

const levelLegend = computed(() => [
  { name: '高度匹配', range: '≥80', color: '#00b07a', count: data.level_distribution['高度匹配'] || 0 },
  { name: '较匹配', range: '60-79', color: '#565e74', count: data.level_distribution['较匹配'] || 0 },
  { name: '一般', range: '45-59', color: '#f97316', count: data.level_distribution['一般'] || 0 },
  { name: '不匹配', range: '<45', color: '#ba1a1a', count: data.level_distribution['不匹配'] || 0 }
])

const dominantLabel = computed(() => {
  const entries = Object.entries(data.level_distribution).sort((a, b) => b[1] - a[1])
  return entries.length && entries[0][1] > 0 ? entries[0][0] : '暂无数据'
})
const dominantRate = computed(() => (data.total ? Math.round(((data.level_distribution[dominantLabel.value] || 0) / data.total) * 100) : 0))
const dominantColor = computed(() => {
  const l = levelLegend.value.find((x) => x.name === dominantLabel.value)
  return l ? l.color : 'var(--secondary)'
})

const donutOption = () => ({
  tooltip: { trigger: 'item', formatter: '{b}: {c} 份 ({d}%)' },
  series: [
    {
      type: 'pie',
      radius: ['64%', '86%'],
      avoidLabelOverlap: false,
      label: { show: false },
      labelLine: { show: false },
      itemStyle: { borderColor: '#ffffff', borderWidth: 3 },
      data: levelLegend.value.map((l) => ({ name: l.name, value: l.count, itemStyle: { color: l.color } }))
    }
  ]
})

const barOption = () => {
  const top5 = data.missing_skill_top5 || []
  const max = Math.max(1, ...top5.map((x) => x.count))
  return {
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' }, formatter: (p) => `${p[0].name}<br/>${p[0].value} 次未满足` },
    grid: { left: 44, right: 16, bottom: 34, top: 26 },
    xAxis: {
      type: 'category',
      data: top5.map((x) => x.skill),
      axisLine: { lineStyle: { color: '#e0c0b1' } },
      axisTick: { show: false },
      axisLabel: { interval: 0, fontSize: 12, fontWeight: 600, color: '#0b1c30' }
    },
    yAxis: {
      type: 'value',
      minInterval: 1,
      splitLine: { lineStyle: { color: '#dce9ff', type: 'dashed' } },
      axisLabel: { fontSize: 11, color: '#565e74' }
    },
    series: [
      {
        type: 'bar',
        barMaxWidth: 52,
        data: top5.map((x, i) => ({
          value: x.count,
          itemStyle: {
            color: i < 2 ? '#f97316' : '#dae2fd',
            borderRadius: [6, 6, 0, 0],
            opacity: i < 2 ? 1 : 1
          },
          label: { show: true, position: 'top', formatter: `${x.count} 次`, fontSize: 11, fontWeight: 700, color: i < 2 ? '#f97316' : '#565e74' }
        })),
        emphasis: { itemStyle: { color: '#9d4300' } }
      },
      {
        type: 'bar',
        barMaxWidth: 52,
        silent: true,
        tooltip: { show: false },
        data: top5.map(() => max),
        itemStyle: { color: '#eff4ff', borderRadius: [6, 6, 0, 0] },
        barGap: '-100%',
        z: -1
      }
    ]
  }
}

const lineOption = () => {
  const trend = data.trend || []
  const values = trend.map((x) => x.count)
  const avg = values.length ? values.reduce((a, b) => a + b, 0) / values.length : 0
  const peak = Math.max(...values, 0)
  return {
    tooltip: { trigger: 'axis' },
    grid: { left: 44, right: 24, bottom: 30, top: 24 },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: trend.map((x) => x.date),
      axisLine: { lineStyle: { color: '#e0c0b1' } },
      axisTick: { show: false },
      axisLabel: { fontSize: 11, color: '#565e74' }
    },
    yAxis: {
      type: 'value',
      minInterval: 1,
      splitLine: { lineStyle: { color: '#dce9ff', type: 'dashed' } },
      axisLabel: { fontSize: 11, color: '#565e74' }
    },
    series: [
      {
        name: '基线均值',
        type: 'line',
        data: trend.map(() => avg),
        smooth: true,
        symbol: 'none',
        lineStyle: { color: '#bec6e0', width: 2, type: 'dashed' },
        itemStyle: { color: '#bec6e0' },
        z: 1
      },
      {
        name: '匹配次数',
        type: 'line',
        smooth: true,
        symbol: 'circle',
        symbolSize: 7,
        showSymbol: true,
        data: values,
        lineStyle: { color: '#f97316', width: 3 },
        itemStyle: { color: '#f97316', borderColor: '#ffffff', borderWidth: 2 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(249,115,22,0.28)' },
            { offset: 1, color: 'rgba(249,115,22,0.00)' }
          ])
        },
        markPoint: {
          symbol: 'circle',
          symbolSize: 9,
          data: [{ type: 'max' }],
          itemStyle: { color: '#00b07a', borderColor: '#ffffff', borderWidth: 2 },
          label: { show: false }
        },
        markLine: peak ? { silent: true, symbol: 'none', data: [{ type: 'max', name: '峰值' }], lineStyle: { color: '#00b07a', type: 'solid', width: 1 }, label: { show: true, formatter: '峰值 {c}', color: '#00b07a', fontSize: 11, fontWeight: 600 } } : undefined
      }
    ]
  }
}

const renderCharts = () => {
  charts.forEach((c) => c.dispose())
  charts = []
  if (pieRef.value) {
    const pie = echarts.init(pieRef.value)
    pie.setOption(donutOption())
    charts.push(pie)
  }
  if (barRef.value) {
    const bar = echarts.init(barRef.value)
    bar.setOption(barOption())
    charts.push(bar)
  }
  if (lineRef.value) {
    const line = echarts.init(lineRef.value)
    line.setOption(lineOption())
    charts.push(line)
  }
}

const onResize = () => charts.forEach((c) => c.resize())

const load = async () => {
  loading.value = true
  try {
    const [statsRes, resumeRes, jobRes, recordRes] = await Promise.all([
      api.get('/stats'),
      api.get('/resumes', { params: { page: 1, size: 100 } }),
      api.get('/jobs', { params: { page: 1, size: 100 } }),
      api.get('/records', { params: { page: 1, size: 100 } })
    ])
    Object.assign(data, statsRes.data)
    resumeCount.value = resumeRes.data.total
    jobCount.value = jobRes.data.total

    const vocab = new Set()
    resumeRes.data.items.forEach((r) => (r.skills || []).forEach((s) => vocab.add(s)))
    jobRes.data.items.forEach((j) => (j.skills || []).forEach((s) => vocab.add(s)))
    skillVocab.value = [...vocab]

    const scores = recordRes.data.items.map((r) => r.score)
    maxScore.value = scores.length ? Math.max(...scores) : 0
    minScore.value = scores.length ? Math.min(...scores) : 0

    const today = new Date().toISOString().slice(0, 10)
    todayCount.value = recordRes.data.items.filter((r) => String(r.created_at || '').slice(0, 10) === today).length

    await nextTick()
    renderCharts()
    window.addEventListener('resize', onResize)
  } finally {
    loading.value = false
  }
}

const recompute = async () => {
  await load()
  ElMessage.success('看板已全量重算')
}

const exportReport = () => {
  const rows = [
    ['指标', '数值'],
    ['总匹配次数', data.total],
    ['平均匹配分', data.avg_score],
    ['高度匹配次数', highCount.value],
    ['覆盖技能词库', skillVocab.value.length],
    [],
    ['匹配等级', '数量'],
    ...levelLegend.value.map((l) => [l.name, l.count]),
    [],
    ['缺失技能', '未满足次数'],
    ...(data.missing_skill_top5 || []).map((x) => [x.skill, x.count]),
    [],
    ['日期', '匹配次数'],
    ...(data.trend || []).map((t) => [t.date, t.count])
  ]
  const csv = '\ufeff' + rows.map((r) => r.map((c) => `"${String(c ?? '').replace(/"/g, '""')}"`).join(',')).join('\n')
  const url = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }))
  const a = document.createElement('a')
  a.href = url
  a.download = 'dashboard-report.csv'
  a.click()
  URL.revokeObjectURL(url)
  ElMessage.success('已导出看板报表')
}

onBeforeUnmount(() => {
  window.removeEventListener('resize', onResize)
  charts.forEach((c) => c.dispose())
  charts = []
})

onMounted(load)
</script>
