from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import os
import numpy as np

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, '..', 'models')
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'frontend')

models = {}
model_status = {}

def load_models():
    model_files = {
        'liver': 'liver_model.pkl',
        'kidney': 'kidney_model.pkl',
        'lung': 'lung_model.pkl',
        'parkinsons': 'parkinsons_model.pkl'
    }
    
    for disease, filename in model_files.items():
        model_path = os.path.join(MODELS_DIR, filename)
        try:
            if os.path.getsize(model_path) == 0:
                model_status[disease] = 'empty'
                print(f"[WARN] {disease.title()} model file is empty: {model_path}")
                continue
            models[disease] = joblib.load(model_path)
            model_status[disease] = 'loaded'
            print(f"[OK] {disease.title()} model loaded: {filename}")
        except FileNotFoundError:
            model_status[disease] = 'not_found'
            print(f"[WARN] {disease.title()} model not found: {model_path}")
        except Exception as e:
            model_status[disease] = f'error: {str(e)}'
            print(f"[ERROR] Failed to load {disease} model: {e}")

load_models()

@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    if filename.startswith('api/') or filename.startswith('predict'):
        return jsonify({'error': 'Not found'}), 404
    return send_from_directory(FRONTEND_DIR, filename)

@app.route('/api/')
def api_info():
    return jsonify({
        'name': 'IntelliCure AI API',
        'status': 'running',
        'models': model_status,
        'endpoints': {
            'GET /api': 'API info',
            'GET /api/health': 'Health check',
            'POST /api/predict/liver': 'Predict liver disease',
            'POST /api/predict/kidney': 'Predict kidney disease',
            'POST /api/predict/lung': 'Predict lung cancer',
            'POST /api/predict/parkinsons': 'Predict parkinsons disease'
        }
    })

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'models_loaded': {k: v == 'loaded' for k, v in model_status.items()}
    })

@app.route('/health')
def health_alias():
    return health()

FEATURE_MAPPING = {
    'liver': ['age', 'gender', 'total_bil', 'direct_bil', 'alk_phos', 'sgpt', 'sgot', 'total_proteins', 'albumin', 'ag_ratio'],
    'kidney': ['age', 'bp', 'sg', 'al', 'su', 'rbc', 'pc', 'pcc', 'ba', 'bgr', 'bu', 'sc', 'sod', 'pot', 'hemo', 'pcv', 'wc', 'rc', 'htn', 'dm', 'cad', 'appet', 'pe', 'ane'],
    'lung': ['GENDER', 'AGE', 'SMOKING', 'FINGER_DISCOLORATION', 'MENTAL_STRESS', 'EXPOSURE_TO_POLLUTION', 'LONG_TERM_ILLNESS', 'ENERGY_LEVEL', 'IMMUNE_WEAKNESS', 'BREATHING_ISSUE', 'ALCOHOL_CONSUMPTION', 'THROAT_DISCOMFORT', 'OXYGEN_SATURATION', 'CHEST_TIGHTNESS', 'FAMILY_HISTORY', 'SMOKING_FAMILY_HISTORY', 'STRESS_IMMUNE', 'PULMONARY_DISEASE'],
    'parkinsons': ['MDVP:Fo(Hz)', 'MDVP:Fhi(Hz)', 'MDVP:Flo(Hz)', 'MDVP:Jitter(%)', 'MDVP:Jitter(Abs)', 'MDVP:RAP', 'MDVP:PPQ', 'Jitter:DDP', 'MDVP:Shimmer', 'MDVP:Shimmer(dB)', 'Shimmer:APQ3', 'Shimmer:APQ5', 'MDVP:APQ', 'Shimmer:DDA', 'NHR', 'HNR', 'RPDE', 'DFA', 'spread1', 'spread2', 'D2', 'PPE']
}

