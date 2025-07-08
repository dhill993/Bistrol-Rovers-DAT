import sys
import os
import streamlit as st
import pandas as pd

# Adjust sys.path for utilities import
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from utilities.utils import (
    get_metrics_by_position,
    get_player_metrics_percentile_ranks,
    get_weighted_score
)

# Replace this with your actual data loading method or dataframe
@st.cache_data
def load_player_data():
    # Example dummy data for testing - replace with your actual DataFrame loading
    data = {
        'Player Name': ['Jack Diamond', 'John Smith'],
        'Position': ['Midfielder', 'Midfielder'],
        'League': ['League One', 'League One'],
        'Club': ['Bristol Rovers', 'Bristol Rovers'],
        # Add all metrics columns your utils expect here:
        'Metric1': [50, 60],
        'Metric2': [70, 80]
    }
    df = pd.DataFrame(data)
    return df

def main():
    st.title("Player Profile Summary")

    df = load_player_data()

    # Sidebar filters
    league = st.sidebar.selectbox("Select League", options=['All'] + sorted(df['League'].unique().tolist()))
    position = st.sidebar.selectbox("Select Position", options=sorted(df['Position'].unique().tolist()))

    # Filter players by league and position
    if league == 'All':
        filtered_df = df[df['Position'] == position]
    else:
        filtered_df = df[(df['League'] == league) & (df['Position'] == position)]
    players = sorted(filtered_df['Player Name'].unique().tolist())

    player = st.sidebar.selectbox("Select Player", options=players)

    # Get metrics for position from utils
    all_metrics = get_metrics_by_position(position, api='statbomb')

    # Player percentile metrics
    player_metrics_df = get_player_metrics_percentile_ranks(df, player, position, all_metrics)

    if player_metrics_df is None or player_metrics_df.empty:
        st.warning("Player data not found or incomplete.")
        return

    # Weighted score for league
    weighted_score = get_weighted_score(league) if league in df['League'].unique() else 1.0

    player_row = filtered_df[filtered_df['Player Name'] == player].iloc[0]
    club = player_row['Club'] if 'Club' in player_row else 'Unknown Club'

    # Show player info
    st.markdown(f"### {player} - {position} - {league}")
    st.markdown(f"**Club:** {club}")
    st.markdown(f"**Weighted League Score:** {weighted_score:.2f}")

    # Display metrics as table
    stats = player_metrics_df[all_metrics].iloc[0].round(1)
    stats_df = pd.DataFrame({"Metric": all_metrics, "Percentile": stats.values})

    st.table(stats_df)

    # Simple summary
    strengths = stats_df[stats_df['Percentile'] > 80]['Metric'].tolist()
    weaknesses = stats_df[stats_df['Percentile'] < 40]['Metric'].tolist()

    st.markdown("#### Summary Insights")
    if strengths:
        st.markdown(f"**Strengths:** {', '.join(strengths)}")
    if weaknesses:
        st.markdown(f"**Areas to improve:** {', '.join(weaknesses)}")

if __name__ == "__main__":
    main()
