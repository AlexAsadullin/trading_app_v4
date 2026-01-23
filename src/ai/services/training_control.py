import uuid
from datetime import datetime
from typing import Dict, Optional, Any

class TrainingService:
    def __init__(self):
        # In-memory store for now (simulating DB)
        self._jobs: Dict[str, Dict[str, Any]] = {}

    async def start_training(self, model_type: str, ticker: str, epochs: int, config: Optional[Dict] = None) -> str:
        job_id = str(uuid.uuid4())
        
        self._jobs[job_id] = {
            "job_id": job_id,
            "status": "queued",
            "model_type": model_type,
            "ticker": ticker,
            "epochs": epochs,
            "current_epoch": 0,
            "progress": 0.0,
            "metrics": {},
            "started_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "message": "Job queued",
        }
        
        # TODO: Trigger actual worker task here
        # For now, we just simulate state
        self._jobs[job_id]["status"] = "running"
        self._jobs[job_id]["message"] = "Training started (mock)"
        
        return job_id

    async def stop_training(self, job_id: str) -> bool:
        if job_id in self._jobs:
            self._jobs[job_id]["status"] = "stopped"
            self._jobs[job_id]["updated_at"] = datetime.utcnow()
            self._jobs[job_id]["message"] = "Training stopped by user"
            return True
        return False

    async def get_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        return self._jobs.get(job_id)

# Singleton instance
training_service = TrainingService()
