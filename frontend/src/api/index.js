import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: '/api',
  timeout: 15000
})

api.interceptors.response.use(
  (res) => res,
  (err) => {
    const detail = err.response && err.response.data && err.response.data.detail
    const msg = typeof detail === 'string' ? detail : err.message || '请求失败，请检查后端服务是否启动'
    ElMessage.error(msg)
    return Promise.reject(err)
  }
)

export default api
