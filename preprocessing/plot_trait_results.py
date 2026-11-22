import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

df = pd.read_csv("outputs/best_trait_models.csv")

Path("outputs/plots").mkdir(parents=True, exist_ok=True)

metrics = ["R2", "MAE", "RMSE"]

for metric in metrics:

    plt.figure(figsize=(11, 6))

    bars = plt.bar(df["Target"], df[metric])

    # Log scale for MAE and RMSE
    if metric in ["MAE", "RMSE"]:
        plt.yscale("log")

    plt.title(f"{metric} Comparison Across Plant Traits")
    plt.xlabel("Plant Traits")
    plt.ylabel(metric)
    plt.xticks(rotation=45)

    # Display values above bars
    for bar, value in zip(bars, df[metric]):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            value,
            f"{value:.3f}",
            ha="center",
            va="bottom",
            fontsize=8
        )

    plt.tight_layout()

    filename = f"outputs/plots/{metric.lower()}_comparison.png"
    plt.savefig(filename, dpi=300)
    plt.close()

    print("Saved:", filename)

print("\nAll plots updated successfully!")