import streamlit as st
from data.retrieve_statbomb_data import get_statsbomb_player_season_stats
from utilities.utils import get_metrics_by_position, get_player_metrics_percentile_ranks
from visualizations.weighted_rank import get_weighted_rank

@st.cache_data(ttl=14400)
def load_data():
    return get_statsbomb_player_season_stats()

df = load_data()

# 🔍 Show available columns
st.write("🔍 Columns in loaded DataFrame:", df.columns.tolist())

# Guard against empty data
if df.empty:
    st.error("❌ No data found.")
    st.stop()

# Guard against missing columns
required_columns = ["Season", "League", "Player Name", "Position", "Minutes", "Age", "Team"]
missing = [col for col in required_columns if col not in df.columns]
if missing:
    st.error(f"❌ Missing columns: {missing}")
    st.stop()

st.title("🧍 Player Profile Summary")

season_list = sorted(df["Season"].dropna().unique())
league_list = sorted(df["League"].dropna().unique())

selected_season = st.selectbox("Select Season", season_list)
selected_league = st.selectbox("Select League", league_list)

filtered_df = df[
    (df["Season"] == selected_season) &
    (df["League"] == selected_league)
]

player_list = sorted(filtered_df["Player Name"].dropna().unique())
selected_player = st.selectbox("Select Player", player_list)

# Pull player row
player_row = filtered_df[filtered_df["Player Name"] == selected_player].iloc[0]
position = player_row["Position"]
club = player_row["Team"]
minutes = int(player_row["Minutes"])
age = int(player_row["Age"])

# Metrics + Percentiles
metrics = get_metrics_by_position(position, api='statbomb')
player_df = get_player_metrics_percentile_ranks(filtered_df, selected_player, position, metrics)

if player_df is None or player_df.empty:
    st.error("Could not find metric values for this player.")
    st.stop()

# Weighted score
rank_df = get_weighted_rank(filtered_df, selected_player, selected_league, selected_season, position)
score = rank_df["Overall Score"].values[0]
score_vs_l1 = rank_df["Score weighted aganist League One"].values[0]

# 🧾 Profile Card
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

# 📊 Percentile Metrics
st.subheader("📊 Percentile Metrics")
for metric in metrics:
    value = player_df[metric].values[0]
    st.markdown(f"**{metric}** — {int(value)}%")
    st.progress(int(value))
