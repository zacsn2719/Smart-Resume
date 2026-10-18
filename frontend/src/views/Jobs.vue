<template>
  <div class="page-inner">
    <!-- 页头 -->
    <div class="page-head">
      <div>
        <div class="row-gap-xs t-label-sm" style="color:var(--secondary);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.25rem">
          <span>招聘与组织</span><span style="color:var(--outline-variant)">•</span><span style="color:var(--primary-container);font-weight:700">Talent Engine</span>
        </div>
        <h1 class="t-headline-xl" style="font-weight:700">岗位管理</h1>
        <p class="page-head-sub">精准解析岗位需求，智能聚合并映射核心技术能力标签</p>
      </div>
      <div class="page-head-actions">
        <div class="segmented">
          <button :class="{ active: view === 'table' }" @click="view = 'table'">
            <span class="material-symbols-outlined" style="font-size:18px;vertical-align:middle">view_agenda</span> 表格视图
          </button>
          <button :class="{ active: view === 'board' }" @click="view = 'board'">
            <span class="material-symbols-outlined" style="font-size:18px;vertical-align:middle">grid_view</span> 看板模式
          </button>
        </div>
        <button class="btn btn-surface" @click="exportCsv">
          <span class="material-symbols-outlined">file_download</span><span>批量导出</span>
        </button>
        <button class="btn btn-primary" @click="focusTitle">
          <span class="material-symbols-outlined">add</span><span>发布新岗位</span>
        </button>
      </div>
    </div>

    <!-- KPI -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-top">
          <div class="kpi-top-left">
            <div class="kpi-icon primary"><span class="material-symbols-outlined">badge</span></div>
            <span class="kpi-label">活跃在招岗位</span>
          </div>
          <span class="pill neutral">在招</span>
        </div>
        <div class="kpi-value-row"><span class="kpi-value">{{ allJobs.length }}</span><span class="kpi-unit">个在线职位</span></div>
        <div class="progress-track mt-md"><span style="width:75%"></span></div>
      </div>

      <div class="kpi-card">
        <div class="kpi-top">
          <div class="kpi-top-left">
            <div class="kpi-icon secondary"><span class="material-symbols-outlined">calendar_today</span></div>
            <span class="kpi-label">本周新增需求</span>
          </div>
          <span class="pill secondary">周增</span>
        </div>
        <div class="kpi-value-row"><span class="kpi-value">{{ weekAdded }}</span><span class="kpi-unit">个新发布</span></div>
        <div class="progress-track secondary mt-md"><span style="width:40%"></span></div>
      </div>

      <div class="kpi-card">
        <div class="kpi-top">
          <div class="kpi-top-left">
            <div class="kpi-icon primary"><span class="material-symbols-outlined">category</span></div>
            <span class="kpi-label">覆盖技能点</span>
          </div>
          <span class="pill neutral">自动图谱</span>
        </div>
        <div class="kpi-value-row"><span class="kpi-value">{{ uniqueSkills }}</span><span class="kpi-unit">项知识标签</span></div>
        <div class="progress-track mt-md"><span style="width:83%"></span></div>
      </div>

      <div class="kpi-card">
        <div class="kpi-top">
          <div class="kpi-top-left">
            <div class="kpi-icon tertiary"><span class="material-symbols-outlined">analytics</span></div>
            <span class="kpi-label">平均匹配度</span>
          </div>
          <span class="pill tertiary">综合基线</span>
        </div>
        <div class="kpi-value-row"><span class="kpi-value">{{ avgScore }}%</span><span class="kpi-unit">综合拟合</span></div>
        <div class="progress-track tertiary mt-md"><span :style="{ width: Math.min(100, avgScore) + '%' }"></span></div>
      </div>
    </div>

    <!-- 工作台 -->
    <div class="grid-2col items-start">
      <!-- 左：新增岗位 -->
      <div class="card" style="display:flex;flex-direction:column;gap:0.75rem">
        <div class="row-between" style="padding-bottom:0.5rem">
          <div class="row-gap-sm">
            <div class="kpi-icon primary" style="width:2rem;height:2rem"><span class="material-symbols-outlined">post_add</span></div>
            <div>
              <h2 class="t-title-sm">新增岗位</h2>
              <p class="t-caption c-secondary">粘贴 JD 原文，系统将利用分词算法提取特征</p>
            </div>
          </div>
          <span class="chip">jieba &amp; TF-IDF</span>
        </div>

        <div class="field">
          <label class="field-label row-between"><span>岗位名称 <span style="color:var(--primary-container)">*</span></span><span class="field-hint" style="font-weight:400">例如: Python 后端开发</span></label>
          <div style="position:relative">
            <span class="material-symbols-outlined" style="position:absolute;left:0.75rem;top:0.6rem;color:var(--secondary);font-size:18px">work_outline</span>
            <input ref="titleInput" v-model="form.title" class="input" style="padding-left:2.25rem" maxlength="100" placeholder="如: 高级后端架构师 / Python 工程师" type="text" />
          </div>
        </div>

        <div class="field">
          <label class="field-label">所属公司 / 归属事业部 <span style="color:var(--primary-container)">*</span></label>
          <div style="position:relative">
            <span class="material-symbols-outlined" style="position:absolute;left:0.75rem;top:0.6rem;color:var(--secondary);font-size:18px">domain</span>
            <input v-model="form.company" class="input" style="padding-left:2.25rem" maxlength="100" placeholder="如: 云盾科技 / 基础架构研发中心" type="text" />
          </div>
        </div>

        <div class="form-grid two">
          <div class="field">
            <label class="field-label">学历要求</label>
            <select v-model="form.degree" class="select">
              <option value="本科">本科及以上</option>
              <option value="硕士">硕士及以上</option>
              <option value="大专">大专及以上</option>
              <option value="不限">不限学历</option>
            </select>
          </div>
          <div class="field">
            <label class="field-label">工作经验</label>
            <select v-model="form.exp" class="select">
              <option value="3">3 年以上</option>
              <option value="1">1-2 年</option>
              <option value="5">5 年以上</option>
              <option value="0">应届毕业生 / 实习</option>
            </select>
          </div>
        </div>

        <div class="field">
          <div class="row-between">
            <label class="field-label">JD 原文描述 <span style="color:var(--primary-container)">*</span></label>
            <button class="btn-text" style="font-size:10px" @click="fillSample"><span class="material-symbols-outlined" style="font-size:13px">auto_fix_high</span>填充示例文本</button>
          </div>
          <div style="position:relative">
            <textarea v-model="form.text" class="textarea" rows="7" maxlength="5000" placeholder="请粘贴岗位职责与技能要求（10-5000 字）..."></textarea>
            <span class="t-caption c-secondary" style="position:absolute;right:0.75rem;bottom:0.625rem;background:rgba(239,244,255,0.8);padding:0 0.25rem;border-radius:0.25rem">{{ form.text.length }} / 5000</span>
          </div>
        </div>

        <div class="tips" style="display:block">
          <div class="row-between" style="margin-bottom:0.375rem">
            <span class="t-caption" style="text-transform:uppercase;letter-spacing:0.06em;display:flex;align-items:center;gap:0.25rem">
              <span class="material-symbols-outlined" style="font-size:14px;color:var(--tertiary)">psychology</span>实时技能推断器
            </span>
            <span class="t-caption c-secondary">{{ skillHints.length ? `已命中 ${skillHints.length} 个特征` : '待输入...' }}</span>
          </div>
          <div class="chip-row" style="min-height:1.5rem;align-items:center">
            <span v-for="s in skillHints" :key="s" class="chip primary">{{ s }}</span>
            <span v-if="!skillHints.length" class="t-caption c-secondary" style="font-style:italic">输入职责后将自动萃取技能标尺</span>
          </div>
        </div>

        <div class="row-gap-sm" style="padding-top:0.25rem">
          <button class="btn btn-primary grow" style="height:2.5rem;justify-content:center" :disabled="submitting" @click="submit">
            <span class="material-symbols-outlined">{{ submitting ? 'sync' : 'neurology' }}</span><span>解析并保存</span>
          </button>
          <button class="btn btn-surface" style="height:2.5rem" @click="resetForm">清空</button>
        </div>
      </div>

      <!-- 右：岗位列表 -->
      <div class="card" style="display:flex;flex-direction:column;gap:0.75rem">
        <div class="row-between wrap">
          <div class="row-gap-sm">
            <h2 class="t-headline-md">岗位列表</h2>
            <span class="pill primary">共 {{ filtered.length }} 条</span>
          </div>
          <div class="row-gap-xs wrap">
            <div style="position:relative">
              <span class="material-symbols-outlined" style="position:absolute;left:0.625rem;top:0.5rem;color:var(--secondary);font-size:16px">search</span>
              <input v-model="search" class="input" style="height:2rem;width:14rem;padding:0 0.75rem 0 2rem;font-size:12px" placeholder="搜索岗位、公司或技能..." />
            </div>
            <select v-model="companyFilter" class="select" style="height:2rem;width:auto;font-size:12px">
              <option value="">全部公司</option>
              <option v-for="c in companies" :key="c" :value="c">{{ c }}</option>
            </select>
            <select v-model="sort" class="select" style="height:2rem;width:auto;font-size:12px">
              <option value="date">时间倒序</option>
              <option value="years">经验要求</option>
              <option value="edu">学历要求</option>
            </select>
          </div>
        </div>

        <!-- 表格视图 -->
        <div v-if="view === 'table'" class="table-wrap">
          <table class="data-table">
            <thead>
              <tr>
                <th style="text-align:center;width:3rem">ID</th>
                <th>岗位名称</th>
                <th>所属公司</th>
                <th style="text-align:center">学历</th>
                <th style="text-align:center">年限</th>
                <th>核心技能点 (自动萃取)</th>
                <th>创建时间</th>
                <th style="text-align:right">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in pageItems" :key="row.id">
                <td style="text-align:center" class="t-caption c-secondary">{{ row.id }}</td>
                <td>
                  <div class="row-gap-sm">
                    <span class="dot" style="width:8px;height:8px" :style="{ background: dotColor(row.id) }"></span>
                    <span class="cell-strong">{{ row.title }}</span>
                  </div>
                </td>
                <td>
                  <div class="row-gap-xs c-secondary">
                    <span class="material-symbols-outlined" style="font-size:16px">apartment</span>
                    <span style="max-width:8rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{{ row.company || '—' }}</span>
                  </div>
                </td>
                <td style="text-align:center"><span class="chip">{{ row.education || '不限' }}</span></td>
                <td style="text-align:center" class="t-label-sm c-secondary">{{ row.years || 0 }}年</td>
                <td style="max-width:17rem">
                  <div class="chip-row">
                    <span v-for="s in row.skills.slice(0, 5)" :key="s" class="chip" style="background:var(--surface-container-low)">{{ s }}</span>
                    <span v-if="row.skills.length > 5" class="chip primary">+{{ row.skills.length - 5 }}</span>
                    <span v-if="!row.skills.length" class="t-caption c-secondary">-</span>
                  </div>
                </td>
                <td class="t-caption c-secondary" style="white-space:nowrap">{{ formatTime(row.created_at) }}</td>
                <td style="text-align:right;white-space:nowrap">
                  <div class="row-gap-xs" style="justify-content:flex-end">
                    <button class="icon-btn" style="color:var(--primary)" title="查看详情" @click="showDetail(row)"><span class="material-symbols-outlined" style="font-size:18px">visibility</span></button>
                    <button class="icon-btn" style="color:var(--tertiary)" title="发起匹配" @click="goMatch(row)"><span class="material-symbols-outlined" style="font-size:18px">hub</span></button>
                    <button class="icon-btn" style="color:var(--error)" title="删除" @click="remove(row)"><span class="material-symbols-outlined" style="font-size:18px">delete</span></button>
                  </div>
                </td>
              </tr>
              <tr v-if="!pageItems.length">
                <td colspan="8"><div class="empty"><span class="material-symbols-outlined">work_off</span><div class="empty-title">暂无岗位数据</div><div class="empty-sub">请在左侧新增岗位或填充示例文本</div></div></td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 看板视图 -->
        <div v-else class="kpi-grid" style="grid-template-columns:repeat(2,1fr)">
          <div v-for="row in pageItems" :key="row.id" class="card card-hover" style="background:var(--surface-container-low)">
            <div class="row-between">
              <span class="t-title-sm">{{ row.title }}</span>
              <span class="chip">{{ row.education || '不限' }}</span>
            </div>
            <div class="row-gap-xs c-secondary t-body-xs" style="margin-top:0.25rem">
              <span class="material-symbols-outlined" style="font-size:15px">apartment</span>{{ row.company || '未填写公司' }} · {{ row.years || 0 }}年
            </div>
            <div class="chip-row" style="margin-top:0.625rem">
              <span v-for="s in row.skills.slice(0, 6)" :key="s" class="chip" style="background:var(--surface-container-lowest)">{{ s }}</span>
            </div>
            <div class="row-gap-xs" style="margin-top:0.75rem;justify-content:flex-end">
              <button class="btn btn-ghost btn-sm" @click="showDetail(row)">详情</button>
              <button class="btn btn-ghost btn-sm" style="color:var(--tertiary)" @click="goMatch(row)">匹配</button>
              <button class="icon-btn" style="color:var(--error)" @click="remove(row)"><span class="material-symbols-outlined" style="font-size:16px">delete</span></button>
            </div>
          </div>
        </div>

        <div class="pagination" style="border-top:none;padding-top:0.25rem">
          <span class="row-gap-xs">共 <strong style="color:var(--on-surface)">{{ filtered.length }}</strong> 条记录，当前显示 {{ pageRange[0] }}-{{ pageRange[1] }}</span>
          <div class="pagination-btns">
            <button class="page-num" :disabled="page <= 1" @click="page--"><span class="material-symbols-outlined" style="font-size:16px">chevron_left</span></button>
            <button v-for="p in totalPages" :key="p" class="page-num" :class="{ active: p === page }" @click="page = p">{{ p }}</button>
            <button class="page-num" :disabled="page >= totalPages" @click="page++"><span class="material-symbols-outlined" style="font-size:16px">chevron_right</span></button>
          </div>
        </div>
      </div>
    </div>

    <!-- 详情 -->
    <div v-if="detailVisible" class="modal-mask" @click.self="detailVisible = false">
      <div class="modal wide">
        <div class="modal-head">
          <span class="modal-title">岗位详情 · {{ detail && detail.title }}</span>
          <button class="icon-btn" @click="detailVisible = false"><span class="material-symbols-outlined">close</span></button>
        </div>
        <div class="modal-body" v-if="detail">
          <div class="row-gap-sm wrap" style="margin-bottom:0.75rem">
            <span class="chip">公司：{{ detail.company || '—' }}</span>
            <span class="chip">学历：{{ detail.education || '不限' }}</span>
            <span class="chip">年限：{{ detail.years || 0 }} 年</span>
          </div>
          <div style="margin-bottom:0.75rem">
            <div class="field-label" style="margin-bottom:0.375rem">所需技能</div>
            <div class="chip-row">
              <span v-for="s in detail.skills" :key="s" class="chip primary">{{ s }}</span>
              <span v-if="!detail.skills.length" class="t-caption c-secondary">未识别到技能</span>
            </div>
          </div>
          <div class="field-label" style="margin-bottom:0.375rem">JD 原文</div>
          <textarea class="textarea" style="min-height:16rem" readonly :value="detail.text"></textarea>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '../api'
