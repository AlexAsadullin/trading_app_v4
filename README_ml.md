# AI Agent Module Documentation

This document describes the Machine Learning (AI) module of the Trading Application. The AI module is designed to operate as an autonomous worker that fetches data, trains models, and executes trading strategies using Reinforcement Learning.

## Architecture Overview

The system is composed of three main "brains":

1.  **The Analyst (Classification)**:
    *   **Goal**: Identify the current market regime (Up Trend, Down Trend, Sideways).
    *   **Model**: Multi-Task InceptionTime (Head A).
2.  **The Quant (Regression)**:
    *   **Goal**: Predict the strength/power of the current trend (0.0 - 1.0).
    *   **Model**: Multi-Task InceptionTime (Head B).
3.  **The Trader (RL Agent)**:
    *   **Goal**: Execute trades (Buy/Sell/Hold) based on market state and account status.
    *   **Model**: PPO (Proximal Policy Optimization).

## Technology Stack

*   **Deep Learning**: `PyTorch`, `tsai` (Time Series SOTA models like InceptionTime).
*   **Reinforcement Learning**: `stable-baselines3`, `Gymnasium`.
*   **Data Processing**: `pandas`, `ta` (Technical Analysis), `scikit-learn` (Scalers).
*   **Infrastructure**: Python 3.10+, MinIO (Object Storage).

## Data Pipeline

### 1. Data Source
*   **T-Tech API**: Historical candle data.
*   **MOEX AlgoPack**: Russian market data.

### 2. Feature Engineering (Strict "No Price" Policy)
The model **NEVER** sees absolute prices (Open/Close values). The dataset is strictly relative to ensure stationarity.

**Base Features (Ratios):**
*   `Close_Ratio`: $Close_t / Close_{t-1}$
*   `High_Ratio`: $High_t / Close_t$ (Upper Shadow proxy)
*   `Low_Ratio`: $Low_t / Close_t$ (Lower Shadow proxy)
*   `Volume_Ratio`: $Volume_t / Volume_{t-1}$

**Custom Indicators (Ratio-Based):**
*   **Ratio RSI**: RSI calculated on the `Close_Ratio`.
*   **Ratio Volatility**: Rolling Standard Deviation of `Close_Ratio`.
*   **Ratio Momentum**: Momentum of `Close_Ratio`.
*   **RROC**: Ratio Rate of Change.
*   **Ratio Bollinger Bands**: Bands derived from `Close_Ratio` stats.
*   **VPRC** (Volume Price Range Composite): Weighted composite of Close, Volume, and Range ratios.
*   **RDI** (Ratio Divergence Index): Correlation between Close and Volume ratios.

### 3. Processing Flow
1.  **Fetch** raw OHLCV from API.
2.  **Process** via `DataProcessor`: Convert to Ratios, calculate Custom TA, Drop Raw OHLCV.
3.  **Scale** via `RobustScaler`.
    *   **Critical**: The Scaler is fitted on training data and **saved** (`.pkl`) to MinIO to ensure consistent inference.
4.  **Save** processed CSV to MinIO.

## Model Details

### AnalystQuantModel (`src/ai/models/analyst_quant.py`)
A custom PyTorch `nn.Module` wrapping the `InceptionTimePlus` backbone.
*   **Input**: Tensor `[Batch, Features=7, Window=64]`.
*   **Backbone**: Extracts a deep feature embedding (vector of size 128).
*   **Head A**: `Linear -> ReLU -> Linear(3)` (Class Logits).
*   **Head B**: `Linear -> ReLU -> Linear(1) -> Sigmoid` (Trend Power).
*   **Forward Pass**: Returns `(logits, power, embedding)`.

### RL Environment (`src/ai/rl/env.py`)
A custom `Gymnasium` environment.
*   **Observation Space**: Concatenation of `[Embedding (128), Balance, Position, Entry Price]`.
*   **Action Space**: Discrete(3) - `0: Hold`, `1: Buy`, `2: Sell`.
*   **Dynamics**:
    *   At each step, the environment feeds the current window of Ratios into the **AnalystQuantModel**.
    *   The model returns the **embedding** (representing the "Market State").
    *   The RL Agent (PPO) uses this embedding + account info to decide the action.

## Usage

### Training Workflow
1.  **Data Prep**: Run the `TrainingDataService` pipeline to populate MinIO with `processed_*.csv` and `scalers/*.pkl`.
2.  **Pre-training**: Train the `AnalystQuantModel` (Supervised) on labeled data (future trend lookahead).
3.  **RL Training**: Initialize `TradingEnv` with the pre-trained model and processed data. Run PPO training loop.
