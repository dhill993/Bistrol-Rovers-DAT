import streamlit as st
from utilities.utils import get_player_metrics_percentile_ranks, get_metrics_by_position
from visualizations.weighted_rank import get_weighted_rank
from data.retrieve_statbomb_data import get_statsbomb_player_season_stats

st.set_page_config(page_title="Player Profile Summary", layout="centered")

# --- Load and cache data ---
@st.cache_data(ttl=14400, show_spinner=True)
def load_data():
    df = get_statsbomb_player_season_stats()
    return df

df = load_data()

# --- Basic sanity checks ---
if df.empty:
    st.error("❌ Data failed to load or is empty.")
    st.stop()

required_cols = ['Season', 'League', 'Player Name', 'Position', 'Age', 'Minutes', 'Team']
missing_cols = [c for c in required_cols if c not in df.columns]
if missing_cols:
    st.error(f"❌ Missing expected columns in data: {missing_cols}")
    st.stop()

# --- Prepare lists for dropdowns ---
season_list = sorted(df['Season'].dropna().unique())
league_list = sorted(df['League'].dropna().unique())

def show_profile_page(complete_data, season_list, league_list):
    st.title("🎯 Player Profile Summary")

    # Dropdowns for filtering
    league = st.selectbox("Select League", league_list)
    season = st.selectbox("Select Season", season_list)

    # Filter dataframe by league and season
    df_filtered = complete_data[
        (complete_data['League'] == league) & 
        (complete_data['Season'] == season)
    ]

    if df_filtered.empty:
        st.warning(f"No data found for {league} in season {season}.")
        return

    # Player selection dropdown
    players = df_filtered['Player Name'].unique()
    player = st.selectbox("Select Player", sorted(players))

    # Get player info row
    player_row = df_filtered[df_filtered['Player Name'] == player].iloc[0]
    position = player_row['Position']
    age = int(player_row['Age'])
    minutes = int(player_row['Minutes'])
    club = player_row['Team']

    # Get position-specific metrics (your utility function)
    metrics = get_metrics_by_position(position, api='statbomb')

    # Get percentile ranks for player metrics (your utility function)
    player_df = get_player_metrics_percentile_ranks(df_filtered, player, position, metrics)
    if player_df is None or player_df.empty:
        st.error("Player percentile rank data not found.")
        return

    # Player header info
    st.markdown(f"""
    ### **{player}**
    - **Club:** {club}
    - **Position:** {position}
    - **Age:** {age}
    - **Minutes Played:** {minutes}
    """)

    st.divider()
    st.subheader("📊 Percentile Metrics")

    # Display each metric with a progress bar
    for metric in metrics:
        val = player_df[metric].values[0]
        st.markdown(f"**{metric}** — {int(val)}%")
        st.progress(int(val))

    st.divider()

    # Weighted rank scores section
    weighted_df = get_weighted_rank(df_filtered, player, league, season, position)
    if weighted_df.empty:
        st.warning("Weighted rank data not available.")
    else:
        score = weighted_df['Overall Score'].values[0]
        score_vs_l1 = weighted_df['Score weighted aganist League One'].values[0]

        st.subheader("🏆 Weighted Scores")
        st.markdown(f"**League Weighted Rank:** `{score:.1f}`")
        st.markdown(f"**vs League One Benchmark:** `{score_vs_l1:.1f}`")

# Run the profile page
show_profile_page(df, season_list, league_list)
