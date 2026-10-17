<template>
  <div class="page-inner">
    <!-- KPI 指标带 -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-top">
          <div class="kpi-top-left">
            <div class="kpi-icon primary"><span class="material-symbols-outlined">description</span></div>
            <span class="kpi-label">总简历库储备</span>
          </div>
          <span class="pill tertiary"><span class="material-symbols-outlined" style="font-size:14px">trending_up</span>+12%</span>
        </div>
        <div class="kpi-value-row">
          <span class="kpi-value">{{ allResumes.length }}</span>
          <span class="kpi-unit">份</span>
        </div>
        <div class="kpi-foot">
          <span class="row-gap-xs"><span class="status-dot"></span>本月新增 {{ monthlyAdded }} 份</span>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-top">
          <div class="kpi-top-left">
            <div class="kpi-icon primary"><span class="material-symbols-outlined">schedule</span></div>
            <span class="kpi-label">今日新增录入</span>
          </div>
          <span class="pill error">{{ todayAdded }} 份今日</span>
        </div>
        <div class="kpi-value-row">
          <span class="kpi-value">{{ todayAdded }}</span>
          <span class="kpi-unit">份</span>
        </div>
        <div class="kpi-foot"><span>已自动解析全部技能标签</span></div>
      </div>

      <div class="kpi-card">
        <div class="kpi-top">
          <div class="kpi-top-left">
            <div class="kpi-icon secondary"><span class="material-symbols-outlined">psychology</span></div>
            <span class="kpi-label">人均提炼技能</span>
          </div>
          <span class="pill neutral">NLP 提取</span>
        </div>
        <div class="kpi-value-row">
          <span class="kpi-value">{{ avgSkills }}</span>
          <span class="kpi-unit">个/份</span>
        </div>
        <div class="kpi-foot"><span>TF-IDF 语义加权提取</span></div>
      </div>

      <div class="kpi-card">
        <div class="kpi-top">
          <div class="kpi-top-left">
            <div class="kpi-icon tertiary"><span class="material-symbols-outlined">verified</span></div>
            <span class="kpi-label">覆盖技能词库</span>
          </div>
          <span class="pill tertiary">自动图谱</span>
        </div>
        <div class="kpi-value-row">
          <span class="kpi-value">{{ uniqueSkills }}</span>
          <span class="kpi-unit">项核心标签</span>
        </div>
        <div class="progress-track tertiary mt-md"><span :style="{ width: skillCoverage + '%' }"></span></div>
      </div>
    </div>

    <!-- 主双栏：录入工作台 + 简历库列表 -->
    <div class="grid-2col items-start">
      <!-- 左：录入与智能解析 -->
      <section class="card" style="display:flex;flex-direction:column;gap:0.75rem">
        <div class="row-between">
          <div class="row-gap-sm">
            <span class="dot" style="background:var(--primary-container)"></span>
            <h2 class="t-title-sm">录入与智能解析</h2>
          </div>
          <div class="row-gap-xs" style="color:var(--secondary)">
            <span class="material-symbols-outlined" style="font-size:16px;color:var(--tertiary)">bolt</span>
            <span class="t-caption">jieba + TF-IDF 算法加速</span>
          </div>
        </div>

        <div class="field">
          <label class="field-label row-between">
            <span>简历名称 / 候选人 <span style="color:var(--error)">*</span></span>
            <span class="field-hint" style="font-weight:400">标准格式：姓名-岗位</span>
          </label>
          <div style="position:relative">
            <span class="material-symbols-outlined" style="position:absolute;left:0.75rem;top:0.6rem;color:var(--secondary);font-size:18px">badge</span>
            <input v-model="form.name" class="input" style="padding-left:2.25rem" maxlength="100" placeholder="例如: 张三 - 资深数据分析师" type="text" />
          </div>
        </div>

        <div class="field">
          <div class="row-between">
            <label class="field-label">本地简历附件上传</label>
            <div class="row-gap-xs">
              <span class="chip" style="font-size:10px">DOCX</span>
              <span class="chip" style="font-size:10px">PDF</span>
              <span class="chip" style="font-size:10px">TXT</span>
            </div>
          </div>
          <div
            class="dropzone"
            :class="{ dragover: dragging }"
            @click="fileInput.click()"
            @dragover.prevent="dragging = true"
            @dragleave.prevent="dragging = false"
            @drop.prevent="onDrop"
          >
            <input ref="fileInput" type="file" accept=".doc,.docx,.pdf,.txt" style="display:none" @change="onPick" />
            <span class="material-symbols-outlined">{{ uploading ? 'sync' : 'cloud_upload' }}</span>
            <p class="dropzone-text">{{ uploading ? '正在解析文件…' : '点击此处选择文件，或直接拖拽进区域' }}</p>
            <p class="dropzone-hint">支持 Word / PDF / TXT，最大 2MB 自动结构化处理</p>
          </div>
        </div>

        <div class="field">
          <div class="row-between">
            <label class="field-label">简历原文直接粘贴</label>
            <span class="field-hint">{{ form.text.length }} / 5000 字</span>
          </div>
          <textarea v-model="form.text" class="textarea" rows="6" maxlength="5000" placeholder="请粘贴候选人简历文本（包含教育背景、工作经历、项目技能等，系统将自动抽取关键特征）..."></textarea>
        </div>

        <!-- 即时预检技能标签 -->
        <div class="tips" style="display:block">
          <div class="row-between" style="margin-bottom:0.375rem">
            <span class="t-caption" style="text-transform:uppercase;letter-spacing:0.06em;display:flex;align-items:center;gap:0.25rem">
              <span class="material-symbols-outlined" style="font-size:14px;color:var(--primary-container)">auto_awesome</span>
              即时预检技能标签
            </span>
            <span class="t-caption" style="color:var(--tertiary)">已命中 {{ skillHints.length }} 个特征词</span>
          </div>
          <div class="chip-row" style="padding-top:0.25rem">
            <span v-for="s in skillHints" :key="s" class="chip" style="background:var(--surface-container-lowest);font-weight:500">{{ s }}</span>
            <span v-if="!skillHints.length" class="t-caption" style="color:var(--secondary);font-style:italic">输入简历原文后将自动预检技能标签</span>
          </div>
        </div>

        <div class="row-gap-sm" style="padding-top:0.25rem">
          <button class="btn btn-primary grow" style="height:2.5rem;justify-content:center" :disabled="submitting" @click="submit">
            <span class="material-symbols-outlined">{{ submitting ? 'sync' : 'psychology' }}</span>
            <span>解析并存入简历库</span>
          </button>
          <button class="btn btn-surface" style="height:2.5rem" @click="resetForm">
            <span class="material-symbols-outlined">refresh</span><span>清空重填</span>
          </button>
        </div>
      </section>

      <!-- 右：简历库档案列表 -->
      <section class="card" style="display:flex;flex-direction:column;gap:0.75rem">
        <div class="row-between wrap" style="padding-bottom:0.25rem">
          <div class="row-gap-sm">
            <span class="dot" style="background:var(--tertiary-container)"></span>
            <h2 class="t-title-sm">简历库档案列表</h2>
            <span class="pill neutral">共 {{ filtered.length }} 份</span>
          </div>
          <div class="row-gap-xs">
            <button class="btn btn-surface btn-sm" @click="exportCsv">
              <span class="material-symbols-outlined">file_download</span>导出Excel
            </button>
            <button class="btn btn-sm" style="background:var(--primary-fixed);color:var(--on-primary-fixed)" @click="$router.push('/match')">
              <span class="material-symbols-outlined">hub</span>一键批量匹配
            </button>
          </div>
        </div>

        <!-- 搜索与筛选 -->
        <div class="row-gap-xs wrap" style="background:rgba(239,244,255,0.6);padding:0.375rem;border-radius:0.75rem">
          <div style="position:relative;flex:1;min-width:11rem">
            <span class="material-symbols-outlined" style="position:absolute;left:0.625rem;top:0.5rem;color:var(--secondary);font-size:18px">search</span>
            <input v-model="search" class="input" style="height:2rem;padding:0 0.75rem 0 2rem;font-size:12px;background:var(--surface-container-lowest)" placeholder="搜索候选人姓名、技术栈或学历..." />
          </div>
          <select v-model="degreeFilter" class="select" style="height:2rem;width:auto;font-size:12px;background:var(--surface-container-lowest)">
            <option value="">学历：全部</option>
            <option value="博士">博士</option>
            <option value="硕士">硕士</option>
            <option value="本科">本科</option>
            <option value="大专">大专</option>
          </select>
          <select v-model="expFilter" class="select" style="height:2rem;width:auto;font-size:12px;background:var(--surface-container-lowest)">
            <option value="">经验：全部</option>
            <option value="fresh">应届生 / 1年内</option>
            <option value="1-3">1-3 年</option>
            <option value="3-5">3-5 年</option>
            <option value="5+">5 年以上</option>
          </select>
          <select v-model="sort" class="select" style="height:2rem;width:auto;font-size:12px;background:var(--surface-container-lowest)">
            <option value="new">最新录入优先</option>
            <option value="years">工龄从高到低</option>
            <option value="skills">技能数从多到少</option>
          </select>
        </div>

        <div class="table-wrap" style="border-radius:0.5rem">
          <table class="data-table">
            <thead>
              <tr>
                <th>候选人 / 简历名</th>
                <th>学历</th>
                <th>年限</th>
                <th>核心提取技能 (TF-IDF)</th>
                <th>录入时间</th>
                <th style="text-align:right">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in pageItems" :key="row.id">
                <td>
                  <div class="row-gap-sm">
                    <div class="avatar-square" style="border-radius:9999px;background:rgba(249,115,22,0.15);color:var(--primary-container)">{{ (row.name || '·').slice(0, 1) }}</div>
                    <div class="stack" style="min-width:0">
                      <span class="cell-strong" style="font-size:15px">{{ row.name }}</span>
                      <span class="t-caption c-secondary">{{ row.skills.slice(0, 2).join(' · ') || '未识别技能' }}</span>
                    </div>
                  </div>
                </td>
                <td><span class="chip">{{ row.education || '未知' }}</span></td>
                <td class="cell-strong">{{ row.years || 0 }} 年</td>
                <td style="max-width:14rem">
                  <div class="chip-row">
                    <span v-for="s in row.skills.slice(0, 3)" :key="s" class="chip" style="background:var(--surface-container)">{{ s }}</span>
                    <span v-if="row.skills.length > 3" class="chip primary">+{{ row.skills.length - 3 }}</span>
                    <span v-if="!row.skills.length" class="t-caption c-secondary">-</span>
                  </div>
                </td>
                <td class="t-caption c-secondary">{{ formatTime(row.created_at) }}</td>
                <td style="text-align:right;white-space:nowrap">
                  <div class="row-gap-xs" style="justify-content:flex-end">
                    <button class="btn btn-ghost btn-sm" style="color:var(--primary-container)" @click="goMatch(row)">匹配</button>
                    <button class="btn btn-ghost btn-sm" @click="showDetail(row)">详情</button>
                    <button class="icon-btn" style="color:var(--secondary)" @click="remove(row)"><span class="material-symbols-outlined" style="font-size:16px">delete</span></button>
                  </div>
                </td>
              </tr>
              <tr v-if="!pageItems.length">
                <td colspan="6">
                  <div class="empty">
                    <span class="material-symbols-outlined">inbox</span>
                    <div class="empty-title">暂无简历数据</div>
                    <div class="empty-sub">请在左侧录入简历文本，或上传简历附件</div>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="pagination" style="border-top:none;padding-top:0">
          <span>显示第 {{ pageRange[0] }} 至 {{ pageRange[1] }} 项，共 {{ filtered.length }} 项记录</span>
          <div class="pagination-btns">
            <button class="page-num" :disabled="page <= 1" @click="page--"><span class="material-symbols-outlined" style="font-size:16px">chevron_left</span></button>
            <button v-for="p in totalPages" :key="p" class="page-num" :class="{ active: p === page }" @click="page = p">{{ p }}</button>
            <button class="page-num" :disabled="page >= totalPages" @click="page++"><span class="material-symbols-outlined" style="font-size:16px">chevron_right</span></button>
          </div>
        </div>
      </section>
    </div>

    <!-- 详情弹窗 -->
    <div v-if="detailVisible" class="modal-mask" @click.self="detailVisible = false">
      <div class="modal wide">
        <div class="modal-head">
          <span class="modal-title">简历详情 · {{ detail && detail.name }}</span>
          <button class="icon-btn" @click="detailVisible = false"><span class="material-symbols-outlined">close</span></button>
        </div>
        <div class="modal-body" v-if="detail">
          <div class="row-gap-sm wrap" style="margin-bottom:0.75rem">
            <span class="chip">学历：{{ detail.education || '未知' }}</span>
            <span class="chip">年限：{{ detail.years || 0 }} 年</span>
            <span class="chip">{{ formatTime(detail.created_at) }}</span>
          </div>
          <div style="margin-bottom:0.75rem">
            <div class="field-label" style="margin-bottom:0.375rem">技能标签</div>
            <div class="chip-row">
              <span v-for="s in detail.skills" :key="s" class="chip primary">{{ s }}</span>
              <span v-if="!detail.skills.length" class="t-caption c-secondary">未识别到技能</span>
            </div>
          </div>
          <div class="field-label" style="margin-bottom:0.375rem">简历原文</div>
          <textarea class="textarea" style="min-height:16rem" readonly :value="detail.text"></textarea>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '../api'