import { formatTime, extractSkillHints } from '../utils/format'
import { normalizeKeyword } from '../utils/search'

const router = useRouter()
const route = useRoute()

const form = reactive({ title: '', company: '', degree: '本科', exp: '3', text: '' })
const allJobs = ref([])
const submitting = ref(false)
const view = ref('table')
const titleInput = ref(null)
const search = ref('')
const companyFilter = ref('')
const sort = ref('date')
const page = ref(1)
const size = 8
const avgScore = ref(0)
const detail = ref(null)
const detailVisible = ref(false)

const skillHints = computed(() => extractSkillHints(form.text).slice(0, 8))

const companies = computed(() => [...new Set(allJobs.value.map((j) => j.company).filter(Boolean))])
const weekAdded = computed(() => {
  const start = new Date(Date.now() - 6 * 86400000).toISOString().slice(0, 10)
  return allJobs.value.filter((j) => String(j.created_at || '').slice(0, 10) >= start).length
})
const uniqueSkills = computed(() => {
  const set = new Set()
  allJobs.value.forEach((j) => j.skills.forEach((s) => set.add(s)))
  return set.size
})

const filtered = computed(() => {
  let arr = allJobs.value.slice()
  const q = search.value.trim().toLowerCase()
  if (q) arr = arr.filter((j) => j.title.toLowerCase().includes(q) || (j.company || '').toLowerCase().includes(q) || j.skills.some((s) => s.toLowerCase().includes(q)))
  if (companyFilter.value) arr = arr.filter((j) => j.company === companyFilter.value)
  if (sort.value === 'years') arr.sort((a, b) => (Number(b.years) || 0) - (Number(a.years) || 0))
  else if (sort.value === 'edu') arr.sort((a, b) => String(a.education || '').localeCompare(String(b.education || ''), 'zh'))
  else arr.sort((a, b) => b.id - a.id)
  return arr
})

