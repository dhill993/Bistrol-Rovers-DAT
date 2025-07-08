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
    player_df = get_player_metrics_percentile_ranks(df_filtered, player, position, metrics)
    if player_df is None or player_df.empty:
        st.error("No percentile rank data available for this player.")
        return

    # Get weighted scores
    weighted_df = get_weighted_rank(df_filtered, player, league, season, position)
    score = weighted_df['Overall Score'].values[0]
    score_vs_l1 = weighted_df['Score weighted aganist League One'].values[0]

    # --- Layout the card ---
    # Use columns for a neat side-by-side display

    left_col, right_col = st.columns([1, 2])

    with left_col:
        # Player basic info header
        st.markdown(f"## {player}")
        st.markdown(f"**Club:** {club}")
        st.markdown(f"**Position:** {position}")
        st.markdown(f"**Age:** {age}")
        st.markdown(f"**Minutes Played:** {minutes}")

        # Weighted Scores Section with emphasis
        st.markdown("---")
        st.markdown("### 🏆 Weighted Scores")
        st.markdown(f"**League Weighted Rank:** `{score:.1f}`")
        st.markdown(f"**vs League One Benchmark:** `{score_vs_l1:.1f}`")

    with right_col:
        st.markdown("### 📊 Percentile Metrics")

        # Show percentile metrics as progress bars with labels
        for metric in metrics:
            value = int(player_df[metric].values[0])
            # Color coding (green if >75, orange if 50-75, red if below 50)
            if value >= 75:
                bar_color = "#1f77b4"  # blue
            elif value >= 50:
                bar_color = "#ff7f0e"  # orange
            else:
                bar_color = "#d62728"  # red

            st.markdown(f"**{metric}:** {value}%")
            st.progress(value)

    st.markdown("---")

# Load and prepare data
@st.cache_data(ttl=14400)
def load_data():
    return get_statsbomb_player_season_stats()

df = load_data()

if not isinstance(df, pd.DataFrame):
    st.error("Failed to load data as a DataFrame.")
    st.stop()

required_cols = ['Season', 'League']
if any(col not in df.columns for col in required_cols):
    st.error(f"Missing columns: {', '.join(set(required_cols) - set(df.columns))}")
    st.stop()

if df.empty:
    st.error("DataFrame is empty.")
    st.stop()

season_list = sorted(df['Season'].dropna().unique())
league_list = sorted(df['League'].dropna().unique())

render_player_card(df, league_list, season_list)
