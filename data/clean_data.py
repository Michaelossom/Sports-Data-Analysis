import pandas as pd

# Load raw dataset
df = pd.read_csv("data/players_2020.csv")

print("Original shape:", df.shape)

# Fill missing categorical values
df["Nationality"].fillna("Unknown", inplace=True)

# Fill missing Age with average age
df["Age"].fillna(df["Age"].mean(), inplace=True)

# Fill all numeric missing values with 0
numeric_cols = df.select_dtypes(include="number").columns
df[numeric_cols] = df[numeric_cols].fillna(0)

# Save cleaned dataset
df.to_csv("data/players_2020_cleaned.csv", index=False)

print("✅ Dataset cleaned and saved as players_2020_cleaned.csv")
