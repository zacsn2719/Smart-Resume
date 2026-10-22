import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: 'https://smart-resume-fy41.onrender.com/api',
  timeout: 15000
})


api.interceptors.response.use(
  (res) => res,
  (err) => {
    const detail = err.response && err.response.data && err.response.data.detail
    const msg = typeof detail === 'string' ? detail : err.message || '请求失败，请检查后端服务是否启动'
    ElMessage.error(msg)
    // 请求失败时返回空数据，避免页面崩溃
    return Promise.resolve({
      data: {
        items: [],
        total: 0,
        avg_score: 0,
        matches: [],
        history: [],
        stats: {}
      }
    })
  }
)

export default api
