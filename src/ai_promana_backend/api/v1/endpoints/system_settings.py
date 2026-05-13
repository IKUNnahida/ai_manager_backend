from typing import Any

from fastapi import APIRouter, Body

from ai_promana_backend.api.v1.endpoints import _mock


settings_router = APIRouter()
admin_router = APIRouter()
ai_router = APIRouter()


DEFAULT_SETTINGS: dict[str, Any] = {
    "siteNotice": True,
    "wecomPush": True,
    "emailSubscription": False,
    "auditTrail": True,
    "maskSensitiveData": True,
}


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@settings_router.get("/me", summary="设置页首屏数据")
def get_my_settings():
    return _mock.api_response(
        {
            "profile": {
                "name": _mock.current_user()["name"],
                "department": _mock.current_user()["department"],
                "email": "zhang@example.com",
                "phone": "13800000000",
            },
            "notifications": {
                "taskStatus": True,
                "logFeedback": True,
                "reportSubscription": "weekly",
            },
            "sessions": [
                {
                    "id": "session_001",
                    "device": "Windows Edge",
                    "ip": "127.0.0.1",
                    "lastActiveAt": _mock.now_iso(),
                    "current": True,
                }
            ],
            "securityHints": [
                {"id": "hint_001", "level": "info", "message": "Password was updated recently."}
            ],
            "aiSuggestions": _mock.ai_suggestions("settings"),
        }
    )


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@settings_router.put("/me", summary="保存个人设置")
def update_my_settings(payload: dict[str, Any] = Body(...)):
    payload["updatedAt"] = _mock.now_iso()
    return _mock.api_response(payload)


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@settings_router.post("/reset", summary="恢复默认设置")
def reset_my_settings():
    return _mock.api_response({"profile": {}, "notifications": DEFAULT_SETTINGS, "resetAt": _mock.now_iso()})


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@settings_router.post("/change-password", summary="修改密码")
def change_password(payload: dict[str, Any] = Body(...)):
    return _mock.api_response({"changed": True, "changedAt": _mock.now_iso(), "needRelogin": True})


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@settings_router.get("/sessions", summary="设备会话列表")
def list_sessions():
    return _mock.api_response(
        [
            {
                "id": "session_001",
                "device": "Windows Edge",
                "ip": "127.0.0.1",
                "lastActiveAt": _mock.now_iso(),
                "current": True,
            },
            {
                "id": "session_002",
                "device": "Mobile Safari",
                "ip": "10.0.0.8",
                "lastActiveAt": "2026-05-12T18:30:00+08:00",
                "current": False,
            },
        ]
    )


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@settings_router.delete("/sessions/{sessionId}", summary="下线某设备")
def revoke_session(sessionId: str):
    return _mock.api_response({"sessionId": sessionId, "revoked": True, "revokedAt": _mock.now_iso()})


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@admin_router.get("/system-config", summary="系统配置读取")
def get_system_config():
    return _mock.api_response(
        {
            "currentUser": _mock.current_user(),
            "settings": DEFAULT_SETTINGS,
            "groups": [
                {
                    "key": "notification",
                    "title": "Notification",
                    "fields": ["siteNotice", "wecomPush", "emailSubscription"],
                },
                {
                    "key": "security",
                    "title": "Security",
                    "fields": ["auditTrail", "maskSensitiveData"],
                },
            ],
            "defaults": DEFAULT_SETTINGS,
        }
    )


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@admin_router.put("/system-config", summary="系统配置保存")
def update_system_config(payload: dict[str, Any] = Body(...)):
    payload["updatedAt"] = _mock.now_iso()
    return _mock.api_response(payload)


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@admin_router.post("/system-config/reset", summary="恢复默认配置")
def reset_system_config():
    return _mock.api_response({"settings": DEFAULT_SETTINGS, "resetAt": _mock.now_iso()})


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@ai_router.get("/settings-suggestions", summary="AI 偏好建议")
def get_ai_settings_suggestions():
    return _mock.api_response({"suggestions": _mock.ai_suggestions("settings")})


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@ai_router.post("/settings-suggestions/{suggestionId}/apply", summary="采纳 AI 偏好建议")
def apply_ai_settings_suggestion(suggestionId: str, payload: dict[str, Any] | None = Body(default=None)):
    return _mock.api_response({"suggestionId": suggestionId, "applied": True, "payload": payload or {}})
