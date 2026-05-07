import pandas as pd

CSV_PATH = "randomness_100_results.csv"

df = pd.read_csv(CSV_PATH)

df["random_score"] = pd.to_numeric(df["random_score"], errors="coerce")
df = df.dropna(subset=["image_name", "random_score"])

# fake = 1, real = 0
df["actual_label"] = df["image_name"].str.lower().str.startswith("fake").astype(int)

# Average randomness per image
image_scores = df.groupby("image_name").agg(
    avg_random_score=("random_score", "mean"),
    actual_label=("actual_label", "first")
).reset_index()

# Since correlation is positive:
# higher randomness -> fake

THRESHOLD = 3.0

image_scores["predicted_label"] = (
    image_scores["avg_random_score"] >= THRESHOLD
).astype(int)

image_scores["correct"] = (
    image_scores["predicted_label"] == image_scores["actual_label"]
)

accuracy = image_scores["correct"].mean() * 100

print("\n=== Prediction Accuracy ===")
print(f"Accuracy: {accuracy:.2f}%")
print(f"Correct Predictions: {image_scores['correct'].sum()}")
print(f"Total Images: {len(image_scores)}")

image_scores.to_csv("prediction_accuracy_100.csv", index=False)

print("\nSaved: prediction_accuracy_100.csv")