import os
import pandas as pd
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

# 1. PSYCHOLOGICAL TAXONOMY (Objective 2)
TAXONOMY = {
    'Authority': [r'ceo', r'admin', r'official', r'director', r'management', r'department', r'security'],
    'Urgency': [r'immediat', r'now', r'deadline', r'urgent', r'asap', r'expir', r'limit', r'quick'],
    'Fear': [r'suspend', r'risk', r'unauthoriz', r'breach', r'lock', r'warn', r'legal', r'compromis'],
    'Elicitation': [r'click', r'login', r'updat', r'submit', r'download', r'confirm', r'verify', r'access']
}

# 2. DATA LOADING
def load_extracted_data():
    data = []
    sources = {'spam': 1, 'spam_2': 1, 'easy_ham': 0, 'easy_ham_2': 0, 'hard_ham': 0}
    print("--- Objective 3: Quantitative Mapping ---")
    for folder, label in sources.items():
        path = os.path.join(os.getcwd(), folder)
        if os.path.exists(path):
            print(f"Reading folder: {folder}...")
            for filename in os.listdir(path):
                file_path = os.path.join(path, filename)
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, 'r', encoding='latin-1', errors='ignore') as f:
                            data.append({'text': f.read(), 'label': label})
                    except: continue
    return pd.DataFrame(data)

# 3. FEATURE EXTRACTION
def extract_features(text):
    text = str(text).lower()
    features = {cat: sum(len(re.findall(p, text)) for p in patterns) for cat, patterns in TAXONOMY.items()}
    total_words = len(text.split())
    features['Density'] = (sum(features.values()) / total_words * 100) if total_words > 0 else 0
    return pd.Series(features)

# --- EXECUTION ---
df = load_extracted_data()
features_df = df['text'].apply(extract_features)
df = pd.concat([df, features_df], axis=1)

# 4. MODEL VALIDATION (Objective 4)
X = df[list(TAXONOMY.keys()) + ['Density']]
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Metrics
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
print(f"ROC-AUC Score: {roc_auc_score(y_test, model.predict_proba(X_test)[:, 1]):.4f}")

# --- VISUALIZATION SUITE ---

# Synergy Heatmap
plt.figure(figsize=(8,6))
sns.heatmap(df[df['label']==1][list(TAXONOMY.keys())].corr(), annot=True, cmap='Reds')
plt.title("Synergy Matrix: Trigger Correlations")
plt.savefig('synergy_matrix.png')

# Feature Importance
importances = model.feature_importances_
plt.figure(figsize=(8,5))
plt.bar(X.columns, importances)
plt.title("Feature Importance: Predictive Power of Biases")
plt.savefig('feature_importance.png')

# Trigger Intensity Comparison
plt.figure(figsize=(8,5))
sns.violinplot(x='label', y='Density', data=df)
plt.title("Density Distribution: Phishing (1) vs Ham (0)")
plt.savefig('trigger_density.png')

# Co-occurrence Matrix
binary_df = (df[list(TAXONOMY.keys())] > 0).astype(int)
co_occurrence = binary_df.T.dot(binary_df)
plt.figure(figsize=(8,6))
sns.heatmap(co_occurrence, annot=True, fmt='d', cmap='Greens')
plt.title("Co-occurrence Matrix: Structural Synergy")
plt.savefig('synergy_co_occurrence.png')

# Confusion Matrix
plt.figure(figsize=(6,5))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix: Risk Scoring')
plt.savefig('confusion_matrix.png')

print("\nAll diagnostics saved successfully.")