import { formatTime, extractSkillHints } from '../utils/format'

const router = useRouter()

const form = reactive({ name: '', text: '' })
const allResumes = ref([])
const loading = ref(false)
const submitting = ref(false)
const uploading = ref(false)
const dragging = ref(false)
const fileInput = ref(null)

const search = ref('')
const degreeFilter = ref('')
const expFilter = ref('')
const sort = ref('new')
const page = ref(1)
const size = 5

const detail = ref(null)
const detailVisible = ref(false)

const skillHints = computed(() => extractSkillHints(form.text).slice(0, 8))

const monthlyAdded = computed(() => {
  const now = new Date()
  const ym = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
  return allResumes.value.filter((r) => formatTime(r.created_at).startsWith(ym)).length
})
const todayAdded = computed(() => {
  const today = formatTime(new Date().toISOString()).slice(0, 10)
  return allResumes.value.filter((r) => formatTime(r.created_at).startsWith(today)).length
})
const avgSkills = computed(() => {
  if (!allResumes.value.length) return '0'
  const total = allResumes.value.reduce((acc, r) => acc + r.skills.length, 0)
  return (total / allResumes.value.length).toFixed(1)
})
const uniqueSkills = computed(() => {
  const set = new Set()
  allResumes.value.forEach((r) => r.skills.forEach((s) => set.add(s)))
  return set.size
})
const skillCoverage = computed(() => Math.min(100, uniqueSkills.value * 2))