const totalPages = computed(() => Math.max(1, Math.ceil(filtered.value.length / size)))
const pageItems = computed(() => filtered.value.slice((page.value - 1) * size, page.value * size))
const pageRange = computed(() => (filtered.value.length ? [(page.value - 1) * size + 1, Math.min(page.value * size, filtered.value.length)] : [0, 0]))

watch(totalPages, (n) => {
  if (page.value > n) page.value = n
})

const dotColor = (id) => ['var(--primary-container)', 'var(--tertiary-container)', 'var(--secondary)', 'var(--secondary-container)'][id % 4]

const load = async () => {
  const res = await api.get('/jobs', { params: { page: 1, size: 100 } })
  allJobs.value = res.data.items
}
const loadStats = async () => {
  try {
    const res = await api.get('/stats')
    avgScore.value = res.data.avg_score
  } catch (e) {
    avgScore.value = 0
  }
}

const focusTitle = () => titleInput.value && titleInput.value.focus()

const fillSample = () => {
  form.title = '高并发系统研发工程师'
  form.company = '智配核心架构部'
  form.degree = '本科'
  form.exp = '3'
  form.text = `岗位职责：
1. 负责核心云原生分布式微服务系统的架构规划与后端演进；
2. 熟练运用 Python (FastAPI/Django) 或 Go 语言开发高性能业务接口；
3. 深入理解 Docker 容器化技术，具备 Kubernetes (K8s) 环境编排与 CI/CD 落地实战经验；
4. 熟练掌握 Linux 体系运维，精通 Redis、MySQL 等核心存储机制及性能调优。
任职要求：
本科及以上学历，计算机相关专业，具备 3 年以上互联网或企业级 SaaS 研发经历。`
}

