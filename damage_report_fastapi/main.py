from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from utils.limiter import limiter, rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from database.connection import db, mysql_db
from config import settings
from auth.routes import router as auth_router
from routers.sticker_routes import router as sticker_router
from routers.game_resource_routes import router as resource_router
from routers.card_routes import router as card_router
from routers.character_routes import router as character_router
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
    if mysql_db.engine:
        await mysql_db.engine.dispose()


app = FastAPI(
    title=settings["app"]["name"],
    debug=settings["app"]["debug"],
    lifespan=lifespan,
    route_class=LoggingRoute,
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ],
    exception_handlers={
        RateLimitExceeded: rate_limit_exceeded_handler
    }
)

# 应用限流中间件
app.state.limiter = limiter

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

app.include_router(auth_router)
app.include_router(sticker_router)
app.include_router(resource_router)
app.include_router(card_router)
app.include_router(character_router)
