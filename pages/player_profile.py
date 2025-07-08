import streamlit as st
import pandas as pd
from utilities.utils import get_player_metrics_percentile_ranks, get_metrics_by_position
from visualizations.weighted_rank import get_weighted_rank
from data.retrieve_statbomb_data import get_statsbomb_player_season_stats

def show_profile_page(complete_data, season_list, league_list):
    st.title("🎯 Player Profile Summary")

    # Dropdowns
    league = st.selectbox("Select League", league_list)
    season = st.selectbox("Select Season", season_list)

    # Filter data for league and season
    df_filtered = complete_data[
        (complete_data['League'] == league) &
        (complete_data['Season'] == season)
    ]

    players = df_filtered['Player Name'].unique()
    player = st.selectbox("Select Player", sorted(players))

    # Extract player info
    player_row = df_filtered[df_filtered['Player Name'] == player].iloc[0]
    position = player_row['Position']
    age = int(player_row['Age'])
    minutes = int(player_row['Minutes'])
    club = player_row['Team']

    # Get position-specific metrics
    metrics = get_metrics_by_position(position, api='statbomb')

    # Get percentile data
    player_df = get_player_metrics_percentile_ranks(df_filtered, player, position, metrics)

    if player_df is None or player_df.empty:
        st.error("Player data not found.")
        return

    # Header
    st.markdown(f"""
    ### **{player}**
    - **Club:** {club}
    - **Position:** {position}
    - **Age:** {age}
    - **Minutes Played:** {minutes}
    """)

    st.divider()
    st.subheader("📊 Percentile Metrics")

    for metric in metrics:
        value = player_df[metric].values[0]
        st.markdown(f"**{metric}** — {int(value)}%")
        st.progress(int(value))

    st.divider()

    # Weighted scores
    weighted_df = get_weighted_rank(df_filtered, player, league, season, position)
    score = weighted_df['Overall Score'].values[0]
    score_vs_l1 = weighted_df['Score weighted aganist League One'].values[0]

    st.subheader("🏆 Weighted Scores")
    st.markdown(f"**League Weighted Rank:** `{score:.1f}`")
    st.markdown(f"**vs League One Benchmark:** `{score_vs_l1:.1f}`")


# Load data with caching
@st.cache_data(ttl=14400)
def load_data():
    return get_statsbomb_player_season_stats()

# Main execution
df = load_data()

# Debug info
st.write("Data type:", type(df).__name__)
if isinstance(df, pd.DataFrame):
    st.write("Columns:", df.columns.tolist())
    st.write("First 5 rows:", df.head())
else:
    st.error("❌ Loaded data is not a pandas DataFrame.")
    st.stop()

# Validate columns
required_columns = ['Season', 'League']
missing_cols = [col for col in required_columns if col not in df.columns]
if missing_cols:
    st.error(f"❌ Missing required columns: {missing_cols}")
    st.stop()

if df.empty:
    st.error("❌ DataFrame is empty.")
    st.stop()

season_list = sorted(df['Season'].dropna().unique())
league_list = sorted(df['League'].dropna().unique())

show_profile_page(df, season_list, league_list)