const filtered = computed(() => {
  let arr = allResumes.value.slice()
  const q = search.value.trim().toLowerCase()
  if (q) {
    arr = arr.filter(
      (r) => r.name.toLowerCase().includes(q) || r.skills.some((s) => s.toLowerCase().includes(q)) || (r.education || '').includes(q)
    )
  }
  if (degreeFilter.value) arr = arr.filter((r) => (r.education || '').includes(degreeFilter.value))
  if (expFilter.value) {
    const y = (r) => Number(r.years) || 0
    if (expFilter.value === 'fresh') arr = arr.filter((r) => y(r) <= 1)
    else if (expFilter.value === '1-3') arr = arr.filter((r) => y(r) > 1 && y(r) <= 3)
    else if (expFilter.value === '3-5') arr = arr.filter((r) => y(r) > 3 && y(r) <= 5)
    else if (expFilter.value === '5+') arr = arr.filter((r) => y(r) > 5)
  }
  if (sort.value === 'years') arr.sort((a, b) => (Number(b.years) || 0) - (Number(a.years) || 0))
  else if (sort.value === 'skills') arr.sort((a, b) => b.skills.length - a.skills.length)
  else arr.sort((a, b) => b.id - a.id)
  return arr
})

const totalPages = computed(() => Math.max(1, Math.ceil(filtered.value.length / size)))
const pageItems = computed(() => filtered.value.slice((page.value - 1) * size, page.value * size))
const pageRange = computed(() => {
  if (!filtered.value.length) return [0, 0]
  return [(page.value - 1) * size + 1, Math.min(page.value * size, filtered.value.length)]
})

