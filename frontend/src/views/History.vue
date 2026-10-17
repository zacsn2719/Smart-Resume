<template>
  <div class="page-inner">
    <!-- 页头 -->
    <div class="page-head">
      <div class="row-gap-md">
        <div class="kpi-icon primary" style="width:2.75rem;height:2.75rem;border-radius:0.75rem">
          <span class="material-symbols-outlined" style="font-size:24px">history_edu</span>
        </div>
        <div>
          <div class="row-gap-sm" style="flex-wrap:wrap">
            <h1 class="t-headline-xl">匹配历史记录</h1>
            <span class="pill secondary">共 {{ all.length }} 条评估记录</span>
          </div>
          <p class="page-head-sub">基于 TF-IDF 向量化与多维余弦语义相似度分析引擎的候选人评测归档</p>
        </div>
      </div>
      <div class="page-head-actions">
        <button class="btn btn-surface" @click="exportCsv">
          <span class="material-symbols-outlined">download</span><span>导出历史报告</span>
        </button>
        <button class="btn" style="background:var(--surface-container-lowest);color:var(--error);box-shadow:var(--shadow-sm)" :disabled="!all.length" @click="clearAll">
          <span class="material-symbols-outlined">delete_sweep</span><span>清空记录</span>
        </button>
        <button class="btn btn-primary" @click="router.push('/match')">
          <span class="material-symbols-outlined">add</span><span>发起新评估</span>
        </button>
      </div>
    </div>

    <!-- KPI -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-top">
          <div class="kpi-top-left" style="flex-direction:column;align-items:flex-start;gap:0.25rem">
            <span class="t-label-sm c-secondary" style="text-transform:uppercase;letter-spacing:0.06em">累计匹配诊断</span>
            <span class="t-headline-xl">{{ all.length }} <span class="t-body-md c-secondary">次</span></span>
          </div>
          <div class="kpi-icon" style="background:rgba(249,115,22,0.16);color:var(--primary)"><span class="material-symbols-outlined">donut_large</span></div>
        </div>
        <div class="kpi-foot">
          <span class="row-gap-xs"><span class="dot" style="width:6px;height:6px;background:var(--primary-container)"></span>已归档诊断报告</span>
          <span class="t-label-sm">本月总览</span>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-top">
          <div class="kpi-top-left" style="flex-direction:column;align-items:flex-start;gap:0.25rem">
            <span class="t-label-sm c-secondary" style="text-transform:uppercase;letter-spacing:0.06em">平均综合评分</span>
            <span class="t-headline-xl">{{ avgScore }}<span class="t-body-md c-secondary">%</span></span>
          </div>
          <div class="kpi-icon" style="background:rgba(255,218,214,0.6);color:var(--error)"><span class="material-symbols-outlined">trending_down</span></div>
        </div>
        <div class="kpi-foot">
          <span class="pill" :class="avgScore >= 60 ? 'tertiary' : 'error'">{{ avgScore >= 60 ? '质量达标' : '专业度偏离' }}</span>
          <span>算法阈值 &lt; 60%</span>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-top">
          <div class="kpi-top-left" style="flex-direction:column;align-items:flex-start;gap:0.25rem">
            <span class="t-label-sm c-secondary" style="text-transform:uppercase;letter-spacing:0.06em">诊断岗位覆盖</span>
            <span class="t-headline-xl">{{ jobCoverage.length }} <span class="t-body-md c-secondary">个方向</span></span>
          </div>
          <div class="kpi-icon" style="background:var(--secondary-fixed);color:var(--on-secondary-fixed)"><span class="material-symbols-outlined">work_history</span></div>
        </div>
        <div class="kpi-foot">
          <span class="t-caption" style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:11rem">{{ jobCoverage.slice(0, 3).join('、') || '暂无岗位' }}</span>
          <span class="t-label-sm c-secondary">技术研发部</span>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-top">
          <div class="kpi-top-left" style="flex-direction:column;align-items:flex-start;gap:0.25rem">
            <span class="t-label-sm c-secondary" style="text-transform:uppercase;letter-spacing:0.06em">最近诊断执行</span>
            <span class="t-title-sm" style="margin-top:0.25rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{{ lastRun ? formatTime(lastRun) : '—' }}</span>
          </div>
          <div class="kpi-icon" style="background:var(--tertiary-fixed);color:var(--tertiary)"><span class="material-symbols-outlined">schedule</span></div>
        </div>
        <div class="kpi-foot">
          <span class="t-label-sm c-tertiary row-gap-xs"><span class="dot" style="width:6px;height:6px;background:var(--tertiary-container)"></span>系统运行正常</span>
          <span>耗时 0.28s</span>
        </div>
      </div>
    </div>

    <!-- 过滤器 -->
    <div class="card" style="padding:0.75rem;display:flex;flex-direction:column;gap:0.75rem" >
      <div class="row-between wrap" style="gap:0.75rem">
        <div class="row-gap-sm wrap" style="flex:1">
          <div style="position:relative;min-width:16rem;flex:1;max-width:24rem">
            <span class="material-symbols-outlined" style="position:absolute;left:0.75rem;top:0.55rem;color:var(--secondary);font-size:18px">search</span>
            <input v-model="search" class="input" style="height:2.25rem;padding-left:2.25rem" placeholder="按候选人姓名、岗位名称搜索..." />
          </div>
          <select v-model="levelFilter" class="select" style="height:2.25rem;width:auto;font-size:13px">
            <option value="">全部等级 (高匹配 / 一般 / 不匹配)</option>
            <option value="高度匹配">高匹配 (85% - 100%)</option>
            <option value="一般">一般匹配 (60% - 84%)</option>
            <option value="不匹配">不匹配 (&lt; 60%)</option>
          </select>
          <div class="row-gap-xs t-body-sm c-secondary">
            <span class="material-symbols-outlined" style="font-size:16px">calendar_today</span>
            <span>2026-10-01 ~ 2026-10-31</span>
            <span class="material-symbols-outlined" style="font-size:16px">arrow_drop_down</span>
          </div>
        </div>
        <div class="row-gap-sm">
          <div class="segmented">
            <button :class="{ active: view === 'table' }" @click="view = 'table'">
              <span class="material-symbols-outlined" style="font-size:16px">table_rows</span>列表
            </button>
            <button :class="{ active: view === 'card' }" @click="view = 'card'">
              <span class="material-symbols-outlined" style="font-size:16px">grid_view</span>卡片
            </button>
          </div>
          <button class="icon-btn" style="background:var(--surface-container-low);padding:0.5rem;border-radius:0.5rem" title="刷新表格" @click="load">
            <span class="material-symbols-outlined" style="font-size:18px">refresh</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 列表视图 -->
    <div v-if="view === 'table'" style="background:var(--surface-container-lowest);border-radius:0.75rem;box-shadow:var(--shadow-sm);overflow:hidden">
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th style="width:4rem;text-align:center">ID</th>
              <th>简历名称 / 候选人</th>
              <th>目标岗位名称</th>
              <th>综合评分与语义契合</th>
              <th>匹配等级</th>
              <th>诊断时间</th>
              <th style="text-align:right">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in pageItems" :key="row.id">
              <td style="text-align:center">
                <span class="t-caption mono" style="background:var(--surface-container-low);padding:0.25rem 0.5rem;border-radius:0.25rem;color:var(--on-surface);font-weight:500">#{{ String(row.id).padStart(2, '0') }}</span>
              </td>
              <td>
                <div class="row-gap-sm">
                  <div class="kpi-icon" style="width:2.25rem;height:2.25rem;background:var(--primary-fixed);color:var(--primary);flex-shrink:0">
                    <span class="material-symbols-outlined" style="font-size:20px">description</span>
                  </div>
                  <div class="stack" style="min-width:0">
                    <span class="t-title-sm" style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{{ row.resume_name }}</span>
                    <span class="t-body-xs c-secondary" style="margin-top:2px">
                      <span class="t-label-sm" :style="{ color: levelColor(row.level) }">{{ row.level }}</span>
                      <span> • 语义评测</span>
                    </span>
                  </div>
                </div>
              </td>
              <td>
                <div class="stack">
                  <span class="t-label-md">{{ row.job_title }}</span>
                  <span class="row-gap-xs t-caption c-secondary" style="margin-top:2px">
                    <span class="material-symbols-outlined" style="font-size:13px">domain</span>语义向量空间比对
                  </span>
                </div>
              </td>
              <td>
                <div class="stack" style="gap:0.375rem;width:11rem">
                  <div class="row-between">
                    <span class="t-label-sm" :style="{ color: levelColor(row.level) }">{{ row.score }}%</span>
                    <span class="t-caption c-secondary">TF-IDF {{ (row.score / 100).toFixed(3) }}</span>
                  </div>
                  <div class="progress-track" style="height:8px">
                    <span :style="{ width: row.score + '%', background: levelColor(row.level) }"></span>
                  </div>
                </div>
              </td>
              <td>
                <span :class="levelPill(row.level)" style="gap:0.375rem;padding:0.25rem 0.625rem;font-weight:600">
                  <span class="dot" style="width:6px;height:6px" :style="{ background: levelColor(row.level) }"></span>
                  {{ row.level }}
                </span>
              </td>
              <td>
                <div class="stack">
                  <span style="font-weight:500">{{ formatDate(row.created_at) }}</span>
                  <span class="t-caption c-secondary">{{ formatClock(row.created_at) }}</span>
                </div>
              </td>
              <td style="text-align:right;white-space:nowrap">
                <div class="row-gap-xs" style="justify-content:flex-end">
                  <button class="btn-text" @click="showDetail(row)">查看详情<span class="material-symbols-outlined" style="font-size:16px">chevron_right</span></button>
                  <button class="icon-btn" title="重新分析" @click="replay(row)"><span class="material-symbols-outlined" style="font-size:18px">replay</span></button>
                  <button class="icon-btn" style="color:var(--error)" title="删除记录" @click="remove(row)"><span class="material-symbols-outlined" style="font-size:18px">delete</span></button>
                </div>
              </td>
            </tr>
            <tr v-if="!pageItems.length">
              <td colspan="7"><div class="empty"><span class="material-symbols-outlined">history_toggle_off</span><div class="empty-title">暂无匹配历史记录</div><div class="empty-sub">点击右上角「发起新评估」开始首次诊断</div></div></td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="pagination">
        <div class="row-gap-sm wrap t-body-xs">
          <span>显示第 {{ pageRange[0] }} 至 {{ pageRange[1] }} 条记录，共 {{ filtered.length }} 条</span>
          <span style="color:var(--outline-variant)">|</span>
          <span class="row-gap-xs">
            每页显示
            <select v-model.number="size" class="select" style="width:auto;padding:0.125rem 1.5rem 0.125rem 0.5rem;border-radius:0.25rem;font-size:11px;font-weight:600">
              <option :value="10">10</option>
              <option :value="20">20</option>
              <option :value="50">50</option>
            </select>
            条
          </span>
        </div>
        <div class="pagination-btns">
          <button class="page-num" :disabled="page <= 1" @click="page--"><span class="material-symbols-outlined" style="font-size:16px">chevron_left</span></button>
          <button v-for="p in totalPages" :key="p" class="page-num" :class="{ active: p === page }" @click="page = p">{{ p }}</button>
          <button class="page-num" :disabled="page >= totalPages" @click="page++"><span class="material-symbols-outlined" style="font-size:16px">chevron_right</span></button>
        </div>
      </div>
    </div>

    <!-- 卡片视图 -->
    <div v-else class="kpi-grid" style="grid-template-columns:repeat(auto-fill,minmax(19rem,1fr))">
      <div v-for="row in pageItems" :key="row.id" class="card card-hover" style="display:flex;flex-direction:column;gap:0.75rem">
        <div class="row-between">
          <span class="t-caption mono c-secondary">#{String(row.id).padStart(2, '0')}</span>
          <span :class="levelPill(row.level)">{{ row.level }}</span>
        </div>
        <div class="stack">
          <span class="t-title-sm">{{ row.resume_name }}</span>
          <span class="t-body-xs c-secondary">× {{ row.job_title }}</span>
        </div>
        <div class="stack" style="gap:0.375rem">
          <div class="row-between">
            <span class="t-label-sm" :style="{ color: levelColor(row.level) }">{{ row.score }}%</span>
            <span class="t-caption c-secondary">TF-IDF {{ (row.score / 100).toFixed(3) }}</span>
          </div>
          <div class="progress-track" style="height:8px"><span :style="{ width: row.score + '%', background: levelColor(row.level) }"></span></div>
        </div>
        <div class="row-between" style="margin-top:auto">
          <span class="t-caption c-secondary">{{ formatTime(row.created_at) }}</span>
          <div class="row-gap-xs">
            <button class="icon-btn" title="重新分析" @click="replay(row)"><span class="material-symbols-outlined" style="font-size:16px">replay</span></button>
            <button class="icon-btn" style="color:var(--error)" title="删除" @click="remove(row)"><span class="material-symbols-outlined" style="font-size:16px">delete</span></button>
            <button class="btn-text" @click="showDetail(row)">详情<span class="material-symbols-outlined" style="font-size:15px">chevron_right</span></button>
          </div>
        </div>
      </div>
      <div v-if="!pageItems.length" class="card" style="grid-column:1/-1">
        <div class="empty"><span class="material-symbols-outlined">history_toggle_off</span><div class="empty-title">暂无匹配历史记录</div></div>
      </div>
    </div>

    <!-- 算法提示 -->
    <div class="card" style="background:var(--surface-container-low);display:flex;flex-direction:column;gap:1rem">
      <div class="row-between wrap" style="gap:1rem">
        <div class="row-gap-md" style="align-items:flex-start">
          <div class="kpi-icon" style="width:2.5rem;height:2.5rem;border-radius:0.75rem;background:var(--surface-container-lowest);color:var(--primary);box-shadow:var(--shadow-sm);flex-shrink:0">
            <span class="material-symbols-outlined" style="font-size:22px">psychology</span>
          </div>
          <div class="stack">
            <span class="t-title-sm">分析算法提示：余弦语义与特征权重比对</span>
            <span class="t-body-xs c-secondary" style="margin-top:2px">
              当前评估样本在核心专业术语匹配度较低时，建议导入针对性简历以获取更佳的匹配诊断评分。
            </span>
          </div>
        </div>
        <button class="btn btn-surface" style="align-self:center">查看算法模型说明</button>
      </div>
    </div>

    <!-- 详情 -->
    <div v-if="detailVisible" class="modal-mask" @click.self="detailVisible = false">
      <div class="modal wide">
        <div class="modal-head">
          <span class="modal-title">匹配记录详情</span>
          <button class="icon-btn" @click="detailVisible = false"><span class="material-symbols-outlined">close</span></button>
        </div>
        <div class="modal-body" v-if="detail">
          <div class="form-grid two" style="gap:0.75rem;margin-bottom:0.75rem">
            <div class="field"><label class="field-label">简历</label><div class="t-body-md">{{ detail.resume_name }}</div></div>
            <div class="field"><label class="field-label">岗位</label><div class="t-body-md">{{ detail.job_title }}</div></div>
            <div class="field">
              <label class="field-label">综合分</label>
              <div class="t-headline-md" :style="{ color: levelColor(detail.level) }">{{ detail.score }}</div>
            </div>
            <div class="field"><label class="field-label">等级</label><div><span :class="levelPill(detail.level)">{{ detail.level }}</span></div></div>
          </div>

          <div class="kpi-grid" style="grid-template-columns:repeat(2,1fr);gap:0.75rem;margin-bottom:0.75rem">
            <div class="legend-card"><span class="legend-text">技能覆盖率</span><span class="legend-val">{{ pct(detail.skill_score) }}%</span></div>
            <div class="legend-card"><span class="legend-text">文本相似度</span><span class="legend-val">{{ pct(detail.text_score) }}%</span></div>
            <div class="legend-card"><span class="legend-text">学历匹配</span><span class="legend-val">{{ pct(detail.edu_score) }}%</span></div>
            <div class="legend-card"><span class="legend-text">年限匹配</span><span class="legend-val">{{ pct(detail.years_score) }}%</span></div>
          </div>

          <div class="field" style="margin-bottom:0.75rem">
            <label class="field-label">已匹配技能</label>
            <div class="chip-row">
              <span v-for="s in detail.matched_skills" :key="s" class="chip tertiary">{{ s }}</span>
              <span v-if="!detail.matched_skills.length" class="t-caption c-secondary">无</span>
            </div>
          </div>

          <div class="field" style="margin-bottom:0.75rem">
            <label class="field-label">缺失技能</label>
            <div class="chip-row">
              <span v-for="s in detail.missing_skills" :key="s" class="chip error">{{ s }}</span>
              <span v-if="!detail.missing_skills.length" class="t-caption c-secondary">无</span>
            </div>
          </div>

          <div class="field" style="margin-bottom:0.75rem">
            <label class="field-label">改进建议</label>
            <p class="t-body-sm" style="margin:0;padding:0.75rem;border-radius:0.5rem;background:var(--surface-container-low);line-height:1.7">{{ detail.suggestion }}</p>
          </div>

          <div class="field">
            <label class="field-label">创建时间</label>
            <div class="t-body-md">{{ formatTime(detail.created_at) }}</div>
          </div>
        </div>
        <div class="modal-foot">
          <button class="btn btn-surface" @click="detailVisible = false">关闭</button>
          <button class="btn btn-primary" @click="detail && replay(detail); detailVisible = false">
            <span class="material-symbols-outlined">replay</span><span>重新分析</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '../api'
