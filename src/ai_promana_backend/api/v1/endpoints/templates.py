from typing import Any

from fastapi import APIRouter, Body

from ai_promana_backend.api.v1.endpoints import _mock


router = APIRouter()


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.get("/project-templates", summary="项目模板列表")
def list_project_templates():
    return _mock.api_response(
        {
            "templates": _mock.project_templates(),
            "pageOptions": ["overview", "members", "kanban", "gantt", "risk", "reports", "docs"],
            "stageOptions": ["Planning", "Validation", "Review", "Launch"],
        }
    )


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.post("/project-templates", summary="新建项目模板")
def create_project_template(payload: dict[str, Any] = Body(...)):
    payload["id"] = _mock.make_id("project_template")
    payload["createdAt"] = _mock.now_iso()
    return _mock.api_response({"template": payload})


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.put("/project-templates/{templateId}", summary="编辑项目模板")
def update_project_template(templateId: str, payload: dict[str, Any] = Body(...)):
    payload["id"] = templateId
    payload["updatedAt"] = _mock.now_iso()
    return _mock.api_response({"template": payload})


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.delete("/project-templates/{templateId}", summary="删除项目模板")
def delete_project_template(templateId: str):
    return _mock.api_response({"templateId": templateId, "deleted": True, "deletedAt": _mock.now_iso()})
