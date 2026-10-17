export function formatTime(t) {
  return t ? String(t).slice(0, 19).replace('T', ' ') : ''
}

export function formatDate(t) {
  return t ? String(t).slice(0, 10) : ''
}

export function formatClock(t) {
  return t ? String(t).slice(11, 19) : ''
}

// 匹配等级 → 语义色（与 Stitch 设计系统一致）
export function levelColor(level) {
  if (level === '高度匹配') return '#00b07a'
  if (level === '较匹配') return '#565e74'
  if (level === '一般') return '#f97316'
  return '#ba1a1a'
}

// 匹配等级 → 药丸样式类
export function levelPill(level) {
  if (level === '高度匹配') return 'pill tertiary'
  if (level === '较匹配') return 'pill secondary'
  if (level === '一般') return 'pill primary'
  return 'pill error'
}

// 维度分（0-1）→ 进度条颜色类
export function scoreTone(ratio) {
  if (ratio >= 0.8) return 'tertiary'
  if (ratio >= 0.6) return 'secondary'
  return ''
}

export const SKILL_KEYWORDS = [
  'Python', 'Java', 'Go', 'C++', 'JavaScript', 'TypeScript', 'Vue', 'React', 'Node.js',
  'FastAPI', 'Django', 'Flask', 'Spring', 'SpringBoot', 'MyBatis', 'RabbitMQ', 'Kafka',
  'Docker', 'Kubernetes', 'K8s', 'Jenkins', 'CI/CD', 'Git', 'Linux', 'Nginx', 'Redis',
  'MySQL', 'PostgreSQL', 'MongoDB', 'Elasticsearch', 'ClickHouse', 'Hadoop', 'Spark',
  'Hive', 'Flink', 'Pandas', 'NumPy', 'Scikit-learn', 'TensorFlow', 'PyTorch', 'NLP',
  '机器学习', '深度学习', '数据分析', '数据挖掘', 'ETL', 'SQL', 'Power BI', 'Tableau',
  'Figma', 'Sketch', '产品设计', '项目管理', '微服务', 'RESTful', '高并发'
]

export function extractSkillHints(text) {
  if (!text) return []
  const lower = text.toLowerCase()
  return SKILL_KEYWORDS.filter((k) => lower.includes(k.toLowerCase()))
}
