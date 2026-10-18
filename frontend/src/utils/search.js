/**
 * 全局搜索工具模块
 * 职责：关键词标准化（空白清洗）、安全正则匹配器构建、输入防抖
 */

/**
 * 关键词标准化：
 * 1. 将所有连续空白字符（含空格、Tab、换行、全角空格等）合并为单个空格；
 * 2. 去除首尾全部空白。
 * 彻底规避用户误输入空格导致的匹配失败、结果遗漏问题。
 * @param {string} raw 用户原始输入
 * @returns {string} 标准化后的关键词；全空白输入返回空字符串
 */
export function normalizeKeyword(raw) {
  return String(raw ?? '')
    .replace(/\s+/g, ' ')
    .trim()
}

/**
 * 转义正则特殊字符，用于非法正则输入的字面量兜底
 */
function escapeRegExp(text) {
  return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

/**
 * 构建正则匹配器。
 * 规则配置：
 * - 多关键词以空格分隔，全部命中（AND 语义）才算匹配；
 * - 每个关键词编译为正则表达式（支持灵活的正则匹配语法，如 j.va、^张|李$）；
 * - 用户输入不是合法正则（如孤立的括号、反斜杠）时，自动降级为字面量匹配，保证不报错；
 * - 正则一次性预编译，避免逐条数据重复编译带来的性能损耗。
 * @param {string} keyword 已标准化的关键词
 * @param {object} options { flags: 'i' } 正则标志位，默认忽略大小写
 * @returns {{ test(text: string): boolean, testFields(fields: string[]): boolean } | null}
 *          关键词为空时返回 null
 */
export function createSearchMatcher(keyword, options = {}) {
  const kw = normalizeKeyword(keyword)
  if (!kw) return null
  const { flags = 'i' } = options
  const tokens = kw.split(' ').filter(Boolean)
  const regexes = tokens.map((token) => {
    try {
      return new RegExp(token, flags)
    } catch (e) {
      // 非法正则输入（如 "("、"\" 等），降级为字面量匹配
      return new RegExp(escapeRegExp(token), flags)
    }
  })
  return {
    tokens,
    /** 对单段文本匹配：所有关键词均命中才算匹配 */
    test(text) {
      const hay = String(text ?? '')
      return regexes.every((re) => re.test(hay))
    },
    /**
     * 对多字段匹配：每个关键词至少命中其中一个字段。
     * 字段以空格拼接为一次性匹配文本；关键词本身不含空格，
     * 因此不会跨字段误匹配。
     */
    testFields(fields) {
      const hay = (fields || []).map((f) => String(f ?? '')).join(' ')
      return regexes.every((re) => re.test(hay))
    },
  }
}

/**
 * 使用匹配器过滤列表（配合 testFields 使用）。
 * @param {Array} items 数据列表
 * @param {object|null} matcher createSearchMatcher 的返回值
 * @param {(item: any) => string[]} getFields 提取参与匹配的字段
 * @param {number} limit 最多返回条数
 * @returns {Array} 命中的条目
 */
export function filterByMatcher(items, matcher, getFields, limit = Infinity) {
  if (!matcher || !Array.isArray(items)) return []
  const out = []
  for (const item of items) {
    if (matcher.testFields(getFields(item))) {
      out.push(item)
      if (out.length >= limit) break
    }
  }
  return out
}

/**
 * 输入防抖：wait 毫秒内连续触发只执行最后一次。
 * @param {Function} fn 待防抖函数
 * @param {number} wait 防抖阈值（毫秒）
 */
export function debounce(fn, wait = 300) {
  let timer = null
  const debounced = (...args) => {
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => {
      timer = null
      fn(...args)
    }, wait)
  }
  debounced.cancel = () => {
    if (timer) clearTimeout(timer)
    timer = null
  }
  return debounced
}
