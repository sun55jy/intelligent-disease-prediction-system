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
kidney_df = pd.read_csv('C:/Users/admin/Desktop/N.B.K.R.IST Project/datasets/kidney_cleaned.csv')

# --- 2. Data Preprocessing ---
kidney_df.columns = kidney_df.columns.str.strip()

# Drop irrelevant columns
if 'ID' in kidney_df.columns:
    kidney_df.drop('ID', axis=1, inplace=True)

# Clean whitespace and tab artifacts
kidney_df.replace(to_replace=r'\t', value='', regex=True, inplace=True)

# Standardize categorical mapping
mapping = {
    'yes': 1, 'no': 0,
    'ckd': 1, 'notckd': 0,
    'present': 1, 'notpresent': 0,
    'abnormal': 1, 'normal': 0,
    'good': 1, 'poor': 0
}

for col in kidney_df.columns:
    if kidney_df[col].dtype == 'object':
        kidney_df[col] = kidney_df[col].str.strip().str.lower()

kidney_df.replace(mapping, inplace=True)

# Convert all columns to numeric and fill missing values
kidney_df = kidney_df.apply(pd.to_numeric, errors='coerce')
kidney_df = kidney_df.fillna(kidney_df.mean())

# --- 3. Split into Parameters and Labels ---
x_parameters = kidney_df.drop('Status', axis=1)
y_parameters = kidney_df['Status']

x_train, x_test, y_train, y_test = train_test_split(
    x_parameters, y_parameters, test_size=0.2, random_state=42
)

# --- 4. Building the Model Pipeline ---
kidney_pipeline = Pipeline([
    ('scaler', RobustScaler()),
    ('classifier', RandomForestClassifier(random_state=42))
])

search_space = {
    'classifier__n_estimators': [100, 200],
    'classifier__max_depth': [5, 10, None]
}

kidney_grid = GridSearchCV(kidney_pipeline, search_space, cv=5, n_jobs=-1)
kidney_grid.fit(x_train, y_train)

final_model = kidney_grid.best_estimator_

# --- 5. Evaluation ---
predictions = final_model.predict(x_test)
final_accuracy = accuracy_score(y_test, predictions)

print(f"--- Kidney Disease Model Results ---")
print(f"Accuracy Achieved: {final_accuracy:.4f}")
print(f"Optimized Parameters: {kidney_grid.best_params_}")

# --- 6. Persistence ---
os.makedirs('../models', exist_ok=True)
joblib.dump(final_model, '../models/kidney_model.pkl')
print("Model persists in ../models/kidney_model.pkl")

# --- 7. Visual Insights ---
# Confusion Matrix
plt.figure(figsize=(6,4))
sns.heatmap(confusion_matrix(y_test, predictions), annot=True, fmt='d', cmap='Greens')
plt.title('Kidney Disease Confusion Matrix')
plt.ylabel('Actual Status')
plt.xlabel('Predicted Status')
plt.show()

# Feature Importance
importances = final_model.named_steps['classifier'].feature_importances_
plt.figure(figsize=(8,6))
plt.barh(x_parameters.columns, importances, color='seagreen')
plt.title('Kidney Feature Importance')
plt.xlabel('Importance Score')
plt.show()

# ROC Curve
probs = final_model.predict_proba(x_test)[:, 1]
fpr, tpr, _ = roc_curve(y_test, probs)
plt.figure(figsize=(6,4))
plt.plot(fpr, tpr, label=f'AUC: {auc(fpr, tpr):.2f}', color='darkgreen')
plt.plot([0, 1], [0, 1], linestyle='--', color='gray')
plt.title('ROC Curve (Kidney)')
plt.legend()
plt.show()