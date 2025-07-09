import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import os

from data.retrieve_wyscout_data import get_wyscout_player_season_stats

st.set_page_config(
    page_title="Player Profile",
    page_icon="🎯",
    layout="wide",
)

# Load pre-processed wyscout data
wyscout_data = get_wyscout_player_season_stats()

# Sidebar selectors
st.sidebar.title("Player Profile Filter")
selected_league = st.sidebar.selectbox("Select League", sorted(wyscout_data["League"].dropna().unique()))
filtered_league_df = wyscout_data[wyscout_data["League"] == selected_league]

selected_season = st.sidebar.selectbox("Select Season", sorted(filtered_league_df["Season"].dropna().unique()))
filtered_season_df = filtered_league_df[filtered_league_df["Season"] == selected_season]

selected_player = st.sidebar.selectbox("Select Player", sorted(filtered_season_df["Player Name"].unique()))
player_df = filtered_season_df[filtered_season_df["Player Name"] == selected_player].reset_index(drop=True)

if player_df.empty:
    st.warning("No data found for this player.")
    st.stop()

# Extract player info
player = player_df.iloc[0]
basic_info_cols = ["Player Name", "Age", "Position", "Minutes", "Team", "Market value", "Contract expires", "Foot", "Height", "Weight"]
metrics_cols = [
    "GOALS", "xG", "ASSISTS", "xA",
    "DUELS PER 90", "DUELS WON %",
    "SUCCESSFUL DEFENSIVE ACTIONS PER 90", "DEFENSIVE DUELS PER 90", "DEFENSIVE DUELS WON %",
    "DRIBBLES PER 90", "SUCCESSFUL DRIBBLES %",
    "PASSING ACCURACY" if "PASSING ACCURACY" in player_df.columns else "ACCURATE PASSES %",
    "PROGRESSIVE PASSES PER 90", "TOUCHES IN BOX PER 90"
]

# Layout: Card style
st.markdown(f"""
    <div style='background-color:#f4f4f4;padding:30px;border-radius:15px;box-shadow:0 4px 8px rgba(0,0,0,0.1);'>
        <h2 style='margin-bottom:5px;'>{player['Player Name']}</h2>
        <p style='font-size:18px;margin-top:0;color:#666;'>{player['Team']} | {player['Position']} | Age: {player['Age']}</p>
        <hr style='margin:10px 0;'>
        <p><strong>Minutes Played:</strong> {int(player['Minutes'])}</p>
        <p><strong>Foot:</strong> {player['Foot']} &nbsp;&nbsp; <strong>Height:</strong> {player['Height']} cm &nbsp;&nbsp; <strong>Weight:</strong> {player['Weight']} kg</p>
        <p><strong>Market Value:</strong> {player['Market value']} &nbsp;&nbsp; <strong>Contract:</strong> {player['Contract expires']}</p>
    </div>
""", unsafe_allow_html=True)

# Spacer
st.markdown("###")

# Metrics Grid
st.subheader("Performance Summary")
cols = st.columns(3)
for i, col in enumerate(cols * ((len(metrics_cols) + 2)//3)):
    if i < len(metrics_cols):
        metric = metrics_cols[i]
        try:
            value = player[metric]
            if isinstance(value, float):
                value = f"{value:.2f}"
            col.metric(label=metric.title(), value=value)
        except KeyError:
            col.metric(label=metric.title(), value="N/A")

# Optionally: add photo or club badge (placeholder if no API logic yet)
img_col1, img_col2 = st.columns([1, 5])
with img_col1:
    try:
        player_img_path = f"./assets/players/{player['Player Name'].replace(' ', '_')}.png"
        if os.path.exists(player_img_path):
            st.image(player_img_path, width=120)
        else:
            st.image("https://via.placeholder.com/120x150?text=Player", width=120)
    except:
        pass

with img_col2:
    st.markdown("#### Notes")
    st.info("You can customize this section with scouting insights or AI-written blurbs based on stats.")

