from typing import Any

from fastapi import APIRouter, Body

from ai_promana_backend.api.v1.endpoints import _mock


router = APIRouter()


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.get("/permission-matrix", summary="平台/项目权限矩阵")
def get_permission_matrix():
    return _mock.api_response(
        {
            "platformMatrix": _mock.platform_matrix(),
            "projectMatrix": _mock.project_matrix(),
            "roles": ["super_admin", "admin", "pm", "developer", "qa", "product", "collaborator", "user"],
            "projectRoles": ["owner", "developer", "qa", "product", "collaborator"],
        }
    )


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.post("/permission-matrix/export", summary="导出矩阵")
def export_permission_matrix(payload: dict[str, Any] | None = Body(default=None)):
    task = _mock.export_task("permission_matrix_export")
    task["filters"] = payload or {}
    return _mock.api_response(task)


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.get("/role-templates", summary="角色模板列表")
def list_role_templates():
    return _mock.api_response(
        {
            "templates": _mock.role_templates(),
            "platformMatrix": _mock.platform_matrix(),
            "projectMatrix": _mock.project_matrix(),
            "visiblePageOptions": [
                {"label": "Overview", "value": "overview"},
                {"label": "Kanban", "value": "kanban"},
                {"label": "Gantt", "value": "gantt"},
                {"label": "Risk", "value": "risk"},
                {"label": "Members", "value": "members"},
                {"label": "Reports", "value": "reports"},
                {"label": "Docs", "value": "docs"},
            ],
            "actionOptions": [
                {"label": "Create task", "value": "create-task"},
                {"label": "Assign owner", "value": "assign-owner"},
                {"label": "Edit milestone", "value": "edit-milestone"},
                {"label": "Set baseline", "value": "set-baseline"},
                {"label": "Drag gantt", "value": "drag-gantt"},
                {"label": "Invite member", "value": "invite-member"},
                {"label": "Export report", "value": "export-report"},
            ],
        }
    )


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.get("/role-templates/{templateId}", summary="角色模板详情")
def get_role_template(templateId: str):
    template = next((item for item in _mock.role_templates() if item["id"] == templateId), _mock.role_templates()[0])
    template["id"] = templateId
    return _mock.api_response({"template": template})


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.post("/role-templates", summary="新建角色模板")
def create_role_template(payload: dict[str, Any] = Body(...)):
    payload["id"] = _mock.make_id("role_template")
    payload["createdAt"] = _mock.now_iso()
    return _mock.api_response({"template": payload})


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.put("/role-templates/{templateId}", summary="更新角色模板")
def update_role_template(templateId: str, payload: dict[str, Any] = Body(...)):
    payload["id"] = templateId
    payload["updatedAt"] = _mock.now_iso()
    return _mock.api_response({"template": payload})


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.post("/role-templates/{templateId}/copy", summary="模板另存为")
def copy_role_template(templateId: str, payload: dict[str, Any] | None = Body(default=None)):
    copied = next((item for item in _mock.role_templates() if item["id"] == templateId), _mock.role_templates()[0])
    copied["id"] = _mock.make_id("role_template")
    copied["title"] = (payload or {}).get("title", f"{copied['title']} Copy")
    copied["createdAt"] = _mock.now_iso()
    return _mock.api_response({"template": copied})
