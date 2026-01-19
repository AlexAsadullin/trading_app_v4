from io import BytesIO

from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import StreamingResponse

from apis.dependencies import get_current_user
from apis.responses import (
    NotFoundErrorResponse,
    SuccessResponse,
    UnauthorizedErrorResponse,
)
from core.users.dtos import UserProfile
from domain.services.storage import storage_service

from .contracts import (
    DownloadFileHttpRequest,
    RenameFileHttpRequest,
    RenameFileHttpResponse,
    UploadFileHttpRequest,
    UploadFileHttpResponse,
)

router = APIRouter(prefix="", tags=["Data"])


@router.post(
    "/files/upload",
    response_model=UploadFileHttpResponse,
    responses={
        401: {"model": UnauthorizedErrorResponse},
    },
)
async def upload_file(
    body: UploadFileHttpRequest,
    file: UploadFile = File(...),
    user: UserProfile = Depends(get_current_user),
):
    file_data = await file.read()
    await storage_service.put_file(
        user_id=user.id,
        source=body.source,
        filename=body.filename,
        file_data=file_data,
    )

    return UploadFileHttpResponse(
        message="File uploaded successfully",
        filename=body.filename,
        source=body.source,
    )


@router.post(
    "/files/download",
    responses={
        401: {"model": UnauthorizedErrorResponse},
        404: {"model": NotFoundErrorResponse},
    },
)
async def download_file(
    body: DownloadFileHttpRequest,
    user: UserProfile = Depends(get_current_user),
):
    file_data = await storage_service.get_file(
        user_id=user.id,
        source=body.source,
        filename=body.filename,
    )

    return StreamingResponse(
        BytesIO(file_data),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={body.filename}"},
    )


@router.post(
    "/files/rename",
    response_model=RenameFileHttpResponse,
    responses={
        401: {"model": UnauthorizedErrorResponse},
        404: {"model": NotFoundErrorResponse},
    },
)
async def rename_file(
    body: RenameFileHttpRequest,
    user: UserProfile = Depends(get_current_user),
):
    await storage_service.rename_file(
        user_id=user.id,
        source=body.source,
        old_filename=body.old_filename,
        new_filename=body.new_filename,
    )

    return RenameFileHttpResponse(
        message="File renamed successfully",
        old_filename=body.old_filename,
        new_filename=body.new_filename,
        source=body.source,
    )
