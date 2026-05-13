from fastapi import APIRouter

from ai_promana_backend.api.v1.endpoints import _mock


router = APIRouter()


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.get("/options", summary="管理端通用选项")
def get_management_options():
    return _mock.api_response(
        {
            "roles": ["super_admin", "admin", "pm", "developer", "qa", "product", "collaborator", "user"],
            "userStatuses": ["pending", "active", "disabled"],
            "projectStatuses": ["pending", "active", "paused", "completed", "archived"],
            "projectHealth": ["good", "attention", "risk", "completed"],
            "teams": _mock.option_items()["teams"],
        }
    )
