from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, Float, JSON, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class TrainingJob(Base):
    __tablename__ = "training_jobs"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="queued") # queued, running, completed, failed, stopped
    model_type: Mapped[str] = mapped_column(String, nullable=False)
    ticker: Mapped[str] = mapped_column(String, nullable=False)
    
    current_epoch: Mapped[int] = mapped_column(Integer, default=0)
    total_epochs: Mapped[int] = mapped_column(Integer, default=10)
    progress: Mapped[float] = mapped_column(Float, default=0.0)
    
    metrics: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    config: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
