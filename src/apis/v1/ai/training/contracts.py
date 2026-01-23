from datetime import datetime
from typing import Annotated, Optional, Dict, Any

from fastapi import Body
from pydantic import BaseModel


class StartTrainingRequest(BaseModel):
    model_type: Annotated[str, Body(..., description="Type of model: 'analyst_quant', 'rl_agent', or 'full_pipeline'")]
    ticker: Annotated[str, Body(..., description="Ticker to train on (or 'ALL')")]
    epochs: Annotated[int, Body(10, description="Number of epochs")]
    config_overrides: Annotated[Optional[Dict[str, Any]], Body(None, description="Optional hyperparameter overrides")]


class StopTrainingRequest(BaseModel):
    job_id: Annotated[str, Body(..., description="ID of the training job to stop")]


class TrainingStatusResponse(BaseModel):
    job_id: str
    status: str  # 'queued', 'running', 'completed', 'failed', 'stopped'
    model_type: str
    progress: float  # 0.0 to 1.0
    current_epoch: int
    total_epochs: int
    metrics: Optional[Dict[str, float]]  # e.g., loss, accuracy, reward
    started_at: datetime
    updated_at: datetime
    message: Optional[str]
