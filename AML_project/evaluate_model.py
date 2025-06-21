import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# === 1. Load cleaned dataset ===
data_path = r"C:\AML-kaushal\AML-2D-System-MyWorks\AML_project\cleaned_master_data.csv"  # change if needed
df = pd.read_csv(data_path)

# === 2. Split features and target ===
X = df.drop(columns=['shape_type'])
y = df['shape_type']

# === 3. Load trained model and label encoder ===
model = joblib.load(r"C:\Users\rahhu\Downloads\random_forest_model.pkl")  # path to your model
label_encoder = joblib.load(r"C:\Users\rahhu\Downloads\label_encoder.pkl")  # path to your encoder

# === 4. Encode true labels ===
y_encoded = label_encoder.transform(y)

# === 5. Predict and evaluate ===
y_pred = model.predict(X)

accuracy = accuracy_score(y_encoded, y_pred)
print(f"Accuracy: {accuracy:.2f}")

print("\nClassification Report:")
print(classification_report(y_encoded, y_pred, target_names=label_encoder.classes_))

# === 6. Confusion matrix ===
cm = confusion_matrix(y_encoded, y_pred)
plt.figure(figsize=(10, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.tight_layout()
plt.show()
