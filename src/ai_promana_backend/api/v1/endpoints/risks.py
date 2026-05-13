from typing import Any

from fastapi import APIRouter, Body

from ai_promana_backend.api.v1.endpoints import _mock


router = APIRouter()


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.get("/{projectId}/risks/page-data", summary="风险页聚合数据")
def get_project_risks_page(projectId: str):
    return _mock.api_response(
        {
            "project": _mock.project_lite(projectId),
            "summary": {
                "open": len([item for item in _mock.risks() if item["status"] == "open"]),
                "processing": len([item for item in _mock.risks() if item["status"] == "processing"]),
                "highOrCritical": len([item for item in _mock.risks() if item["level"] in {"high", "critical"}]),
                "updatedAt": _mock.now_iso(),
            },
            "resourceHeatmap": [
                {"resource": "Lab A", "date": "2026-05-12", "level": "high"},
                {"resource": "Reviewer", "date": "2026-05-13", "level": "medium"},
            ],
            "risks": _mock.risks(),
            "filters": {
                "levels": ["low", "medium", "high", "critical"],
                "statuses": ["open", "processing", "mitigated", "closed"],
                "owners": _mock.users(),
            },
            "aiInsights": _mock.ai_suggestions("risk"),
        }
    )


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.post("/{projectId}/risks", summary="新建风险")
def create_project_risk(projectId: str, payload: dict[str, Any] = Body(...)):
    risk = {
        "id": _mock.make_id("risk"),
        "projectId": projectId,
        "title": payload.get("title", "Untitled risk"),
        "level": payload.get("level", "medium"),
        "status": payload.get("status", "open"),
        "ownerId": payload.get("ownerId", "u_10001"),
        "impact": payload.get("impact"),
        "mitigation": payload.get("mitigation"),
        "createdAt": _mock.now_iso(),
    }
    return _mock.api_response({"risk": risk})


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.put("/{projectId}/risks/{riskId}", summary="更新风险")
def update_project_risk(projectId: str, riskId: str, payload: dict[str, Any] = Body(...)):
    return _mock.api_response({"projectId": projectId, "riskId": riskId, "risk": payload, "updatedAt": _mock.now_iso()})


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.post("/{projectId}/risks/{riskId}/transition", summary="风险状态流转")
def transition_project_risk(projectId: str, riskId: str, payload: dict[str, Any] = Body(...)):
    return _mock.api_response(
        {
            "projectId": projectId,
            "riskId": riskId,
            "status": payload.get("toStatus", payload.get("status", "processing")),
            "handledAt": _mock.now_iso(),
        }
    )


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.post("/{projectId}/risks/batch-resolve", summary="批量处理风险")
def batch_resolve_project_risks(projectId: str, payload: dict[str, Any] = Body(...)):
    return _mock.api_response(
        {
            "projectId": projectId,
            "riskIds": payload.get("riskIds", []),
            "status": payload.get("status", "mitigated"),
            "resolvedAt": _mock.now_iso(),
        }
    )


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.post("/{projectId}/risks/export", summary="导出风险清单")
def export_project_risks(projectId: str, payload: dict[str, Any] | None = Body(default=None)):
    task = _mock.export_task("risk_export")
    task["projectId"] = projectId
    task["filters"] = payload or {}
    return _mock.api_response(task)
