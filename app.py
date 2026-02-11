import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .metric-label {
        font-size: 14px;
        color: #9aa0a6;
    }
    .metric-value {
        font-size: 32px;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.set_page_config(
    page_title="Player Performance Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
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

st.markdown("## 🔍 Filters")

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        club_filter = st.selectbox(
    "🏟️ Club",
    options=sorted(df["Club"].dropna().unique())
)


    with col2:
        position_filter = st.multiselect(
            "🧍 Position",
            options=df["Position"].unique(),
            default=df["Position"].unique()
        )


position_filter = st.radio(
    "🧍 Position",
    options=df["Position"].unique(),
    horizontal=True
)


filtered_df = df[
    (df["Club"].isin([club_filter])) &
    (df["Position"].isin([position_filter]))
]

# =========================
# TEAM PERFORMANCE DATA
# =========================
team_df = (
    filtered_df
    .groupby("Club", as_index=False)
    .agg({
        "Appearances": "sum",
        "Wins": "sum",
        "Losses": "sum"
    })
)

team_df["Win Rate (%)"] = (
    team_df["Wins"] / team_df["Appearances"] * 100
).round(1)

team_df["Points"] = team_df["Wins"] * 3


# =========================
# KPIs
# =========================
st.markdown("## 📊 Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("👥 Total Players", filtered_df.shape[0])

with col2:
    st.metric("📅 Average Age", round(filtered_df["Age"].mean(), 1))

with col3:
    st.metric("🎮 Total Appearances", int(filtered_df["Appearances"].sum()))

st.markdown("## 🏟️ Team Performance Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🏆 Teams", team_df.shape[0])

with col2:
    st.metric("⚽ Total Team Wins", int(team_df["Wins"].sum()))

with col3:
    st.metric("🎯 Avg Team Win Rate (%)", round(team_df["Win Rate (%)"].mean(), 1))

st.markdown("## 📊 League Standings")

standings = team_df.sort_values(
    by=["Points", "Win Rate (%)"],
    ascending=False
).reset_index(drop=True)

standings.index = standings.index + 1  # Rank starts at 1

st.dataframe(
    standings,
    use_container_width=True
)


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

st.markdown("## 📈 Team Points Comparison")

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(
    standings["Club"],
    standings["Points"]
)
ax.set_title("Team Points by Club")
ax.set_ylabel("Points")
ax.set_xlabel("Club")
ax.tick_params(axis='x', rotation=45)

st.pyplot(fig)


# =========================
# VISUALS
# =========================
st.subheader("📈 Age vs Appearances")

fig, ax = plt.subplots(figsize=(7, 4))
ax.scatter(
    filtered_df["Age"],
    filtered_df["Appearances"],
    alpha=0.7
)
ax.set_title("Age vs Appearances")
ax.set_xlabel("Age")
ax.set_ylabel("Appearances")
st.pyplot(fig)


st.subheader("📊 Wins vs Losses Distribution")

fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(
    filtered_df["Wins"],
    bins=15,
    alpha=0.7,
    label="Wins"
)
ax.hist(
    filtered_df["Losses"],
    bins=15,
    alpha=0.7,
    label="Losses"
)
ax.set_title("Distribution of Wins and Losses")
ax.legend()
st.pyplot(fig)


# =========================
# RAW DATA
# =========================
with st.expander("📁 View Raw Data"):
    st.dataframe(filtered_df, use_container_width=True)
st.markdown("---")
st.markdown(
    "Built by **Angel Michael ** · Python & Streamlit",
    help="Sports Data Analysis Dashboard"
)


