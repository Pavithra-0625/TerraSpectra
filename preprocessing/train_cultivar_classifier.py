
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

# Load feature dataset
df = pd.read_csv("outputs/plant_trait_features.csv")

# Cultivar columns
cultivars = ["Heerup", "Kvium", "Rembrandt", "Sheriff"]

# Input features
X = df.drop(columns=[
    "ImageId", "GrainWeight", "Gsw", "PhiPS2",
    "Fertilizer", "Heerup", "Kvium", "Rembrandt", "Sheriff"
])

# Convert one-hot labels into class names
y = df[cultivars].idxmax(axis=1)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Train classifier
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
accuracy = accuracy_score(y_test, y_pred)

print("===== CULTIVAR CLASSIFICATION RESULTS =====")
print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))
print("Accuracy:", round(accuracy, 4))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred, labels=cultivars))

# Save model
joblib.dump(model, "outputs/cultivar_classifier.pkl")

# Save predictions
results = pd.DataFrame({
    "ImageId": df.loc[X_test.index, "ImageId"].values,
    "Actual": y_test.values,
    "Predicted": y_pred
})

results.to_csv("outputs/cultivar_predictions.csv", index=False)

# Confusion matrix plot
cm = confusion_matrix(y_test, y_pred, labels=cultivars)

plt.figure(figsize=(8, 6))

plt.imshow(cm, cmap="Blues")
plt.colorbar()

plt.xticks(range(len(cultivars)), cultivars, rotation=30)
plt.yticks(range(len(cultivars)), cultivars)

for i in range(len(cultivars)):
    for j in range(len(cultivars)):
        plt.text(j, i, cm[i, j], ha="center", va="center")

plt.title("Wheat Cultivar Classification")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()

plt.savefig("outputs/plots/cultivar_confusion_matrix.png")
plt.show()

plt.title("Wheat Cultivar Classification")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()

plt.savefig("outputs/plots/cultivar_confusion_matrix.png")
plt.show()

print("\nModel and results saved successfully!")
