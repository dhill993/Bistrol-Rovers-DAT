import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data")))
import sys
import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Adjust sys.path for utilities import
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from utilities.utils import (
    get_metrics_by_position,
    get_player_metrics_percentile_ranks,
    get_weighted_score
)
from retrieve_statbomb_data import get_player_season_data

def color_from_value(val):
    if val >= 70:
        return "#58AC4E"  # Green
    elif val >= 50:
        return "#1A78CF"  # Blue
    else:
        return "#aa42af"  # Purple


def plot_horizontal_bars(metrics: pd.Series):
    colors = [color_from_value(v) for v in metrics.values]
    fig = go.Figure(go.Bar(
        x=metrics.values,
        y=metrics.index,
        orientation='h',
        marker=dict(color=colors),
        text=[f"{v:.0f}%" for v in metrics.values],
        textposition='auto',
    ))
    fig.update_layout(
        xaxis=dict(range=[0, 100], title='Percentile'),
        yaxis=dict(autorange='reversed'),
        height=600,
        margin=dict(l=100, r=40, t=30, b=40),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig


def main():
    st.title("Player Profile View")

    df = get_player_season_data()

    with st.sidebar:
        clubs = sorted(df['Team'].unique())
        club = st.selectbox("Select Club", clubs)

        league = st.selectbox("Select League", sorted(df['League'].unique()))

        filtered = df[(df['Club'] == club) & (df['League'] == league)]
        player = st.selectbox("Select Player", sorted(filtered['Player Name'].unique()))

    # Get full player row
    player_row = df[df['Player Name'] == player].iloc[0]
    position = player_row['Position']
    age = int(player_row['Age']) if 'Age' in player_row else 'N/A'
    minutes = int(player_row['Minutes']) if 'Minutes' in player_row else 'N/A'

    st.markdown(f"### {player}")
    st.markdown(f"**Club:** {club}  ")
    st.markdown(f"**League:** {league}  ")
    st.markdown(f"**Position:** {position}  ")
    st.markdown(f"**Age:** {age}  |  **Minutes:** {minutes}")

    metrics = get_metrics_by_position(position, api="statbomb")
    player_percentiles = get_player_metrics_percentile_ranks(df, player, position, metrics)

    if player_percentiles is None or player_percentiles.empty:
        st.warning("Player metric data not found or incomplete.")
        return

    percentiles = player_percentiles[metrics].iloc[0].round(1)
    fig = plot_horizontal_bars(percentiles)
    st.plotly_chart(fig, use_container_width=True)

    overall_score = percentiles.mean()
    weighted_score = overall_score * get_weighted_score(league)

    col1, col2 = st.columns(2)
    col1.metric("Overall Percentile Score", f"{overall_score:.0f}%")
    col2.metric(f"{league} Weighted Score", f"{weighted_score:.0f}%")


if __name__ == '__main__':
    main()
