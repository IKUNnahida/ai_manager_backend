from copy import deepcopy
from datetime import datetime, timedelta, timezone
from typing import Any


# TODO: 后续接入真实数据库、service/repository 和权限体系后，移除这些首版联调用 mock 数据。
CN_TZ = timezone(timedelta(hours=8))


def now_iso() -> str:
    return datetime.now(CN_TZ).isoformat(timespec="seconds")


def today() -> str:
    return datetime.now(CN_TZ).date().isoformat()


def make_id(prefix: str) -> str:
    return f"{prefix}_{datetime.now(CN_TZ).strftime('%Y%m%d%H%M%S')}"


def api_response(data: Any = None, message: str = "success") -> dict[str, Any]:
    return {
        "code": 0,
        "message": message,
        "data": {} if data is None else data,
        "requestId": make_id("req"),
        "timestamp": now_iso(),
    }


def paged(items: list[dict[str, Any]], page: int = 1, page_size: int = 20) -> dict[str, Any]:
    safe_page = max(page, 1)
    safe_page_size = min(max(page_size, 1), 100)
    start = (safe_page - 1) * safe_page_size
    return {
        "list": deepcopy(items[start : start + safe_page_size]),
        "page": safe_page,
        "pageSize": safe_page_size,
        "total": len(items),
    }


def export_task(prefix: str = "export") -> dict[str, Any]:
    return {"taskId": make_id(prefix), "status": "pending", "downloadUrl": None}


CURRENT_USER: dict[str, Any] = {
    "id": "u_10001",
    "username": "zhanggong",
    "name": "Zhang Gong",
    "nickname": "Zhang",
    "avatar": "https://example.com/avatar.png",
    "platformRole": "admin",
    "department": "R&D Center",
    "position": "R&D Director",
    "permissions": [
        "admin:access",
        "project:create",
        "project:read",
        "project:update",
        "task:create",
        "task:update",
        "report:export",
    ],
}


USERS: list[dict[str, Any]] = [
    {
        "id": "u_10001",
        "name": "Zhang Gong",
        "email": "zhang@example.com",
        "department": "R&D Center",
        "platformRole": "admin",
        "platformRoleLabel": "Admin",
        "status": "active",
        "joinDate": "2026-04-01",
    },
    {
        "id": "u_10002",
        "name": "Chen Siyuan",
        "email": "chen@example.com",
        "department": "Material Science",
        "platformRole": "developer",
        "platformRoleLabel": "Developer",
        "status": "active",
        "joinDate": "2026-04-08",
    },
    {
        "id": "u_10003",
        "name": "Wang Yating",
        "email": "wang@example.com",
        "department": "Quality Lab",
        "platformRole": "qa",
        "platformRoleLabel": "QA",
        "status": "pending",
        "joinDate": "2026-05-12",
    },
]


MEMBERS: list[dict[str, Any]] = [
    {
        "id": "member_001",
        "userId": "u_10001",
        "name": "Zhang Gong",
        "avatar": "https://example.com/avatar-1.png",
        "role": "owner",
        "status": "active",
        "workload": 74,
        "taskCount": 8,
    },
    {
        "id": "member_002",
        "userId": "u_10002",
        "name": "Chen Siyuan",
        "avatar": "https://example.com/avatar-2.png",
        "role": "developer",
        "status": "active",
        "workload": 68,
        "taskCount": 11,
    },
    {
        "id": "member_003",
        "userId": "u_10003",
        "name": "Wang Yating",
        "avatar": "https://example.com/avatar-3.png",
        "role": "qa",
        "status": "active",
        "workload": 61,
        "taskCount": 6,
    },
]


PROJECTS: list[dict[str, Any]] = [
    {
        "id": "project_001",
        "code": "RD-2026-001",
        "name": "Nano Crystal Structure Optimization",
        "status": "active",
        "health": "good",
        "progress": 72,
        "ownerId": "u_10001",
        "ownerName": "Zhang Gong",
        "teamId": "team_material",
        "teamName": "Material Science",
        "memberCount": 12,
        "startDate": "2026-04-14",
        "endDate": "2026-05-16",
        "tags": ["iteration", "validation"],
        "ownerAvatar": "https://example.com/avatar-1.png",
        "activeMemberAvatars": [
            "https://example.com/avatar-1.png",
            "https://example.com/avatar-2.png",
            "https://example.com/avatar-3.png",
        ],
        "templateName": "Requirement Iteration",
        "riskCount": 3,
        "defaultView": "overview",
    },
    {
        "id": "project_002",
        "code": "RD-2026-018",
        "name": "Thermal Stability Verification",
        "status": "active",
        "health": "attention",
        "progress": 48,
        "ownerId": "u_10002",
        "ownerName": "Chen Siyuan",
        "teamId": "team_material",
        "teamName": "Material Science",
        "memberCount": 8,
        "startDate": "2026-05-01",
        "endDate": "2026-06-10",
        "tags": ["thermal", "samples"],
        "ownerAvatar": "https://example.com/avatar-2.png",
        "activeMemberAvatars": [
            "https://example.com/avatar-2.png",
            "https://example.com/avatar-3.png",
        ],
        "templateName": "Verification Project",
        "riskCount": 5,
        "defaultView": "kanban",
    },
    {
        "id": "project_003",
        "code": "RD-2026-026",
        "name": "Automated Lab Data Pipeline",
        "status": "pending",
        "health": "good",
        "progress": 12,
        "ownerId": "u_10001",
        "ownerName": "Zhang Gong",
        "teamId": "team_platform",
        "teamName": "Platform Engineering",
        "memberCount": 5,
        "startDate": "2026-05-20",
        "endDate": "2026-07-02",
        "tags": ["automation", "data"],
        "ownerAvatar": "https://example.com/avatar-1.png",
        "activeMemberAvatars": ["https://example.com/avatar-1.png"],
        "templateName": "Platform Delivery",
        "riskCount": 1,
        "defaultView": "gantt",
    },
]


