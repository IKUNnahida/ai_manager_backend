from typing import Any

from fastapi import APIRouter, Body, Query

from ai_promana_backend.api.v1.endpoints import _mock


router = APIRouter()


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.get("/{projectId}/members/page-data", summary="成员页聚合数据")
def get_project_members_page(projectId: str):
    return _mock.api_response(
        {
            "project": _mock.project_lite(projectId),
            "summary": {
                "totalMembers": len(_mock.members()),
                "activeMembers": len([item for item in _mock.members() if item["status"] == "active"]),
                "averageWorkload": 68,
                "updatedAt": _mock.now_iso(),
            },
            "members": _mock.members(),
            "inviteFlow": {
                "steps": ["select-user", "assign-role", "send-notice"],
                "defaultRole": "collaborator",
            },
            "heatmap": [
                {"memberId": "u_10001", "date": "2026-05-12", "load": 7},
                {"memberId": "u_10002", "date": "2026-05-12", "load": 8},
                {"memberId": "u_10003", "date": "2026-05-12", "load": 6},
            ],
            "filters": {
                "roles": ["owner", "developer", "qa", "product", "collaborator"],
                "statuses": ["active", "pending", "disabled"],
            },
            "aiSuggestions": _mock.ai_suggestions("members"),
        }
    )


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.get("/{projectId}/member-candidates", summary="可邀请成员搜索")
def search_member_candidates(
    projectId: str,
    keyword: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    pageSize: int = Query(default=20, ge=1, le=100),
):
    candidates = _mock.users()
    if keyword:
        lowered = keyword.lower()
        candidates = [
            item
            for item in candidates
            if lowered in item["name"].lower() or lowered in item["email"].lower()
        ]
    return _mock.api_response(_mock.paged(candidates, page, pageSize))


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.post("/{projectId}/member-invitations", summary="邀请成员")
def invite_project_members(projectId: str, payload: dict[str, Any] = Body(...)):
    return _mock.api_response(
        {
            "projectId": projectId,
            "invitationId": _mock.make_id("member_invitation"),
            "memberIds": payload.get("memberIds", []),
            "role": payload.get("role", "collaborator"),
            "status": "sent",
        }
    )


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.patch("/{projectId}/members/{memberId}", summary="调整成员角色/状态")
def update_project_member(projectId: str, memberId: str, payload: dict[str, Any] = Body(...)):
    return _mock.api_response(
        {
            "projectId": projectId,
            "memberId": memberId,
            "role": payload.get("role"),
            "status": payload.get("status"),
            "updatedAt": _mock.now_iso(),
        }
    )


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.delete("/{projectId}/members/{memberId}", summary="移除成员")
def remove_project_member(projectId: str, memberId: str):
    return _mock.api_response({"projectId": projectId, "memberId": memberId, "removed": True})
