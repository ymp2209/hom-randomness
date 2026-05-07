import pandas as pd
from scipy.stats import pearsonr

CSV_PATH = "randomness_100_results.csv"

# Read CSV
df = pd.read_csv(CSV_PATH)

# Convert random score to numeric
df["random_score"] = pd.to_numeric(df["random_score"], errors="coerce")

# Remove invalid rows
df = df.dropna(subset=["image_name", "random_score"])

# Create fake/real label
# fake = 1
# real = 0
df["fake_label"] = df["image_name"].str.lower().str.startswith("fake").astype(int)

print("Rows used:", len(df))
print("Fake rows:", (df["fake_label"] == 1).sum())
print("Real rows:", (df["fake_label"] == 0).sum())

# Calculate Pearson correlation
r, p = pearsonr(df["fake_label"], df["random_score"])

print("\n=== Correlation Result ===")
print(f"Correlation (r): {r:.4f}")
print(f"P-value: {p:.6f}")

# Interpretation
if r < 0:
    print("\nInterpretation:")
    print("Higher randomness scores are associated with LESS fake images.")
else:
    print("\nInterpretation:")
    print("Higher randomness scores are associated with MORE fake images.")