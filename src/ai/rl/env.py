import gymnasium as gym
import numpy as np
import torch
from gymnasium import spaces

from ai.models.analyst_quant import AnalystQuantModel

class TradingEnv(gym.Env):
    """
    Custom Environment that follows gym interface.
    Integrates AnalystQuantModel for feature extraction.
    """
    metadata = {'render_modes': ['human']}

    def __init__(self, df_ratios, model: AnalystQuantModel, window_size=64):
        super(TradingEnv, self).__init__()
        
        self.df = df_ratios
        self.model = model
        self.window_size = window_size
        self.device = next(model.parameters()).device
        
        # Define Action Space: 0=Hold, 1=Buy, 2=Sell
        self.action_space = spaces.Discrete(3)
        
        # Define Observation Space
        # Embedding (d_model=128) + Account State (PnL, Position, etc. ~ 4 features)
        self.d_model = 128 # matched with AnalystQuantModel
        self.account_features = 4 
        total_obs_size = self.d_model + self.account_features
        
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(total_obs_size,), dtype=np.float32
        )
        
        # Internal State
        self.current_step = 0
        self.balance = 10000.0
        self.position = 0 # 0=None, 1=Long, -1=Short (Simple)
        self.entry_price = 0.0

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = self.window_size
        self.balance = 10000.0
        self.position = 0
        
        return self._get_observation(), {}

    def _get_observation(self):
        # 1. Get Window
        # This is simplified; in real implementation we slide efficiently.
        # df should be a numpy array ideally for speed.
        # Assuming df is ratio dataframe
        window_data = self.df.iloc[self.current_step-self.window_size : self.current_step]
        
        # Drops timestamp if present, just ensure numeric features
        numeric_data = window_data.select_dtypes(include=[np.number]).values
        
        # Prepare Tensor [Batch=1, Features, Seq_Len]
        # Transpose to (Batch, Features, Seq)
        tensor_in = torch.tensor(numeric_data, dtype=torch.float32).T.unsqueeze(0).to(self.device)
        
        # 2. Run Model -> Get Embedding
        with torch.no_grad():
            _, _, embedding = self.model(tensor_in)
            embedding_np = embedding.cpu().numpy().flatten()
            
        # 3. Account State
        account_state = np.array([
            self.balance,
            float(self.position),
            self.entry_price,
            0.0 # Placeholder (e.g., unrealized PnL)
        ], dtype=np.float32)
        
        return np.concatenate([embedding_np, account_state])

    def step(self, action):
        # Execute Action
        # (Simplified logic)
        # 0: Hold, 1: Buy, 2: Sell
        
        # Calculate Reward (Realized PnL change)
        reward = 0
        terminated = False
        truncated = False
        
        # Simulate simple step
        self.current_step += 1
        
        if self.current_step >= len(self.df):
            terminated = True
            
        return self._get_observation(), reward, terminated, truncated, {}
