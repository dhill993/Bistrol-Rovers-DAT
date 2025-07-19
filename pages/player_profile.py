st.set_page_config(page_title="Player Performance Dashboard", layout="wide")

# Position mapping from pizza chart logic
position_mapping = {
    "Centre Back": "Number 6", "Left Centre Back": "Number 6", "Right Centre Back": "Number 6",
    "Left Back": "Number 3", "Right Back": "Number 3", "Left Wing Back": "Number 3",
    "Right Wing Back": "Number 3",
    "Defensive Midfielder": "Number 8", "Left Defensive Midfielder": "Number 8",
    "Right Defensive Midfielder": "Number 8", "Centre Defensive Midfielder": "Number 8",
    "Left Centre Midfield": "Number 8", "Left Centre Midfielder": "Number 8",
    "Right Centre Midfield": "Number 8", "Right Centre Midfielder": "Number 8",
    "Centre Midfield": "Number 8", "Left Attacking Midfield": "Number 8",
    "Right Attacking Midfield": "Number 8", "Right Attacking Midfielder": "Number 8",
    "Attacking Midfield": "Number 8",
    "Secondary Striker": "Number 10", "Centre Attacking Midfielder": "Number 10",
    "Left Attacking Midfielder": "Number 10",
    "Winger": "Winger", "Right Midfielder": "Winger", "Left Midfielder": "Winger",
    "Left Wing": "Winger", "Right Wing": "Winger",
    "Centre Forward": "Runner", "Left Centre Forward": "Runner", "Right Centre Forward": "Runner",
    "Goalkeeper": "Goalkeeper"
}

# All available metrics for selection
ALL_METRICS = [
    'player_season_aerial_ratio', 'player_season_ball_recoveries_90', 'player_season_blocks_per_shot',
    'player_season_carries_90', 'player_season_crossing_ratio', 'player_season_deep_progressions_90',
    'player_season_defensive_action_regains_90', 'player_season_defensive_actions_90',
    'player_season_dribble_faced_ratio', 'player_season_dribble_ratio', 'player_season_dribbles_90',
    'player_season_np_shots_90', 'player_season_np_xg_90', 'player_season_np_xg_per_shot',
    'player_season_npg_90', 'player_season_npxgxa_90', 'player_season_obv_90',
    'player_season_obv_defensive_action_90', 'player_season_obv_dribble_carry_90',
    'player_season_obv_pass_90', 'player_season_obv_shot_90', 'player_season_op_f3_passes_90',
    'player_season_op_key_passes_90', 'player_season_op_passes_into_and_touches_inside_box_90',
    'player_season_op_passes_into_box_90', 'player_season_padj_clearances_90',
    'player_season_padj_interceptions_90', 'player_season_padj_pressures_90', 'player_season_padj_tackles_90',
    'player_season_passing_ratio', 'player_season_shot_on_target_ratio', 'player_season_shot_touch_ratio',
    'player_season_touches_inside_box_90', 'player_season_xgbuildup_90', 'player_season_op_xa_90',
    'player_season_pressured_passing_ratio', 'player_season_da_aggressive_distance',
    'player_season_clcaa', 'player_season_gsaa_ratio', 'player_season_gsaa_90',
    'player_season_save_ratio', 'player_season_xs_ratio', 'player_season_positive_outcome_score',
    'player_season_obv_gk_90', 'player_season_forward_pass_ratio',
    'player_season_forward_pass_proportion', 'player_season_scoring_contribution_90',
    'player_season_fouls_won_90', 'player_season_pressures_90', 'player_season_counterpressures_90',
    'player_season_aggressive_actions_90'
]

# Styling
st.markdown("""
<style>
    .main { background-color: #1e3a8a; color: white; }
    .metric-card {
        background-color: #16a34a; padding: 20px; border-radius: 10px;
        text-align: center; color: white; margin: 5px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3); border: 2px solid #22c55e;
    }
    .metric-title { font-size: 12px; font-weight: bold; margin-bottom: 5px; text-transform: uppercase; }
    .metric-value { font-size: 36px; font-weight: bold; }
    .chart-container { background-color: #1e40af; padding: 15px; border-radius: 8px; }
    .stMultiSelect > div > div > div { background-color: #1e40af; }
</style>
""", unsafe_allow_html=True)

# Comparison View

def compare_players(filtered_df, available_metrics, metric_display_names):
    st.markdown("## 📊 Compare Players")

    # Multiselect for players
    players = sorted(filtered_df['player_name'].unique().tolist())
    selected_players = st.multiselect("Select up to 3 players to compare", players, max_selections=3)

    if not selected_players or len(selected_players) < 2:
        st.info("Please select at least 2 players to compare.")
        return

    # Select metrics
    selected_metrics = st.multiselect(
        "Choose metrics to compare (up to 10):",
        options=available_metrics,
        default=available_metrics[:10],
        format_func=lambda x: metric_display_names.get(x, x)
    )

    if not selected_metrics:
        st.warning("Please select at least one metric.")
        return

    # Filter comparison data
    comparison_data = filtered_df[filtered_df['player_name'].isin(selected_players)]

    # Create columns based on number of players
    cols = st.columns(len(selected_players))

    for i, player in enumerate(selected_players):
        with cols[i]:
            player_row = comparison_data[comparison_data['player_name'] == player].iloc[0]

            # Player info
            st.markdown(f"### {player}")
            st.markdown(f"**Club:** {player_row['team_name']}")
            st.markdown(f"**Age:** {player_row['player_age']}")
            st.markdown(f"**Minutes:** {int(player_row['player_season_minutes']):,}")

            # Metrics
            for metric in selected_metrics:
                value = player_row.get(metric, None)

                try:
                    val_display = f"{value:.2f}" if isinstance(value, float) else str(value)
                    bg_color = "#16a34a" if isinstance(value, (int, float)) and value >= 1 else "#1e3a8a"
                except:
                    val_display = "N/A"
                    bg_color = "#6b7280"

                st.markdown(f"""
                    <div style="background-color:{bg_color};padding:6px;border-radius:6px;
                                margin-bottom:6px;color:white;text-align:center;">
                        <strong>{metric_display_names.get(metric, metric)}</strong><br>{val_display}
                    </div>
                """, unsafe_allow_html=True)
