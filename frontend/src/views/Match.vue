<template>
  <div class="page-inner" style="max-width:1520px">
    <!-- 页头 -->
    <div class="page-head">
      <div>
        <div class="row-gap-xs t-caption" style="color:var(--secondary);text-transform:uppercase;letter-spacing:0.06em">
          <span>AI ENGINE</span><span>•</span><span class="t-label-sm" style="color:var(--tertiary)">JIEBA + TF-IDF NLP HYBRID</span>
        </div>
        <div class="row-gap-sm" style="align-items:baseline;margin-top:0.125rem">
          <span class="t-headline-lg">智能匹配与全景画像分析</span>
          <span class="pill neutral">TF-IDF 语义加权</span>
        </div>
      </div>
      <div class="page-head-actions">
        <button class="btn btn-surface" @click="drawer = !drawer">
          <span class="material-symbols-outlined">compare</span><span>双栏对照预览</span>
        </button>
        <button class="btn btn-surface" :disabled="!result" @click="exportReport">
          <span class="material-symbols-outlined">download</span><span>导出完整诊断</span>
        </button>
      </div>
    </div>

    <!-- 选择与配置 -->
    <section class="card">
      <div class="row-between wrap" style="gap:1.25rem">
        <div class="kpi-grid grow" style="grid-template-columns:1fr 1fr">
          <div class="field">
            <label class="field-label row-between" style="color:var(--secondary)">
              <span class="row-gap-xs"><span class="material-symbols-outlined" style="font-size:16px;color:var(--primary-container)">badge</span>候选人简历档案</span>
              <span class="t-caption">已解析 {{ resumes.length }} 份</span>
            </label>
            <select v-model="resumeId" class="select" style="height:2.75rem;font-size:15px;font-weight:600">
              <option :value="null" disabled>请选择简历…</option>
              <option v-for="r in resumes" :key="r.id" :value="r.id">{{ r.name }}（{{ r.education || '未知' }} • {{ r.years || 0 }}年）</option>
            </select>
          </div>
          <div class="field">
            <label class="field-label row-between" style="color:var(--secondary)">
              <span class="row-gap-xs"><span class="material-symbols-outlined" style="font-size:16px;color:var(--primary-container)">domain_verification</span>目标招聘岗位 (JD)</span>
              <span class="t-caption" style="color:var(--tertiary)">在招 {{ jobs.length }} 个</span>
            </label>
            <select v-model="jobId" class="select" style="height:2.75rem;font-size:15px;font-weight:600">
              <option :value="null" disabled>请选择岗位…</option>
              <option v-for="j in jobs" :key="j.id" :value="j.id">{{ j.title }}（{{ j.company || '未知公司' }}）</option>
            </select>
          </div>
        </div>
        <div class="row-gap-sm" style="align-self:flex-end">
          <button class="btn btn-primary" style="height:2.75rem;font-size:15px" :disabled="matching" @click="doMatch">
            <span class="material-symbols-outlined">{{ matching ? 'sync' : 'auto_awesome' }}</span><span>开始AI深度匹配</span>
          </button>
          <button class="btn btn-surface" style="height:2.75rem" :disabled="batching" @click="doBatch">
            <span class="material-symbols-outlined">{{ batching ? 'sync' : 'sync_alt' }}</span><span>批量跑批匹配</span>
          </button>
        </div>
      </div>
    </section>

    <!-- 单条结果 -->
    <template v-if="result">
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-top">
            <div class="kpi-top-left">
              <div class="kpi-icon error"><span class="material-symbols-outlined">analytics</span></div>
              <span class="kpi-label">综合匹配指数</span>
            </div>
            <span class="pill error">{{ result.level }}</span>
          </div>
          <div class="kpi-value-row"><span class="kpi-value" :style="{ color: levelColor(result.level) }">{{ result.score }}</span><span class="kpi-unit">/ 100 分</span></div>
          <div class="kpi-foot"><span>{{ result.resume_name }} × {{ result.job_title }}</span></div>
        </div>

        <div class="kpi-card">
          <div class="kpi-top">
            <div class="kpi-top-left">
              <div class="kpi-icon primary"><span class="material-symbols-outlined">psychology</span></div>
              <span class="kpi-label">技能重合覆盖率</span>
            </div>
            <span class="pill primary">{{ result.matched_skills.length }} / {{ jobSkillsTotal }} 项</span>
          </div>
          <div class="kpi-value-row"><span class="kpi-value">{{ pct(result.skill_score) }}%</span><span class="kpi-unit">关键技术命中</span></div>
          <div class="kpi-foot"><span>缺失 {{ result.missing_skills.length }} 项</span></div>
        </div>

        <div class="kpi-card">
          <div class="kpi-top">
            <div class="kpi-top-left">
              <div class="kpi-icon secondary"><span class="material-symbols-outlined">document_scanner</span></div>
              <span class="kpi-label">文本语义相似度</span>
            </div>
            <span class="pill neutral">TF-IDF 余弦</span>
          </div>
          <div class="kpi-value-row"><span class="kpi-value">{{ pct(result.text_score) }}%</span><span class="kpi-unit">词向量距离</span></div>
          <div class="kpi-foot"><span>分词向量空间重叠度</span></div>
        </div>

        <div class="kpi-card">
          <div class="kpi-top">
            <div class="kpi-top-left">
              <div class="kpi-icon tertiary"><span class="material-symbols-outlined">verified</span></div>
              <span class="kpi-label">门槛硬性达标</span>
            </div>
            <span class="pill tertiary">双项加权</span>
          </div>
          <div class="kpi-value-row"><span class="kpi-value" style="color:var(--tertiary)">{{ pct((result.edu_score + result.years_score) / 2) }}%</span></div>
          <div class="kpi-foot"><span>学历 {{ pct(result.edu_score) }}% · 年限 {{ pct(result.years_score) }}%</span></div>
        </div>
      </div>

      <div class="grid-2col items-start">
        <!-- 左：技能矩阵 + 权重距离 -->
        <div class="stack" style="gap:0.75rem">
          <div class="card" style="display:flex;flex-direction:column;gap:0.75rem">
            <div class="card-head" style="padding-bottom:0.5rem">
              <div class="row-gap-xs">
                <span class="material-symbols-outlined" style="color:var(--primary-container)">fact_check</span>
                <span class="section-title">技能与关键词交叉比对</span>
              </div>
              <span class="t-caption c-secondary">比对基准：岗位技能字典</span>
            </div>

            <div style="padding:0.75rem;border-radius:0.5rem;background:var(--surface-container-low);display:flex;flex-direction:column;gap:0.5rem">
              <div class="row-between">
                <span class="row-gap-sm"><span class="dot" style="width:8px;height:8px;background:var(--tertiary)"></span><span class="t-label-md">已精准匹配技能 ({{ result.matched_skills.length }})</span></span>
                <span class="t-caption" style="color:var(--tertiary)">具备实操经验</span>
              </div>
              <div class="chip-row">
                <span v-for="s in result.matched_skills" :key="s" class="chip tertiary" style="background:var(--surface-container-lowest);display:inline-flex;align-items:center;gap:0.375rem;padding:0.25rem 0.75rem">
                  <span class="material-symbols-outlined" style="font-size:16px">check_circle</span>{{ s }}
                </span>
                <span v-if="!result.matched_skills.length" class="t-caption c-secondary">无匹配技能</span>
              </div>
            </div>

            <div style="padding:0.75rem;border-radius:0.5rem;background:var(--surface-container-low);display:flex;flex-direction:column;gap:0.5rem">
              <div class="row-between">
                <span class="row-gap-sm"><span class="dot" style="width:8px;height:8px;background:var(--error)"></span><span class="t-label-md">岗位刚需但简历未提及 ({{ result.missing_skills.length }})</span></span>
                <span class="t-caption" style="color:var(--error)">阻断性技能缺口</span>
              </div>
              <div class="chip-row">
                <span v-for="s in result.missing_skills" :key="s" class="chip error" style="display:inline-flex;align-items:center;gap:0.25rem;padding:0.25rem 0.625rem">
                  <span class="material-symbols-outlined" style="font-size:15px">cancel</span>{{ s }}
                </span>
                <span v-if="!result.missing_skills.length" class="t-caption" style="color:var(--tertiary)">无技能缺口</span>
              </div>
            </div>

            <div v-if="extraSkills.length" style="padding:0.75rem;border-radius:0.5rem;background:var(--surface-container-low);display:flex;flex-direction:column;gap:0.5rem">
              <div class="row-between">
                <span class="row-gap-sm"><span class="dot" style="width:8px;height:8px;background:var(--secondary)"></span><span class="t-label-md">候选人额外富余能力 (跨领域)</span></span>
                <span class="t-caption c-secondary">可用作加分参考</span>
              </div>
              <div class="chip-row">
                <span v-for="s in extraSkills" :key="s" class="chip" style="background:var(--surface-container-lowest);padding:0.25rem 0.625rem">{{ s }}</span>
              </div>
            </div>
          </div>

          <div class="card" style="display:flex;flex-direction:column;gap:0.75rem">
            <div class="row-between">
              <span class="section-title">各维度得分权重距离</span>
              <span class="t-caption c-secondary">四维加权模型</span>
            </div>
            <div
              v-for="d in subScores"
              :key="d.label"
              style="display:flex;flex-direction:column;gap:0.25rem"
            >
              <div class="row-between t-body-xs">
                <span class="t-label-md">{{ d.label }}（权重 {{ d.weight }}）</span>
                <span class="t-label-md" :style="{ color: levelColor(d.level) }">实测 {{ pct(d.value) }}%</span>
              </div>
              <div class="progress-track"><span :style="{ width: pct(d.value) + '%', background: levelColor(d.level) }"></span></div>
            </div>
          </div>
        </div>

        <!-- 右：AI 综述 + 候选人快照 -->
        <div class="stack" style="gap:0.75rem">
          <div class="card" style="display:flex;flex-direction:column;gap:0.75rem">
            <div class="row-gap-sm" style="padding-bottom:0.25rem">
              <div class="kpi-icon primary" style="width:2.25rem;height:2.25rem"><span class="material-symbols-outlined">smart_toy</span></div>
              <div>
                <span class="t-title-sm">AI 智能匹配综述与改进建议</span>
                <p class="t-caption c-secondary">智配模型基于当前岗位要求自动生成</p>
              </div>
            </div>
            <div style="padding:0.75rem;border-radius:0.75rem;background:var(--surface-container-low);display:flex;flex-direction:column;gap:0.5rem">
              <div class="row-between">
                <span class="pill error" style="display:inline-flex;align-items:center;gap:0.25rem"><span class="material-symbols-outlined" style="font-size:14px">priority_high</span>综合诊断：{{ result.level }}</span>
                <span class="t-caption c-secondary">综合分 {{ result.score }}</span>
              </div>
              <p class="t-body-sm" style="line-height:1.7">{{ result.suggestion }}</p>
            </div>
            <div class="row-gap-sm" style="padding-top:0.25rem">
              <button class="btn btn-primary grow" style="height:2.5rem;justify-content:center" @click="copySuggestion">
                <span class="material-symbols-outlined">outgoing_mail</span><span>复制技能诊断反馈</span>
              </button>
            </div>
          </div>

          <div class="card" style="display:flex;flex-direction:column;gap:0.75rem">
            <div class="row-between">
              <span class="t-label-sm c-secondary" style="text-transform:uppercase;letter-spacing:0.06em">CANDIDATE SNAPSHOT</span>
              <span class="material-symbols-outlined c-secondary" style="font-size:18px">person_search</span>
            </div>
            <div class="row-gap-sm" style="align-items:flex-start">
              <div class="avatar-square" style="border-radius:0.75rem;width:3rem;height:3rem;background:var(--secondary-fixed);color:var(--on-secondary-fixed);font-size:15px">{{ (result.resume_name || '·').slice(0, 1) }}</div>
              <div class="stack" style="min-width:0">
                <span class="t-title-sm">{{ result.resume_name }}</span>
                <span class="t-body-xs c-secondary">{{ resumeDetail ? (resumeDetail.education || '学历未知') : '' }} · {{ resumeDetail ? (resumeDetail.years || 0) : 0 }} 年经验</span>
                <span class="t-caption c-secondary">{{ jobDetail ? jobDetail.title + ' @ ' + (jobDetail.company || '—') : '' }}</span>
              </div>
            </div>
            <div class="kpi-grid" style="grid-template-columns:1fr 1fr;gap:0.5rem">
              <div style="padding:0.5rem;border-radius:0.5rem;background:var(--surface-container-low)">
                <div class="t-caption c-secondary">简历技能数</div>
                <div class="t-label-md">{{ resumeDetail ? resumeDetail.skills.length : 0 }} 项</div>
              </div>
              <div style="padding:0.5rem;border-radius:0.5rem;background:var(--surface-container-low)">
                <div class="t-caption c-secondary">岗位技能数</div>
                <div class="t-label-md">{{ jobSkillsTotal }} 项</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 双栏对照抽屉 -->
      <div v-if="drawer" class="card" style="display:flex;flex-direction:column;gap:0.75rem">
        <div class="row-between">
          <div class="row-gap-xs">
            <span class="material-symbols-outlined" style="color:var(--primary-container)">vertical_split</span>
            <span class="section-title">文本分词原文精准对照</span>
          </div>
          <button class="icon-btn" @click="drawer = false"><span class="material-symbols-outlined">close</span></button>
        </div>
        <div class="grid-halves">
          <div style="display:flex;flex-direction:column;gap:0.5rem;padding:0.75rem;border-radius:0.5rem;background:var(--surface-container-low)">
            <div class="row-between">
              <span class="t-label-md row-gap-xs"><span class="material-symbols-outlined" style="font-size:16px">description</span>简历内容摘录</span>
            </div>
            <div class="t-body-xs" style="line-height:1.7;background:var(--surface-container-lowest);padding:0.75rem;border-radius:0.5rem;height:12rem;overflow-y:auto;white-space:pre-wrap">{{ resumeDetail ? resumeDetail.text : '暂无数据' }}</div>
          </div>
          <div style="display:flex;flex-direction:column;gap:0.5rem;padding:0.75rem;border-radius:0.5rem;background:var(--surface-container-low)">
            <div class="row-between">
              <span class="t-label-md row-gap-xs"><span class="material-symbols-outlined" style="font-size:16px;color:var(--primary-container)">work_outline</span>岗位要求 (JD)</span>
            </div>
            <div class="t-body-xs" style="line-height:1.7;background:var(--surface-container-lowest);padding:0.75rem;border-radius:0.5rem;height:12rem;overflow-y:auto;white-space:pre-wrap">{{ jobDetail ? jobDetail.text : '暂无数据' }}</div>
          </div>
        </div>
      </div>
    </template>

    <!-- 批量结果 -->
    <div v-if="batchResults.length" class="card" style="display:flex;flex-direction:column;gap:0.75rem">
      <div class="row-between">
        <div class="row-gap-sm">
          <span class="section-title">批量匹配结果</span>
          <span class="pill primary">共 {{ batchResults.length }} 个岗位</span>
        </div>
        <span class="t-caption c-secondary">按综合分降序</span>
      </div>
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th style="width:3rem">#</th>
              <th>岗位</th>
              <th>公司</th>
              <th>综合分</th>
              <th>等级</th>
              <th>缺失技能</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, i) in batchResults" :key="row.id">
              <td class="c-secondary">{{ i + 1 }}</td>
              <td class="cell-strong">{{ row.job_title }}</td>
              <td class="c-secondary">{{ row.company || '—' }}</td>
              <td>
                <div class="row-gap-sm">
                  <div class="score-bar"><span :style="{ width: row.score + '%', background: levelColor(row.level) }"></span></div>
                  <span class="t-label-md" :style="{ color: levelColor(row.level) }">{{ row.score }}</span>
                </div>
              </td>
              <td><span :class="levelPill(row.level)">{{ row.level }}</span></td>
              <td>
                <div class="chip-row">
                  <span v-for="s in row.missing_skills.slice(0, 3)" :key="s" class="chip error">{{ s }}</span>
                  <span v-if="!row.missing_skills.length" class="t-caption" style="color:var(--tertiary)">无</span>
                  <span v-if="row.missing_skills.length > 3" class="chip">+{{ row.missing_skills.length - 3 }}</span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 空态 -->
    <div v-if="!result && !batchResults.length" class="card">
      <div class="empty">
        <span class="material-symbols-outlined">insights</span>
        <div class="empty-title">尚未执行匹配诊断</div>
        <div class="empty-sub">请选择简历与目标岗位，点击「开始AI深度匹配」或「批量跑批匹配」</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '../api'
