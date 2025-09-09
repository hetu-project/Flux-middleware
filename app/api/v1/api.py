from fastapi import APIRouter
from app.api.v1.health import router as health_router

router = APIRouter()

# 注册健康检查路由
router.include_router(health_router, prefix="/health")
