import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from utilities.utils import get_metrics_by_position, get_player_metrics_percentile_ranks, custom_fontt


def create_summary_profile_card(
    complete_data,
    league_name,
    season,
    selected_player,
    position,
    api="statbomb"
):
    # Normalize position (like pizza chart)
    original_position = position
    if position == 'Number 6' and api == 'statbomb':
        position = 'Number 8'
    if position in ['Number 8', 'Number 10'] and api == 'wyscout':
        position = 'Number 6'

    # Filter data
    df = complete_data.copy()
    if league_name not in ["All", ""]:
        df = df[df['League'] == league_name]
    if season != "":
        df = df[df['Season'] == season]

    # Filter for player
    player_df = df[df['Player Name'] == selected_player]
    if player_df.empty:
        st.error(f"Player {selected_player} not found in dataset.")
        return

    # Get metrics and percentiles
    metrics = get_metrics_by_position(position, api)
    percentiles = get_player_metrics_percentile_ranks(df, selected_player, position, metrics)

    if percentiles is None or percentiles.empty:
        st.error(f"No percentile data available for {selected_player}.")
        return

    # Chart values
    values = percentiles[metrics].iloc[0].values
    colors = ['#58AC4E' if val >= 70 else '#1A78CF' if val >= 50 else '#aa42af' for val in values]
    y_pos = np.arange(len(metrics))

    # Plot setup
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#111111')
    ax.set_facecolor('#111111')

    bars = ax.barh(y_pos, values, color=colors, edgecolor='white', height=0.5)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(metrics, color='white', fontsize=10, fontproperties=custom_fontt)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("Percentile", color='white', fontsize=12, fontproperties=custom_fontt)
    ax.set_title(f"{selected_player} | {original_position}", color='white', fontsize=18, loc='left', fontproperties=custom_fontt)

    # Add value labels
    for i, bar in enumerate(bars):
        ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height() / 2,
                f"{int(values[i])}%", va='center', color='white', fontsize=9, fontproperties=custom_fontt)

    # Info panel (text)
    st.markdown(f"""
    <div style='background-color:#111111; padding:10px; border-radius:10px; color:white'>
    <b>Club:</b> {player_df.iloc[0]['Team']}<br>
    <b>Age:</b> {int(player_df.iloc[0]['Age'])}<br>
    <b>Minutes Played:</b> {int(player_df.iloc[0]['Minutes'])}<br>
    </div>
    """, unsafe_allow_html=True)

    st.pyplot(fig)
