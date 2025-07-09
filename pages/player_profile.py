import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

# --- Import your Wyscout processing function ---
from wyscout_parser import get_wyscout_player_season_stats  # adjust if needed

st.set_page_config(layout="wide")
st.title("🎯 Player Profile Summary")

# --- Load and prepare data ---
DATA_DIR = "data/uploads"  # Adjust if needed
files = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith(".xlsx")]
if not files:
    st.warning("Upload Wyscout Excel files to begin.")
    st.stop()

df = get_wyscout_player_season_stats(files)

# --- Player selector ---
player_list = df["Player"].sort_values().unique()
selected_player = st.selectbox("Select player", player_list)
player = df[df["Player"] == selected_player].iloc[0]

# --- Position group mappings ---
position_group_map = {
    "Left Back": "FB", "Right Back": "FB",
    "Centre Back": "CB",
    "Central Midfield": "CM", "Defensive Midfield": "CM",
    "Attacking Midfield": "AM",
    "Left Winger": "W", "Right Winger": "W",
    "Centre Forward": "ST"
}

position_to_metrics = {
    "FB": ["ASSISTS", "xA", "CROSSES PER 90", "DEFENSIVE DUELS PER 90", "DEFENSIVE DUELS WON %", "PROGRESSIVE PASSES PER 90"],
    "CB": ["DEFENSIVE DUELS PER 90", "DEFENSIVE DUELS WON %", "AERIAL DUELS WON %", "PASSING ACCURACY", "CLEARANCES PER 90"],
    "CM": ["ASSISTS", "xA", "PASSING ACCURACY", "PROGRESSIVE PASSES PER 90", "DEFENSIVE DUELS PER 90"],
    "AM": ["GOALS", "xG", "ASSISTS", "xA", "DRIBBLES PER 90", "SUCCESSFUL DRIBBLES %"],
    "W": ["GOALS", "xG", "ASSISTS", "xA", "DRIBBLES PER 90", "TOUCHES IN BOX PER 90"],
    "ST": ["GOALS", "xG", "TOUCHES IN BOX PER 90", "SHOT ACCURACY %"]
}

# --- Infer position group ---
position_raw = player["Position"]
pos_group = position_group_map.get(position_raw)

if not pos_group or pos_group not in position_to_metrics:
    st.warning(f"No metric mapping found for position: {position_raw}")
    st.stop()

metrics = position_to_metrics[pos_group]

# --- Subset comparison group ---
df["PosGroup"] = df["Position"].map(position_group_map)
compare_df = df[df["PosGroup"] == pos_group].copy()

# --- Compute percentiles ---
percentiles = {}
for metric in metrics:
    if metric not in compare_df.columns:
        continue
    values = compare_df[metric].dropna()
    player_value = player[metric]
    try:
        percentile = sum(values < player_value) / len(values) * 100
        percentiles[metric] = round(percentile)
    except:
        percentiles[metric] = None

# --- Plotting ---
fig, ax = plt.subplots(figsize=(7, len(percentiles) * 0.6))

metric_names = list(percentiles.keys())
scores = [percentiles[m] for m in metric_names]

# Color bands
colors = []
for val in scores:
    if val >= 70:
        colors.append('#2ecc71')  # Green
    elif val >= 50:
        colors.append('#f39c12')  # Amber
    else:
        colors.append('#e74c3c')  # Red

bars = ax.barh(metric_names, scores, color=colors, edgecolor='black')

# Text inside bars
for bar, val in zip(bars, scores):
    ax.text(val + 2, bar.get_y() + bar.get_height()/2, f"{val}%", va='center', fontsize=10)

# Chart aesthetics
ax.set_xlim(0, 100)
ax.set_xlabel("Percentile vs Same Position Group")
ax.invert_yaxis()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.grid(axis='x', linestyle='--', alpha=0.5)

# Color legend
green_patch = mpatches.Patch(color='#2ecc71', label='≥ 70%')
amber_patch = mpatches.Patch(color='#f39c12', label='50–69%')
red_patch = mpatches.Patch(color='#e74c3c', label='< 50%')
ax.legend(handles=[green_patch, amber_patch, red_patch], loc='lower right')

st.pyplot(fig)
