<template>
  <div class="page-inner" style="max-width:1440px;padding:1.5rem">
    <!-- 顶部系统概览 -->
    <div class="card" style="display:flex;flex-direction:column;gap:1rem">
      <div class="row-between wrap" style="gap:1rem">
        <div class="row-gap-md">
          <div class="kpi-icon primary" style="width:3rem;height:3rem;border-radius:0.75rem">
            <span class="material-symbols-outlined" style="font-size:28px;font-variation-settings:'FILL' 1">insights</span>
          </div>
          <div>
            <div class="row-gap-sm" style="flex-wrap:wrap">
              <h1 class="t-headline-lg">关于智配简历 (Smart Match OS)</h1>
              <span class="pill primary">v2.4 Pro</span>
              <span class="pill neutral">jieba 分词 · TF-IDF · 余弦相似度</span>
            </div>
            <p class="page-head-sub">基于自然语言处理与语义余弦相似度算法的智能人岗匹配分析系统</p>
          </div>
        </div>
        <div class="row-gap-sm">
          <div class="row-gap-xs" style="padding:0.5rem 0.75rem;border-radius:0.5rem;background:var(--surface-container-low);color:var(--tertiary)">
            <span class="dot" style="width:8px;height:8px;background:var(--tertiary-container);animation:pulse 1.6s ease-in-out infinite"></span>
            <span class="t-label-md">算法引擎运行正常</span>
          </div>
          <button class="btn btn-surface" style="background:var(--surface-container-high)" @click="share">
            <span class="material-symbols-outlined">share</span><span>分享</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 4 指标卡 -->
    <div class="kpi-grid" style="grid-template-columns:repeat(auto-fit,minmax(14rem,1fr));gap:0.75rem">
      <div v-for="m in metrics" :key="m.title" class="kpi-card">
        <div class="row-between">
          <div class="kpi-icon" :style="{ background: m.iconBg, color: m.iconColor }"><span class="material-symbols-outlined">{{ m.icon }}</span></div>
          <span class="t-caption" :style="{ background: 'var(--surface-container-high)', color: m.tagColor || 'var(--secondary)', padding: '2px 0.5rem', borderRadius: '0.25rem', fontWeight: 600 }">{{ m.tag }}</span>
        </div>
        <div style="margin-top:0.75rem">
          <div class="t-headline-xl">{{ m.value }}<span v-if="m.unit" class="t-title-sm c-secondary" style="font-weight:400">{{ m.unit }}</span></div>
          <div class="row-between" style="margin-top:0.25rem">
            <span class="t-body-sm c-secondary">{{ m.label }}</span>
            <span class="t-caption" :style="{ color: m.footColor, fontWeight: 600 }">{{ m.foot }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- SECTION 1 项目说明与核心流程 -->
    <div class="card" style="display:flex;flex-direction:column;gap:1.25rem">
      <div class="card-head">
        <div class="row-gap-sm">
          <div class="kpi-icon" style="background:var(--surface-container-low);color:var(--primary-container)"><span class="material-symbols-outlined">menu_book</span></div>
          <div>
            <h2 class="t-headline-md">项目说明与核心流程</h2>
            <p class="t-caption c-secondary">系统定位、业务闭环与五步自动化交付链路</p>
          </div>
        </div>
        <span class="pill neutral">ARCHITECTURE FLOW</span>
      </div>

      <div style="padding:1.25rem;border-radius:0.75rem;background:var(--surface-container-low);display:flex;gap:1.25rem;align-items:flex-start">
        <div class="kpi-icon" style="width:2.5rem;height:2.5rem;border-radius:9999px;background:var(--surface-container-lowest);color:var(--primary-container);box-shadow:var(--shadow-sm);flex-shrink:0">
          <span class="material-symbols-outlined" style="font-size:22px">auto_stories</span>
        </div>
        <div class="stack" style="gap:0.5rem">
          <p class="t-body-md" style="margin:0;line-height:1.75">
            <strong class="t-title-sm" style="color:var(--primary-container)">「智配简历」</strong>
            是一个智能简历-岗位匹配与技能差距分析系统。用户录入简历文本与岗位 JD 后，系统通过 NLP 方法自动抽取技能、学历与工作年限，计算匹配综合分，给出已匹配技能、缺失技能与可执行的改进建议，帮助求职者与 HR 快速评估简历与岗位的匹配程度。
          </p>
          <div class="row-gap-sm t-body-sm c-secondary">
            <span class="material-symbols-outlined" style="font-size:16px;color:var(--tertiary)">check_circle</span>
            <span>实现从原始非结构化文本录入到精细化多维度评分建议的全流程自动化支持。</span>
          </div>
        </div>
      </div>

      <div class="stack" style="gap:0.625rem">
        <span class="t-label-sm c-secondary" style="text-transform:uppercase;letter-spacing:0.06em">五步核心交互管道 (Core Pipeline)</span>
        <div class="grid-5" style="position:relative">
          <div v-for="(s, i) in pipeline" :key="s.title" style="position:relative;padding:0.75rem;border-radius:0.75rem;background:var(--surface-container-lowest);box-shadow:var(--shadow-sm);display:flex;flex-direction:column;gap:0.5rem">
            <div class="row-between">
              <span class="kpi-icon" :style="{ width: '1.75rem', height: '1.75rem', borderRadius: '9999px', fontSize: '11px', fontWeight: 600, background: i === 4 ? 'var(--tertiary-fixed)' : 'var(--primary-fixed)', color: i === 4 ? 'var(--on-tertiary-fixed)' : 'var(--on-primary-fixed)' }">{{ s.no }}</span>
              <span class="material-symbols-outlined c-secondary" :style="{ fontSize: '18px', color: i === 4 ? 'var(--tertiary)' : 'var(--secondary)' }">{{ s.icon }}</span>
            </div>
            <div>
              <div class="t-title-sm">{{ s.title }}</div>
              <p class="t-caption c-secondary" style="margin:4px 0 0">{{ s.sub }}</p>
            </div>
            <span v-if="i < 4" class="pipeline-arrow">→</span>
          </div>
        </div>
      </div>
    </div>

    <!-- SECTION 2 AI 方法说明 -->
    <div class="card" style="display:flex;flex-direction:column;gap:1.25rem">
      <div class="card-head">
        <div class="row-gap-sm">
          <div class="kpi-icon" style="background:var(--surface-container-low);color:var(--primary-container)"><span class="material-symbols-outlined">account_tree</span></div>
          <div>
            <h2 class="t-headline-md">AI 方法说明与算法规则</h2>
            <p class="t-caption c-secondary">严格可解释性的数学与工程规则定义</p>
          </div>
        </div>
        <span class="pill secondary">100% EXPLAINABLE</span>
      </div>

      <div class="grid-3">
        <div v-for="r in rules" :key="r.title" style="padding:0.75rem;border-radius:0.75rem;background:var(--surface-container-low);display:flex;flex-direction:column;gap:0.75rem" class="card-hover">
          <div class="stack" style="gap:0.25rem">
            <div class="row-between">
              <span class="t-caption" :style="{ background: r.badgeBg, color: r.badgeFg, padding: '2px 0.5rem', borderRadius: '0.25rem', fontWeight: 600 }">{{ r.badge }}</span>
              <span class="t-label-md" style="color:var(--primary);font-weight:700">权重 {{ r.weight }}</span>
            </div>
            <h3 class="t-title-sm" style="margin:0.25rem 0 0">{{ r.title }}</h3>
            <p class="t-body-sm c-secondary" style="margin:0;line-height:1.65">{{ r.desc }}</p>
          </div>
          <div class="row-between" style="margin-top:auto;padding:0.375rem 0.625rem;border-radius:0.375rem;background:var(--surface-container-lowest)">
            <span class="t-caption c-secondary">{{ r.label }}</span>
            <span class="t-caption" style="font-weight:600;color:var(--on-surface)">{{ r.formula }}</span>
          </div>
        </div>

        <div class="span-2" style="padding:0.75rem;border-radius:0.75rem;background:var(--surface-container-low);display:flex;flex-direction:column;gap:0.75rem">
          <div class="row-between">
            <span class="t-caption" style="background:var(--primary-fixed);color:var(--on-primary-fixed);padding:2px 0.5rem;border-radius:0.25rem;font-weight:600">算法总公式</span>
            <span class="t-caption c-secondary">归一化百分制</span>
          </div>
          <div>
            <h3 class="t-title-sm" style="margin:0.25rem 0 0">综合匹配分加权方程</h3>
            <div class="row-gap-xs" style="margin-top:0.5rem;padding:0.625rem;border-radius:0.5rem;background:var(--surface-container-lowest);overflow-x:auto;white-space:nowrap">
              <span style="font-weight:600;color:var(--primary);flex-shrink:0">综合分 =</span>
              <span class="mono t-body-sm">( 技能覆盖率 × 40% + 文本相似度 × 30% + 学历匹配 × 20% + 年限匹配 × 10% ) × 100</span>
            </div>
            <p class="t-body-sm c-secondary" style="margin:0.5rem 0 0;line-height:1.65">
              建议生成机制：算法系统依据缺失技能（重点取前 3 个核心缺口）、学历差距、年限差距、文本相似度偏低四类规则，自动生成针对性改进的中文实操建议。
            </p>
          </div>
        </div>
      </div>

      <div style="padding:0.75rem;border-radius:0.75rem;background:rgba(111,251,190,0.3);display:flex;gap:0.75rem;align-items:flex-start">
        <div class="kpi-icon" style="width:2.25rem;height:2.25rem;border-radius:9999px;background:var(--tertiary-container);color:var(--on-primary);flex-shrink:0">
          <span class="material-symbols-outlined" style="font-size:20px">verified_user</span>
        </div>
        <div class="stack">
          <span class="t-label-md" style="font-weight:700;color:var(--on-tertiary-fixed)">AI 结果完全可解释机制保证</span>
          <span class="t-body-sm" style="color:var(--on-tertiary-fixed-variant);line-height:1.65">所有得分均来自真实的 jieba 分词与 TF-IDF 余弦相似度计算，绝不使用随机数或无法溯源的生成式黑盒，每个分项都能精准定位到具体数据来源。</span>
        </div>
      </div>
    </div>

    <!-- SECTION 3 技术栈 -->
    <div class="card" style="display:flex;flex-direction:column;gap:1.25rem">
      <div class="card-head">
        <div class="row-gap-sm">
          <div class="kpi-icon" style="background:var(--surface-container-low);color:var(--primary-container)"><span class="material-symbols-outlined">terminal</span></div>
          <div>
            <h2 class="t-headline-md">系统技术栈</h2>
            <p class="t-caption c-secondary">高吞吐量工程架构与高效算法生态整合</p>
          </div>
        </div>
        <span class="pill neutral">TECH STACK</span>
      </div>

      <div class="grid-3">
        <div v-for="t in stacks" :key="t.title" style="padding:0.75rem;border-radius:0.75rem;background:var(--surface-container-low);display:flex;flex-direction:column;gap:0.5rem">
          <div class="row-gap-sm">
            <span class="material-symbols-outlined" :style="{ fontSize: '20px', color: t.iconColor }">{{ t.icon }}</span>
            <span class="t-title-sm">{{ t.title }}</span>
          </div>
          <p class="t-caption c-secondary" style="margin:0">{{ t.sub }}</p>
          <div class="chip-row" style="margin-top:auto;padding-top:0.5rem">
            <span v-for="p in t.pills" :key="p.name" class="chip" :style="{ background: 'var(--surface-container-lowest)', color: p.hl ? 'var(--tertiary)' : 'var(--on-surface)', boxShadow: 'var(--shadow-sm)', padding: '0.25rem 0.625rem', fontWeight: p.hl ? 700 : 600 }">{{ p.name }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- SECTION 4 小组成员与分工 -->
    <div class="card" style="display:flex;flex-direction:column;gap:1.25rem">
      <div class="card-head">
        <div class="row-gap-sm">
          <div class="kpi-icon" style="background:var(--surface-container-low);color:var(--primary-container)"><span class="material-symbols-outlined">badge</span></div>
          <div>
            <h2 class="t-headline-md">小组成员与职责分工</h2>
            <p class="t-caption c-secondary">敏捷开发团队角色分配与模块责任人</p>
          </div>
        </div>
        <span class="row-gap-xs t-caption c-secondary"><span class="material-symbols-outlined" style="font-size:16px">info</span>请按小组实际情况修改成员与分工</span>
      </div>

      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>成员</th>
              <th>角色定位</th>
              <th>主导任务模块</th>
              <th>交付状态</th>
              <th style="text-align:right">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(m, i) in members" :key="m.member">
              <td>
                <div class="row-gap-sm">
                  <div class="avatar-square" :style="{ background: m.avatarBg, color: m.avatarFg, borderRadius: '9999px', fontWeight: 700, boxShadow: 'var(--shadow-sm)' }">{{ m.initial }}</div>
                  <div class="stack">
                    <span class="t-title-sm">{{ m.member }}</span>
                    <span class="t-caption c-secondary">{{ m.role }}</span>
                  </div>
                </div>
              </td>
              <td><span class="t-caption" :style="{ background: m.badgeBg, color: m.badgeFg, padding: '2px 0.5rem', borderRadius: '0.25rem' }">{{ m.tag }}</span></td>
              <td class="t-body-sm" style="max-width:26rem">{{ m.module }}</td>
              <td>
                <span class="pill tertiary" style="gap:0.375rem;padding:0.25rem 0.625rem;font-weight:600">
                  <span class="dot" style="width:6px;height:6px;background:var(--tertiary)"></span>{{ m.status }}
                </span>
              </td>
              <td style="text-align:right"><button class="btn btn-ghost btn-sm">查看代码</button></td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="row-between wrap" style="gap:0.5rem;padding:0.75rem;border-radius:0.5rem;background:var(--surface-container-low)">
        <span class="row-gap-sm t-caption c-secondary"><span class="material-symbols-outlined" style="font-size:18px">terminal</span>代码仓库已在 GitLab / GitHub 同步维护 · CI/CD 自动化检测已全部通过</span>
        <span class="t-caption c-secondary mono">智配简历 System © 2026. All rights reserved.</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ElMessage } from 'element-plus'

const metrics = [
  { icon: 'psychology', iconBg: 'var(--surface-container-high)', iconColor: 'var(--primary-container)', tag: 'NLP 核心', value: '100+', label: '内置专业技能词库', foot: '精准词界判定', footColor: 'var(--tertiary)' },
  { icon: 'functions', iconBg: 'var(--surface-container-high)', iconColor: 'var(--tertiary)', tag: '四维加权', value: '100%', label: '全流程白盒可解释', foot: '余弦向量空间', footColor: 'var(--tertiary)' },
  { icon: 'speed', iconBg: 'var(--surface-container-high)', iconColor: 'var(--on-secondary-container)', tag: '毫秒响应', value: '< 85', unit: 'ms', label: '单份简历解析延迟', foot: 'FastAPI驱动', footColor: 'var(--secondary)' },
  { icon: 'groups', iconBg: 'var(--surface-container-high)', iconColor: 'var(--primary)', tag: '敏捷交付', value: '3', unit: ' 人分工', label: '后端 · 算法 · 前端', foot: '全功能闭环', footColor: 'var(--primary)' }
]

const pipeline = [
  { no: '01', icon: 'input', title: '录入简历与岗位', sub: '支持文本直接粘贴、PDF/DOCX 导入与批量存储' },
  { no: '02', icon: 'rule', title: '解析抽取实体', sub: '词典边界匹配技能，正则抽取工作年限与学历层级' },
  { no: '03', icon: 'join', title: '选择匹配对比', sub: '自由组合候选人与岗位，支持 1v1 或 1vN 批量诊断' },
  { no: '04', icon: 'calculate', title: 'AI 算法综合评分', sub: 'jieba分词结合余弦相似度与规则权重计算综合得分' },
  { no: '05', icon: 'verified', title: '结果建议与统计', sub: '呈现雷达画像、技能缺口对齐与简历改进建议报告' }
]

const rules = [
  {
    badge: '维度一', badgeBg: 'var(--primary-fixed)', badgeFg: 'var(--on-primary-fixed)', weight: '40%',
    title: '技能抽取与覆盖率',
    desc: '基于内置 100+ 条技能词典 (skill_dict.txt)，对文本做词边界正则匹配（大小写不敏感），去重输出结构化技能标签并计算匹配比例。',
    label: '覆盖率公式', formula: '已匹配数 / 岗位要求数'
  },
  {
    badge: '维度二', badgeBg: 'var(--secondary-container)', badgeFg: 'var(--on-secondary-fixed)', weight: '30%',
    title: '文本语义相似度',
    desc: '使用 jieba 对简历与 JD 进行中文精确切词，经 scikit-learn 的 TfidfVectorizer 转换为 TF-IDF 高维向量，计算余弦相似度并归一化到 [0, 1]。',
    label: '余弦向量夹角', formula: 'Cosine(V_resume, V_jd)'
  },
  {
    badge: '维度三', badgeBg: 'var(--surface-container-highest)', badgeFg: 'var(--on-surface)', weight: '20%',
    title: '学历匹配分级',
    desc: '正则抽取学历等级（博士 / 硕士 / 本科 / 专科），对比简历学历与岗位要求：简历满足或超越要求得 1.0，不足档位则降权得 0.5；岗位未作学历限制时默认计满分 1.0。',
    label: '梯度评分', formula: '满足: 1.0 | 不足: 0.5'
  },
  {
    badge: '维度四', badgeBg: 'var(--surface-container-highest)', badgeFg: 'var(--on-surface)', weight: '10%',
    title: '工作年限容差匹配',
    desc: '正则提取工作年限数值（如 "3年经验"、"5年以上"），当存在负向差距时阶梯扣减：相差 0/1/2/更多 年分别得分 1.0 / 0.7 / 0.4 / 0.2，岗位无硬性要求时直接判定为 1.0。',
    label: '阶梯扣减值', formula: '1.0 → 0.7 → 0.4 → 0.2'
  }
]

const stacks = [
  {
    icon: 'dns', iconColor: 'var(--primary)', title: '后端服务',
    sub: '负责 RESTful API、数据库映射与高并发请求调度',
    pills: [{ name: 'Python 3.10+' }, { name: 'FastAPI' }, { name: 'SQLAlchemy' }, { name: 'SQLite' }]
  },
  {
    icon: 'model_training', iconColor: 'var(--tertiary)', title: 'AI 与算法',
    sub: '中文分词、高维特征向量化与余弦距离度量',
    pills: [{ name: 'jieba 分词', hl: true }, { name: 'scikit-learn' }, { name: 'TF-IDF Vectorizer' }, { name: '余弦相似度' }]
  },
  {
    icon: 'web', iconColor: 'var(--on-secondary-container)', title: '前端与可视化',
    sub: '响应式单页应用、动态雷达图表与轻量级状态管理',
    pills: [{ name: 'Vue 3' }, { name: 'Vite' }, { name: 'Element Plus' }, { name: 'ECharts' }, { name: 'Axios' }]
  }
]

const members = [
  {
    initial: 'A', member: '成员 A', role: '后端架构师', tag: '后端接口开发',
    avatarBg: 'var(--primary-fixed)', avatarFg: 'var(--on-primary-fixed)',
    badgeBg: 'var(--primary-fixed)', badgeFg: 'var(--on-primary-fixed)',
    module: 'FastAPI 接口设计、数据库建模 (SQLAlchemy/SQLite)、CORS 与全局异常处理中间件',
    status: '已完成交付'
  },
  {
    initial: 'B', member: '成员 B', role: 'AI 算法工程师', tag: 'AI 模块开发',
    avatarBg: 'var(--secondary-container)', avatarFg: 'var(--on-secondary-fixed)',
    badgeBg: 'var(--secondary-container)', badgeFg: 'var(--on-secondary-fixed)',
    module: '技能词典工程化、技能/学历/年限多维特征抽取、TF-IDF 相似度计算、综合加权评分与文本建议自动生成',
    status: '已完成交付'
  },
  {
    initial: 'C', member: '成员 C', role: '前端开发工程师', tag: '前端页面开发',
    avatarBg: 'var(--surface-container-high)', avatarFg: 'var(--on-surface)',
    badgeBg: 'var(--surface-container-highest)', badgeFg: 'var(--on-surface)',
    module: '六个页面组件实现、Vue Router 路由控制、Axios 请求与响应拦截封装、ECharts 图表交互与前后端协同联调',
    status: '已完成交付'
  }
]

const share = async () => {
  try {
    await navigator.clipboard.writeText(window.location.href)
    ElMessage.success('系统版本链接已复制')
  } catch (e) {
    ElMessage.info(window.location.href)
  }
}
</script>

<style scoped>
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.45; transform: scale(1.35); }
}
.pipeline-arrow {
  display: none;
}
@media (min-width: 768px) {
  .pipeline-arrow {
    display: block;
    position: absolute;
    right: -0.75rem;
    top: 50%;
    transform: translateY(-50%);
    color: var(--outline-variant);
    font-weight: 700;
    z-index: 10;
  }
}
</style>