TASKS: list[dict[str, Any]] = [
    {
        "id": "task_001",
        "title": "Backfill integration environment parameters",
        "status": "blocked",
        "columnKey": "blocked",
        "priority": "p0",
        "projectId": "project_001",
        "projectName": "Nano Crystal Structure Optimization",
        "assigneeId": "u_10002",
        "assigneeName": "Chen Siyuan",
        "reviewerId": "u_10003",
        "reviewerName": "Wang Yating",
        "progress": 62,
        "startDate": today(),
        "dueAt": now_iso(),
        "estimatedHours": 12,
        "blockedReason": "Environment window is not confirmed",
        "tags": ["integration", "PBC"],
    },
    {
        "id": "task_002",
        "title": "Complete abnormal sample notes",
        "status": "in_progress",
        "columnKey": "doing",
        "priority": "p2",
        "projectId": "project_001",
        "projectName": "Nano Crystal Structure Optimization",
        "assigneeId": "u_10001",
        "assigneeName": "Zhang Gong",
        "reviewerId": "u_10003",
        "reviewerName": "Wang Yating",
        "progress": 35,
        "startDate": today(),
        "dueAt": now_iso(),
        "estimatedHours": 8,
        "blockedReason": None,
        "tags": ["report"],
    },
    {
        "id": "task_003",
        "title": "Review phase-one stability report",
        "status": "review",
        "columnKey": "review",
        "priority": "p1",
        "projectId": "project_002",
        "projectName": "Thermal Stability Verification",
        "assigneeId": "u_10003",
        "assigneeName": "Wang Yating",
        "reviewerId": "u_10001",
        "reviewerName": "Zhang Gong",
        "progress": 90,
        "startDate": "2026-05-10",
        "dueAt": now_iso(),
        "estimatedHours": 6,
        "blockedReason": None,
        "tags": ["review"],
    },
]


RISKS: list[dict[str, Any]] = [
    {
        "id": "risk_001",
        "title": "Key equipment schedule conflict",
        "level": "high",
        "status": "open",
        "ownerId": "u_10001",
        "ownerName": "Zhang Gong",
        "impact": "Integration validation may slip by two days",
        "mitigation": "Reserve fallback lab slot",
        "relatedTaskId": "task_001",
        "createdAt": now_iso(),
    },
    {
        "id": "risk_002",
        "title": "Sample batch has incomplete metadata",
        "level": "medium",
        "status": "processing",
        "ownerId": "u_10003",
        "ownerName": "Wang Yating",
        "impact": "Report confidence may be reduced",
        "mitigation": "Add manual verification checklist",
        "relatedTaskId": "task_002",
        "createdAt": now_iso(),
    },
]


DOCUMENTS: list[dict[str, Any]] = [
    {
        "id": "doc_001",
        "title": "Project Kickoff Notes",
        "type": "markdown",
        "status": "active",
        "ownerId": "u_10001",
        "ownerName": "Zhang Gong",
        "updatedAt": now_iso(),
        "tags": ["kickoff"],
    },
    {
        "id": "doc_002",
        "title": "Validation Checklist",
        "type": "spreadsheet",
        "status": "active",
        "ownerId": "u_10003",
        "ownerName": "Wang Yating",
        "updatedAt": now_iso(),
        "tags": ["qa"],
    },
]


NOTIFICATIONS: list[dict[str, Any]] = [
    {
        "id": "notice_001",
        "title": "Blocked task needs attention",
        "content": "Integration environment parameters are blocked.",
        "category": "pending",
        "status": "pending",
        "read": False,
        "createdAt": now_iso(),
        "targetPath": "/project/project_001/kanban",
    },
    {
        "id": "notice_002",
        "title": "Weekly report is ready",
        "content": "The latest project report has been generated.",
        "category": "system",
        "status": "completed",
        "read": True,
        "createdAt": now_iso(),
        "targetPath": "/reports",
    },
]


