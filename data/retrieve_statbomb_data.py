import pandas as pd
from datetime import datetime
import numpy as np
from statsbombpy import sb
import streamlit as st

# --- Position Mapping ---
position_mapping = {
    "Full Back": "Full Back", "Left Back": "Full Back", "Right Back": "Full Back",
    "Left Wing Back": "Full Back", "Right Wing Back": "Full Back",
    "Centre Back": "Centre Back", "Left Centre Back": "Centre Back", "Right Centre Back": "Centre Back",
    "Number 6": "Number 6", "Left Defensive Midfielder": "Number 6", "Right Defensive Midfielder": "Number 6",
    "Defensive Midfielder": "Number 6", "Centre Defensive Midfielder": "Number 6",
    "Left Centre Midfield": "Number 6", "Left Centre Midfielder": "Number 6",
    "Right Centre Midfield": "Number 6", "Right Centre Midfielder": "Number 6", "Centre Midfield": "Number 6",
    "Number 8": "Number 8", "Left Attacking Midfielder": "Number 8", "Right Attacking Midfielder": "Number 8",
    "Right Attacking Midfielder": "Number 8", "Attacking Midfield": "Number 8",
    "Secondary Striker": "Number 10", "Centre Attacking Midfielder": "Number 10",
    "Winger": "Winger", "Right Midfielder": "Winger", "Left Midfielder": "Winger",
    "Left Wing": "Winger", "Right Wing": "Winger",
    "Centre Forward": "Centre Forward", "Left Centre Forward": "Centre Forward", "Right Centre Forward": "Centre Forward",
    "Goalkeeper": "Goal Keeper"
}

# --- Metrics Needed ---
statbomb_metrics_needed = [
    'player_name', 'team_name', 'season_name', 'competition_name', 'Age',
    'player_season_minutes', 'primary_position', "player_season_aerial_ratio",
    "player_season_ball_recoveries_90", "player_season_blocks_per_shot", "player_season_carries_90",
    "player_season_crossing_ratio", "player_season_deep_progressions_90", "player_season_Pressures_90",
    "player_season_defensive_action_regains_90", "player_season_defensive_actions_90",
    "player_season_dribble_faced_ratio", "player_season_dribble_ratio", "player_season_dribbles_90",
    "player_season_np_shots_90", "player_season_np_xg_90", "player_season_np_xg_per_shot",
    "player_season_npg_90", "player_season_npxgxa_90", "player_season_obv_90",
    "player_season_obv_defensive_action_90", "player_season_obv_dribble_carry_90",
    "player_season_obv_pass_90", "player_season_obv_shot_90", "player_season_op_f3_passes_90",
    "player_season_op_key_passes_90", "player_season_op_passes_into_and_touches_inside_box_90",
    "player_season_op_passes_into_box_90", "player_season_padj_clearances_90", "player_season_Scoring_Contribution_90",
    "player_season_padj_interceptions_90", "player_season_padj_pressures_90", "player_season_padj_tackles_90",
    "player_season_passing_ratio", "player_season_shot_on_target_ratio", "player_season_shot_touch_ratio",
    "player_season_touches_inside_box_90", "player_season_xgbuildup_90", "player_season_op_xa_90",
    "player_season_pressured_passing_ratio", 'player_season_da_aggressive_distance', 'player_season_clcaa',
    'player_season_gsaa_ratio', 'player_season_gsaa_90', 'player_season_save_ratio', "player_season_Counter_Pressures_90",
    'player_season_xs_ratio', 'player_season_foul_won', 'player_season_positive_outcome_score',
    'player_season_obv_gk_90', "player_season_Aggressive_actions_90"
]

