# 后端接口主文档

> 文档定位：当前项目后端接口的唯一实施依据  
> 生效日期：2026-05-12  
> 适用范围：`src/router/index.js` 中当前已启用的全部路由页面

## 1. 目标

本文件用于把当前前端界面设计、已存在的页面草稿文档和接口 TODO 统一收口为一套后端可直接实现的接口契约，避免以下问题：

- 同一个页面存在多份草稿，接口口径不一致
- 接口清单有定义，但没有请求/响应结构
- 路由已启用，但没有对应后端对接文档
- 前端 mock 状态值与数据库/后端状态值不统一

本文件的设计原则：

- 读接口尽量按页面聚合，减少首屏多请求
- 写接口按业务动作拆分，保证职责清晰
- 统一返回结构、统一分页、统一时间格式、统一枚举值
- 前端展示文案允许映射，但后端返回值必须固定

## 2. 路由覆盖矩阵

| 路由 | 前端文件 | 后端模块 |
| --- | --- | --- |
| `/login` | `src/views/Login.vue` | 认证 |
| `/register` | `src/views/Register.vue` | 认证 |
| `/dashboard` | `src/views/Dashboard.vue` | 工作台 / AI 简报 / 项目创建 |
| `/projects` | `src/views/Projects.vue` | 项目矩阵 / 项目创建 |
| `/workbench` | `src/views/Workbench.vue` | 个人工作台 / 任务草稿 / PBC |
| `/reports` | `src/views/Reports.vue` | 全局报表 |
| `/settings` | `src/views/Settings.vue` | 个人设置 / 安全设置 |
| `/notifications` | `src/views/Notifications.vue` | 通知中心 |
| `/admin` | `src/views/admin/AdminHome.vue` | 后台首页 |
| `/admin/users` | `src/views/admin/AdminUsers.vue` | 用户管理 |
| `/admin/roles` | `src/views/admin/AdminRoles.vue` | 角色模板 / 权限矩阵 |
| `/admin/project-templates` | `src/views/admin/AdminProjectTemplates.vue` | 项目模板管理 |
| `/admin/logs` | `src/views/admin/AdminLogs.vue` | 审计日志 |
| `/admin/system` | `src/views/admin/AdminSystem.vue` | 系统配置 |
| `/project/:id` | `src/views/ProjectDetail.vue` | 项目详情 / 项目概览 |
| `/project/:id/:tab` | `src/views/ProjectDetail.vue` | 项目成员 / 看板 / 甘特 / 风险 / 报表 / 文档 |
| `/task/:id` | `src/views/TaskDetail.vue` | 任务详情 / 评论 / AI 建议 |

## 3. 统一实现约定

### 3.1 接口前缀

- 统一使用 `/api`

### 3.2 统一响应结构

```json
{
  "code": 0,
  "message": "success",
  "data": {},
  "requestId": "req_20260512_0001",
  "timestamp": "2026-05-12T10:30:00+08:00"
}
```

说明：

- `code = 0` 表示成功
- 非 0 由业务错误码定义
- `timestamp` 使用 ISO 8601，带时区
- 对于文件导出、导入预览等耗时任务，允许返回异步任务 ID

### 3.3 鉴权约定

- 默认所有接口都需要登录态
- 免登录接口仅有：
  - `POST /api/auth/login`
  - `POST /api/auth/register`
  - `POST /api/auth/refresh`
  - `GET /api/auth/providers`
  - `POST /api/auth/social/start`
  - `POST /api/auth/social/confirm`

### 3.4 分页约定

统一分页请求参数：

- `page`: 从 `1` 开始
- `pageSize`: 默认 `20`，最大 `100`

统一分页响应：

```json
{
  "list": [],
  "page": 1,
  "pageSize": 20,
  "total": 0
}
```

### 3.5 排序约定

- `sortField`: 字段名
- `sortOrder`: `asc` / `desc`

### 3.6 导出约定

导出类接口统一返回任务结构：

```json
{
  "taskId": "export_001",
  "status": "pending",
  "downloadUrl": null
}
```

首期允许同步导出；如果改为异步，响应结构不变。

### 3.7 ID 与时间

- 对前端统一返回字符串 ID
- 数据库内部可以继续使用自增整数
- 日期字段统一返回：
  - 纯日期：`YYYY-MM-DD`
  - 日期时间：ISO 8601

## 4. 统一枚举口径

### 4.1 平台角色 `platformRole`

| 值 | 中文 |
| --- | --- |
| `super_admin` | 超级管理员 |
| `admin` | 管理员 |
| `pm` | 项目负责人 |
| `developer` | 研发 |
| `qa` | QA |
| `product` | 产品 |
| `collaborator` | 协作者 |
| `user` | 普通用户 |

### 4.2 用户状态 `userStatus`

