import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# Load dataset
df = pd.read_csv("outputs/plant_trait_features.csv")

# Select PCA features
X = df.drop(columns=[
    "ImageId", "GrainWeight", "Gsw", "PhiPS2",
    "Fertilizer", "Heerup", "Kvium", "Rembrandt", "Sheriff"
])

# Eight prediction targets
targets = [
    "GrainWeight", "Gsw", "PhiPS2", "Fertilizer",
    "Heerup", "Kvium", "Rembrandt", "Sheriff"
]

results = []

for target in targets:

    print("\n==============================")
    print("TARGET:", target)
    print("==============================")

    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    models = {
        "Random Forest": RandomForestRegressor(
            n_estimators=100, random_state=42
        ),
        "Decision Tree": DecisionTreeRegressor(random_state=42),
        "Linear Regression": LinearRegression()
    }

    for name, model in models.items():

        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        r2 = r2_score(y_test, predictions)
        mae = mean_absolute_error(y_test, predictions)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))

        results.append([target, name, r2, mae, rmse])

        print("\nModel:", name)
        print("R2:", round(r2, 4))
        print("MAE:", round(mae, 4))
        print("RMSE:", round(rmse, 4))

# Save results
results_df = pd.DataFrame(
    results,
    columns=["Target", "Model", "R2", "MAE", "RMSE"]
)

results_df.to_csv(
    "outputs/all_trait_model_results.csv", index=False
)

print("\n================================")
print("ALL TARGETS COMPLETED")
print("Total experiments:", len(results_df))
print("Saved: outputs/all_trait_model_results.csv")
print("================================")