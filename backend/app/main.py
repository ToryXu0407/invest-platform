from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import sentry_sdk

from app.core.config import settings
from app.api import stocks, articles, auth, alerts, ai, screener
from app.core.database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    print(f"🚀 Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    
    # 创建数据库表（开发环境）- 如果数据库可用
    if settings.ENVIRONMENT == "development":
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            print("✅ Database connected and tables created")
        except Exception as e:
            print(f"⚠️  Database not available: {e}")
            print("📝 API will work but database operations will fail")
    
    yield
    
    # 关闭时执行
    print(f"👋 Shutting down {settings.PROJECT_NAME}")


# Sentry 初始化（生产环境）
if settings.ENVIRONMENT == "production" and settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=0.1,
        profiles_sample_rate=0.1,
    )


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="基于价值投资理念的股票分析平台 - 股息率锚定分析、财务数据可视化、AI 问答",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["认证"])
app.include_router(stocks.router, prefix=f"{settings.API_V1_STR}/stocks", tags=["股票"])
app.include_router(articles.router, prefix=f"{settings.API_V1_STR}/articles", tags=["文章"])
app.include_router(alerts.router, prefix=f"{settings.API_V1_STR}/alerts", tags=["预警"])
app.include_router(ai.router, prefix=f"{settings.API_V1_STR}/ai", tags=["AI 问答"])
app.include_router(screener.router, prefix=f"{settings.API_V1_STR}/screener", tags=["选股器"])


@app.get("/", tags=["根路径"])
async def root():
    """根路径"""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", tags=["健康检查"])
async def health_check():
    """健康检查"""
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development",
    )