const load = async () => {
  loading.value = true
  try {
    const res = await api.get('/resumes', { params: { page: 1, size: 100 } })
    allResumes.value = res.data.items
  } finally {
    loading.value = false
  }
}

const getExt = (name) => {
  const i = String(name || '').lastIndexOf('.')
  return i === -1 ? '' : name.slice(i).toLowerCase()
}

const handleFile = async (file) => {
  if (!file) return
  const ext = getExt(file.name)
  if (!['.doc', '.docx', '.pdf', '.txt'].includes(ext)) {
    return ElMessage.warning('不支持的文件类型，仅允许 .doc / .docx / .pdf / .txt')
  }
  if (file.size > 2 * 1024 * 1024) return ElMessage.warning('文件大小超过 2MB 限制，请压缩后重新上传')
  if (ext === '.txt') {
    const reader = new FileReader()
    reader.onload = (e) => {
      form.text = String(e.target.result || '').trim()
      if (!form.name) form.name = file.name.replace(/\.txt$/i, '')
      ElMessage.success('文件读取成功，请点击「解析并存入简历库」')
    }
    reader.readAsText(file, 'utf-8')
    return
  }
  uploading.value = true
  const fd = new FormData()
  fd.append('file', file)
  try {
    const res = await api.post('/resumes/upload', fd)
    form.text = res.data.text
    if (!form.name) form.name = file.name.replace(/\.(docx?|pdf)$/i, '')
    ElMessage.success('文件解析成功，请确认内容后保存')
  } finally {
    uploading.value = false
  }
}