| 值 | 中文 |
| --- | --- |
| `pending` | 待激活 |
| `active` | 正常 |
| `disabled` | 停用 |

### 4.3 项目状态 `projectStatus`

| 值 | 中文 |
| --- | --- |
| `pending` | 待启动 |
| `active` | 进行中 |
| `paused` | 已暂停 |
| `completed` | 已完成 |
| `archived` | 已归档 |

### 4.4 项目健康度 `projectHealth`

| 值 | 中文 |
| --- | --- |
| `good` | 良好 |
| `attention` | 需关注 |
| `risk` | 高风险 |
| `completed` | 已完成 |

### 4.5 任务状态 `taskStatus`

| 值 | 中文 | 前端列映射 |
| --- | --- | --- |
| `pending` | 待开始 | `todo` |
| `in_progress` | 进行中 | `doing` |
| `review` | 待评审 | `review` |
| `completed` | 已完成 | `done` |
| `blocked` | 已阻塞 | `blocked` |

说明：

- 后端返回的状态值统一使用上表左列
- 看板列如果需要单独标识，额外返回 `columnKey`

### 4.6 优先级 `priority`

| 值 | 中文 |
| --- | --- |
| `p0` | P0 |
| `p1` | P1 |
| `p2` | P2 |
| `p3` | P3 |

### 4.7 通知分类 `notificationCategory`

| 值 | 中文 |
| --- | --- |
| `pending` | 待处理 |
| `system` | 系统更新 |
| `ai` | AI 提醒 |
| `other` | 其他 |

### 4.8 通知处理状态 `notificationStatus`

| 值 | 中文 |
| --- | --- |
| `pending` | 待处理 |
| `completed` | 已完成 |

### 4.9 风险等级 `riskLevel`

| 值 | 中文 |
| --- | --- |
| `low` | 低 |
| `medium` | 中 |
| `high` | 高 |
| `critical` | 极高 |

### 4.10 风险状态 `riskStatus`

| 值 | 中文 |
| --- | --- |
| `open` | 待处理 |
| `processing` | 处理中 |
| `mitigated` | 已缓解 |
| `closed` | 已关闭 |

## 5. 共享对象

### 5.1 当前用户 `CurrentUser`

```json
{
  "id": "u_10001",
  "username": "zhanggong",
  "name": "张工",
  "nickname": "张工",
  "avatar": "https://example.com/avatar.png",
  "platformRole": "admin",
  "department": "研发中心",
  "position": "研发总监",
  "permissions": ["admin:access", "project:create"]
}
```

### 5.2 通用选项 `OptionItem`

```json
{
  "id": "team_material",
  "label": "材料科学部",
  "value": "team_material",
  "extra": {}
}
```

### 5.3 轻量任务 `TaskLite`

```json
{
  "id": "task_001",
  "title": "联调环境参数回灌",
  "status": "blocked",
  "columnKey": "blocked",
  "priority": "p0",
  "projectId": "project_001",
  "projectName": "纳米晶体结构优化",
  "assigneeId": "u_10002",
  "assigneeName": "陈思远",
  "reviewerId": "u_10003",
  "reviewerName": "王雅婷",
  "progress": 62,
  "startDate": "2026-05-12",
  "dueAt": "2026-05-13T18:00:00+08:00",
  "estimatedHours": 12,
  "blockedReason": "环境配置窗口未确认",
  "tags": ["联调", "PBC"]
}
```

### 5.4 轻量项目 `ProjectLite`

```json
{
  "id": "project_001",
  "code": "RD-2026-001",
  "name": "纳米晶体结构优化",
  "status": "active",
  "health": "good",
  "progress": 72,
  "ownerId": "u_10001",
  "ownerName": "王志强",
  "teamId": "team_material",
  "teamName": "材料科学部",
  "memberCount": 12,
  "startDate": "2026-04-14",
  "endDate": "2026-05-16",
  "tags": ["需求迭代", "联调验证"]
}
```

## 6. 核心请求体模型

### 6.1 登录请求 `LoginRequest`

```json
{
  "username": "zhanggong",
  "password": "******",
  "rememberMe": true
}
```

### 6.2 注册请求 `RegisterRequest`

```json
{
  "account": "RD0001",
  "name": "张工",
  "email": "zhang@example.com",
  "department": "研发中心",
  "password": "******",
  "confirmPassword": "******"
}
```

### 6.3 创建项目 `ProjectCreateRequest`

