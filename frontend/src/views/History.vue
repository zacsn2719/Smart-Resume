<template>
  <div>
    <el-card shadow="never">
      <template #header><b>匹配历史记录（共 {{ total }} 条，按时间倒序）</b></template>
      <el-table :data="list" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="resume_name" label="简历名称" min-width="150" show-overflow-tooltip />
        <el-table-column prop="job_title" label="岗位名称" min-width="140" show-overflow-tooltip />
        <el-table-column label="综合分" width="180">
          <template #default="{ row }">
            <el-progress :percentage="row.score" :color="levelColor(row.level)" :stroke-width="14" :text-inside="true" />
          </template>
        </el-table-column>
        <el-table-column label="等级" width="110">
          <template #default="{ row }">
            <el-tag :type="levelType(row.level)">{{ row.level }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" width="160">
          <template #default="{ row }">{{ formatTime(row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="125" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="showDetail(row)">详情</el-button>
            <el-button link type="danger" @click="remove(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        style="margin-top: 12px; justify-content: flex-end"
        layout="total, prev, pager, next"
        :total="total"
        :page-size="query.size"
        :current-page="query.page"
        @current-change="onPageChange"
      />
    </el-card>

    <el-dialog v-model="detailVisible" title="匹配记录详情" width="680px">
      <template v-if="detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="简历">{{ detail.resume_name }}</el-descriptions-item>
          <el-descriptions-item label="岗位">{{ detail.job_title }}</el-descriptions-item>
          <el-descriptions-item label="综合分">
            <span class="detail-score" :style="{ color: levelColor(detail.level) }">{{ detail.score }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="等级">
            <el-tag :type="levelType(detail.level)">{{ detail.level }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="技能覆盖率">{{ (detail.skill_score * 100).toFixed(1) }}%</el-descriptions-item>
          <el-descriptions-item label="文本相似度">{{ (detail.text_score * 100).toFixed(1) }}%</el-descriptions-item>
          <el-descriptions-item label="学历匹配">{{ (detail.edu_score * 100).toFixed(0) }}%</el-descriptions-item>
          <el-descriptions-item label="年限匹配">{{ (detail.years_score * 100).toFixed(0) }}%</el-descriptions-item>
          <el-descriptions-item label="已匹配技能" :span="2">
            <template v-if="detail.matched_skills.length">
              <el-tag v-for="s in detail.matched_skills" :key="s" type="success" size="small" style="margin: 2px 6px 2px 0">{{ s }}</el-tag>
            </template>
            <span v-else class="muted">无</span>
          </el-descriptions-item>
          <el-descriptions-item label="缺失技能" :span="2">
            <template v-if="detail.missing_skills.length">
              <el-tag v-for="s in detail.missing_skills" :key="s" type="danger" size="small" style="margin: 2px 6px 2px 0">{{ s }}</el-tag>
            </template>
            <span v-else class="muted">无</span>
          </el-descriptions-item>
          <el-descriptions-item label="改进建议" :span="2">{{ detail.suggestion }}</el-descriptions-item>
          <el-descriptions-item label="创建时间" :span="2">{{ formatTime(detail.created_at) }}</el-descriptions-item>
        </el-descriptions>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '../api'

const list = ref([])
const total = ref(0)
const loading = ref(false)
const query = reactive({ page: 1, size: 10 })
const detail = ref(null)
const detailVisible = ref(false)

const formatTime = (t) => (t ? String(t).slice(0, 19).replace('T', ' ') : '')

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

const load = async () => {
  loading.value = true
  try {
    const res = await api.get('/records', { params: { page: query.page, size: query.size } })
    list.value = res.data.items
    total.value = res.data.total
  } finally {
    loading.value = false
  }
}

const showDetail = async (row) => {
  const res = await api.get('/records/' + row.id)
  detail.value = res.data
  detailVisible.value = true
}

const remove = (row) => {
  ElMessageBox.confirm('确定删除记录 #' + row.id + ' 吗？', '提示', { type: 'warning' })
    .then(async () => {
      await api.delete('/records/' + row.id)
      ElMessage.success('已删除')
      if (list.value.length === 1 && query.page > 1) query.page -= 1
      load()
    })
    .catch(() => {})
}

const onPageChange = (p) => {
  query.page = p
  load()
}

onMounted(load)
</script>

<style scoped>
.detail-score {
  font-size: 20px;
  font-weight: 700;
}

.muted {
  color: #909399;
}
</style>