import { levelColor, levelPill } from '../utils/format'

const route = useRoute()

const resumes = ref([])
const jobs = ref([])
const resumeId = ref(null)
const jobId = ref(null)
const result = ref(null)
const batchResults = ref([])
const matching = ref(false)
const batching = ref(false)
const resumeDetail = ref(null)
const jobDetail = ref(null)
const drawer = ref(false)

const pct = (v) => Math.round((Number(v) || 0) * 100)

const jobSkillsTotal = computed(() => {
  if (jobDetail.value) return jobDetail.value.skills.length
  return result.value ? result.value.matched_skills.length + result.value.missing_skills.length : 0
})

const extraSkills = computed(() => {
  if (!resumeDetail.value || !jobDetail.value) return []
  const jobSet = new Set(jobDetail.value.skills.map((s) => s.toLowerCase()))
  return resumeDetail.value.skills.filter((s) => !jobSet.has(s.toLowerCase()))
})

const subScores = computed(() => {
  if (!result.value) return []
  return [
    { label: '技能覆盖率', weight: '40%', value: result.value.skill_score, level: result.value.skill_score >= 0.8 ? '高度匹配' : result.value.skill_score >= 0.6 ? '较匹配' : '不匹配' },
    { label: '文本相似度', weight: '30%', value: result.value.text_score, level: result.value.text_score >= 0.8 ? '高度匹配' : result.value.text_score >= 0.6 ? '较匹配' : '不匹配' },
    { label: '学历匹配', weight: '20%', value: result.value.edu_score, level: result.value.edu_score >= 1 ? '高度匹配' : '一般' },
    { label: '年限匹配', weight: '10%', value: result.value.years_score, level: result.value.years_score >= 1 ? '高度匹配' : result.value.years_score >= 0.7 ? '较匹配' : '一般' }
  ]
})

