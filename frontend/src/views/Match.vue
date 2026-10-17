<template>
  <div>
    <el-card shadow="never">
      <template #header><b>智能匹配</b></template>
      <el-form inline>
        <el-form-item label="选择简历">
          <el-select v-model="resumeId" placeholder="请选择简历" style="width: 280px" filterable clearable>
            <el-option v-for="r in resumes" :key="r.id" :label="r.name" :value="r.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="选择岗位">
          <el-select v-model="jobId" placeholder="请选择岗位" style="width: 280px" filterable clearable>
            <el-option v-for="j in jobs" :key="j.id" :label="j.title + '（' + j.company + '）'" :value="j.id" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="matching" @click="doMatch">开始匹配</el-button>
          <el-button :loading="batching" @click="doBatch">批量匹配全部岗位</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 单岗位匹配结果 -->
    <el-card v-if="result" shadow="never" style="margin-top: 16px">
      <template #header>
        <b>匹配结果：{{ result.resume_name }} × {{ result.job_title }}</b>
      </template>
      <div class="score-line">
        <span class="score-num" :style="{ color: levelColor(result.level) }">{{ result.score }}</span>
        <span class="score-unit">分</span>
        <el-tag :type="levelType(result.level)" size="large" style="margin-left: 12px">{{ result.level }}</el-tag>
      </div>

      <el-row :gutter="16" style="margin-top: 12px">
        <el-col :span="6" v-for="item in subScores" :key="item.label">
          <div class="sub-score">
            <div class="sub-score-label">{{ item.label }}</div>
            <el-progress type="dashboard" :percentage="Math.round(item.value * 100)" :color="scoreColors" :width="110" />
          </div>
        </el-col>
      </el-row>

      <el-descriptions :column="1" border style="margin-top: 16px">
        <el-descriptions-item label="已匹配技能">
          <template v-if="result.matched_skills.length">
            <el-tag v-for="s in result.matched_skills" :key="s" type="success" size="small" style="margin: 2px 6px 2px 0">{{ s }}</el-tag>
          </template>
          <span v-else class="muted">无</span>
        </el-descriptions-item>
        <el-descriptions-item label="缺失技能">
          <template v-if="result.missing_skills.length">
            <el-tag v-for="s in result.missing_skills" :key="s" type="danger" size="small" style="margin: 2px 6px 2px 0">{{ s }}</el-tag>
          </template>
          <span v-else class="muted">无</span>
        </el-descriptions-item>
        <el-descriptions-item label="改进建议">{{ result.suggestion }}</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- 批量匹配结果 -->
    <el-card v-if="batchResults.length" shadow="never" style="margin-top: 16px">
      <template #header><b>批量匹配结果（按综合分降序，共 {{ batchResults.length }} 个岗位）</b></template>
      <el-table :data="batchResults" stripe>
        <el-table-column type="expand">
          <template #default="{ row }">
            <div style="padding: 8px 24px">
              <p><b>已匹配：</b>{{ row.matched_skills.join('、') || '无' }}</p>
              <p style="margin-top: 4px"><b>缺失：</b>{{ row.missing_skills.join('、') || '无' }}</p>
              <p style="margin-top: 4px"><b>建议：</b>{{ row.suggestion }}</p>
            </div>
          </template>
        </el-table-column>
        <el-table-column type="index" label="#" width="60" />
        <el-table-column prop="job_title" label="岗位" min-width="140" />
        <el-table-column prop="company" label="公司" min-width="120" />
        <el-table-column label="综合分" width="200">
          <template #default="{ row }">
            <el-progress :percentage="row.score" :color="levelColor(row.level)" :stroke-width="14" :text-inside="true" />
          </template>
        </el-table-column>
        <el-table-column label="等级" width="110">
          <template #default="{ row }">
            <el-tag :type="levelType(row.level)">{{ row.level }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="缺失技能数" width="110">
          <template #default="{ row }">{{ row.missing_skills.length }}</template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '../api'

const resumes = ref([])
const jobs = ref([])
const resumeId = ref(null)
const jobId = ref(null)
const result = ref(null)
const batchResults = ref([])
const matching = ref(false)
const batching = ref(false)

const subScores = computed(() => {
  if (!result.value) return []
  return [
    { label: '技能覆盖率', value: result.value.skill_score },
    { label: '文本相似度', value: result.value.text_score },
    { label: '学历匹配', value: result.value.edu_score },
    { label: '年限匹配', value: result.value.years_score }
  ]
})

const levelType = (level) => {
  if (level === '高度匹配') return 'success'
  if (level === '较匹配') return 'primary'
  if (level === '一般') return 'warning'
  return 'danger'
}

const levelColor = (level) => {
  if (level === '高度匹配') return '#67c23a'
  if (level === '较匹配') return '#409eff'
  if (level === '一般') return '#e6a23c'
  return '#f56c6c'
}

const scoreColors = [
  { color: '#f56c6c', percentage: 50 },
  { color: '#e6a23c', percentage: 65 },
  { color: '#409eff', percentage: 80 },
  { color: '#67c23a', percentage: 100 }
]

const load = async () => {
  const [r1, r2] = await Promise.all([api.get('/resumes', { params: { page: 1, size: 100 } }), api.get('/jobs', { params: { page: 1, size: 100 } })])
  resumes.value = r1.data.items
  jobs.value = r2.data.items
}

const doMatch = async () => {
  if (!resumeId.value) return ElMessage.warning('请选择简历')
  if (!jobId.value) return ElMessage.warning('请选择岗位')
  matching.value = true
  batchResults.value = []
  try {
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

onMounted(load)
</script>

<style scoped>
.score-line {
  display: flex;
  align-items: baseline;
}

.score-num {
  font-size: 48px;
  font-weight: 700;
}

.score-unit {
  font-size: 16px;
  margin-left: 4px;
  color: #606266;
}

.sub-score {
  text-align: center;
}

.sub-score-label {
  margin-bottom: 8px;
  color: #606266;
}

.muted {
  color: #909399;
}
</style>
