<template>
  <div>
    <el-row :gutter="16">
      <el-col :span="10">
        <el-card shadow="never">
          <template #header><b>新增岗位</b></template>
          <el-form label-width="80px">
            <el-form-item label="岗位名称">
              <el-input v-model="form.title" maxlength="100" placeholder="如：Python 后端开发" />
            </el-form-item>
            <el-form-item label="公司名称">
              <el-input v-model="form.company" maxlength="100" placeholder="选填" />
            </el-form-item>
            <el-form-item label="JD 原文">
              <el-input
                v-model="form.text"
                type="textarea"
                :rows="12"
                maxlength="5000"
                show-word-limit
                placeholder="粘贴岗位描述（10-5000 字）"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="submitting" @click="submit">解析并保存</el-button>
              <el-button @click="resetForm">清空</el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <el-card v-if="lastResult" shadow="never" style="margin-top: 16px">
          <template #header><b>最近一次解析结果</b></template>
          <p><b>学历要求：</b>{{ lastResult.education }}　　<b>年限要求：</b>{{ lastResult.years }} 年</p>
          <p style="margin-top: 8px">
            <b>所需技能：</b>
            <template v-if="lastResult.skills.length">
              <el-tag v-for="s in lastResult.skills" :key="s" size="small" style="margin: 2px 6px 2px 0">{{ s }}</el-tag>
            </template>
            <span v-else class="muted">未识别到技能</span>
          </p>
        </el-card>
      </el-col>

      <el-col :span="14">
        <el-card shadow="never">
          <template #header><b>岗位列表（共 {{ total }} 条）</b></template>
          <el-table :data="list" v-loading="loading" stripe>
            <el-table-column prop="id" label="ID" width="60" />
            <el-table-column prop="title" label="岗位名称" min-width="130" show-overflow-tooltip />
            <el-table-column prop="company" label="公司" min-width="110" show-overflow-tooltip />
            <el-table-column prop="education" label="学历" width="80" />
            <el-table-column prop="years" label="年限" width="70" />
            <el-table-column label="技能" min-width="170">
              <template #default="{ row }">
                <template v-if="row.skills.length">
                  <el-tag v-for="s in row.skills.slice(0, 5)" :key="s" size="small" type="info" style="margin: 2px">{{ s }}</el-tag>
                  <span v-if="row.skills.length > 5" class="muted"> +{{ row.skills.length - 5 }}</span>
                </template>
                <span v-else class="muted">-</span>
              </template>
            </el-table-column>
            <el-table-column label="创建时间" width="155">
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
      </el-col>
    </el-row>

    <el-dialog v-model="detailVisible" :title="'岗位详情 - ' + (detail ? detail.title : '')" width="640px">
      <template v-if="detail">
        <p>
          <b>公司：</b>{{ detail.company }}　　<b>学历要求：</b>{{ detail.education }}　　<b>年限要求：</b>{{ detail.years }} 年
        </p>
        <p style="margin: 8px 0">
          <b>所需技能：</b>
          <template v-if="detail.skills.length">
            <el-tag v-for="s in detail.skills" :key="s" size="small" style="margin: 2px 6px 2px 0">{{ s }}</el-tag>
          </template>
          <span v-else class="muted">未识别到技能</span>
        </p>
        <el-input type="textarea" :model-value="detail.text" :rows="12" readonly />
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '../api'

const form = reactive({ title: '', company: '', text: '' })
const list = ref([])
const total = ref(0)
const loading = ref(false)
const submitting = ref(false)
const query = reactive({ page: 1, size: 10 })
const lastResult = ref(null)
const detail = ref(null)
const detailVisible = ref(false)

const formatTime = (t) => (t ? String(t).slice(0, 19).replace('T', ' ') : '')

const load = async () => {
  loading.value = true
  try {
    const res = await api.get('/jobs', { params: { page: query.page, size: query.size } })
    list.value = res.data.items
    total.value = res.data.total
  } finally {
    loading.value = false
  }
}

const submit = async () => {
  if (!form.title.trim()) return ElMessage.warning('请填写岗位名称')
  if (form.text.trim().length < 10) return ElMessage.warning('JD 原文不能少于 10 字')
  submitting.value = true
  try {
    const res = await api.post('/jobs', {
      title: form.title.trim(),
      company: form.company.trim(),
      text: form.text.trim()
    })
    lastResult.value = res.data
    ElMessage.success('解析并保存成功')
    resetForm()
    query.page = 1
    load()
  } finally {
    submitting.value = false
  }
}

const resetForm = () => {
  form.title = ''
  form.company = ''
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
.muted {
  color: #909399;
}
</style>
