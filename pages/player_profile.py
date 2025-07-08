import streamlit as st
import pandas as pd
from utilities.utils import get_player_metrics_percentile_ranks, get_metrics_by_position
from visualizations.weighted_rank import get_weighted_rank
from data.retrieve_statbomb_data import get_statsbomb_player_season_stats

# Function to render the player profile card like Jack Diamond example
def render_player_card(df, league_list, season_list):
    st.title("🎯 Player Profile Summary")

    # Select league, season, and player
    league = st.selectbox("Select League", league_list)
    season = st.selectbox("Select Season", season_list)

    # Filter the dataframe
    df_filtered = df[(df['League'] == league) & (df['Season'] == season)]

    if df_filtered.empty:
        st.warning("No data for this league/season combination.")
        return

    players = df_filtered['Player Name'].unique()
    player = st.selectbox("Select Player", sorted(players))

    player_row = df_filtered[df_filtered['Player Name'] == player].iloc[0]
    position = player_row['Position']
    age = int(player_row['Age'])
    minutes = int(player_row['Minutes'])
    club = player_row['Team']

    metrics = get_metrics_by_position(position, api='statbomb')

    # Get percentile ranks for selected player
    player_df = get_player_metrics_percentile_ranks(df_filtered, player,
