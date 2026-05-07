import pandas as pd

CSV_PATH = "randomness_100_results.csv"

df = pd.read_csv(CSV_PATH)

df["random_score"] = pd.to_numeric(df["random_score"], errors="coerce")
df = df.dropna(subset=["image_name", "random_score"])

# fake = 1, real = 0
df["fake_label"] = df["image_name"].str.lower().str.startswith("fake").astype(int)

print("Rows used:", len(df))
print("Fake rows:", (df["fake_label"] == 1).sum())
print("Real rows:", (df["fake_label"] == 0).sum())

# Pearson correlation using pandas
r = df["fake_label"].corr(df["random_score"])

print("\n=== Correlation Result ===")
print(f"Fake label vs randomness score: r = {r:.4f}")

if r < 0:
    print("Interpretation: Higher randomness scores are associated with LESS fake images.")
else:
    print("Interpretation: Higher randomness scores are associated with MORE fake images.")