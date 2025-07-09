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
from data.retrieve_statbomb_data import get_player_season_data


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

    # Ensure 'Season' column exists by renaming if necessary
    if 'Season' not in df.columns:
        if 'season_name' in df.columns:
            df.rename(columns={'season_name': 'Season'}, inplace=True)
        else:
            st.error("ERROR: Neither 'Season' nor 'season_name' column found in data.")
            st.stop()

    # Debug: show columns in data
    st.write("Columns in loaded data:", df.columns.tolist())

    # Sidebar filters
    with st.sidebar:
        # Season select (sorted descending so recent first)
        seasons = sorted(df['Season'].unique(), reverse=True)
        season = st.selectbox("Select Season", seasons)

        # Filter by season first to narrow leagues
        df_season = df[df['Season'] == season]
        leagues = sorted(df_season['League'].unique())
        league = st.selectbox("Select League", leagues)

        # Filter by season and league to narrow teams
        df_league = df_season[df_season['League'] == league]
        teams = sorted(df_league['Team'].unique())
        team = st.selectbox("Select Team", teams)

        # Filter by season, league, team for positions
        df_team = df_league[df_league['Team'] == team]
        positions = sorted(df_team['Position'].unique())
        position = st.selectbox("Select Player Position", positions)

        # Players filtered by season, league, team, position
        players = sorted(df_team[df_team['Position'] == position]['Player Name'].unique())
        player = st.selectbox("Select Player", players)

    # Filter the full DataFrame for selected player row
    player_row = df[
        (df['Player Name'] == player) &
        (df['Team'] == team) &
        (df['League'] == league) &
        (df['Season'] == season)
    ]

    if player_row.empty:
        st.warning("Player data not found.")
        return

    player_row = player_row.iloc[0]

    # Display player info
    st.markdown(f"### {player}")
    st.markdown(f"**Team:** {team}  ")
    st.markdown(f"**League:** {league}  ")
    st.markdown(f"**Season:** {season}  ")
    st.markdown(f"**Position:** {position}  ")
    st.markdown(f"**Age:** {int(player_row['Age']) if 'Age' in player_row else 'N/A'}  |  **Minutes:** {int(player_row['Minutes']) if 'Minutes' in player_row else 'N/A'}")

    # Get metrics for position
    metrics = get_metrics_by_position(position, api="statbomb")

    # Calculate percentile ranks
    player_percentiles = get_player_metrics_percentile_ranks(df_team, player, position, metrics)

    if player_percentiles is None or player_percentiles.empty:
        st.warning("Player metric data not found or incomplete.")
        return

    percentiles = player_percentiles[metrics].iloc[0].round(1)

    # Plot percentile bar chart
    fig = plot_horizontal_bars(percentiles)
    st.plotly_chart(fig, use_container_width=True)

    # Calculate scores
    overall_score = percentiles.mean()
    weighted_score = overall_score * get_weighted_score(league)

    col1, col2 = st.columns(2)
    col1.metric("Overall Percentile Score", f"{overall_score:.0f}%")
    col2.metric(f"{league} Weighted Score", f"{weighted_score:.0f}%")


if __name__ == '__main__':
    main()