import { formatTime, formatDate, formatClock, levelColor, levelPill } from '../utils/format'

const router = useRouter()

const all = ref([])
const view = ref('table')
const search = ref('')
const levelFilter = ref('')
const size = ref(10)
const page = ref(1)
const detail = ref(null)
const detailVisible = ref(false)
const loading = ref(false)

const pct = (v) => Math.round((Number(v) || 0) * 100)

const load = async () => {
  loading.value = true
  try {
    const items = []
    let p = 1
    while (p <= 10) {
      const res = await api.get('/records', { params: { page: p, size: 100 } })
      items.push(...res.data.items)
      if (items.length >= res.data.total) break
      p++
    }
    all.value = items
  } finally {
    loading.value = false
  }
}

const avgScore = computed(() => {
  if (!all.value.length) return 0
  return Math.round(all.value.reduce((s, r) => s + (r.score || 0), 0) / all.value.length * 10) / 10
})

const jobCoverage = computed(() => [...new Set(all.value.map((r) => r.job_title))])
const lastRun = computed(() => all.value.length ? all.value[0].created_at : null)

const filtered = computed(() => {
  let arr = all.value.slice()
  const q = search.value.trim().toLowerCase()
  if (q) arr = arr.filter((r) => r.resume_name.toLowerCase().includes(q) || r.job_title.toLowerCase().includes(q))
  if (levelFilter.value) arr = arr.filter((r) => r.level === levelFilter.value)
  return arr
})

