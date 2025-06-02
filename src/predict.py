import numpy as np
import pandas as pd
import joblib
import os

class XGPredictor:
    """NHL Expected Goals Predictor"""
    
    def __init__(self, model_path='models/xg_model_final.pkl'):
        """Initialize with pre-trained model"""
        # For demo purposes, use simplified logic
        # In production, you'd load the actual model:
        # self.model = joblib.load(model_path)
        # self.feature_cols = joblib.load('models/feature_cols.pkl')
        
        self.model_loaded = os.path.exists(model_path)
        
    def predict_shot(self, x, y, is_rebound=False, is_rush=False, strength_state='5v5'):
        """
        Predict xG for a shot
        
        Args:
            x: X coordinate on ice (-100 to 100)
            y: Y coordinate on ice (-42.5 to 42.5)
            is_rebound: Boolean, is this a rebound shot
            is_rush: Boolean, is this a rush chance
            strength_state: Game state (5v5, PP, PK)
        
        Returns:
            float: Expected goal probability (0-1)
        """
        # Calculate features
        distance = np.sqrt((x - 89)**2 + y**2)
        angle = np.degrees(np.arctan2(abs(y), 89 - x))
        
        # Base xG calculation (simplified model)
        if distance < 10:  # Crease area
            base_xg = 0.35
        elif distance < 20 and angle < 45:  # Slot
            base_xg = 0.18
        elif distance < 30:  # High slot
            base_xg = 0.08
        elif distance < 40:  # Medium danger
            base_xg = 0.045
        else:  # Low danger
            base_xg = 0.022
        
        # Adjustments
        if is_rebound:
            base_xg *= 1.25  # 25% increase for rebounds
        
        if is_rush:
            base_xg *= 1.15  # 15% increase for rush chances
            
        if strength_state == 'PP':
            base_xg *= 1.10  # 10% increase on power play
        elif strength_state == 'PK':
            base_xg *= 0.85  # 15% decrease on penalty kill
            
        # Cap at reasonable maximum
        return min(base_xg, 0.95)
    
    def predict_batch(self, shots_df):
        """Predict xG for multiple shots"""
        shots_df['xG'] = shots_df.apply(
            lambda row: self.predict_shot(
                row.get('x', 0),
                row.get('y', 0),
                row.get('is_rebound', False),
                row.get('is_rush', False),
                row.get('strength_state', '5v5')
            ), axis=1
        )
        return shots_df
    
    def get_danger_zone(self, x, y):
        """Classify shot danger level"""
        distance = np.sqrt((x - 89)**2 + y**2)
        angle = np.degrees(np.arctan2(abs(y), 89 - x))
        
        if distance < 20 and angle < 45:
            return "High Danger"
        elif distance < 40:
            return "Medium Danger"
        else:
            return "Low Danger"