```json
{
  "name": "新型复合材料热稳定性验证",
  "code": "RD-2026-318",
  "teamId": "team_material",
  "ownerId": "u_10001",
  "estimatedMemberCount": 8,
  "templateId": "template_requirement_iteration",
  "startDate": "2026-05-20",
  "endDate": "2026-06-20",
  "status": "active",
  "health": "good",
  "initialProgress": 0,
  "priority": "p1",
  "riskSyncEnabled": true,
  "reportSubscriptionCycle": "weekly",
  "defaultView": "overview",
  "summary": "围绕热稳定性验证开展协同研发。",
  "tags": ["结构迭代", "性能验证"],
  "memberIds": ["u_10002", "u_10003"],
  "subscriberIds": ["u_10001", "u_10003"],
  "riskReminderFrequency": "daily",
  "initMode": "auto_structure",
  "enabledPages": ["overview", "members", "kanban", "gantt", "risk", "reports", "docs"],
  "notifyAllMembers": false
}
```

### 6.4 更新项目 `ProjectUpdateRequest`

```json
{
  "name": "纳米晶体结构优化",
  "ownerId": "u_10001",
  "teamId": "team_material",
  "startDate": "2026-04-14",
  "endDate": "2026-05-16",
  "status": "active",
  "health": "good",
  "progress": 72,
  "currentStage": "联调验证",
  "summary": "当前阶段集中处理联调验证中的时间偏差。",
  "memberIds": ["u_10001", "u_10002", "u_10003"],
  "subscriberIds": ["u_10001", "u_10003"],
  "enabledPages": ["overview", "members", "kanban", "gantt", "risk", "reports", "docs"],
  "version": 3
}
```

### 6.5 创建/编辑任务 `TaskUpsertRequest`

```json
{
  "title": "补充异常样本说明",
  "projectId": "project_001",
  "assigneeId": "u_10002",
  "reviewerId": "u_10003",
  "priority": "p2",
  "status": "pending",
  "startDate": "2026-05-12",
  "dueAt": "2026-05-13T18:00:00+08:00",
  "estimatedHours": 8,
  "progress": 0,
  "riskTag": "resource_risk",
  "description": "补齐联调验证中的说明文本。",
  "logSection": "tomorrow_plan",
  "pbcObjectiveId": "pbc_001",
  "notifyTargets": ["u_10001", "u_10003"],
  "tags": ["联调", "PBC"]
}
```

### 6.6 创建用户 `AdminUserCreateRequest`

```json
{
  "name": "李技术员",
  "email": "li@example.com",
  "department": "测试组",
  "joinDate": "2026-05-12",
  "platformRole": "user",
  "status": "pending",
  "note": "导入自 2026-05 新同事名单"
}
```

### 6.7 角色模板 `RoleTemplateRequest`

```json
{
  "title": "PM 模板",
  "scope": "project",
  "description": "项目负责人模板",
  "visiblePages": ["overview", "kanban", "gantt", "risk", "members", "reports"],
  "actions": ["create-task", "assign-owner", "edit-milestone", "set-baseline", "drag-gantt", "invite-member", "export-report"]
}
```

### 6.8 系统配置 `SystemConfigRequest`

```json
{
  "siteNotice": true,
  "wecomPush": true,
  "emailSubscription": false,
  "auditTrail": true,
  "maskSensitiveData": true
}
```

## 7. 接口总表

### 7.1 认证与账户

| 方法 | 路径 | 页面 | 用途 | 权限 |
| --- | --- | --- | --- | --- |
| `POST` | `/api/auth/login` | Login | 账号密码登录 | 免登录 |
| `POST` | `/api/auth/register` | Register | 注册 | 免登录 |
| `GET` | `/api/auth/me` | 全局通用 | 获取当前用户 | 登录 |
| `POST` | `/api/auth/refresh` | 全局通用 | 刷新会话 | 免登录 |
| `POST` | `/api/auth/logout` | 全局通用 | 退出登录 | 登录 |
| `GET` | `/api/auth/providers` | Login | 第三方登录方式 | 免登录 |
| `POST` | `/api/auth/social/start` | Login | 发起扫码/外部登录 | 免登录 |
| `POST` | `/api/auth/social/confirm` | Login | 第三方登录确认 | 免登录 |

### 7.2 工作台、搜索、通知

