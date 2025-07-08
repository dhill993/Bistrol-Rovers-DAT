import sys
import os
import streamlit as st
import pandas as pd

# Ensure root folder is in sys.path to import utilities
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from utilities.utils import (
    get_metrics_by_position,
    get_player_metrics_percentile_ranks,
    get_weighted_score
)

# Mock data loading functions (replace with your actual data source)
@st.cache_data
def load_player_data():
    # Load your player dataset here (with columns like 'Player Name', 'Position', 'League', 'Club', etc.)
    return pd.read_csv('data/player_data.csv')

@st.cache_data
def load_club_logos():
    # Load mapping club name -> logo URL or filepath
    return {
        "Bristol Rovers": "https://upload.wikimedia.org/wikipedia/en/thumb/3/30/Bristol_Rovers_FC_crest.svg/1200px-Bristol_Rovers_FC_crest.svg.png",
        # Add more clubs/logos here
    }

@st.cache_data
def load_player_photos():
    # Load mapping player name -> photo URL or filepath
    return {
        "Jack Diamond": "https://example.com/photos/jack_diamond.jpg",
        # Add more players/photos here
    }

def main():
    st.title("Player Profile Summary")

    df = load_player_data()
    club_logos = load_club_logos()
    player_photos = load_player_photos()

    # Sidebar filters
    league = st.sidebar.selectbox("Select League", options=['All'] + sorted(df['League'].unique().tolist()))
    position = st.sidebar.selectbox("Select Position", options=sorted(df['Position'].unique().tolist()))
    
    # Get player list based on league and position
    if league == 'All':
        filtered_df = df[df['Position'] == position]
    else:
        filtered_df = df[(df['League'] == league) & (df['Position'] == position)]
    players = sorted(filtered_df['Player Name'].unique().tolist())

    player = st.sidebar.selectbox("Select Player", options=players)

    # Fetch metrics to show for this position (from utils)
    all_metrics = get_metrics_by_position(position, api='statbomb')

    # Get player percentile metrics DataFrame
    player_metrics_df = get_player_metrics_percentile_ranks(df, player, position, all_metrics)

    if player_metrics_df is None or player_metrics_df.empty:
        st.warning("Player data not found or incomplete.")
        return

    # Get weighted score for league
    weighted_score = get_weighted_score(league) if league in df['League'].unique() else 1.0

    # Player basic info
    player_row = filtered_df[filtered_df['Player Name'] == player].iloc[0]
    club = player_row['Club'] if 'Club' in player_row else 'Unknown Club'
    
    # Show player photo and club badge side by side
    cols = st.columns([1, 1])
    with cols[0]:
        if player in player_photos:
            st.image(player_photos[player], width=150, caption=player)
        else:
            st.write("No player photo available")
    with cols[1]:
        if club in club_logos:
            st.image(club_logos[club], width=150, caption=club)
        else:
            st.write("No club logo available")

    st.markdown(f"### {player} - {position} - {league}")

    # Show weighted score
    st.markdown(f"**Weighted League Score:** {weighted_score:.2f}")

    # Prepare stats display (percentiles scaled 0-100)
    stats = player_metrics_df[all_metrics].iloc[0].round(1)

    # Format stats table
    stats_df = pd.DataFrame({
        "Metric": all_metrics,
        "Percentile": stats.values
    })

    # You could add coloring or formatting here
    st.table(stats_df.style.background_gradient(cmap='Blues'))

    # Summary text example
    st.markdown("#### Summary Insights")
    strengths = stats_df[stats_df['Percentile'] > 80]['Metric'].tolist()
    weaknesses = stats_df[stats_df['Percentile'] < 40]['Metric'].tolist()

    if strengths:
        st.markdown(f"**Strengths:** {', '.join(strengths)}")
    if weaknesses:
        st.markdown(f"**Areas to improve:** {', '.join(weaknesses)}")

if __name__ == "__main__":
    main()
