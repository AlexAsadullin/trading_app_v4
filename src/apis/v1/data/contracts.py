from typing import Annotated

from fastapi import Body
from pydantic import BaseModel

from apis.responses import SuccessResponse


class UploadFileHttpRequest(BaseModel):
    source: Annotated[str, Body(..., description="File source/category")]
    filename: Annotated[str, Body(..., description="File name")]


class UploadFileHttpResponse(SuccessResponse):
    filename: str
    source: str


class DownloadFileHttpRequest(BaseModel):
    source: Annotated[str, Body(..., description="File source/category")]
    filename: Annotated[str, Body(..., description="File name")]


class RenameFileHttpRequest(BaseModel):
    source: Annotated[str, Body(..., description="File source/category")]
    old_filename: Annotated[str, Body(..., description="Current file name")]
    new_filename: Annotated[str, Body(..., description="New file name")]


class RenameFileHttpResponse(SuccessResponse):
    old_filename: str
    new_filename: str
    source: str