const load = async () => {
  const [r1, r2] = await Promise.all([
    api.get('/resumes', { params: { page: 1, size: 100 } }),
    api.get('/jobs', { params: { page: 1, size: 100 } })
  ])
  resumes.value = r1.data.items
  jobs.value = r2.data.items
}

const loadContext = async () => {
  if (!resumeId.value || !jobId.value) return
  const [r, j] = await Promise.all([api.get('/resumes/' + resumeId.value), api.get('/jobs/' + jobId.value)])
  resumeDetail.value = r.data
  jobDetail.value = j.data
}

const doMatch = async () => {
  if (!resumeId.value) return ElMessage.warning('请选择简历')
  if (!jobId.value) return ElMessage.warning('请选择岗位')
  matching.value = true
  batchResults.value = []
  try {
    await loadContext()
    const res = await api.post('/match', { resume_id: resumeId.value, job_id: jobId.value })
    result.value = res.data
    ElMessage.success('匹配完成')
  } finally {
    matching.value = false
  }
}

const doBatch = async () => {
  if (!resumeId.value) return ElMessage.warning('请选择简历')
  batching.value = true
  result.value = null
  try {
    const res = await api.post('/match/batch', { resume_id: resumeId.value })
    batchResults.value = res.data.results
    ElMessage.success('批量匹配完成')
  } finally {
    batching.value = false
  }
}