// 后端仅接收 title/company/text，学历与经验要求拼接进原文，由抽取算法解析
const composedText = () => `${form.text.trim()}\n学历要求：${form.degree === '不限' ? '不限学历' : form.degree + '及以上'}\n工作经验：${form.exp === '0' ? '应届毕业生或实习' : form.exp + '年以上'}`

const submit = async () => {
  if (!form.title.trim()) return ElMessage.warning('请填写岗位名称')
  if (form.text.trim().length < 10) return ElMessage.warning('JD 原文不能少于 10 字')
  submitting.value = true
  try {
    await api.post('/jobs', { title: form.title.trim(), company: form.company.trim(), text: composedText() })
    ElMessage.success('解析并保存成功')
    resetForm()
    page.value = 1
    load()
  } finally {
    submitting.value = false
  }
}

const resetForm = () => {
  form.title = ''
  form.company = ''
  form.degree = '本科'
  form.exp = '3'
  form.text = ''
}

const showDetail = async (row) => {
  const res = await api.get('/jobs/' + row.id)
  detail.value = res.data
  detailVisible.value = true
}

const remove = (row) => {
  ElMessageBox.confirm('确定删除岗位「' + row.title + '」吗？', '提示', { type: 'warning' })
    .then(async () => {
      await api.delete('/jobs/' + row.id)
      ElMessage.success('已删除')
      load()
    })
    .catch(() => {})
}

const goMatch = (row) => router.push({ path: '/match', query: { job_id: row.id } })

const exportCsv = () => {
  const rows = [['ID', '岗位名称', '公司', '学历', '年限', '技能', '创建时间']]
  filtered.value.forEach((j) => rows.push([j.id, j.title, j.company || '', j.education || '', j.years || 0, j.skills.join(' / '), formatTime(j.created_at)]))
  const csv = '\ufeff' + rows.map((r) => r.map((c) => `"${String(c).replace(/"/g, '""')}"`).join(',')).join('\n')
  const url = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }))
  const a = document.createElement('a')
  a.href = url
  a.download = 'jobs.csv'
  a.click()
  URL.revokeObjectURL(url)
  ElMessage.success('已导出 CSV 文件')
}

// 支持全局搜索结果跳转携带 ?q= 预填页面搜索框
const applyQuerySearch = () => {
  const q = normalizeKeyword(route.query.q)
  if (q) search.value = q
}

onMounted(() => {
  load()
  loadStats()
  applyQuerySearch()
})

watch(
  () => route.query.q,
  () => {
    if (route.path === '/jobs') applyQuerySearch()
  }
)
</script>
