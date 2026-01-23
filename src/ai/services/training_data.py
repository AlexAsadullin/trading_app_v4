from io import BytesIO
import joblib
import pandas as pd
from sklearn.preprocessing import RobustScaler

from ai.services.processor import DataProcessor
from domain.services.storage import storage_service

class TrainingDataService:
    def __init__(self):
        self.processor = DataProcessor()
        self.bucket = "training-data" # Separate bucket or path prefix
        
    async def prepare_training_data(self, user_id: int, source_filename: str):
        """
        Full pipeline: Load Raw -> Process -> Scale -> Save.
        """
        raw_bytes = await storage_service.get_file(user_id=user_id, source="t_tech", filename=source_filename)
        df_raw = pd.read_csv(BytesIO(raw_bytes))
        

        df_processed = self.processor.process_candles(df_raw)
        
        features = [c for c in df_processed.columns if c != 'timestamp']
        scaler = RobustScaler()
        df_processed[features] = scaler.fit_transform(df_processed[features])
        
        scaler_filename = f"scalers/{source_filename.replace('.csv', '.pkl')}"
        scaler_buffer = BytesIO()
        joblib.dump(scaler, scaler_buffer)
        await storage_service.put_file(
            user_id=user_id, 
            source="scalers", 
            filename=source_filename.replace('.csv', '.pkl'), 
            file_data=scaler_buffer.getvalue()
        )
        
        processed_filename = f"processed_{source_filename}"
        csv_buffer = BytesIO()
        df_processed.to_csv(csv_buffer, index=False)
        
        await storage_service.put_file(
            user_id=user_id,
            source="processed",
            filename=processed_filename,
            file_data=csv_buffer.getvalue()
        )
        
        return processed_filename, scaler_filename
