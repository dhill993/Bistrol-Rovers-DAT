import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from statsbombpy import sb
from sklearn.metrics.pairwise import cosine_similarity

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

st.set_page_config(page_title="Player Performance Dashboard", layout="wide")

@st.cache_data
def get_statsbomb_data():
    try:
        user = st.secrets["user"]
        passwd = st.secrets["passwd"]
        creds = {"user": user, "passwd": passwd}
        all_comps = sb.competitions(creds=creds)
        dataframes = []
        for _, row in all_comps.iterrows():
            try:
                comp_id, season_id = row["competition_id"], row["season_id"]
                df = sb.player_season_stats(comp_id, season_id, creds=creds)
                df['League'] = row['competition_name']
                df['Season'] = row['season_name']
                df['mapped_position'] = df['primary_position'].map(position_mapping)
                df = df.dropna(subset=['mapped_position'])
                dataframes.append(df)
            except:
                continue
        return pd.concat(dataframes, ignore_index=True) if dataframes else pd.DataFrame()
    except Exception as e:
        st.error(f"StatsBomb API error: {e}")
        return pd.DataFrame()

def get_available_metrics(df):
    return [metric for metric in ALL_METRICS if metric in df.columns]

def find_similar_players(df, player_row, selected_metrics):
    if player_row is None or not selected_metrics:
        return pd.DataFrame()

    df_clean = df.dropna(subset=selected_metrics)
    if df_clean.empty or player_row.name not in df_clean.index:
        # Use elite metrics as fallback
        elite_df = df_clean.copy()
        elite_df['elite_score'] = elite_df[selected_metrics].mean(axis=1)
        elite_df = elite_df.nlargest(1, 'elite_score')
        player_vector = elite_df[selected_metrics].iloc[0].values.reshape(1, -1)
    else:
        player_vector = df_clean.loc[[player_row.name], selected_metrics].values

    matrix = df_clean[selected_metrics].values
    similarity_scores = cosine_similarity(player_vector, matrix)[0]

    df_clean['similarity'] = similarity_scores
    df_clean = df_clean[df_clean['player_name'] != player_row['player_name']]
    df_clean = df_clean.sort_values(by='similarity', ascending=False).head(5)

    return df_clean[['player_name', 'team_name', 'Season', 'player_age', 'similarity']]

st.title("🏆 Player Performance Dashboard")

with st.spinner("Loading StatsBomb data..."):
    df = get_statsbomb_data()
    if not df.empty:
        st.success(f"Loaded {len(df)} player records")

if not df.empty:
    col1, col2, col3 = st.columns(3)
    with col1:
        leagues = ['All'] + sorted(df['League'].unique().tolist())
        selected_league = st.selectbox("League", leagues)
    with col2:
        seasons = ['All'] + sorted(df['Season'].unique().tolist())
        selected_season = st.selectbox("Season", seasons)
    with col3:
        positions = ['All'] + sorted(df['mapped_position'].dropna().unique().tolist())
        selected_position = st.selectbox("Position", positions)

    filtered_df = df.copy()
    if selected_league != 'All':
        filtered_df = filtered_df[filtered_df['League'] == selected_league]
    if selected_season != 'All':
        filtered_df = filtered_df[filtered_df['Season'] == selected_season]
    if selected_position != 'All':
        filtered_df = filtered_df[filtered_df['mapped_position'] == selected_position]

    players = ['Select a player'] + sorted(filtered_df['player_name'].unique().tolist())
    selected_player = st.selectbox("Select Player", players)

    if selected_player != "Select a player":
        player_data = filtered_df[filtered_df['player_name'] == selected_player].iloc[0]
        player_position = player_data.get('mapped_position', 'Unknown')
        available_metrics = get_available_metrics(filtered_df)

        st.markdown("### Select Metrics (Min: 10, Max: 15)")
        metric_display_names = {
            metric: metric.replace('player_season_', '').replace('_', ' ').title()
            for metric in available_metrics
        }

        selected_metrics = st.multiselect(
            "Choose metrics to analyze:",
            options=available_metrics,
            format_func=lambda x: metric_display_names[x],
            help="Select between 10 and 15 metrics for analysis"
        )

        if len(selected_metrics) < 10:
            st.warning(f"Please select at least 10 metrics. Currently selected: {len(selected_metrics)}")
        elif len(selected_metrics) > 15:
            st.warning(f"Please select maximum 15 metrics. Currently selected: {len(selected_metrics)}")
        else:
            st.success(f"✅ {len(selected_metrics)} metrics selected")
            position_df = filtered_df[filtered_df['mapped_position'] == player_position]

            st.subheader(f"Player Profile: {selected_player} - {player_position}")

            values = []
            labels = []
            for metric in selected_metrics:
                if metric in position_df.columns and pd.notna(player_data.get(metric)):
                    percentile = position_df[metric].rank(pct=True).loc[player_data.name] * 100
                    values.append(percentile)
                    labels.append(metric_display_names[metric])

            if values:
                colors = ['#16a34a' if v >= 70 else '#eab308' if v >= 50 else '#ef4444' for v in values]
                fig = go.Figure(go.Bar(
                    y=labels, x=values, orientation='h',
                    marker_color=colors,
                    text=[f'{v:.0f}%' for v in values],
                    textposition='outside',
                    textfont=dict(color='white', size=12, family='Arial Black')
                ))
                fig.update_layout(
                    title=dict(text=f"Custom Metrics Analysis - {selected_player} ({player_position})",
                              font=dict(color='white', size=16), x=0.5),
                    plot_bgcolor='#1e40af', paper_bgcolor='#1e40af',
                    font=dict(color='white'), height=max(400, len(values) * 30),
                    xaxis=dict(range=[0, 100], showgrid=True, gridcolor='rgba(255,255,255,0.2)',
                              title="Percentile Ranking vs Same Position", tickfont=dict(color='white')),
                    yaxis=dict(tickfont=dict(color='white'), categoryorder='array',
                              categoryarray=labels[::-1]),
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)

                col1, col2, col3, col4 = st.columns(4)
                overall_rank = np.mean(values) if values else 0
                minutes_played = int(player_data.get('player_season_minutes', 0))
                metrics_above_70 = sum(1 for v in values if v >= 70)

                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Overall Rank</div>
                        <div class="metric-value">{overall_rank:.0f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Position</div>
                        <div class="metric-value">{player_position}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Elite Metrics</div>
                        <div class="metric-value">{metrics_above_70}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col4:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Minutes</div>
                        <div class="metric-value">{minutes_played:,}</div>
                    </div>
                    """, unsafe_allow_html=True)

                # Similar players
                st.markdown("---")
                st.markdown("### 🔍 Most Similar Players Across All Leagues and Seasons")
                similar_df = find_similar_players(df, player_data, selected_metrics)
                if not similar_df.empty:
                    similar_df['similarity'] = similar_df['similarity'].round(4)
                    st.dataframe(similar_df.rename(columns={
                        'player_name': 'Player',
                        'team_name': 'Club',
                        'Season': 'Season',
                        'player_age': 'Age',
                        'similarity': 'Similarity'
                    }))
                else:
                    st.info("No similar players found.")
            else:
                st.warning("No valid data for selected metrics")
else:
    st.error("No data available. Please check your StatsBomb API credentials.")
