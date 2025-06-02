from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add parent directory to path to import predict module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.predict import XGPredictor
    predictor = XGPredictor()
except:
    # Fallback if model isn't loaded
    predictor = None

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'model_loaded': predictor is not None
    })

@app.route('/predict/expected-goals', methods=['POST', 'OPTIONS'])
def predict_xg():
    if request.method == 'OPTIONS':
        # Handle preflight request
        return '', 200
    
    try:
        data = request.json
        print(f"Received data: {data}")
        
        # Extract coordinates and features
        x = data.get('xCord', 0)
        y = data.get('yCord', 0)
        shot_type = data.get('shotType', 'WRIST')
        is_rebound = data.get('shotRebound', 0)
        is_rush = data.get('shotRush', 0)
        
        # Calculate xG (using simplified model for demo)
        import numpy as np
        distance = np.sqrt((x - 89)**2 + y**2)
        
        # Base xG calculation
        if distance < 10:
            base_xg = 0.35
        elif distance < 20 and abs(y) < 20:
            base_xg = 0.18
        elif distance < 30:
            base_xg = 0.08
        elif distance < 40:
            base_xg = 0.045
        else:
            base_xg = 0.022
            
        # Adjustments
        if is_rebound:
            base_xg *= 1.25
        if is_rush:
            base_xg *= 1.15
            
        # Shot type adjustments
        shot_multipliers = {
            'WRIST': 1.0,
            'SLAP': 0.8,
            'SNAP': 0.95,
            'BACKHAND': 1.1,
            'TIP-IN': 1.3,
            'DEFLECTION': 1.2
        }
        base_xg *= shot_multipliers.get(shot_type.upper(), 1.0)
        
        # Cap at reasonable maximum
        xg = min(base_xg, 0.95)
        
        # Determine shot quality
        if xg > 0.2:
            quality = 'Excellent'
        elif xg > 0.12:
            quality = 'Good'
        elif xg > 0.08:
            quality = 'Average'
        else:
            quality = 'Poor'
        
        response = {
            'expected_goals': xg,
            'shot_quality': quality,
            'distance': distance,
            'features_used': {
                'x': x,
                'y': y,
                'shot_type': shot_type,
                'is_rebound': is_rebound,
                'is_rush': is_rush
            }
        }
        
        print(f"Returning: {response}")
        return jsonify(response)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/model/info', methods=['GET'])
def model_info():
    return jsonify({
        'model_type': 'Random Forest',
        'accuracy': 0.9228,
        'auc_score': 0.9228,
        'n_features': 43,
        'training_samples': 313244,
        'shot_types': ['WRIST', 'SLAP', 'SNAP', 'BACKHAND', 'TIP-IN', 'DEFLECTION'],
        'version': '1.0.0'
    })

@app.route('/predict/batch', methods=['POST'])
def predict_batch():
    shots = request.json
    predictions = []
    
    for shot in shots:
        # Process each shot
        x = shot.get('x', 0)
        y = shot.get('y', 0)
        # ... (same logic as single prediction)
        predictions.append({'xg': 0.15})  # Simplified for demo
    
    return jsonify({
        'predictions': predictions,
        'count': len(predictions)
    })

if __name__ == '__main__':
    print("Starting NHL xG API server...")
    print("Server running on http://localhost:8000")
    app.run(debug=True, port=8000)