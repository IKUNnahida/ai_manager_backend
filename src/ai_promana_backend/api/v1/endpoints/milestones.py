from typing import Any

from fastapi import APIRouter, Body

from ai_promana_backend.api.v1.endpoints import _mock
from ai_promana_backend.api.v1.endpoints.projects import gantt_items


router = APIRouter()


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.get("/{projectId}/gantt/page-data", summary="甘特页聚合数据")
def get_project_gantt_page(projectId: str):
    project = _mock.project_lite(projectId)
    return _mock.api_response(
        {
            "project": project,
            "summary": {
                "startDate": project["startDate"],
                "endDate": project["endDate"],
                "progress": project["progress"],
                "baselineCount": 2,
            },
            "timeline": {"start": project["startDate"], "end": project["endDate"], "unit": "day"},
            "items": gantt_items(projectId),
            "baselines": [
                {"id": "baseline_001", "name": "Initial baseline", "createdAt": "2026-04-14T09:00:00+08:00"},
                {"id": "baseline_002", "name": "Integration baseline", "createdAt": "2026-05-01T09:00:00+08:00"},
            ],
            "dependencies": [
                {"id": "dep_001", "sourceId": "task_001", "targetId": "task_002", "type": "finish_to_start"}
            ],
            "aiSuggestions": _mock.ai_suggestions("gantt"),
        }
    )


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.patch("/{projectId}/schedule/items/{itemId}", summary="更新排期")
def update_schedule_item(projectId: str, itemId: str, payload: dict[str, Any] = Body(...)):
    return _mock.api_response({"projectId": projectId, "itemId": itemId, "schedule": payload, "updatedAt": _mock.now_iso()})


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.get("/{projectId}/baselines", summary="获取基线列表")
def list_project_baselines(projectId: str):
    return _mock.api_response(
        [
            {"id": "baseline_001", "projectId": projectId, "name": "Initial baseline", "createdAt": "2026-04-14T09:00:00+08:00"},
            {"id": "baseline_002", "projectId": projectId, "name": "Integration baseline", "createdAt": "2026-05-01T09:00:00+08:00"},
        ]
    )


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.put("/{projectId}/dependencies", summary="保存任务依赖")
def save_project_dependencies(projectId: str, payload: dict[str, Any] = Body(...)):
    return _mock.api_response({"projectId": projectId, "dependencies": payload.get("dependencies", []), "updatedAt": _mock.now_iso()})
