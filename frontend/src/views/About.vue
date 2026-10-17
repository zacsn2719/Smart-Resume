<template>
  <div>
    <el-card shadow="never">
      <template #header><b>项目说明</b></template>
      <p>「智配简历」是一个智能简历-岗位匹配与技能差距分析系统。用户录入简历文本与岗位 JD 后，系统通过 NLP 方法自动抽取技能、学历与工作年限，计算匹配综合分，给出已匹配技能、缺失技能与可执行的改进建议，帮助求职者与 HR 快速评估简历与岗位的匹配程度。</p>
      <p class="section">核心流程：录入简历/岗位 → 解析抽取 → 选择简历与岗位 → AI 匹配计算 → 展示结果与建议 → 历史与统计。</p>
    </el-card>

    <el-card shadow="never" style="margin-top: 16px">
      <template #header><b>AI 方法说明</b></template>
      <el-descriptions :column="1" border>
        <el-descriptions-item label="技能抽取">基于内置 100+ 条技能词典（skill_dict.txt），对文本做词边界正则匹配（大小写不敏感），去重输出技能标签。</el-descriptions-item>
        <el-descriptions-item label="文本相似度">使用 jieba 对简历与 JD 分词，经 scikit-learn TfidfVectorizer 转换为 TF-IDF 向量，计算余弦相似度，归一化到 0-1。</el-descriptions-item>
        <el-descriptions-item label="学历匹配">正则抽取学历等级（博士/硕士/本科/专科），比较简历学历与岗位要求：满足为 1，不足为 0.5，岗位不限为 1。</el-descriptions-item>
        <el-descriptions-item label="年限匹配">正则抽取工作年限（如 3 年经验、工作 5 年），差距 0/1/2/更多年分别得 1/0.7/0.4/0.2，岗位未要求为 1。</el-descriptions-item>
        <el-descriptions-item label="综合评分">综合分 = (技能覆盖率 × 40% + 文本相似度 × 30% + 学历匹配 × 20% + 年限匹配 × 10%) × 100</el-descriptions-item>
        <el-descriptions-item label="建议生成">依据缺失技能（前 3 个）、学历差距、年限差距、文本相似度低四类规则自动生成中文改进建议。</el-descriptions-item>
      </el-descriptions>
      <el-alert
        style="margin-top: 12px"
        title="AI 结果完全可解释：所有得分均来自真实的 jieba 分词与 TF-IDF 余弦相似度计算，不使用随机数，每个分项都能追溯到具体数据来源。"
        type="success"
        :closable="false"
      />
    </el-card>

    <el-card shadow="never" style="margin-top: 16px">
      <template #header><b>技术栈</b></template>
      <el-row :gutter="16">
        <el-col :span="8">
          <el-tag size="large" style="width: 100%; justify-content: center">后端：Python / FastAPI / SQLAlchemy / SQLite</el-tag>
        </el-col>
        <el-col :span="8">
          <el-tag size="large" type="success" style="width: 100%; justify-content: center">AI：jieba 分词 / scikit-learn TF-IDF / 余弦相似度</el-tag>
        </el-col>
        <el-col :span="8">
          <el-tag size="large" type="warning" style="width: 100%; justify-content: center">前端：Vue 3 / Vite / Element Plus / ECharts / Axios</el-tag>
        </el-col>
      </el-row>
    </el-card>

    <el-card shadow="never" style="margin-top: 16px">
      <template #header><b>小组成员与分工</b></template>
      <el-table :data="members" border>
        <el-table-column prop="member" label="成员" width="140" />
        <el-table-column prop="duty" label="分工" />
      </el-table>
      <p class="muted" style="margin-top: 8px">请按小组实际情况修改 src/views/About.vue 中的成员与分工。</p>
    </el-card>
  </div>
</template>

<script setup>
const members = [
  { member: '成员 A', duty: '后端接口开发：FastAPI 接口设计、数据库建模、CORS 与异常处理' },
  { member: '成员 B', duty: 'AI 模块开发：技能词典、技能/学历/年限抽取、TF-IDF 相似度、综合评分与建议生成' },
  { member: '成员 C', duty: '前端页面开发：六个页面组件、路由、Axios 封装、ECharts 图表与前后端联调' }
]
</script>

<style scoped>
p {
  line-height: 1.8;
}

.section {
  margin-top: 8px;
  color: #606266;
}

.muted {
  color: #909399;
}
</style>
