# IntelliCure AI

> Your intelligent health companion for early disease detection powered by machine learning

![Project Status](https://img.shields.io/badge/status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-REST%20API-green)

IntelliCure AI is a web-based health prediction system that uses trained machine learning models to assess the risk of four major diseases: **Liver Disease**, **Kidney Disease**, **Lung Cancer**, and **Parkinson's Disease**. Enter your health parameters and receive instant risk assessments with actionable insights.

---

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [API Reference](#api-reference)
- [Disease Parameters](#disease-parameters)
- [Machine Learning Models](#machine-learning-models)
- [Technology Stack](#technology-stack)
- [Configuration](#configuration)
- [Data Privacy](#data-privacy)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Browser Support](#browser-support)
- [License](#license)
- [Credits](#credits)

---

## Features

- **4 Disease Predictions** - Liver, Kidney, Lung Cancer, and Parkinson's
- **Real-time Results** - Instant predictions with probability percentages
- **Modern Dark UI** - Beautiful, responsive interface with smooth animations
- **Health Insights** - Precautions and recommendations with each prediction
- **History Tracking** - Predictions saved locally in your browser
- **Dashboard** - View statistics and recent activity
- **No Account Required** - Fully local, your data stays private

---

## Quick Start

### Prerequisites

- Python 3.7+
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Edge, Safari)

### Installation

1. **Clone or download the project**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the backend server**
   ```bash
   cd backend
   python app.py
   ```

   Server will start at: `http://127.0.0.1:5000`

4. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

---

## Project Structure

```
IntelliCure AI/
├── backend/
│   └── app.py                 # Flask server & API endpoints
├── frontend/
│   ├── index.html             # Home page with disease selection
│   ├── dashboard.html         # Statistics & recent predictions
│   ├── history.html           # Full prediction history
│   ├── liver.html             # Liver disease prediction form
│   ├── kidney.html            # Kidney disease prediction form
│   ├── lung.html              # Lung cancer prediction form
│   ├── parkinsons.html        # Parkinson's disease prediction form
│   ├── common.css             # Shared styles & variables
│   ├── form.css               # Form-specific styling
│   └── app.js                 # Frontend JavaScript logic
├── models/
│   ├── liver_model.pkl        # Trained liver disease model
│   ├── kidney_model.pkl       # Trained kidney disease model
│   ├── lung_model.pkl         # Trained lung cancer model
│   ├── parkinsons_model.pkl   # Trained Parkinson's model
│   ├── trained_liver_model.py      # Liver training script
│   ├── trained_kidney_model.py     # Kidney training script
│   ├── trained_lung_model.py       # Lung training script
│   └── trained_parkinsons_model.py # Parkinson's training script
├── datasets/
│   ├── Liver Patient Dataset (LPD)_train.csv
│   ├── kidney_cleaned.csv
│   ├── Lung Cancer Dataset.csv
│   └── parkinsons_cleaned.csv
└── requirements.txt            # Python dependencies
```

---

## How It Works

### Architecture

```
┌──────────────────┐          ┌──────────────────┐
│   Your Browser   │ ──────► │   Flask Server   │
│   (Frontend)     │ ◄────── │   (Backend)      │
│                  │   JSON  │                  │
│  - HTML/CSS/JS   │         │  - ML Models     │
│  - localStorage  │         │  - Predictions   │
└──────────────────┘         └──────────────────┘
```

**Workflow:**
1. User enters health data via HTML forms
2. JavaScript sends data to Flask backend via API
3. Backend loads appropriate ML model and generates predictions
4. Results returned with probability scores
5. Frontend displays prediction with visual feedback
6. Prediction saved to browser localStorage

---

## API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serve main application |
| GET | `/api/health` | Health check |
| POST | `/predict/liver` | Predict liver disease |
| POST | `/predict/kidney` | Predict kidney disease |
| POST | `/predict/lung` | Predict lung cancer |
| POST | `/predict/parkinsons` | Predict Parkinson's |

### Example Request

```json
POST /predict/liver
{
  "inputs": [65, 1, 0.9, 0.3, 200, 30, 25, 3.5, 1.0]
}
```

### Example Response

```json
{
  "prediction": 1,
  "probability": 0.85,
  "disease": "liver",
  "status": "success"
}
```

---

## Disease Parameters

### Liver Disease (9 inputs)

| Parameter | Description |
|-----------|-------------|
| Age | Patient age |
| Gender | Male/Female |
| Total Bilirubin | Bilirubin level |
| Direct Bilirubin | Direct bilirubin |
| Alkaline Phosphatase | Enzyme level |
| ALT | Alamine Aminotransferase |
| AST | Aspartate Aminotransferase |
| Albumin | Protein level |
| Albumin/Globulin Ratio | A/G ratio |

**Dataset:** 547 patient records

### Kidney Disease (24 inputs)

| Parameter | Description |
|-----------|-------------|
| Age, Blood Pressure | Basic vitals |
| Urine Specific Gravity, Albumin, Sugar | Urine analysis |
| Red Blood Cells, Pus Cells, Bacteria | Microscopic examination |
| Blood Glucose Random, Blood Urea, Serum Creatinine | Blood tests |
| Sodium, Potassium | Electrolytes |
| Hemoglobin, PCV, WBC, RBC Count | Blood counts |
| Hypertension, Diabetes, CAD | Comorbidities |
| Appetite, Pedal Edema, Anemia | Symptoms |

**Dataset:** 385 patient records

### Lung Cancer (15 inputs)

| Parameter | Description |
|-----------|-------------|
| Age, Gender | Demographics |
| Smoking Status | Tobacco use |
| Yellow Fingers | Discoloration indicator |
| Anxiety, Fatigue, Wheezing | Symptoms |
| Coughing, Shortness of Breath | Respiratory symptoms |
| Swallowing Difficulty | Dysphagia |
| Chest Pain | Cardiac/respiratory symptom |
| Chronic Disease, Allergy History | Medical history |
| Family History of Cancer | Genetic risk |

**Dataset:** 5,001 patient records

### Parkinson's Disease (22 voice measurements)

| Parameter | Description |
|-----------|-------------|
| MDVP:Fo(Hz) | Average vocal frequency |
| MDVP:Fhi(Hz) | Maximum vocal frequency |
| MDVP:Flo(Hz) | Minimum vocal frequency |
| MDVP:Jitter(%) | Frequency perturbation |
| MDVP:Jitter(Abs) | Absolute jitter |
| MDVP:RAP | Relative average perturbation |
| MDVP:PPQ | Five-point period perturbation quotient |
| Jitter:DDP | Average absolute difference of differences |
| MDVP:Shimmer | Amplitude perturbation |
| MDVP:Shimmer(dB) | Shimmer in decibels |
| Shimmer:APQ3, APQ5, MDVP:APQ | Amplitude quotients |
| Shimmer:DDA | Three-point amplitude difference |
| NHR, HNR | Noise-to-harmonics ratios |
| RPDE | Recurrence period density entropy |
| DFA | Signal fractal scaling exponent |
| spread1, spread2, D2 | Nonlinear measures |
| PPE | Pitch period entropy |

**Dataset:** 196 voice recordings

---

## Machine Learning Models

### Training Pipeline

1. **Data Preprocessing** - Clean data, handle missing values, encode categories
2. **Feature Scaling** - RobustScaler for outlier handling
3. **Model** - Random Forest Classifier with hyperparameter tuning
4. **Evaluation** - 5-fold cross-validation, accuracy scoring
5. **Serialization** - Save as `.pkl` for production use

### Model Performance

| Disease | Accuracy | Features | Training Size |
|---------|----------|----------|---------------|
| Liver | ~98% | 9 | 547 records |
| Kidney | ~98% | 24 | 385 records |
| Lung | ~98% | 15 | 5,001 records |
| Parkinson's | ~98% | 22 | 196 records |

---

## Technology Stack

### Frontend

| Technology | Purpose |
|------------|---------|
| HTML5 | Semantic markup |
| CSS3 | Custom properties, flexbox, grid, animations |
| JavaScript (ES6) | Fetch API, localStorage, DOM manipulation |
| Google Fonts | Poppins typeface |

### Backend

| Technology | Purpose |
|------------|---------|
| Python 3 | Server-side logic |
| Flask | Lightweight web framework |
| Flask-CORS | Cross-origin support |
| Scikit-learn | Machine learning |
| Joblib | Model serialization |
| Pandas & NumPy | Data processing |

### UI Features

- Dark theme with gradient backgrounds
- Color-coded disease categories (Red, Purple, Cyan, Yellow)
- Animated progress bars for risk percentages
- Responsive layout (mobile, tablet, desktop)
- Smooth page transitions and hover effects
- Info panels with precautions and health tips

---

## Configuration

### Server Settings

| Setting | Value |
|---------|-------|
| Host | 0.0.0.0 |
| Port | 5000 |
| Debug | Enabled |

To change the port, edit `backend/app.py`:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### API Configuration

Frontend expects API at `http://127.0.0.1:5000`. To change, update `frontend/app.js`:

```javascript
const API_BASE = 'http://127.0.0.1:5000';
```

### Model Location

Models should be in the `models/` directory relative to the backend.

---

## Data Privacy

- **Local Storage Only** - All predictions stored in browser localStorage
- **No External Servers** - Data sent only to local Flask backend
- **No Accounts** - No registration required
- **Device-Only Data** - Health data never leaves your device
- **Clear Cache** - Delete all predictions by clearing browser cache

---

## Troubleshooting

### Models Not Loading

If you see "Model not available" errors:
1. Verify `.pkl` files exist in `models/` directory
2. Run training scripts in `models/` to generate models
3. Ensure `joblib` and `scikit-learn` are installed

### CORS Errors

If you get cross-origin errors:
1. Install Flask-CORS: `pip install flask-cors`
2. Verify backend is running on port 5000

### Port Already in Use

If port 5000 is busy:
1. Find process: `netstat -ano | findstr :5000`
2. Stop the process or change port in `backend/app.py`

---

## Development

### Training New Models

1. Place dataset in `datasets/` folder
2. Edit corresponding training script in `models/`
3. Update file paths and column names
4. Run the script:
   ```bash
   python models/trained_liver_model.py
   ```
5. New `.pkl` file saved automatically

### Adding New Diseases

1. Create prediction page (copy existing template)
2. Add form fields in `frontend/app.js` under `diseaseForms`
3. Add route in `backend/app.py`
4. Train and save new model
5. Update navigation in sidebar

---

## Browser Support

| Browser | Version | Support |
|---------|---------|---------|
| Chrome | Latest | Full |
| Firefox | Latest | Full |
| Edge | Latest | Full |
| Safari | Latest | Full |

---

## License

This project is for educational and research purposes.

---

## Credits

Built with care for early disease detection. The machine learning models are trained on publicly available medical datasets.
