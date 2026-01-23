from decimal import Decimal
import pandas as pd
import ta
import numpy as np

class DataProcessor:
    def process_candles(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Converts raw OHLCV DataFrame to Ratio-only DataFrame.
        Strictly removes absolute price/volume values.
        """

        df = df.sort_values('timestamp') if 'timestamp' in df.columns else df
        df['Close_Ratio'] = df['close'] / df['close'].shift(1)
        df['High_Ratio'] = df['high'] / df['close']
        df['Low_Ratio'] = df['low'] / df['close']
        # Handle division by zero
        df['Volume_Ratio'] = df['volume'] / df['volume'].shift(1)
        df['Volume_Ratio'] = df['Volume_Ratio'].replace([np.inf, -np.inf], 0)

        # 2. Custom TA (Ratio Based)
        # Ratio RSI
        df['Ratio_RSI'] = ta.momentum.rsi(df['Close_Ratio'], window=14)
        
        # Ratio Volatility
        df['Ratio_Vol'] = df['Close_Ratio'].rolling(window=20).std()
        
        # Ratio Momentum
        df['Ratio_Mom'] = df['Close_Ratio'] / df['Close_Ratio'].shift(5)

        # --- New Custom Indicators ---
        n_period = 14
        k_factor = 2.0
        
        # RROC (Ratio Rate of Change)
        df['RROC'] = df['Close_Ratio'].pct_change(periods=n_period) * 100

        # Bollinger Bands on Ratio
        rolling_mean = df['Close_Ratio'].rolling(window=n_period).mean()
        rolling_std = df['Close_Ratio'].rolling(window=n_period).std()
        df['Ratio_Middle_Band'] = rolling_mean
        df['Ratio_Upper_Band'] = rolling_mean + (k_factor * rolling_std)
        df['Ratio_Lower_Band'] = rolling_mean - (k_factor * rolling_std)

        # Z-Score
        # Avoid division by zero
        df['Ratio_Z_Score'] = (df['Close_Ratio'] - rolling_mean) / rolling_std.replace(0, np.nan)

        # VPRC (Volume Price Range Composite)
        # Weights (assumed equal if not specified, or optimized)
        w_close = 0.4
        w_vol = 0.4
        w_range = 0.2
        # Range Ratio = High_Ratio - Low_Ratio (Normalized range relative to Close)
        df['Range_Ratio'] = df['High_Ratio'] - df['Low_Ratio']
        df['VPRC'] = (w_close * df['Close_Ratio']) + (w_vol * df['Volume_Ratio']) + (w_range * df['Range_Ratio'])

        # RDI (Ratio Divergence Index) - Correlation between Close Ratio and Volume Ratio
        df['RDI'] = df['Close_Ratio'].rolling(window=n_period).corr(df['Volume_Ratio'])

        # Adaptive Thresholds (Mean +/- Volatility Factor * Std)
        # Assuming volatility_factor same as k_factor unless distinct
        vol_factor = 2.0
        df['Upper_Threshold'] = rolling_mean + (vol_factor * rolling_std)
        df['Lower_Threshold'] = rolling_mean - (vol_factor * rolling_std)
        
        # 3. Clean up
        features = [
            'Close_Ratio', 'High_Ratio', 'Low_Ratio', 'Volume_Ratio',
            'Ratio_RSI', 'Ratio_Vol', 'Ratio_Mom',
            'RROC', 'Ratio_Middle_Band', 'Ratio_Upper_Band', 'Ratio_Lower_Band',
            'Ratio_Z_Score', 'VPRC', 'RDI', 'Upper_Threshold', 'Lower_Threshold'
        ]
        
        final_cols = ['timestamp'] if 'timestamp' in df.columns else []
        final_cols += features
        
        # Ensure we don't try to access columns that weren't calculated if something failed
        # (Though logic above is sequential)
        
        df_processed = df[final_cols].copy()
    
        # Drop NaNs created by shifting/rolling
        # Since we use windows up to 20, we drop the first ~20 rows
        df_processed.replace([np.inf, -np.inf], np.nan, inplace=True)
        df_processed.dropna(inplace=True)
        
        return df_processed