| 方法 | 路径 | 页面 | 用途 | 权限 |
| --- | --- | --- | --- | --- |
| `GET` | `/api/dashboard/overview` | Dashboard | 首屏聚合数据 | 登录 |
| `GET` | `/api/search` | Dashboard / Projects / Reports / Workbench | 全局搜索 | 登录 |
| `GET` | `/api/notifications/unread-count` | 全局通用 | 顶部未读角标 | 登录 |
| `POST` | `/api/ai/daily-report/generate` | Dashboard | 生成 AI 日报 | `ai:briefing:generate` |
| `GET` | `/api/ai/daily-report/latest` | Dashboard | 获取最新日报 | 登录 |
| `POST` | `/api/dashboard/morning-report/export` | Dashboard | 导出晨报 | `dashboard:briefing:export` |
| `GET` | `/api/notifications/summary` | Notifications | 通知统计 | 登录 |
| `GET` | `/api/notifications` | Notifications | 通知列表 | 登录 |
| `GET` | `/api/notifications/{notificationId}` | Notifications | 通知详情 | 登录 |
| `POST` | `/api/notifications/{notificationId}/read` | Notifications | 单条已读 | 登录 |
| `POST` | `/api/notifications/read-batch` | Notifications | 批量已读 | 登录 |
| `POST` | `/api/notifications/{notificationId}/handle` | Notifications | 处理通知动作 | 登录 |
| `GET` | `/api/notifications/process-advice` | Notifications | 处理建议面板 | 登录 |
| `GET` | `/api/notification-preferences/me` | Notifications / Settings | 获取通知偏好 | 登录 |
| `PUT` | `/api/notification-preferences/me` | Notifications / Settings | 保存通知偏好 | 登录 |
| `GET` | `/api/ai/notification-suggestions` | Notifications | AI 通知建议 | 登录 |
| `POST` | `/api/ai/notification-suggestions/{suggestionId}/apply` | Notifications | 采纳 AI 通知建议 | 登录 |

### 7.3 项目矩阵与项目创建

| 方法 | 路径 | 页面 | 用途 | 权限 |
| --- | --- | --- | --- | --- |
| `GET` | `/api/projects/summary` | Projects | 项目矩阵头部统计 | 登录 |
| `GET` | `/api/projects` | Projects | 项目列表、筛选、排序 | 登录 |
| `GET` | `/api/projects/create-options` | Dashboard / Projects | 新建项目弹窗字典 | `project:create` |
| `POST` | `/api/projects/drafts` | Dashboard / Projects | 保存项目草稿 | `project:create` |
| `POST` | `/api/projects` | Dashboard / Projects | 创建项目 | `project:create` |
| `GET` | `/api/ai/project-matrix-suggestions` | Projects | AI 项目建议 | 登录 |
| `POST` | `/api/ai/project-suggestions/{suggestionId}/apply` | Projects | 采纳项目建议 | 登录 |

### 7.4 项目详情与各 Tab

| 方法 | 路径 | 页面 | 用途 | 权限 |
| --- | --- | --- | --- | --- |
| `GET` | `/api/projects/{projectId}` | ProjectDetail + 所有 project tab | 头部信息、可用页签、权限 | `project:read` |
| `GET` | `/api/projects/{projectId}/overview` | ProjectDetail | 概览页聚合数据 | `project:read` |
| `GET` | `/api/projects/{projectId}/edit-form` | ProjectDetail | 编辑弹窗初始化 | `project:update` |
| `PUT` | `/api/projects/{projectId}` | ProjectDetail | 保存项目变更 | `project:update` |
| `POST` | `/api/projects/{projectId}/draft` | ProjectDetail | 保存编辑草稿 | `project:update` |
| `POST` | `/api/projects/{projectId}/archive` | ProjectDetail | 归档项目 | `project:archive` |
| `POST` | `/api/projects/{projectId}/baseline` | ProjectDetail / ProjectGantt | 设置项目基线 | `project:baseline` |
| `GET` | `/api/projects/{projectId}/members/page-data` | ProjectMembers | 成员页聚合数据 | `project:member:read` |
| `GET` | `/api/projects/{projectId}/member-candidates` | ProjectMembers | 可邀请成员搜索 | `project:member:update` |
| `POST` | `/api/projects/{projectId}/member-invitations` | ProjectMembers | 邀请成员 | `project:member:update` |
| `PATCH` | `/api/projects/{projectId}/members/{memberId}` | ProjectMembers | 调整成员角色/状态 | `project:member:update` |
| `DELETE` | `/api/projects/{projectId}/members/{memberId}` | ProjectMembers | 移除成员 | `project:member:update` |
| `GET` | `/api/projects/{projectId}/kanban/page-data` | ProjectKanban | 看板聚合数据 | `project:task:read` |
| `POST` | `/api/projects/{projectId}/tasks` | ProjectKanban | 在项目内创建任务 | `task:create` |
| `PUT` | `/api/projects/{projectId}/tasks/{taskId}` | ProjectKanban | 编辑任务 | `task:update` |
| `POST` | `/api/projects/{projectId}/tasks/{taskId}/transition` | ProjectKanban | 任务状态流转 | `task:update` |
| `PATCH` | `/api/projects/{projectId}/kanban/order` | ProjectKanban | 调整看板顺序 | `task:update` |
| `GET` | `/api/projects/{projectId}/gantt/page-data` | ProjectGantt | 甘特页聚合数据 | `project:schedule:read` |
| `PATCH` | `/api/projects/{projectId}/schedule/items/{itemId}` | ProjectGantt | 更新排期 | `project:schedule:update` |
| `GET` | `/api/projects/{projectId}/baselines` | ProjectGantt | 获取基线列表 | `project:baseline:read` |
| `PUT` | `/api/projects/{projectId}/dependencies` | ProjectGantt | 保存任务依赖 | `project:schedule:update` |
| `GET` | `/api/projects/{projectId}/risks/page-data` | ProjectRisk | 风险页聚合数据 | `project:risk:read` |
| `POST` | `/api/projects/{projectId}/risks` | ProjectRisk | 新建风险 | `project:risk:update` |
| `PUT` | `/api/projects/{projectId}/risks/{riskId}` | ProjectRisk | 更新风险 | `project:risk:update` |
| `POST` | `/api/projects/{projectId}/risks/{riskId}/transition` | ProjectRisk | 风险状态流转 | `project:risk:update` |
| `POST` | `/api/projects/{projectId}/risks/batch-resolve` | ProjectRisk | 批量处理风险 | `project:risk:update` |
| `POST` | `/api/projects/{projectId}/risks/export` | ProjectRisk | 导出风险清单 | `project:risk:export` |
| `GET` | `/api/projects/{projectId}/reports/page-data` | ProjectReports | 项目报表聚合数据 | `project:report:read` |
| `POST` | `/api/projects/{projectId}/reports/export` | ProjectReports | 导出项目报表 | `project:report:export` |
| `POST` | `/api/projects/{projectId}/reports/subscriptions` | ProjectReports | 订阅报表 | `project:report:subscribe` |
| `GET` | `/api/projects/{projectId}/docs/page-data` | ProjectDocs | 文档页聚合数据 | `project:doc:read` |
| `GET` | `/api/projects/{projectId}/docs/{docId}` | ProjectDocs | 文档详情 | `project:doc:read` |
| `GET` | `/api/projects/{projectId}/docs/{docId}/versions` | ProjectDocs | 文档版本 | `project:doc:read` |
| `POST` | `/api/projects/{projectId}/docs` | ProjectDocs | 新建文档 | `project:doc:update` |
| `PUT` | `/api/projects/{projectId}/docs/{docId}` | ProjectDocs | 编辑文档 | `project:doc:update` |
| `DELETE` | `/api/projects/{projectId}/docs/{docId}` | ProjectDocs | 删除/归档文档 | `project:doc:update` |
| `POST` | `/api/projects/{projectId}/docs/{docId}/attachments` | ProjectDocs | 上传附件 | `project:doc:update` |

