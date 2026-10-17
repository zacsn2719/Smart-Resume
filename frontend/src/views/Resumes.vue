<template>
  <div>
    <el-row :gutter="16">
      <el-col :span="10">
        <el-card shadow="never">
          <template #header><b>简历录入</b></template>
          <el-form label-width="80px">
            <el-form-item label="简历名称">
              <el-input v-model="form.name" maxlength="100" placeholder="如：张三-Python后端" />
            </el-form-item>
            <el-form-item label="简历原文">
              <el-input
                v-model="form.text"
                type="textarea"
                :rows="12"
                maxlength="5000"
                show-word-limit
                placeholder="粘贴简历内容（10-5000 字），或使用下方上传 .txt 文件"
              />
            </el-form-item>
            <el-form-item label="文件类型">
              <div class="type-radios">
                <label class="type-radio type-word">
                  <input v-model="uploadType" type="radio" value="word" name="uploadType" />
                  <span>Word文档</span>
                </label>
                <label class="type-radio type-pdf">
                  <input v-model="uploadType" type="radio" value="pdf" name="uploadType" />
                  <span>PDF文档</span>
                </label>
                <label class="type-radio type-txt">
                  <input v-model="uploadType" type="radio" value="txt" name="uploadType" />
                  <span>纯文本TXT</span>
                </label>
              </div>
            </el-form-item>
            <el-form-item label="简历上传">
              <el-upload :auto-upload="false" :show-file-list="false" :accept="uploadAccept" :on-change="onFileChange">
                <el-button :loading="uploading">上传文件</el-button>
                <template #tip>
                  <div class="upload-tip">
                    已选类型「{{ currentType.label }}」：文件对话框仅显示 {{ uploadAccept }} 文件，其他类型将被拦截
                  </div>
                </template>
              </el-upload>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="submitting" @click="submit">解析并保存</el-button>
              <el-button @click="resetForm">清空</el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <el-card v-if="lastResult" shadow="never" style="margin-top: 16px">
          <template #header><b>最近一次解析结果</b></template>
          <p><b>学历：</b>{{ lastResult.education }}　　<b>年限：</b>{{ lastResult.years }} 年</p>
          <p style="margin-top: 8px">
            <b>技能：</b>
            <template v-if="lastResult.skills.length">
              <el-tag v-for="s in lastResult.skills" :key="s" size="small" style="margin: 2px 6px 2px 0">{{ s }}</el-tag>
            </template>
            <span v-else class="muted">未识别到技能</span>
          </p>
        </el-card>
      </el-col>

      <el-col :span="14">
        <el-card shadow="never">
          <template #header><b>简历列表（共 {{ total }} 条）</b></template>
          <el-table :data="list" v-loading="loading" stripe>
            <el-table-column prop="id" label="ID" width="60" />
            <el-table-column prop="name" label="名称" min-width="140" show-overflow-tooltip />
            <el-table-column prop="education" label="学历" width="80" />
            <el-table-column prop="years" label="年限" width="70" />
            <el-table-column label="技能" min-width="180">
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

    <el-dialog v-model="detailVisible" :title="'简历详情 - ' + (detail ? detail.name : '')" width="640px">
      <template v-if="detail">
        <p>
          <b>学历：</b>{{ detail.education }}　　<b>年限：</b>{{ detail.years }} 年　　<b>创建时间：</b>{{ formatTime(detail.created_at) }}
        </p>
        <p style="margin: 8px 0">
          <b>技能：</b>
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
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '../api'

const form = reactive({ name: '', text: '' })
const list = ref([])
const total = ref(0)
const loading = ref(false)
const submitting = ref(false)
const uploading = ref(false)
const query = reactive({ page: 1, size: 10 })
const lastResult = ref(null)
const detail = ref(null)
const detailVisible = ref(false)

// ===== 文件类型选择（单选，三种类型互斥）=====
const UPLOAD_TYPES = {
  word: { label: 'Word文档', accept: '.doc,.docx', exts: ['.doc', '.docx'] },
  pdf: { label: 'PDF文档', accept: '.pdf', exts: ['.pdf'] },
  txt: { label: '纯文本TXT', accept: '.txt', exts: ['.txt'] }
}
const uploadType = ref('txt') // 默认 TXT，保持原有上传行为

const currentType = computed(() => UPLOAD_TYPES[uploadType.value])
const uploadAccept = computed(() => currentType.value.accept)

const getExt = (name) => {
  const i = String(name || '').lastIndexOf('.')
  return i === -1 ? '' : name.slice(i).toLowerCase()
}

const formatTime = (t) => (t ? String(t).slice(0, 19).replace('T', ' ') : '')

const load = async () => {
  loading.value = true
  try {
    const res = await api.get('/resumes', { params: { page: query.page, size: query.size } })
    list.value = res.data.items
    total.value = res.data.total
  } finally {
    loading.value = false
  }
}

const onFileChange = (file) => {
  // 1. 类型校验：文件后缀必须与所选单选类型一致，否则拦截
  const conf = currentType.value
  const ext = getExt(file.name)
  if (!conf.exts.includes(ext)) {
    ElMessage.warning('文件类型不匹配：已选择「' + conf.label + '」，仅允许上传 ' + conf.accept + ' 文件，请重新选择')
    return
  }
  // 2. 大小校验（与后端 2MB 限制保持一致）
  if (file.raw && file.raw.size > 2 * 1024 * 1024) {
    ElMessage.warning('文件大小超过 2MB 限制，请压缩后重新上传')
    return
  }
  // 3. TXT：保持原有 FileReader 读取逻辑
  if (uploadType.value === 'txt') {
    const reader = new FileReader()
    reader.onload = (e) => {
      form.text = String(e.target.result || '').trim()
      if (!form.name) form.name = file.name.replace(/\.txt$/i, '')
      ElMessage.success('文件读取成功，请点击「解析并保存」')
    }
    reader.readAsText(file.raw, 'utf-8')
    return
  }
  // 4. Word / PDF：提交后端提取文本后填入文本框
  uploading.value = true
  const fd = new FormData()
  fd.append('file', file.raw)
  api
    .post('/resumes/upload', fd)
    .then((res) => {
      form.text = res.data.text
      if (!form.name) form.name = file.name.replace(/\.(docx?|pdf)$/i, '')
      ElMessage.success(conf.label + '解析成功，请确认内容后点击「解析并保存」')
    })
    .finally(() => {
      uploading.value = false
    })
}

const submit = async () => {
  if (!form.name.trim()) return ElMessage.warning('请填写简历名称')
  if (form.text.trim().length < 10) return ElMessage.warning('简历原文不能少于 10 字')
  submitting.value = true
  try {
    const res = await api.post('/resumes', { name: form.name.trim(), text: form.text.trim() })
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
/* ===== 文件类型单选按钮（Word 蓝 / PDF 红 / TXT 灰，选中与未选中状态颜色一致）===== */
.type-radios {
  display: flex;
  gap: 18px;
  align-items: center;
}

.type-radio {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 14px;
  cursor: pointer;
  user-select: none;
}

.type-radio input[type='radio'] {
  margin: 0;
  cursor: pointer;
  width: 15px;
  height: 15px;
}

.type-word {
  color: #409eff;
}

.type-word input[type='radio'] {
  accent-color: #409eff;
}

.type-pdf {
  color: #f56c6c;
}

.type-pdf input[type='radio'] {
  accent-color: #f56c6c;
}

.type-txt {
  color: #909399;
}

.type-txt input[type='radio'] {
  accent-color: #909399;
}

.upload-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.muted {
  color: #909399;
}
</style>