const totalPages = computed(() => Math.max(1, Math.ceil(filtered.value.length / size.value)))
const pageItems = computed(() => filtered.value.slice((page.value - 1) * size.value, page.value * size.value))
const pageRange = computed(() => (filtered.value.length ? [(page.value - 1) * size.value + 1, Math.min(page.value * size.value, filtered.value.length)] : [0, 0]))

watch(totalPages, (n) => {
  if (page.value > n) page.value = n
})

const showDetail = async (row) => {
  const res = await api.get('/records/' + row.id)
  detail.value = res.data
  detailVisible.value = true
}

const replay = (row) => {
  if (!row || !row.resume_id || !row.job_id) return ElMessage.info('关联数据已失效，请重新选择')
  router.push({ path: '/match', query: { resume_id: row.resume_id, job_id: row.job_id } })
}

const remove = (row) => {
  ElMessageBox.confirm('确定删除记录 #' + row.id + ' 吗？', '提示', { type: 'warning' })
    .then(async () => {
      await api.delete('/records/' + row.id)
      ElMessage.success('已删除')
      load()
    })
    .catch(() => {})
}

const clearAll = () => {
  ElMessageBox.confirm(`确定清空全部 ${all.value.length} 条历史记录吗？此操作不可撤销。`, '警告', {
    type: 'warning',
    confirmButtonText: '清空',
    confirmButtonClass: 'el-button--danger'
  })
    .then(async () => {
      for (const r of all.value) {
        await api.delete('/records/' + r.id)
      }
      ElMessage.success('已清空历史记录')
      load()
    })
    .catch(() => {})
}

const exportCsv = () => {
  const rows = [['ID', '简历名称', '岗位名称', '综合分', '等级', '创建时间']]
  filtered.value.forEach((r) => rows.push([r.id, r.resume_name, r.job_title, r.score, r.level, formatTime(r.created_at)]))
  const csv = '\ufeff' + rows.map((r) => r.map((c) => `"${String(c).replace(/"/g, '""')}"`).join(',')).join('\n')
  const url = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }))
  const a = document.createElement('a')
  a.href = url
  a.download = 'match-history.csv'
  a.click()
  URL.revokeObjectURL(url)
  ElMessage.success('已导出历史报告')
}

onMounted(load)
</script>
