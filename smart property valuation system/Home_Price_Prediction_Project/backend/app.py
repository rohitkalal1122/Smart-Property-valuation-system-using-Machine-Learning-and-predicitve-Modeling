from flask import Flask, request, jsonify
import pickle
import numpy as np
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Load model with error handling
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'home_price_model.pkl')
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    model = None
    print(f"Error loading model: {e}")

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded. Check server logs.'}), 500
    try:
        data = request.json
        features = np.array([
            data['sqft'],
            data['bedrooms'],
            data['bathrooms'],
            data['year'],
            data['walk_index'],
            data['risk_score']
        ]).reshape(1, -1)
        
        price = model.predict(features)[0]
        walk_premium = data['walk_index'] * 5000
        risk_discount = -data['risk_score'] * 10000
        
        return jsonify({
            'predicted_price': round(price, 2),
            'walk_premium': walk_premium,
            'risk_discount': risk_discount
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)