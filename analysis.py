import pandas as pd

print("🧤 Goalkeeper Analysis Started")

# Load cleaned dataset
df = pd.read_csv("data/players_2020_cleaned.csv")

print("\nDataset shape:", df.shape)

# Top goalkeepers by saves
print("\n🏆 Top 10 Goalkeepers by Saves")
top_saves = (
    df.sort_values("Saves", ascending=False)
    [["Saves", "Clean sheets", "Yellow cards", "Red cards"]]
    .head(10)
)
print(top_saves)

# Discipline analysis
print("\n🟨 Goalkeepers with most yellow cards")
print(
    df.sort_values("Yellow cards", ascending=False)
    [["Yellow cards", "Fouls"]]
    .head(5)
)

print("\n🟥 Goalkeepers with red cards")
print(
    df[df["Red cards"] > 0]
    [["Red cards", "Fouls"]]
    .head(5)
)