### 7.5 个人工作台、任务详情、全局报表、个人设置

| 方法 | 路径 | 页面 | 用途 | 权限 |
| --- | --- | --- | --- | --- |
| `GET` | `/api/workbench/overview` | Workbench | 工作台聚合数据 | 登录 |
| `POST` | `/api/tasks/drafts` | Workbench | 保存任务草稿 | `task:create` |
| `POST` | `/api/tasks` | Workbench | 创建任务 | `task:create` |
| `GET` | `/api/tasks/{taskId}` | TaskDetail | 任务详情 | `task:read` |
| `PATCH` | `/api/tasks/{taskId}` | TaskDetail | 更新任务字段 | `task:update` |
| `POST` | `/api/tasks/{taskId}/comments` | TaskDetail | 添加评论 | `task:comment` |
| `PATCH` | `/api/tasks/{taskId}/subtasks/{subtaskId}` | TaskDetail | 勾选子任务 | `task:update` |
| `GET` | `/api/ai/tasks/{taskId}/suggestions` | TaskDetail | 任务 AI 建议 | `task:read` |
| `POST` | `/api/ai/tasks/{taskId}/suggestions/{suggestionId}/apply` | TaskDetail | 采纳任务 AI 建议 | `task:update` |
| `GET` | `/api/reports/overview` | Reports | 全局报表聚合 | 登录 |
| `GET` | `/api/reports/options` | Reports | 报表筛选项 | 登录 |
| `POST` | `/api/reports/export` | Reports | 导出全局报表 | `report:export` |
| `GET` | `/api/ai/report-suggestions` | Reports | 全局报表 AI 建议 | 登录 |
| `GET` | `/api/settings/me` | Settings | 设置页首屏数据 | 登录 |
| `PUT` | `/api/settings/me` | Settings | 保存个人设置 | 登录 |
| `POST` | `/api/settings/reset` | Settings | 恢复默认设置 | 登录 |
| `POST` | `/api/settings/change-password` | Settings | 修改密码 | 登录 |
| `GET` | `/api/settings/sessions` | Settings | 设备会话列表 | 登录 |
| `DELETE` | `/api/settings/sessions/{sessionId}` | Settings | 下线某设备 | 登录 |
| `GET` | `/api/ai/settings-suggestions` | Settings | AI 偏好建议 | 登录 |
| `POST` | `/api/ai/settings-suggestions/{suggestionId}/apply` | Settings | 采纳 AI 建议 | 登录 |

