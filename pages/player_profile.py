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

                # Calculate age from date_of_birth
                if 'date_of_birth' in df.columns:
                    df['age'] = df['date_of_birth'].apply(
                        lambda dob: datetime.now().year - pd.to_datetime(dob, errors='coerce').year
                        if pd.notna(dob) else np.nan
                    )
                else:
                    df['age'] = np.nan

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

    # Column mapping (flexible to actual column names)
    column_mapping = {
        'player_name': next((c for c in df_clean.columns if c.lower() == 'player_name'), None),
        'team_name': next((c for c in df_clean.columns if c.lower() == 'team_name'), None),
        'season': next((c for c in df_clean.columns if c.lower() == 'season'), None),
        'age': next((c for c in df_clean.columns if c.lower() in ['age', 'player_age']), None),
        'similarity': 'similarity'
    }

    missing = [k for k, v in column_mapping.items() if v is None]
    if missing:
        st.warning(f"Missing columns in similarity table: {missing}")
        return pd.DataFrame()

    return df_clean[[column_mapping['player_name'], column_mapping['team_name'],
                     column_mapping['season'], column_mapping['age'], 'similarity']]

# The rest of your code for UI and charts remains unchanged — no edits needed there

