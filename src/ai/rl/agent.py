from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv

from ai.rl.env import TradingEnv

def create_agent(env: TradingEnv, verbose=1):
    """
    Creates and returns a PPO agent for the Trading Environment.
    
    Args:
        env: Instance of TradingEnv (or VecEnv)
        verbose: PPO verbosity level
    """
    # We use MlpPolicy because the 'Env' already returns a flat embedding vector 
    # (extracted by the AnalystQuantModel CNN). 
    # So the RL agent just essentially sees a feature vector.
    model = PPO("MlpPolicy", env, verbose=verbose)
    return model

def train_rl(agent: PPO, total_timesteps: int = 10000):
    """
    Wrapper to start training.
    """
    agent.learn(total_timesteps=total_timesteps)
    return agent
