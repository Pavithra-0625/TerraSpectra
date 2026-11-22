import numpy as np
import pandas as pd
from pathlib import Path

labels = pd.read_csv("outputs/reports/matched_training_labels.csv")
pca_folder = Path("data/processed/shared_pca")

records = []

for _, row in labels.iterrows():
    image_id = int(row["ImageId"])
    file = pca_folder / f"{image_id:05d}_pca.npy"

    cube = np.load(file)

    features = {"ImageId": image_id}

    for i in range(cube.shape[0]):
        features[f"PC{i+1}_mean"] = float(np.mean(cube[i]))
        features[f"PC{i+1}_std"] = float(np.std(cube[i]))

    records.append(features)

feature_df = pd.DataFrame(records)

target_columns = [
    "GrainWeight", "Gsw", "PhiPS2", "Fertilizer",
    "Heerup", "Kvium", "Rembrandt", "Sheriff"
]

final_df = feature_df.merge(
    labels[["ImageId"] + target_columns],
    on="ImageId"
)

Path("outputs").mkdir(exist_ok=True)
final_df.to_csv("outputs/plant_trait_features.csv", index=False)

print("===== TERRASPECTRA FEATURE DATASET =====")
print("Images:", len(final_df))
print("Total columns:", len(final_df.columns))
print("PCA features:", 40)
print("Target columns:", len(target_columns))
print("Saved: outputs/plant_trait_features.csv")
print(final_df.head())