const onPick = (e) => {
  handleFile(e.target.files[0])
  e.target.value = ''
}
const onDrop = (e) => {
  dragging.value = false
  handleFile(e.dataTransfer.files[0])
}

const submit = async () => {
  if (!form.name.trim()) return ElMessage.warning('请填写简历名称')
  if (form.text.trim().length < 10) return ElMessage.warning('简历原文不能少于 10 字')
  submitting.value = true
  try {
    await api.post('/resumes', { name: form.name.trim(), text: form.text.trim() })
    ElMessage.success('解析并保存成功')
    resetForm()
    page.value = 1
    load()
  } finally {
    submitting.value = false
  }
}

const resetForm = () => {
  form.name = ''
  form.text = ''
}

const showDetail = async (row) => {
  const res = await api.get('/resumes/' + row.id)
  detail.value = res.data
  detailVisible.value = true
}

const remove = (row) => {
  ElMessageBox.confirm('确定删除简历「' + row.name + '」吗？', '提示', { type: 'warning' })
    .then(async () => {
      await api.delete('/resumes/' + row.id)
      ElMessage.success('已删除')
      load()
    })
    .catch(() => {})
}

const goMatch = (row) => router.push({ path: '/match', query: { resume_id: row.id } })

const exportCsv = () => {
  const rows = [['ID', '名称', '学历', '年限', '技能', '录入时间']]
  filtered.value.forEach((r) => rows.push([r.id, r.name, r.education || '', r.years || 0, r.skills.join(' / '), formatTime(r.created_at)]))
  const csv = '\ufeff' + rows.map((r) => r.map((c) => `"${String(c).replace(/"/g, '""')}"`).join(',')).join('\n')
  const url = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }))
  const a = document.createElement('a')
  a.href = url
  a.download = 'resumes.csv'
  a.click()
  URL.revokeObjectURL(url)
  ElMessage.success('已导出 CSV 文件')
}

onMounted(load)
</script>
