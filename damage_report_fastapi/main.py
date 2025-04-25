from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.connection import db
from config import settings
from routers.damage_report_routes import router as damage_router
from auth.routes import router as auth_router
from services.logging_monitoring import MonitoringMiddleware, LoggingRoute
from services.security import SecurityMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时连接数据库
    await db.connect(settings["database"]["mongo_uri"], settings["database"]["db_name"])
    yield
    # 关闭时断开数据库连接
    await db.close()

app = FastAPI(
    title=settings["app"]["name"],
    debug=settings["app"]["debug"],
    lifespan=lifespan,
    route_class=LoggingRoute
)

# 添加安全中间件 (最先执行)
app.add_middleware(SecurityMiddleware)
# 添加监控中间件
app.add_middleware(MonitoringMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(damage_router)
app.include_router(auth_router)