const copySuggestion = async () => {
  if (!result.value) return
  try {
    await navigator.clipboard.writeText(result.value.suggestion)
    ElMessage.success('已复制诊断建议')
  } catch (e) {
    ElMessage.info(result.value.suggestion)
  }
}

const exportReport = () => {
  if (!result.value) return
  const r = result.value
  const lines = [
    `简历：${r.resume_name}`,
    `岗位：${r.job_title}`,
    `综合分：${r.score}（${r.level}）`,
    `技能覆盖率：${pct(r.skill_score)}%  文本相似度：${pct(r.text_score)}%  学历：${pct(r.edu_score)}%  年限：${pct(r.years_score)}%`,
    `已匹配技能：${r.matched_skills.join('、') || '无'}`,
    `缺失技能：${r.missing_skills.join('、') || '无'}`,
    `改进建议：${r.suggestion}`
  ]
  const url = URL.createObjectURL(new Blob(['\ufeff' + lines.join('\n')], { type: 'text/plain;charset=utf-8' }))
  const a = document.createElement('a')
  a.href = url
  a.download = 'match-report.txt'
  a.click()
  URL.revokeObjectURL(url)
  ElMessage.success('已导出诊断报告')
}

onMounted(async () => {
  await load()
  if (route.query.resume_id) resumeId.value = Number(route.query.resume_id)
  if (route.query.job_id) jobId.value = Number(route.query.job_id)
  if (resumeId.value && jobId.value) doMatch()
})
</script>
