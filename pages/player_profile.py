import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from statsbombpy import sb
from sklearn.metrics.pairwise import cosine_similarity

# Position mapping
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
    return [m for m in ALL_METRICS if m in df.columns]

def find_similar_players(df, player_name, selected_metrics, position):
    position_df = df[df['mapped_position'] == position]
    if player_name not in position_df['player_name'].values:
        return pd.DataFrame()

    if len(position_df) <= 1:
        position_df = df[df['mapped_position'] == position]  # fallback to all data

    feature_df = position_df[selected_metrics].fillna(0)
    metric_values = feature_df.values

    try:
        target_index = position_df[position_df['player_name'] == player_name].index[0]
        sims = cosine_similarity([metric_values[position_df.index.get_loc(target_index)]], metric_values)[0]
        position_df = position_df.copy()
        position_df['similarity'] = sims
        similar_players = position_df.sort_values(by='similarity', ascending=False)
        return similar_players[similar_players['player_name'] != player_name].head(5)[['player_name', 'similarity']]
    except:
        return pd.DataFrame()

# Load data
df = get_statsbomb_data()
st.title("🏆 Player Performance Dashboard")

if df.empty:
    st.error("No data loaded")
    st.stop()

# Sidebar filters
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

if selected_player != 'Select a player':
    player_data = filtered_df[filtered_df['player_name'] == selected_player].iloc[0]
    player_position = player_data['mapped_position']

    available_metrics = get_available_metrics(filtered_df)
    metric_display_names = {m: m.replace('player_season_', '').replace('_', ' ').title() for m in available_metrics}
    selected_metrics = st.multiselect("Select Metrics", available_metrics, format_func=lambda x: metric_display_names[x])

    if 10 <= len(selected_metrics) <= 15:
        st.success("✅ Metrics selected")
        position_df = filtered_df[filtered_df['mapped_position'] == player_position]

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
                y=labels, x=values, orientation='h', marker_color=colors,
                text=[f'{v:.0f}%' for v in values], textposition='outside'))
            fig.update_layout(title=f"{selected_player} - {player_position} Profile",
                              xaxis=dict(range=[0, 100]), height=max(400, len(values)*30))
            st.plotly_chart(fig)

            st.markdown("### Similar Players")
            similar_df = find_similar_players(df, selected_player, selected_metrics, player_position)
            if not similar_df.empty:
                st.dataframe(similar_df)
            else:
                st.info("No similar players found or insufficient data.")
        else:
            st.warning("No valid data for selected metrics")
    else:
        st.warning("Please select between 10 and 15 metrics")
