df = load_data()

# Debug: See what columns are present
st.write("Available columns:", df.columns.tolist())

# Guard for missing columns
if df.empty or "Season" not in df.columns or "League" not in df.columns:
    st.error("❌ Could not find required columns: 'Season' and/or 'League'.")
    st.stop()

import streamlit as st
from utilities.utils import get_player_metrics_percentile_ranks, get_metrics_by_position
from visualizations.weighted_rank import get_weighted_rank
from data.retrieve_statbomb_data import get_statsbomb_player_season_stats

# Load the full dataset
@st.cache_data(ttl=14400)
def load_data():
    return get_statsbomb_player_season_stats()

df = load_data()

# Guard against missing data
if df.empty or "Season" not in df.columns or "League" not in df.columns:
    st.error("❌ Could not load season or league data.")
    st.stop()

# Dropdowns
st.title("🧍 Player Profile Summary")
season_list = sorted(df["Season"].dropna().unique())
league_list = sorted(df["League"].dropna().unique())

selected_league = st.selectbox("Select League", league_list)
selected_season = st.selectbox("Select Season", season_list)

df_filtered = df[
    (df["League"] == selected_league) &
    (df["Season"] == selected_season)
]

players = df_filtered["Player Name"].dropna().unique()
selected_player = st.selectbox("Select Player", sorted(players))

# Get the selected player's row
player_row = df_filtered[df_filtered["Player Name"] == selected_player].iloc[0]
position = player_row["Position"]
age = int(player_row["Age"])
minutes = int(player_row["Minutes"])
club = player_row["Team"]

# Metrics
metrics = get_metrics_by_position(position, api="statbomb")
player_df = get_player_metrics_percentile_ranks(df_filtered, selected_player, position, metrics)

if player_df is None or player_df.empty:
    st.error("Player data not found.")
    st.stop()

# Weighted scores
weighted_df = get_weighted_rank(df_filtered, selected_player, selected_league, selected_season, position)
score = weighted_df["Overall Score"].values[0]
score_vs_l1 = weighted_df["Score weighted aganist League One"].values[0]

# 🧾 Profile block
st.markdown(f"""
<div style="background-color:#1a1a1a;padding:1.5rem;border-radius:12px;margin-bottom:1rem;">
    <h2 style="color:#F2F2F2;">{selected_player}</h2>
    <p style="color:#aaa;font-size:14px;">
    <b>Club:</b> {club}<br>
    <b>Position:</b> {position} | <b>Age:</b> {age} | <b>Minutes:</b> {minutes}
    </p>
    <div style="background-color:#2ecc71;padding:0.8rem;border-radius:8px;margin-top:1rem;">
        <b style="color:white;">League Score:</b> {score:.1f} &nbsp;&nbsp;|&nbsp;&nbsp;
        <b style="color:white;">vs League One:</b> {score_vs_l1:.1f}
    </div>
</div>
""", unsafe_allow_html=True)

# 📊 Percentile Bars
st.subheader("📊 Percentile Metrics")

for metric in metrics:
    val = player_df[metric].values[0]
    st.markdown(f"**{metric}** — {int(val)}%")
    st.progress(int(val))
