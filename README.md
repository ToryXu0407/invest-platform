# 价值投资分析平台

基于价值投资理念的股票分析平台，提供股息率锚定分析、财务数据可视化、AI 问答等功能。

## 🚀 技术栈

### 前端
- **Next.js 14** - React 全栈框架
- **TypeScript** - 类型安全
- **Tailwind CSS** - 样式
- **TanStack Query** - 数据请求
- **Zustand** - 状态管理
- **Recharts** - 图表

### 后端
- **FastAPI** - Python Web 框架
- **SQLAlchemy** - ORM
- **PostgreSQL** - 数据库
- **Redis** - 缓存
- **Celery** - 任务队列
- **LangChain** - AI/RAG

## 📁 项目结构

```
invest-platform/
├── backend/              # Python 后端
│   ├── app/
│   │   ├── api/         # API 路由
│   │   ├── models/      # SQLAlchemy 模型
│   │   ├── schemas/     # Pydantic 模式
│   │   ├── services/    # 业务逻辑
│   │   ├── core/        # 配置、安全
│   │   └── main.py      # 应用入口
│   ├── requirements.txt
│   └── Dockerfile
├── apps/web/            # Next.js 前端
│   ├── src/
│   │   └── app/
│   ├── package.json
│   └── next.config.js
├── docker-compose.yml
└── README.md
```

## 🛠️ 快速开始

### 环境要求
- Python 3.11+
- Node.js 20+
- Docker & Docker Compose

### 方式一：Docker Compose（推荐）

```bash
# 启动所有服务（数据库、Redis、后端 API）
docker-compose up -d

# 查看日志
docker-compose logs -f api

# 停止服务
docker-compose down
```

访问 http://localhost:8000/docs 查看 API 文档

### 方式二：本地开发

#### 后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入实际配置

# 启动开发服务器
uvicorn app.main:app --reload --port 8000
```

#### 前端

```bash
cd apps/web

# 安装依赖
pnpm install  # 或 npm install

# 启动开发服务器
pnpm dev
```

访问 http://localhost:3000

## 📖 API 文档

启动后端后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔧 开发工具

### 后端
```bash
# 运行测试
pytest

# 代码格式化
black app/
ruff check app/

# 数据库迁移
alembic revision --autogenerate -m "migration message"
alembic upgrade head
```

### 前端
```bash
# 代码检查
pnpm lint

# 格式化
pnpm format

# 测试
pnpm test
```

## 📝 功能模块

- ✅ 用户认证（注册/登录/JWT）
- 🚧 股票分析（股息率、PE/PB 百分位）
- 🚧 文章知识库
- 🚧 AI 问答
- 🚧 价格预警
- 🚧 选股器

## 📄 License

MIT