### 7.6 后台管理

| 方法 | 路径 | 页面 | 用途 | 权限 |
| --- | --- | --- | --- | --- |
| `GET` | `/api/admin/overview` | AdminHome | 后台首页聚合数据 | `admin:access` |
| `GET` | `/api/admin/permission-matrix` | AdminHome / AdminRoles | 平台/项目权限矩阵 | `admin:access` |
| `POST` | `/api/admin/permission-matrix/export` | AdminHome / AdminRoles | 导出矩阵 | `admin:access` |
| `GET` | `/api/admin/users` | AdminUsers | 用户列表 | `admin:user:read` |
| `POST` | `/api/admin/users` | AdminUsers | 创建用户 | `admin:user:update` |
| `PATCH` | `/api/admin/users/{userId}` | AdminUsers | 编辑用户资料 | `admin:user:update` |
| `PATCH` | `/api/admin/users/{userId}/status` | AdminUsers | 激活/停用用户 | `admin:user:update` |
| `GET` | `/api/admin/users/import/template` | AdminUsers | 下载导入模板 | `admin:user:update` |
| `POST` | `/api/admin/users/import/preview` | AdminUsers | 上传并预览导入 | `admin:user:update` |
| `POST` | `/api/admin/users/import/commit` | AdminUsers | 确认导入 | `admin:user:update` |
| `GET` | `/api/admin/role-templates` | AdminHome / AdminRoles | 角色模板列表 | `admin:role:read` |
| `GET` | `/api/admin/role-templates/{templateId}` | AdminRoles | 角色模板详情 | `admin:role:read` |
| `POST` | `/api/admin/role-templates` | AdminHome / AdminRoles | 新建角色模板 | `admin:role:update` |
| `PUT` | `/api/admin/role-templates/{templateId}` | AdminRoles | 更新角色模板 | `admin:role:update` |
| `POST` | `/api/admin/role-templates/{templateId}/copy` | AdminHome / AdminRoles | 模板另存为 | `admin:role:update` |
| `GET` | `/api/admin/project-templates` | AdminProjectTemplates | 项目模板列表 | `admin:project-template:read` |
| `POST` | `/api/admin/project-templates` | AdminProjectTemplates | 新建项目模板 | `admin:project-template:update` |
| `PUT` | `/api/admin/project-templates/{templateId}` | AdminProjectTemplates | 编辑项目模板 | `admin:project-template:update` |
| `DELETE` | `/api/admin/project-templates/{templateId}` | AdminProjectTemplates | 删除项目模板 | `admin:project-template:update` |
| `GET` | `/api/admin/logs` | AdminLogs | 审计日志列表 | `admin:log:read` |
| `POST` | `/api/admin/logs/export` | AdminLogs | 导出审计日志 | `admin:log:export` |
| `GET` | `/api/admin/system-config` | AdminSystem | 系统配置读取 | `admin:system:read` |
| `PUT` | `/api/admin/system-config` | AdminSystem | 系统配置保存 | `admin:system:update` |
| `POST` | `/api/admin/system-config/reset` | AdminSystem | 恢复默认配置 | `admin:system:update` |
| `GET` | `/api/ai/admin-suggestions` | AdminHome | 后台 AI 建议 | `admin:access` |
| `POST` | `/api/ai/admin-suggestions/{suggestionId}/apply` | AdminHome | 采纳后台 AI 建议 | `admin:access` |

## 8. 页面聚合接口返回要求

### 8.1 `GET /api/dashboard/overview`

`data` 必须包含：

- `currentUser: CurrentUser`
- `unreadCount: number`
- `greeting: { title, summary, updatedAt }`
- `kpis: { todoCompletionRate, blockedTaskCount, pbcCompletionRate, activeProjectCount }`
- `teamEfficiency: { value, progress, description, tags[] }`
- `todos: TaskLite[]`
- `activities: [{ id, type, title, content, occurredAt, targetPath }]`
- `projectHealth: [{ projectId, projectName, progress, health, note }]`
- `deliveryConfidence: { level, score }`
- `operationMetrics: [{ key, name, value, unit, status }]`

### 8.2 `GET /api/projects`

支持参数：

- `keyword`
- `status`
- `health`
- `ownerId`
- `tag`
- `sortField`
- `sortOrder`
- `page`
- `pageSize`

`data` 使用分页结构，`list` 每项至少包含：

- `ProjectLite`
- `ownerAvatar`
- `activeMemberAvatars`
- `templateName`
- `riskCount`
- `defaultView`

### 8.3 `GET /api/projects/{projectId}`

`data` 必须包含：

