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

# --- 1. Load Dataset ---
df = pd.read_csv(r"C:\Users\admin\Desktop\N.B.K.R.IST Project\datasets\Liver Patient Dataset (LPD)_train.csv", encoding='latin1')

# --- 2. Clean Column Names ---
df.columns = df.columns.str.strip()

# Rename columns (based on actual dataset)
df.rename(columns={
    'Age of the patient': 'age',
    'Gender of the patient': 'gender',
    'Total Bilirubin': 'total_bil',
    'Direct Bilirubin': 'direct_bil',
    'Total Protiens': 'total_proteins',
    'Alkphos Alkaline Phosphotase': 'alk_phos',
    'Sgpt Alamine Aminotransferase': 'sgpt',
    'Sgot Aspartate Aminotransferase': 'sgot',
    'ALB Albumin': 'albumin',
    'A/G Ratio Albumin and Globulin Ratio': 'ag_ratio',
    'Result': 'label'
}, inplace=True)

# --- 3. Encoding Gender ---
df['gender'] = df['gender'].map({'Male': 1, 'Female': 0})

# --- 4. Handle Missing Values ---
df = df.apply(pd.to_numeric, errors='coerce')
df = df.fillna(df.mean())

# --- 5. Convert Label (1 & 2 → YES / NO) ---
# Standard: 1 = Disease, 2 = No Disease
df['label'] = df['label'].replace({
    1: 'YES',
    2: 'NO'
})

# Convert YES/NO to numeric for model
df['label'] = df['label'].map({'YES': 1, 'NO': 0})

# --- 6. Split Data ---
X = df.drop('label', axis=1)
y = df['label']

x_train, x_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --- 7. Model Pipeline ---
pipeline = Pipeline([
    ('scaler', RobustScaler()),
    ('classifier', RandomForestClassifier(random_state=42))
])

# --- 8. Hyperparameter Tuning ---
param_grid = {
    'classifier__n_estimators': [100],
    'classifier__max_depth': [10]
}

grid = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=-1)
grid.fit(x_train, y_train)

final_model = grid.best_estimator_

# --- 9. Evaluation ---
predictions = final_model.predict(x_test)
accuracy = accuracy_score(y_test, predictions)

print("\n--- Liver Disease Model Results ---")
print(f"Accuracy: {accuracy:.4f}")
print(f"Best Parameters: {grid.best_params_}")

# --- 10. Save Model ---
os.makedirs('../models', exist_ok=True)
joblib.dump(final_model, '../models/liver_model.pkl')
print("Model saved at ../models/liver_model.pkl")

# --- 11. Confusion Matrix ---
plt.figure(figsize=(6,4))
cm = confusion_matrix(y_test, predictions)

sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['NO', 'YES'],
            yticklabels=['NO', 'YES'])

plt.title('Confusion Matrix')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.show()

# --- 12. Feature Importance ---
importances = final_model.named_steps['classifier'].feature_importances_

plt.figure(figsize=(8,5))
plt.barh(X.columns, importances)
plt.title('Feature Importance')
plt.xlabel('Score')
plt.show()

# --- 13. ROC Curve ---
probs = final_model.predict_proba(x_test)[:, 1]
fpr, tpr, _ = roc_curve(y_test, probs)

plt.figure(figsize=(6,4))
plt.plot(fpr, tpr, label=f"AUC = {auc(fpr, tpr):.2f}")
plt.plot([0, 1], [0, 1], linestyle='--')

plt.title('ROC Curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend()
plt.show()