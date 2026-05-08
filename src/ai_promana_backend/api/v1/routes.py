from fastapi import APIRouter
from ai_promana_backend.api.v1.endpoints import users

router = APIRouter(prefix="/api/v1")

router.include_router(users.router, prefix="/users", tags=["用户管理"])
