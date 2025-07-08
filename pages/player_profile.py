import streamlit as st
from utilities.utils import get_player_metrics_percentile_ranks, get_metrics_by_position
from visualizations.weighted_rank import get_weighted_rank

def show_profile_page(complete_data, season_list, league_list):
    st.title("🎯 Player Profile Summary")

    # Dropdowns
    league = st.selectbox("Select League", league_list)
    season = st.selectbox("Select Season", season_list)

    # Filter data
    df_filtered = complete_data[
        (complete_data['League'] == league) &
        (complete_data['Season'] == season)
    ]

    players = df_filtered['Player Name'].unique()
    player = st.selectbox("Select Player", sorted(players))

    # Get player's row to extract position, minutes, etc.
    player_row = df_filtered[df_filtered['Player Name'] == player].iloc[0]
    position = player_row['Position']
    age = int(player_row['Age'])
    minutes = int(player_row['Minutes'])
    club = player_row['Team']

    # Position-specific metrics
    metrics = get_metrics_by_position(position, api='statbomb')

    # Get percentile data
    player_df = get_player_metrics_percentile_ranks(df_filtered, player, position, metrics)

    if player_df is None or player_df.empty:
        st.error("Player data not found.")
        return

    # Header section
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
        color = "green" if value >= 75 else "orange" if value >= 50 else "red"
        st.markdown(f"**{metric}** — {int(value)}%")
        st.progress(int(value))

    st.divider()

    # Weighted Scores Section
    weighted_df = get_weighted_rank(df_filtered, player, league, season, position)
    score = weighted_df['Overall Score'].values[0]
    score_vs_l1 = weighted_df['Score weighted aganist League One'].values[0]

    st.subheader("🏆 Weighted Scores")
    st.markdown(f"**League Weighted Rank:** `{score:.1f}`")
    st.markdown(f"**vs League One Bench**
