from flask import Flask, request, jsonify
from flask_cors import CORS
from predict import XGPredictor

app = Flask(__name__)
CORS(app)

predictor = XGPredictor()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    xg = predictor.predict_shot(
        data.get('x', 0),
        data.get('y', 0),
        data.get('is_rebound', False)
    )
    return jsonify({'xg': xg, 'percentage': f"{xg:.1%}"})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'model': 'loaded'})

if __name__ == '__main__':
    app.run(debug=True)