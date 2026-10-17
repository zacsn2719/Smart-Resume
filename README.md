# 智能简历-岗位匹配与技能差距分析系统

## 项目简介

一个前后端分离的 Web 系统：通过录入简历文本与岗位 JD，使用 NLP 方法（jieba 分词 + TF-IDF + 余弦相似度）自动计算匹配度，给出综合分、分项得分、已匹配技能、缺失技能和改进建议，帮助求职者与 HR 快速评估简历与岗位的匹配程度。

## 技术栈

| 类别   | 技术                                           |
| :----- | :--------------------------------------------- |
| 后端   | Python 3.10+ / FastAPI / SQLAlchemy / SQLite   |
| AI 模型 | jieba 分词 / scikit-learn TF-IDF / 余弦相似度 |
| 前端   | Vue 3 / Vite / Element Plus / Axios / ECharts  |

## 环境要求

| 依赖    | 版本要求      |
| :------ | :------------ |
| Python  | 3.10 / 3.11   |
| Node.js | 18 LTS        |
| npm     | 9+            |

## 快速启动

### 1. 启动后端

```bash
cd backend

# 创建虚拟环境（可选）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库并写入内置岗位（可选，应用启动时也会自动初始化）
python seed.py

# 启动服务
uvicorn main:app --reload --port 8000
```

后端 Swagger 接口文档: http://127.0.0.1:8000/docs

### 2. 启动前端

```bash
cd frontend

# 安装依赖（首次）
npm install

# 启动开发服务器
npm run dev
```

打开前端页面: http://localhost:5173

> 前端已通过 Vite 代理将 `/api` 请求转发到 `http://127.0.0.1:8000`，无需额外配置跨域。

## 项目结构

```
project/
├── backend/
│   ├── main.py            # FastAPI 应用与全部接口
│   ├── database.py        # 数据库连接配置
│   ├── models.py          # ORM 数据模型
│   ├── schemas.py         # Pydantic 请求/响应模型
│   ├── ai_service.py      # AI 匹配核心算法
│   ├── skill_dict.txt     # 技能词典（100+ 条）
│   ├── seed.py            # 数据库初始化与内置岗位
│   ├── requirements.txt   # Python 依赖
│   └── app.db             # SQLite 数据库文件（启动后生成）
├── frontend/
│   ├── src/
│   │   ├── api/index.js   # Axios 封装
│   │   ├── router/        # 路由配置
│   │   ├── views/
│   │   │   ├── Resumes.vue  # 简历管理
│   │   │   ├── Jobs.vue     # 岗位管理
│   │   │   ├── Match.vue    # 匹配分析
│   │   │   ├── History.vue  # 历史记录
│   │   │   ├── Stats.vue    # 统计看板
│   │   │   └── About.vue    # 关于页
│   │   ├── App.vue
│   │   └── main.js
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
└── README.md
```

## API 接口说明

统一前缀: `/api`

### 简历接口

| 方法   | 路径                | 说明           |
| :----- | :------------------ | :------------- |
| POST   | `/api/resumes`      | 新增并解析简历 |
| GET    | `/api/resumes`      | 简历列表（分页） |
| GET    | `/api/resumes/{id}` | 简历详情       |
| DELETE | `/api/resumes/{id}` | 删除简历       |

### 岗位接口

| 方法   | 路径             | 说明           |
| :----- | :--------------- | :------------- |
| POST   | `/api/jobs`      | 新增并解析岗位 |
| GET    | `/api/jobs`      | 岗位列表（分页） |
| GET    | `/api/jobs/{id}` | 岗位详情       |
| DELETE | `/api/jobs/{id}` | 删除岗位       |

### 匹配接口

| 方法   | 路径                | 说明             |
| :----- | :------------------ | :--------------- |
| POST   | `/api/match`        | 单岗位匹配       |
| POST   | `/api/match/batch`  | 批量匹配全部岗位 |
| GET    | `/api/records`      | 历史记录（分页） |
| GET    | `/api/records/{id}` | 记录详情         |
| DELETE | `/api/records/{id}` | 删除记录         |
| GET    | `/api/stats`        | 统计数据         |

## AI 算法说明

1. **技能抽取**: 基于内置 100+ 技能词典，对文本做词边界正则匹配（大小写不敏感），去重输出。
2. **TF-IDF + 余弦相似度**: 使用 jieba 分词和 scikit-learn 计算简历与 JD 的文本相似度。
3. **学历匹配**: 正则抽取学历等级后比较。
4. **年限匹配**: 正则抽取工作年限要求后比较。
5. **综合评分**: `(技能覆盖率×40% + 文本相似度×30% + 学历匹配×20% + 年限匹配×10%) × 100`
6. **建议生成**: 依据缺失技能、学历差距、年限差距、文本相似度自动生成改进建议。

## 开源许可证

本项目基于 [MIT License](LICENSE) 开源。

## 匹配等级

| 综合分   | 等级     |
| :------- | :------- |
| 80—100  | 高度匹配 |
| 65—79   | 较匹配   |
| 50—64   | 一般     |
| 0—49    | 不匹配   |

## 常见问题

| 问题                  | 解决方式                                                   |
| :-------------------- | :--------------------------------------------------------- |
| 前端请求 404          | 检查 `vite.config.js` 代理配置和后端端口是否为 8000        |
| CORS 错误             | 后端已启用 CORSMiddleware，正常不会出现                    |
| SQLite 没有表         | 确认 `main.py` 启动时已执行 `Base.metadata.create_all`     |
| jieba 第一次分词慢    | 正常现象，首次运行需加载词典                               |
| scikit-learn 安装失败 | 升级 pip 或使用国内镜像源                                  |
| 端口被占用            | 更换端口，如 8001、5174（同步修改 vite 代理目标）          |
| 技能抽取为空          | 检查 `skill_dict.txt` 路径与文件编码（UTF-8）              |
