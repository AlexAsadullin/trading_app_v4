from fastapi import APIRouter, HTTPException, Depends

from apis.dependencies import get_current_user
from apis.responses import UnauthorizedErrorResponse, NotFoundErrorResponse
from core.users.dtos import UserProfile
from ai.services.training_control import training_service

from .contracts import StartTrainingRequest, StopTrainingRequest, TrainingStatusResponse

router = APIRouter(prefix="/training", tags=["AI Training"])


@router.post(
    "/start",
    response_model=TrainingStatusResponse,
    description="Start a new training job",
    responses={401: {"model": UnauthorizedErrorResponse}},
)
async def start_training(
    body: StartTrainingRequest,
    user: UserProfile = Depends(get_current_user),
):
    job_id = await training_service.start_training(
        model_type=body.model_type,
        ticker=body.ticker,
        epochs=body.epochs,
        config=body.config_overrides,
    )
    
    status_dict = await training_service.get_status(job_id)
    return TrainingStatusResponse(**status_dict)


@router.post(
    "/stop",
    response_model=TrainingStatusResponse,
    description="Stop a running training job",
    responses={
        401: {"model": UnauthorizedErrorResponse},
        404: {"model": NotFoundErrorResponse},
    },
)
async def stop_training(
    body: StopTrainingRequest,
    user: UserProfile = Depends(get_current_user),
):
    success = await training_service.stop_training(body.job_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Job {body.job_id} not found")
        
    status_dict = await training_service.get_status(body.job_id)
    return TrainingStatusResponse(**status_dict)


@router.get(
    "/{job_id}",
    response_model=TrainingStatusResponse,
    description="Get status of a training job",
    responses={
        401: {"model": UnauthorizedErrorResponse},
        404: {"model": NotFoundErrorResponse},
    },
)
async def get_training_status(
    job_id: str,
    user: UserProfile = Depends(get_current_user),
):
    status_dict = await training_service.get_status(job_id)
    if not status_dict:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
        
    return TrainingStatusResponse(**status_dict)