- `project: ProjectLite`
- `summary`
- `currentStage`
- `enabledTabs: string[]`
- `defaultTab: string`
- `permissions: string[]`
- `membersBrief: [{ id, name, avatar, role }]`

### 8.4 `GET /api/projects/{projectId}/overview`

`data` 必须包含：

- `milestones`
- `weekTasks`
- `loads`
- `memberList`
- `heatmap`
- `kanbanPreview`
- `flowRules`
- `ganttPreview`
- `riskInsights`
- `riskTasks`
- `reportsPreview`
- `docList`
- `aiDrawer`

### 8.5 `GET /api/projects/{projectId}/members/page-data`

`data` 必须包含：

- `project`
- `summary`
- `members`
- `inviteFlow`
- `heatmap`
- `filters`
- `aiSuggestions`

### 8.6 `GET /api/projects/{projectId}/kanban/page-data`

`data` 必须包含：

- `project`
- `summary`
- `columns`
- `flowRules`
- `filters`
- `aiSuggestions`

### 8.7 `GET /api/projects/{projectId}/gantt/page-data`

`data` 必须包含：

- `project`
- `summary`
- `timeline`
- `items`
- `baselines`
- `dependencies`
- `aiSuggestions`

### 8.8 `GET /api/projects/{projectId}/risks/page-data`

`data` 必须包含：

- `project`
- `summary`
- `resourceHeatmap`
- `risks`
- `filters`
- `aiInsights`

### 8.9 `GET /api/projects/{projectId}/reports/page-data`

`data` 必须包含：

- `project`
- `options`
- `aiInsight`
- `burndown`
- `workHours`
- `bugs`
- `blockLoad`

### 8.10 `GET /api/projects/{projectId}/docs/page-data`

`data` 必须包含：

- `project`
- `summary`
- `options`
- `documents`
- `aiSuggestions`

### 8.11 `GET /api/workbench/overview`

`data` 必须包含：

- `currentUser`
- `unreadCount`
- `todayLogs`
- `tomorrowPlans`
- `blockedItems`
- `kanbanTasks`
- `pbcObjectives`
- `quickTaskDefaults`
- `aiSuggestions`

### 8.12 `GET /api/tasks/{taskId}`

`data` 必须包含：

- `task: TaskLite`
- `description`
- `subtasks`
- `comments`
- `aiSuggestions`

### 8.13 `GET /api/settings/me`

`data` 必须包含：

- `profile: { name, department, email, phone }`
- `notifications: { taskStatus, logFeedback, reportSubscription }`
- `sessions`
- `securityHints`
- `aiSuggestions`

### 8.14 `GET /api/admin/overview`

`data` 必须包含：

- `currentUser`
- `unreadCount`
- `metrics`
- `roleUsageBars`
- `configChangeRows`
- `recentAuditItems`
- `platformMatrix`
- `projectMatrix`
- `roleTemplateDefaults`
- `aiSuggestions`

### 8.15 `GET /api/admin/users`

支持参数：

- `keyword`
- `role`
- `status`
- `page`
- `pageSize`

`data` 必须包含：

- `list`
- `page`
- `pageSize`
- `total`
- `filterOptions`

每个用户项至少包含：

- `id`
- `name`
- `email`
- `department`
- `platformRole`
- `platformRoleLabel`
- `status`
- `joinDate`

### 8.16 `GET /api/admin/role-templates`

`data` 必须包含：

- `templates`
- `platformMatrix`
- `projectMatrix`
- `visiblePageOptions`
- `actionOptions`

### 8.17 `GET /api/admin/logs`

支持参数：

- `keyword`
- `type`
- `page`
- `pageSize`

每条日志至少包含：

- `id`
- `time`
- `operator`
- `action`
- `target`
- `result`
- `type`

### 8.18 `GET /api/admin/system-config`

`data` 必须包含：

- `currentUser`
- `settings`
- `groups`
- `defaults`

### 8.19 `GET /api/reports/overview`

`data` 必须包含：

- `currentUser`
- `unreadCount`
- `filters`
- `summaryCards`
- `trendCharts`
- `rankingLists`
- `aiInsight`

## 9. 关键写接口约束

### 9.1 登录

- `POST /api/auth/login`
- 请求体：`LoginRequest`
- 成功返回：

```json
{
  "accessToken": "jwt",
  "refreshToken": "jwt",
  "expiresIn": 7200,
  "currentUser": {
    "id": "u_10001",
    "name": "张工",
    "platformRole": "admin"
  }
}
```

### 9.2 注册

- `POST /api/auth/register`
- 请求体：`RegisterRequest`
- 首期默认返回审核中或创建成功状态：

```json
{
  "userId": "u_10020",
  "status": "pending"
}
```

### 9.3 创建项目

