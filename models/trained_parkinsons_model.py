import pandas as pd
import numpy as np
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, roc_curve, auc

# --- 1. Load the Dataset ---
parkinsons_df = pd.read_csv(r'C:\Users\admin\Desktop\N.B.K.R.IST Project\datasets\parkinsons_cleaned.csv')

# --- 2. Data Preprocessing ---
parkinsons_df.columns = parkinsons_df.columns.str.strip()

# Drop metadata columns
if 'name' in parkinsons_df.columns:
    parkinsons_df.drop('name', axis=1, inplace=True)
if 'Unnamed: 0' in parkinsons_df.columns:
    parkinsons_df.drop('Unnamed: 0', axis=1, inplace=True)

# Handle categorical target values ('Yes'/'No') before numeric conversion
target_col = 'Disease_Status'
if parkinsons_df[target_col].dtype == 'object':
    parkinsons_df[target_col] = parkinsons_df[target_col].str.strip().str.lower().map({'yes': 1, 'no': 0})

# Convert all features to numeric and handle missing data
parkinsons_df = parkinsons_df.apply(pd.to_numeric, errors='coerce')
parkinsons_df.dropna(subset=[target_col], inplace=True)
parkinsons_df = parkinsons_df.fillna(parkinsons_df.mean())

# --- 3. Split into Parameters and Labels ---
x_parameters = parkinsons_df.drop(target_col, axis=1)
y_parameters = parkinsons_df[target_col]

x_train, x_test, y_train, y_test = train_test_split(
    x_parameters, y_parameters, test_size=0.2, random_state=42
)

# --- 4. Building the Model Pipeline ---
parkinsons_pipeline = Pipeline([
    ('scaler', RobustScaler()),
    ('classifier', RandomForestClassifier(random_state=42))
])

search_space = {
    'classifier__n_estimators': [100, 200],
    'classifier__max_depth': [5, 10, None]
}

parkinsons_grid = GridSearchCV(parkinsons_pipeline, search_space, cv=5, n_jobs=-1)
parkinsons_grid.fit(x_train, y_train)

final_model = parkinsons_grid.best_estimator_

# --- 5. Evaluation ---
predictions = final_model.predict(x_test)
final_accuracy = accuracy_score(y_test, predictions)

print(f"--- Parkinson's Disease Model Results ---")
print(f"Accuracy Achieved: {final_accuracy:.4f}")
print(f"Optimized Parameters: {parkinsons_grid.best_params_}")

# --- 6. Persistence ---
os.makedirs('../models', exist_ok=True)
joblib.dump(final_model, '../models/parkinsons_model.pkl')
print("Model persists in ../models/parkinsons_model.pkl")

# --- 7. Visual Insights ---
# Confusion Matrix
plt.figure(figsize=(6,4))
sns.heatmap(confusion_matrix(y_test, predictions), annot=True, fmt='d', cmap='Oranges')
plt.title('Parkinson\'s Prediction Confusion Matrix')
plt.ylabel('Actual Status')
plt.xlabel('Predicted Status')
plt.show()

# Feature Importance
importances = final_model.named_steps['classifier'].feature_importances_
plt.figure(figsize=(8,6))
plt.barh(x_parameters.columns, importances, color='chocolate')
plt.title('Key Parkinson\'s Diagnostic Features')
plt.xlabel('Importance Score')
plt.show()

# ROC Curve
probs = final_model.predict_proba(x_test)[:, 1]
fpr, tpr, _ = roc_curve(y_test, probs)
plt.figure(figsize=(6,4))
plt.plot(fpr, tpr, label=f'AUC: {auc(fpr, tpr):.2f}', color='darkred')
plt.plot([0, 1], [0, 1], linestyle='--', color='gray')
plt.title('ROC Curve (Parkinson\'s)')
plt.legend()
plt.show()