import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle

# Load dataset
file_path = r"C:\AML-kaushal\AML-2D-System-MyWorks\AML_project\cleaned_master_data.csv"  # 🔁 Replace with your actual CSV file
data = pd.read_csv(file_path)

# Show available columns
print("📄 Columns in dataset:", data.columns.tolist())

# Manually set label column
label_column = "shape_type"
print(f"✅ Using '{label_column}' as label column.")

# Separate features and target
X = data.drop(label_column, axis=1)
y = data[label_column]

# Encode labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Define model and hyperparameters
model = RandomForestClassifier(random_state=42)
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10]
}

# Perform grid search
grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, verbose=2, n_jobs=-1)
grid_search.fit(X_train, y_train)

# Best model
best_model = grid_search.best_estimator_

# Evaluate
y_pred = best_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\n✅ Accuracy: {accuracy:.4f}\n")
print("📊 Classification Report:\n", classification_report(y_test, y_pred, target_names=label_encoder.classes_))
print("🧩 Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Save model and encoder
with open("optimized_model.pkl", "wb") as f:
    pickle.dump(best_model, f)
with open("label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

print("✅ Optimized model and label encoder saved successfully.")
