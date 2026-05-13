from typing import Any

from fastapi import APIRouter, Body, UploadFile, File

from ai_promana_backend.api.v1.endpoints import _mock


router = APIRouter()


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.get("/{projectId}/docs/page-data", summary="文档页聚合数据")
def get_project_docs_page(projectId: str):
    return _mock.api_response(
        {
            "project": _mock.project_lite(projectId),
            "summary": {
                "total": len(_mock.documents()),
                "recentUpdated": 2,
                "lastUpdatedAt": _mock.now_iso(),
            },
            "options": {
                "types": ["markdown", "spreadsheet", "pdf", "attachment"],
                "statuses": ["active", "archived"],
                "owners": _mock.users(),
            },
            "documents": _mock.documents(),
            "aiSuggestions": _mock.ai_suggestions("docs"),
        }
    )


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.get("/{projectId}/docs/{docId}", summary="文档详情")
def get_project_doc(projectId: str, docId: str):
    doc = next((item for item in _mock.documents() if item["id"] == docId), _mock.documents()[0])
    doc["projectId"] = projectId
    doc["content"] = "# Project Document\n\nThis is a first-version backend placeholder document."
    return _mock.api_response({"document": doc})


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.get("/{projectId}/docs/{docId}/versions", summary="文档版本")
def list_project_doc_versions(projectId: str, docId: str):
    return _mock.api_response(
        {
            "projectId": projectId,
            "docId": docId,
            "versions": [
                {"id": "doc_version_001", "version": 1, "createdAt": "2026-05-10T10:00:00+08:00", "authorName": "Zhang Gong"},
                {"id": "doc_version_002", "version": 2, "createdAt": _mock.now_iso(), "authorName": "Wang Yating"},
            ],
        }
    )


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.post("/{projectId}/docs", summary="新建文档")
def create_project_doc(projectId: str, payload: dict[str, Any] = Body(...)):
    return _mock.api_response(
        {
            "document": {
                "id": _mock.make_id("doc"),
                "projectId": projectId,
                "title": payload.get("title", "Untitled document"),
                "type": payload.get("type", "markdown"),
                "content": payload.get("content", ""),
                "createdAt": _mock.now_iso(),
            }
        }
    )


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.put("/{projectId}/docs/{docId}", summary="编辑文档")
def update_project_doc(projectId: str, docId: str, payload: dict[str, Any] = Body(...)):
    return _mock.api_response({"projectId": projectId, "docId": docId, "document": payload, "updatedAt": _mock.now_iso()})


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.delete("/{projectId}/docs/{docId}", summary="删除/归档文档")
def delete_project_doc(projectId: str, docId: str):
    return _mock.api_response({"projectId": projectId, "docId": docId, "archived": True, "updatedAt": _mock.now_iso()})


# TODO: 接入真实业务服务、权限校验、数据持久化和业务错误码。
@router.post("/{projectId}/docs/{docId}/attachments", summary="上传附件")
def upload_project_doc_attachment(projectId: str, docId: str, file: UploadFile = File(...)):
    return _mock.api_response(
        {
            "projectId": projectId,
            "docId": docId,
            "attachment": {
                "id": _mock.make_id("attachment"),
                "fileName": file.filename,
                "contentType": file.content_type,
                "url": f"https://example.com/files/{file.filename}",
                "uploadedAt": _mock.now_iso(),
            },
        }
    )
