from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.connection import db, mysql_db
from config import settings
from routers.damage_report_routes import router as damage_router
from auth.routes import router as auth_router
from routers.sticker_routes import router as sticker_router
from routers.game_resource_routes import router as resource_router
from services.logging_monitoring import MonitoringMiddleware, LoggingRoute
from services.security import SecurityMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时连接数据库
    await db.connect(settings["database"]["mongo_uri"], settings["database"]["db_name"])
    await mysql_db.connect(
        host=settings["database"]["mysql_host"],
        port=int(settings["database"]["mysql_port"]),
        user=settings["database"]["mysql_user"],
        password=settings["database"]["mysql_password"],
        database=settings["database"]["mysql_db"],
        pool_size=10
    )
    yield
    # 关闭时断开数据库连接
    await db.close()
    if mysql_db.pool:
        mysql_db.pool.close()
        await mysql_db.pool.wait_closed()

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
app.include_router(sticker_router)
app.include_router(resource_router)
