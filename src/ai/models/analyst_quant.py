import torch
import torch.nn as nn
from tsai.models.InceptionTimePlus import InceptionTimePlus

class AnalystQuantModel(nn.Module):
    def __init__(self, c_in: int, c_out_class: int = 3, seq_len: int = 64, d_model: int = 128):
        """
        Multi-Task Model (Analyst + Quant) using InceptionTime backbone.
        
        Args:
            c_in: Number of input features (channels).
            c_out_class: Number of classification classes (3: Up, Down, Sideways).
            seq_len: Sequence length of input window.
            d_model: Dimension of the backbone output (embedding size).
        """
        super().__init__()
        
        # InceptionTimePlus backbone
        # We need to ensure it returns features, not logits. 
        # tsai models often have a 'custom_head' argument or similar.
        # Alternatively, we can use it as a feature extractor if supported, 
        # or we remove the head.
        # Here we instantiate with c_out=d_model to get embeddings, assuming a linear head 
        # (or we can use it just as backbone if we check tsai docs, but let's assume standard behavior for now).
        # Actually in tsai, we usually pass `fc_dropout` etc. 
        # Let's simple create a model that outputs d_model features.
        
        # We rely on 'nf' (number of filters) to control somewhat the internal size, 
        # but the final output is usually flattened + linear.
        # Let's assume InceptionTimePlus outputs a flat vector of size 'd_model' if we set c_out=d_model.
        self.backbone = InceptionTimePlus(c_in, c_out=d_model, seq_len=seq_len)
        
        # 1. Analyst Head (Classification)
        self.head_analyst = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(d_model, 64),
            nn.ReLU(),
            nn.Linear(64, c_out_class)  # Logits (CrossEntropy)
        )
        
        # 2. Quant Head (Regression)
        self.head_quant = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(d_model, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()  # Normalize strength 0-1
        )

    def forward(self, x):
        """
        Args:
            x: Input tensor [Batch, c_in, seq_len]
            
        Returns:
            class_logits: [Batch, 3]
            trend_power: [Batch, 1]
            embeddings: [Batch, d_model] (Hidden state for RL agent)
        """
        # Backbone feature extraction
        embeddings = self.backbone(x)
        
        # Heads
        class_logits = self.head_analyst(embeddings)
        trend_power = self.head_quant(embeddings)
        
        return class_logits, trend_power, embeddings