- `POST /api/projects`
- 请求体：`ProjectCreateRequest`
- 校验：
  - `code` 唯一
  - `endDate >= startDate`
  - `templateId` 必须有效
  - `ownerId`、`memberIds`、`subscriberIds` 必须存在

### 9.4 任务状态流转

- `POST /api/projects/{projectId}/tasks/{taskId}/transition`
- 请求体：

```json
{
  "toStatus": "blocked",
  "columnKey": "blocked",
  "blockedReason": "环境配置窗口未确认"
}
```

约束：

- 当 `toStatus = blocked` 时，`blockedReason` 必填
- 非法流转必须返回业务错误码

### 9.5 新增评论

- `POST /api/tasks/{taskId}/comments`
- 请求体：

```json
{
  "content": "登录页面需要支持记住密码功能"
}
```

### 9.6 用户导入

#### 预览

- `POST /api/admin/users/import/preview`
- 使用 multipart/form-data 上传 Excel
- 返回：

```json
{
  "fileName": "users.xlsx",
  "totalCount": 3,
  "rows": [
    {
      "name": "赵经理",
      "email": "zhao@example.com",
      "department": "产品部",
      "platformRole": "user",
      "platformRoleLabel": "普通用户"
    }
  ]
}
```

#### 确认导入

- `POST /api/admin/users/import/commit`
- 请求体：

```json
{
  "fileName": "users.xlsx",
  "rows": []
}
```

### 9.7 角色模板保存

- `POST /api/admin/role-templates`
- `PUT /api/admin/role-templates/{templateId}`
- 请求体：`RoleTemplateRequest`

### 9.8 系统配置保存

- `PUT /api/admin/system-config`
- 请求体：`SystemConfigRequest`

## 10. 错误码

| code | 含义 | 场景 |
| --- | --- | --- |
| `0` | 成功 | 通用 |
| `AUTH_INVALID` | 账号或密码错误 | 登录 |
| `AUTH_TOKEN_EXPIRED` | 登录失效 | 通用 |
| `AUTH_FORBIDDEN` | 无权限 | 通用 |
| `USER_EMAIL_EXISTS` | 邮箱已存在 | 注册 / 用户创建 |
| `USER_STATUS_INVALID` | 用户状态不允许当前操作 | 用户激活/停用 |
| `PROJECT_CODE_EXISTS` | 项目编号重复 | 创建/编辑项目 |
| `PROJECT_DATE_INVALID` | 项目日期范围错误 | 创建/编辑项目 |
| `PROJECT_NOT_FOUND` | 项目不存在 | 项目详情 |
| `TASK_NOT_FOUND` | 任务不存在 | 任务详情 / 看板 |
| `TASK_TRANSITION_INVALID` | 任务状态流转非法 | 看板拖拽 |
| `TASK_BLOCK_REASON_REQUIRED` | 阻塞原因必填 | 看板拖拽 |
| `RISK_NOT_FOUND` | 风险不存在 | 风险页 |
| `DOC_NOT_FOUND` | 文档不存在 | 文档页 |
| `ROLE_TEMPLATE_EXISTS` | 模板名称重复 | 角色模板 |
| `IMPORT_FILE_INVALID` | 导入文件格式错误 | 用户导入 |
| `IMPORT_ROW_INVALID` | 导入行数据非法 | 用户导入 |
| `EXPORT_TASK_FAILED` | 导出任务失败 | 各类导出 |
| `AI_RATE_LIMITED` | AI 请求过于频繁 | 各类 AI 能力 |
| `COMMON_SERVER_ERROR` | 服务异常 | 通用 |

## 11. 实施优先级

### P0 必做

- 认证：登录、注册、当前用户、退出
- Dashboard 首屏聚合
- Notifications 列表、已读、处理
- Projects 列表、创建、草稿
- ProjectDetail 头部、概览、编辑、归档、基线
- ProjectMembers / ProjectKanban / ProjectGantt / ProjectRisk / ProjectReports / ProjectDocs 各自 page-data
- Workbench 聚合、创建任务、保存草稿
- TaskDetail、评论
- Settings 读取、保存、重置、改密码
- AdminHome、AdminUsers、AdminRoles、AdminLogs、AdminSystem、AdminProjectTemplates

### P1 可后补

- 所有 AI 建议采纳接口
- 第三方登录
- 批量风险处理
- 全局报表导出
- 审计日志导出
- 用户导入预览/确认
- 文档附件上传与 AI 摘要

## 12. 最终说明

- 后端首期实现时，允许读接口先按“聚合接口优先”方案落地
- 只要保持本文件中的路径、请求体和响应体结构不变，内部可以继续拆服务
- 前端后续接入时，如果页面仍保留部分静态展示字段，可从本文件定义的数据结构中直接取值
- 如果后端实现需要裁剪接口，请先更新本文件，再通知前端，不允许仅在线下口头变更
