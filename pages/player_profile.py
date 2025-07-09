import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

from data.retrieve_wyscout_data import get_wyscout_player_season_stats

st.set_page_config(layout="wide")

st.title("Player Profile View (Jack Diamond Style)")

# Load the Wyscout data
if "wyscout_data" not in st.session_state:
    try:
        wyscout_data = get_wyscout_player_season_stats()
        st.session_state["wyscout_data"] = wyscout_data
    except Exception as e:
        st.error("No Wyscout data loaded. Please upload data on the upload page.")
        st.stop()

df = st.session_state["wyscout_data"]

# Position-specific metrics
position_metric_map = {
    "Centre Forward": ["GOALS PER 90", "xG PER 90", "SHOTS PER 90", "ASSISTS PER 90", "TOUCHES IN BOX PER 90", "OFFENSIVE DUELS WON %"],
    "Winger": ["GOALS PER 90", "xA PER 90", "CROSSES PER 90", "SUCCESSFUL DRIBBLES %", "TOUCHES IN BOX PER 90", "PROGRESSIVE RUNS PER 90"],
    "Number 6": ["DEFENSIVE DUELS WON %", "INTERCEPTIONS PER 90", "xA PER 90", "PASS TO FINAL THIRD PER 90", "SMART PASSES PER 90", "PASS ACCURACY %"],
    "Centre Back": ["DEFENSIVE DUELS WON %", "AERIAL DUELS WON %", "INTERCEPTIONS PER 90", "PADJ SLIDING TACKLES", "PASS ACCURACY %", "LONG PASSES PER 90"],
    "Full Back": ["CROSSES PER 90", "ACCURATE CROSSES %", "INTERCEPTIONS PER 90", "SMART PASSES PER 90", "DEFENSIVE DUELS WON %", "PROGRESSIVE RUNS PER 90"],
    "Goal Keeper": ["SAVE RATE (%)", "CLEAN SHEETS", "PREVENTED GOALS PER 90", "EXITS PER 90"]
}

# Sidebar selections
player_list = df["Player Name"].unique()
selected_player = st.sidebar.selectbox("Select Player", player_list)

player_df = df[df["Player Name"] == selected_player]

if player_df.empty:
    st.warning("Player data not found.")
    st.stop()

player_row = player_df.iloc[0]
player_position = player_row["Position"]
metrics = position_metric_map.get(player_position, [])

if not metrics:
    st.warning(f"No metrics configured for position: {player_position}")
    st.stop()

# Filter data for same-position players
same_position_df = df[df["Position"] == player_position]

# Compute percentiles
percentiles = {}
for metric in metrics:
    try:
        series = same_position_df[metric].astype(float)
        player_value = player_row[metric]
        percentile = np.round((series < player_value).mean() * 100)
        percentiles[metric] = percentile
    except:
        percentiles[metric] = None

# Plotting function
def plot_horizontal_percentile_bars(percentiles_dict):
    fig, ax = plt.subplots(figsize=(10, len(percentiles_dict)*0.6))
    metrics = list(percentiles_dict.keys())
    values = [percentiles_dict[m] if percentiles_dict[m] is not None else 0 for m in metrics]

    colors = []
    for val in values:
        if val >= 70:
            colors.append('#4CAF50')  # green
        elif val >= 50:
            colors.append('#FFC107')  # amber
        else:
            colors.append('#F44336')  # red

    y_pos = np.arange(len(metrics))
    ax.barh(y_pos, values, color=colors)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(metrics)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel('Percentile')
    ax.set_title(f"{selected_player} ({player_position}) Percentile Comparison")

    # Label values on the bars
    for i, v in enumerate(values):
        ax.text(v + 1, i, f"{v}%", va='center', fontweight='bold')

    sns.despine()
    plt.tight_layout()
    return fig

# Show player metadata
st.markdown(f"### {selected_player} — *{player_position}*")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Minutes", int(player_row["Minutes"]))
with col2:
    st.metric("Matches", int(player_row["Matches played"]))
with col3:
    st.metric("Age", int(player_row["Age"]))

# Display the chart
fig = plot_horizontal_percentile_bars(percentiles)
st.pyplot(fig)
