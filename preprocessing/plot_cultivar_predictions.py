
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("outputs/cultivar_predictions.csv")

df["Correct"] = df["Actual"] == df["Predicted"]

summary = df.groupby("Actual")["Correct"].value_counts().unstack(fill_value=0)

summary = summary.reindex(
    ["Heerup", "Kvium", "Rembrandt", "Sheriff"],
    fill_value=0
)

summary.columns = [
    "Incorrect" if col is False else "Correct"
    for col in summary.columns
]

summary.plot(kind="bar", figsize=(9, 5))

plt.title("Cultivar Prediction Results")
plt.xlabel("Actual Cultivar")
plt.ylabel("Number of Images")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("outputs/plots/cultivar_prediction_summary.png")
plt.show()

print("Prediction visualization saved successfully!")
print(summary)
