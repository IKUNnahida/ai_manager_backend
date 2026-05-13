# backend-requirements 使用说明

## 当前生效文档

- `BACKEND_API_MASTER.md` 是当前**唯一对后端实施生效**的接口需求文档。
- 本目录下已有的 `*.backend.md` 文件保留为页面分析草稿和设计过程记录。
- 如果 `BACKEND_API_MASTER.md` 与任意旧草稿存在冲突，**一律以 `BACKEND_API_MASTER.md` 为准**。

## 适用范围

- 适用于当前路由中所有已启用页面：
  - `/login`
  - `/register`
  - `/dashboard`
  - `/projects`
  - `/workbench`
  - `/reports`
  - `/settings`
  - `/notifications`
  - `/admin`
  - `/admin/users`
  - `/admin/roles`
  - `/admin/project-templates`
  - `/admin/logs`
  - `/admin/system`
  - `/project/:id`
  - `/project/:id/:tab`
  - `/task/:id`

## 后端阅读顺序

1. 先看 `BACKEND_API_MASTER.md` 的“统一实现约定”和“统一枚举口径”
2. 再看“路由覆盖矩阵”和“接口总表”
3. 最后按模块看每个接口的请求体、响应体和权限说明

## 维护约定

- 后续新增页面时，先更新 `BACKEND_API_MASTER.md`
- 单页草稿如需保留，可继续放在本目录，但不得作为后端实施依据
- 新增接口时，必须同步补充：
  - 路由归属
  - 鉴权要求
  - 请求参数
  - `data` 结构
  - 枚举值
  - 错误码
