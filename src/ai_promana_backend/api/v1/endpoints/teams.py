from fastapi import APIRouter, Query

from ai_promana_backend.api.v1.endpoints import _mock


router = APIRouter()


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.get("", summary="团队列表")
def list_teams(keyword: str | None = Query(default=None)):
    teams = _mock.option_items()["teams"]
    if keyword:
        lowered = keyword.lower()
        teams = [item for item in teams if lowered in item["label"].lower()]
    return _mock.api_response(teams)


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.get("/{teamId}/members", summary="团队成员")
def list_team_members(teamId: str):
    return _mock.api_response({"teamId": teamId, "members": _mock.users()})
