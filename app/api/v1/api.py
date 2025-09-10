from fastapi import APIRouter
from app.api.v1.health import router as health_router
from app.api.v1.subnet import router as subnet_router
from app.api.v1.twitter import router as twitter_router

router = APIRouter()

# 注册健康检查路由
router.include_router(health_router, prefix="/health")

# 注册子网路由
router.include_router(subnet_router, prefix="/subnet")

# 注册 Twitter 路由
router.include_router(twitter_router, prefix="/twitter")
