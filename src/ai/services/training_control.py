import uuid
from datetime import datetime
from typing import Dict, Optional, Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from dal.engines import get_async_engine
from domain.models.training import TrainingJob

class TrainingService:
    def __init__(self):
        self.engine = get_async_engine()

    async def start_training(self, model_type: str, ticker: str, epochs: int, config: Optional[Dict] = None) -> str:
        job_id = str(uuid.uuid4())
        
        job = TrainingJob(
            id=job_id,
            status="queued",
            model_type=model_type,
            ticker=ticker,
            total_epochs=epochs,
            config=config or {},
            metrics={},
            started_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            message="Job queued"
        )
        
        async with AsyncSession(self.engine) as session:
            session.add(job)
            await session.commit()
            
        return job_id

    async def stop_training(self, job_id: str) -> bool:
        async with AsyncSession(self.engine) as session:
            stmt = select(TrainingJob).where(TrainingJob.id == job_id)
            result = await session.execute(stmt)
            job = result.scalar_one_or_none()
            
            if job:
                job.status = "stopped"
                job.message = "Training stopped by user"
                await session.commit()
                return True
        return False

    async def get_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        async with AsyncSession(self.engine) as session:
            stmt = select(TrainingJob).where(TrainingJob.id == job_id)
            result = await session.execute(stmt)
            job = result.scalar_one_or_none()
            
            if job:
                return {
                    "job_id": job.id,
                    "status": job.status,
                    "model_type": job.model_type,
                    "ticker": job.ticker,
                    "epochs": job.total_epochs,
                    "current_epoch": job.current_epoch,
                    "progress": job.progress,
                    "metrics": job.metrics,
                    "started_at": job.started_at,
                    "updated_at": job.updated_at,
                    "message": job.message,
                }
        return None

# Singleton instance
training_service = TrainingService()