FRONTEND_ORDER = {
    'liver': ['age', 'gender', 'total_bil', 'direct_bil', 'alk_phos', 'sgpt', 'sgot', 'total_proteins', 'albumin', 'ag_ratio'],
    'kidney': ['age', 'bp', 'sg', 'al', 'su', 'rbc', 'pc', 'pcc', 'ba', 'bgr', 'bu', 'sc', 'sod', 'pot', 'hemo', 'pcv', 'wc', 'rc', 'htn', 'dm', 'cad', 'appet', 'pe', 'ane'],
    'lung': ['GENDER', 'AGE', 'SMOKING', 'FINGER_DISCOLORATION', 'MENTAL_STRESS', 'EXPOSURE_TO_POLLUTION', 'LONG_TERM_ILLNESS', 'ENERGY_LEVEL', 'IMMUNE_WEAKNESS', 'BREATHING_ISSUE', 'ALCOHOL_CONSUMPTION', 'THROAT_DISCOMFORT', 'OXYGEN_SATURATION', 'CHEST_TIGHTNESS', 'FAMILY_HISTORY', 'SMOKING_FAMILY_HISTORY', 'STRESS_IMMUNE', 'PULMONARY_DISEASE'],
    'parkinsons': ['MDVP:Fo(Hz)', 'MDVP:Fhi(Hz)', 'MDVP:Flo(Hz)', 'MDVP:Jitter(%)', 'MDVP:Jitter(Abs)', 'MDVP:RAP', 'MDVP:PPQ', 'Jitter:DDP', 'MDVP:Shimmer', 'MDVP:Shimmer(dB)', 'Shimmer:APQ3', 'Shimmer:APQ5', 'MDVP:APQ', 'Shimmer:DDA', 'NHR', 'HNR', 'RPDE', 'DFA', 'spread1', 'spread2', 'D2', 'PPE']
}

def reorder_inputs(inputs, disease):
    if disease not in FEATURE_MAPPING:
        return inputs
    
    expected_features = FEATURE_MAPPING[disease]
    frontend_features = FRONTEND_ORDER.get(disease, expected_features)
    
    if len(inputs) == len(expected_features):
        return inputs
    
    mapping = {feat: idx for idx, feat in enumerate(expected_features)}
    reordered = [0.0] * len(expected_features)
    
    for idx, feat in enumerate(frontend_features):
        if feat in mapping and idx < len(inputs):
            reordered[mapping[feat]] = inputs[idx]
    
    return reordered

def make_prediction(disease, data, use_mock=False):
    if disease not in models or use_mock:
        if disease not in model_status:
            return {'error': f'Unknown disease: {disease}', 'available': ['liver', 'kidney', 'lung', 'parkinsons']}, 404
        
        if model_status.get(disease) != 'loaded':
            import random
            inputs = data.get('inputs', data) if isinstance(data, dict) else data
            if not isinstance(inputs, list):
                inputs = list(inputs) if hasattr(inputs, '__iter__') else [inputs]
            try:
                inputs = [float(x) for x in inputs]
            except:
                return {'error': 'Invalid input format'}, 400
            
            mock_prediction = 0 if sum(inputs) / max(len(inputs), 1) < 50 else 1
            mock_prob = random.uniform(0.6, 0.95)
            
            return {
                'prediction': mock_prediction,
                'disease': disease,
                'status': 'mock',
                'probability': mock_prob,
                'message': 'Using mock prediction (model not trained)'
            }, 200
    
    if model_status[disease] != 'loaded':
        return {'error': f'{disease.title()} model not available', 'status': model_status[disease]}, 503
    
    try:
        if 'inputs' in data:
            inputs = data['inputs']
        else:
            inputs = data
        
        if not isinstance(inputs, list):
            return {'error': 'inputs must be a list'}, 400
        
        inputs = [float(x) for x in inputs]
        inputs = reorder_inputs(inputs, disease)
        
        prediction = models[disease].predict([inputs])[0]
        
        result = {
            'prediction': int(prediction),
            'disease': disease,
            'status': 'success'
        }
        
        if hasattr(models[disease], 'predict_proba'):
            try:
                proba = models[disease].predict_proba([inputs])[0]
                result['probability'] = float(max(proba))
                result['confidence'] = float(proba[prediction])
            except:
                pass
        
        return result, 200
    
    except Exception as e:
        return {'error': str(e), 'disease': disease}, 400

@app.route('/api/predict/<disease>', methods=['POST'])
@app.route('/predict/<disease>', methods=['POST'])
def predict(disease):
    if disease not in model_status:
        return jsonify({'error': f'Unknown disease: {disease}', 'available': ['liver', 'kidney', 'lung', 'parkinsons']}), 404
    
    use_mock = model_status.get(disease) != 'loaded'
    if use_mock:
        print(f"[WARN] Using mock prediction for {disease} (model not loaded)")
    
    result, status_code = make_prediction(disease, request.json, use_mock)
    return jsonify(result), status_code

if __name__ == '__main__':
    print("\n" + "="*50)
    print("  N.B.K.R.IST AI - Disease Prediction API")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
