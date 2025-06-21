import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# ✅ Create necessary directories
os.makedirs('models', exist_ok=True)
os.makedirs('results', exist_ok=True)

# 📥 Load the dataset
df = pd.read_csv('C:\AML-kaushal\AML-2D-System-MyWorks\AML_project\master_dataset (2).csv')

# 🧼 Split features and target
X = df.drop('shape_type', axis=1)
y = df['shape_type']

# 🧪 Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🔍 Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 💾 Save the scaler
joblib.dump(scaler, 'models/scaler.joblib')

# 🌲 Train Random Forest model
model = RandomForestClassifier(random_state=42)
model.fit(X_train_scaled, y_train)

# 💾 Save the trained model
joblib.dump(model, 'models/rf_model.joblib')

# 📈 Predictions
y_pred = model.predict(X_test_scaled)

# 🧮 Evaluation
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred, labels=model.classes_)

cm_df = pd.DataFrame(cm, index=model.classes_, columns=model.classes_)

# 🔥 Plot and save confusion matrix heatmap
plt.figure(figsize=(10, 7))
sns.heatmap(cm_df, annot=True, fmt='d', cmap='Blues')
plt.title("Confusion Matrix")
plt.ylabel("Actual")
plt.xlabel("Predicted")
plt.tight_layout()
plt.savefig('results/confusion_matrix.png')
plt.show()
