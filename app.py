import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Player Performance Dashboard",
    layout="wide"
)

st.title("⚽ Player Performance & Participation Dashboard")
st.markdown("Analysis based on appearances, wins, and losses")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("data/players_2020_cleaned.csv")

df = load_data()

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🔍 Filters")

club_filter = st.sidebar.multiselect(
    "Select Club(s)",
    options=df["Club"].unique(),
    default=df["Club"].unique()
)

position_filter = st.sidebar.multiselect(
    "Select Position(s)",
    options=df["Position"].unique(),
    default=df["Position"].unique()
)

filtered_df = df[
    (df["Club"].isin(club_filter)) &
    (df["Position"].isin(position_filter))
]

# =========================
# KPIs
# =========================
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Players", filtered_df.shape[0])
col2.metric("Average Age", round(filtered_df["Age"].mean(), 1))
col3.metric("Total Appearances", int(filtered_df["Appearances"].sum()))

# =========================
# PERFORMANCE ANALYSIS
# =========================
st.subheader("🏆 Player Performance Overview")

filtered_df["Win Rate (%)"] = (
    filtered_df["Wins"] / filtered_df["Appearances"] * 100
).fillna(0)

top_players = filtered_df.sort_values(
    "Win Rate (%)", ascending=False
).head(10)

st.dataframe(top_players, use_container_width=True)

# =========================
# VISUALS
# =========================
st.subheader("📈 Age vs Appearances")

fig1, ax1 = plt.subplots()
ax1.scatter(
    filtered_df["Age"],
    filtered_df["Appearances"]
)
ax1.set_xlabel("Age")
ax1.set_ylabel("Appearances")
st.pyplot(fig1)

st.subheader("📊 Wins vs Losses Distribution")

fig2, ax2 = plt.subplots()
ax2.hist(
    [filtered_df["Wins"], filtered_df["Losses"]],
    label=["Wins", "Losses"],
    bins=15
)
ax2.legend()
st.pyplot(fig2)

# =========================
# RAW DATA
# =========================
st.subheader("📁 Raw Data")
st.dataframe(filtered_df, use_container_width=True)
# =========================
# ADVANCED METRICS
# =========================
st.subheader("🧠 Advanced Player Metrics")

filtered_df["Win Rate (%)"] = (
    filtered_df["Wins"] / filtered_df["Appearances"] * 100
).fillna(0)

filtered_df["Consistency Score"] = (
    filtered_df["Appearances"] - filtered_df["Losses"]
)

filtered_df["Impact Score"] = (
    (filtered_df["Wins"] * 3) +
    filtered_df["Appearances"] -
    (filtered_df["Losses"] * 2)
)

# =========================
# TOP PLAYERS
# =========================
st.subheader("🌟 Top Players by Impact Score")

top_impact = filtered_df.sort_values(
    "Impact Score", ascending=False
).head(10)

st.dataframe(
    top_impact[
        [
            "Jersey Number",
            "Club",
            "Position",
            "Age",
            "Appearances",
            "Wins",
            "Losses",
            "Win Rate (%)",
            "Consistency Score",
            "Impact Score"
        ]
    ],
    use_container_width=True
)
