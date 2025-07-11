import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

from utilities.utils import get_metrics_by_position, get_player_metrics_percentile_ranks

def create_summary_profile_card(
    complete_data,
    league_name,
    season,
    selected_player,
    position,
    api="statbomb"
):
    # Use your same position normalization rules
    original_position = position
    if position == 'Number 6' and api == 'statbomb':
        position = 'Number 8'
    if (position == 'Number 8' or position == 'Number 10') and api == 'wyscout':
        position = 'Number 6'

    # Filter dataset for selected league and season
    filtered_df = complete_data.copy()
    if league_name not in ['All', '']:
        filtered_df = filtered_df[filtered_df['League'] == league_name]
    if season != '':
        filtered_df = filtered_df[filtered_df['Season'] == season]

    # Get player's data
    player_df = filtered_df[filtered_df['Player Name'] == selected_player]
    if player_df.empty:
        st.error(f"Player {selected_player} not found in filtered data.")
        return None

    # Get position-specific metrics
    metrics = get_metrics_by_position(position, api)
    player_percentiles = get_player_metrics_percentile_ranks(
        filtered_df, selected_player, position, metrics
    )

    if player_percentiles is None or player_percentiles.empty:
        st.error(f"No percentile data found for {selected_player}.")
        return None

    # Styling
    st.markdown("### Player Summary Profile")
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#111111')
    ax.set_facecolor('#111111')

    values = player_percentiles[metrics].iloc[0].values
    colors = ['#58AC4E' if val >= 70 else '#1A78CF' if val >= 50 else '#aa42af' for val in values]

    # Horizontal bar chart
    y_pos = np.arange(len(metrics))
    bars = ax.barh(y_pos, values, color=colors, edgecolor='white')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(metrics, color='white', fontsize=10)
    ax.set_xlim(0, 100)
    ax.invert_yaxis()

    # Add value markers
    for i, bar in enumerate(bars):
        ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2,
                f"{int(values[i])}%", va='center', color='white', fontsize=9)

    # Titles and labels
    ax.set_xlabel("Percentile", color='white')
    ax.set_title(f"{selected_player} | {original_position}", color='white', fontsize=16, loc='left')

    # Footer info (Minutes, Age, Team)
    info = f"""
    **Club:** {player_df.iloc[0]['Team']}  
    **Age:** {int(player_df.iloc[0]['Age'])}  
    **Minutes Played:** {int(player_df.iloc[0]['Minutes'])}
    """
    st.markdown(info)

    st.pyplot(fig)
