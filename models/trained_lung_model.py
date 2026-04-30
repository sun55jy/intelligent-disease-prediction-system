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
lung_df = pd.read_csv('C:/Users/admin/Desktop/N.B.K.R.IST Project/datasets/Lung Cancer Dataset.csv')

# --- 2. Data Preprocessing ---
lung_df.columns = lung_df.columns.str.strip()

target_col = 'PULMONARY_DISEASE'

# Encoding Gender (M: 1, F: 0)
lung_df['GENDER'] = lung_df['GENDER'].map({'M': 1, 'F': 0})

# Handle other categorical and numeric 1/2 mappings
for col in lung_df.columns:
    if col == 'GENDER':
        continue

    # Convert categorical strings to numeric
    if lung_df[col].dtype == 'object':
        if lung_df[col].astype(str).str.upper().isin(['YES', 'NO']).any():
            lung_df[col] = lung_df[col].str.upper().map({'YES': 1, 'NO': 0})
        lung_df[col] = pd.to_numeric(lung_df[col], errors='coerce')

    # Convert 1/2 encoding to 0/1 for features
    if col != target_col and lung_df[col].isin([1, 2]).all():
        lung_df[col] = lung_df[col].replace({1: 0, 2: 1})

# Fill missing values and handle target integrity
lung_df = lung_df.fillna(lung_df.mean())

# --- 3. Split into Parameters and Labels ---
x_parameters = lung_df.drop(target_col, axis=1)
y_parameters = lung_df[target_col]

x_train, x_test, y_train, y_test = train_test_split(
    x_parameters, y_parameters, test_size=0.2, random_state=42, stratify=y_parameters
)

# --- 4. Building the Model Pipeline ---
lung_pipeline = Pipeline([
    ('scaler', RobustScaler()),
    ('classifier', RandomForestClassifier(random_state=42))
])

search_space = {
    'classifier__n_estimators': [100, 200],
    'classifier__max_depth': [5, 10, None]
}

lung_grid = GridSearchCV(lung_pipeline, search_space, cv=5, n_jobs=-1)
lung_grid.fit(x_train, y_train)

final_model = lung_grid.best_estimator_

# --- 5. Evaluation ---
predictions = final_model.predict(x_test)
final_accuracy = accuracy_score(y_test, predictions)

print(f"--- Lung Cancer Model Results ---")
print(f"Accuracy Achieved: {final_accuracy:.4f}")
print(f"Optimized Parameters: {lung_grid.best_params_}")

# --- 6. Persistence ---
os.makedirs('../models', exist_ok=True)
joblib.dump(final_model, '../models/lung_model.pkl')
print("Model persists in ../models/lung_model.pkl")

# --- 7. Visual Insights ---
# Confusion Matrix
plt.figure(figsize=(6,4))
sns.heatmap(confusion_matrix(y_test, predictions), annot=True, fmt='d', cmap='Reds')
plt.title('Lung Cancer Confusion Matrix')
plt.ylabel('Actual Status')
plt.xlabel('Predicted Status')
plt.show()

# Feature Importance
importances = final_model.named_steps['classifier'].feature_importances_
plt.figure(figsize=(8,6))
plt.barh(x_parameters.columns, importances, color='crimson')
plt.title('Lung Cancer Key Indicators')
plt.xlabel('Importance Score')
plt.show()

# ROC Curve
probs = final_model.predict_proba(x_test)[:, 1]
fpr, tpr, _ = roc_curve(y_test, probs)
plt.figure(figsize=(6,4))
plt.plot(fpr, tpr, label=f'AUC: {auc(fpr, tpr):.2f}', color='red')
plt.plot([0, 1], [0, 1], linestyle='--', color='gray')
plt.title('ROC Curve (Lung Cancer)')
plt.legend()
plt.show()