ROLE_TEMPLATES: list[dict[str, Any]] = [
    {
        "id": "role_template_pm",
        "title": "PM Template",
        "scope": "project",
        "description": "Project owner default permissions",
        "visiblePages": ["overview", "kanban", "gantt", "risk", "members", "reports"],
        "actions": [
            "create-task",
            "assign-owner",
            "edit-milestone",
            "set-baseline",
            "drag-gantt",
            "invite-member",
            "export-report",
        ],
    },
    {
        "id": "role_template_member",
        "title": "Member Template",
        "scope": "project",
        "description": "Project collaborator default permissions",
        "visiblePages": ["overview", "kanban", "docs"],
        "actions": ["create-task", "comment-task"],
    },
]


PROJECT_TEMPLATES: list[dict[str, Any]] = [
    {
        "id": "template_requirement_iteration",
        "name": "Requirement Iteration",
        "description": "Default structure for iterative R&D delivery",
        "enabledPages": ["overview", "members", "kanban", "gantt", "risk", "reports", "docs"],
        "defaultStages": ["Planning", "Validation", "Review"],
        "active": True,
    },
    {
        "id": "template_platform_delivery",
        "name": "Platform Delivery",
        "description": "Template for platform engineering work",
        "enabledPages": ["overview", "kanban", "gantt", "docs"],
        "defaultStages": ["Design", "Build", "Launch"],
        "active": True,
    },
]


def current_user() -> dict[str, Any]:
    return deepcopy(CURRENT_USER)


def users() -> list[dict[str, Any]]:
    return deepcopy(USERS)


def project_lite(project_id: str = "project_001") -> dict[str, Any]:
    project = next((item for item in PROJECTS if item["id"] == project_id), PROJECTS[0])
    return deepcopy(project)


def projects() -> list[dict[str, Any]]:
    return deepcopy(PROJECTS)


def task_lite(task_id: str = "task_001") -> dict[str, Any]:
    task = next((item for item in TASKS if item["id"] == task_id), TASKS[0])
    result = deepcopy(task)
    result["id"] = task_id
    return result


def tasks(project_id: str | None = None) -> list[dict[str, Any]]:
    items = TASKS if project_id is None else [item for item in TASKS if item["projectId"] == project_id]
    return deepcopy(items)


def members() -> list[dict[str, Any]]:
    return deepcopy(MEMBERS)


def risks() -> list[dict[str, Any]]:
    return deepcopy(RISKS)


def documents() -> list[dict[str, Any]]:
    return deepcopy(DOCUMENTS)


def notifications() -> list[dict[str, Any]]:
    return deepcopy(NOTIFICATIONS)


def role_templates() -> list[dict[str, Any]]:
    return deepcopy(ROLE_TEMPLATES)


def project_templates() -> list[dict[str, Any]]:
    return deepcopy(PROJECT_TEMPLATES)


def option_items() -> dict[str, list[dict[str, Any]]]:
    return {
        "teams": [
            {"id": "team_material", "label": "Material Science", "value": "team_material", "extra": {}},
            {"id": "team_platform", "label": "Platform Engineering", "value": "team_platform", "extra": {}},
        ],
        "owners": [
            {"id": item["id"], "label": item["name"], "value": item["id"], "extra": item}
            for item in USERS
        ],
        "statuses": [
            {"id": "pending", "label": "Pending", "value": "pending", "extra": {}},
            {"id": "active", "label": "Active", "value": "active", "extra": {}},
            {"id": "paused", "label": "Paused", "value": "paused", "extra": {}},
            {"id": "completed", "label": "Completed", "value": "completed", "extra": {}},
            {"id": "archived", "label": "Archived", "value": "archived", "extra": {}},
        ],
        "health": [
            {"id": "good", "label": "Good", "value": "good", "extra": {}},
            {"id": "attention", "label": "Attention", "value": "attention", "extra": {}},
            {"id": "risk", "label": "Risk", "value": "risk", "extra": {}},
            {"id": "completed", "label": "Completed", "value": "completed", "extra": {}},
        ],
    }


def ai_suggestions(scope: str) -> list[dict[str, Any]]:
    return [
        {
            "id": f"{scope}_suggestion_001",
            "title": "Prioritize blocked work",
            "summary": "Focus on the blocked integration task before adding more scope.",
            "confidence": 0.86,
            "action": "create_follow_up",
        },
        {
            "id": f"{scope}_suggestion_002",
            "title": "Notify reviewers earlier",
            "summary": "Reviewer load is rising; send review reminders one day earlier.",
            "confidence": 0.79,
            "action": "notify_reviewers",
        },
    ]


def platform_matrix() -> list[dict[str, Any]]:
    return [
        {"permission": "admin:access", "super_admin": True, "admin": True, "user": False},
        {"permission": "project:create", "super_admin": True, "admin": True, "user": False},
        {"permission": "report:export", "super_admin": True, "admin": True, "user": False},
    ]


def project_matrix() -> list[dict[str, Any]]:
    return [
        {"permission": "task:create", "owner": True, "developer": True, "qa": True},
        {"permission": "task:update", "owner": True, "developer": True, "qa": False},
        {"permission": "project:baseline", "owner": True, "developer": False, "qa": False},
    ]