# --- Metric Rename Mapping ---
metrics_mapping = {
    'player_name': "Player Name", 'team_name': 'Team', 'season_name': "Season", 'competition_name': 'League',
    'player_season_minutes': 'Minutes', 'primary_position': 'Position', "player_season_aerial_ratio": "Aerial Win %",
    "player_season_ball_recoveries_90": "Ball Recoveries", "player_season_blocks_per_shot": "Blocks/Shots",
    "player_season_carries_90": "Carries", "player_season_crossing_ratio": "Successful Crosses",
    "player_season_Pressures_90": "Pressures", "player_season_Counter_Pressures_90": "CounterPressures",
    "player_season_deep_progressions_90": "Deep Progressions", "player_season_defensive_action_regains_90": "Defensive Regains",
    "player_season_Aggressive_actions_90": "Aggressive Actions", "player_season_defensive_actions_90": "Defensive Actions",
    "player_season_dribble_faced_ratio": "Dribbles Stopped %", "player_season_dribble_ratio": "Successful Dribbles",
    "player_season_dribbles_90": "Dribbles", "player_season_np_shots_90": "Shots", "player_season_np_xg_90": "xG",
    "player_season_np_xg_per_shot": "xG/Shot", "player_season_npg_90": "NP Goals", "player_season_npxgxa_90": "xG Assisted",
    "player_season_obv_90": "OBV", "player_season_obv_defensive_action_90": "DA OBV", "player_season_obv_dribble_carry_90": "OBV D&C",
    'player_season_foul_won': "Fouls Won", "player_season_obv_pass_90": "Pass OBV", "player_season_obv_shot_90": "Shot OBV",
    "player_season_op_f3_passes_90": "OP F3 Passes", "player_season_op_key_passes_90": "OP Key Passes",
    "player_season_op_passes_into_and_touches_inside_box_90": "PINTIN", "player_season_Scoring_Contribution_90": "Scoring Contribution",
    "player_season_op_passes_into_box_90": "OP Passes Into Box", "player_season_padj_clearances_90": "PADJ Clearances",
    "player_season_padj_interceptions_90": "PADJ Interceptions", "player_season_padj_pressures_90": "PADJ Pressures",
    "player_season_padj_tackles_90": "PADJ Tackles", "player_season_passing_ratio": "Passing %",
    "player_season_shot_on_target_ratio": "Shooting %", "player_season_shot_touch_ratio": "Shot Touch %",
    "player_season_touches_inside_box_90": "Touches in Box", "player_season_xgbuildup_90": "xG Buildup",
    "player_season_op_xa_90": "OP XG ASSISTED", "player_season_pressured_passing_ratio": "PR. Pass %",
    'player_season_da_aggressive_distance': 'GK AGGRESSIVE DIST', 'player_season_clcaa': 'CLAIMS %',
    'player_season_gsaa_ratio': 'SHOT STOPPING %', 'player_season_gsaa_90': 'GSAA',
    'player_season_save_ratio': 'SAVE %', 'player_season_xs_ratio': 'XSV %',
    'player_season_positive_outcome_score': 'POSITIVE OUTCOME', 'player_season_obv_gk_90': 'GOALKEEPER OBV'
}

# --- Main Statsbomb Load Function ---
@st.cache_data(ttl=14400, show_spinner=False)
def get_statsbomb_player_season_stats():
    user = st.secrets["user"]
    passwd = st.secrets["passwd"]
    creds = {"user": user, "passwd": passwd}
    all_comps = sb.competitions(creds=creds)
    dataframes = []

    def calculate_age(birth_date):
        today = datetime.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    for _, row in all_comps.iterrows():
        try:
            comp_id, season_id = row["competition_id"], row["season_id"]
            df = sb.player_season_stats(comp_id, season_id, creds=creds)

            df['birth_date'] = pd.to_datetime(df['birth_date'])
            df['Age'] = df['birth_date'].apply(calculate_age)

            available_cols = [col for col in statbomb_metrics_needed if col in df.columns]
            df = df[available_cols]

            df = df.replace([np.nan, 'NaN', 'None', '', 'nan', 'null'], 0)
            df = df.apply(pd.to_numeric, errors='ignore')

            df.rename(columns={k: v for k, v in metrics_mapping.items() if k in df.columns}, inplace=True)

            df['Position'] = df['Position'].map(position_mapping)
            df = df.dropna(subset=['Position'])
            df = df[df['Minutes'] >= 600]
            df['Minutes'] = df['Minutes'].astype(int)

            dataframes.append(df)

        except Exception as e:
            print(f"Error: {e}")

    return pd.concat(dataframes, ignore_index=True)
