# ───────────────────────────────────────────────────────────────────  
#  retrieve_statbomb_data.py  |  same logic • refreshed metric list  
# ───────────────────────────────────────────────────────────────────  
import pandas as pd  
from datetime import datetime  
import numpy as np  
from statsbombpy import sb  
import streamlit as st                              # keep original import  
  
# ── NEW METRIC LIST ONLY ───────────────────────────────────────────  
statbomb_metrics_needed = [  
    # identity  
    "player_name", "team_name", "season_name", "competition_name",  
    "birth_date", "Age",  
    # minutes / position (unchanged keys)  
    "player_season_minutes", "primary_position",  
  
    # ─ advanced metrics you supplied ─  
    "player_season_aerial_ratio",  
    "player_season_ball_recoveries_90",  
    "player_season_blocks_per_shot",  
    "player_season_carries_90",  
    "player_season_crossing_ratio",  
    "player_season_deep_progressions_90",  
    "player_season_defensive_action_regains_90",  
    "player_season_defensive_actions_90",  
    "player_season_dribble_faced_ratio",  
    "player_season_dribble_ratio",  
    "player_season_dribbles_90",  
    "player_season_np_shots_90",  
    "player_season_np_xg_90",  
    "player_season_np_xg_per_shot",  
    "player_season_npg_90",  
    "player_season_npxgxa_90",  
    "player_season_obv_90",  
    "player_season_obv_defensive_action_90",  
    "player_season_obv_dribble_carry_90",  
    "player_season_obv_pass_90",  
    "player_season_obv_shot_90",  
    "player_season_op_f3_passes_90",  
    "player_season_op_key_passes_90",  
    "player_season_op_passes_into_and_touches_inside_box_90",  
    "player_season_op_passes_into_box_90",  
    "player_season_padj_clearances_90",  
    "player_season_padj_interceptions_90",  
    "player_season_padj_pressures_90",  
    "player_season_padj_tackles_90",  
    "player_season_passing_ratio",  
    "player_season_shot_on_target_ratio",  
    "player_season_shot_touch_ratio",  
    "player_season_touches_inside_box_90",  
    "player_season_xgbuildup_90",  
    "player_season_op_xa_90",  
    "player_season_pressured_passing_ratio",  
    "player_season_da_aggressive_distance",  
    "player_season_clcaa",  
    "player_season_gsaa_ratio",  
    "player_season_gsaa_90",  
    "player_season_save_ratio",  
    "player_season_xs_ratio",  
    "player_season_positive_outcome_score",  
    "player_season_obv_gk_90Carries",  
    "Successful Crosses",  
    "OP Passes Into Box",  
    "OP F3 Passes",  
    "Scoring Contribution",  
    "PR. Pass %",  
    "Fouls Won",  
    "Pressures",  
    "Counterpressures",  
    "Aggressive Actions",  
]  
  
# ── REST OF FILE UNCHANGED (↓↓ copy from your last good version) ──  
  
@st.cache_data(show_spinner=False)  
def _competition_table():  
    comps = sb.competitions()  
    comps["season_label"] = (  
        comps["season_name"].astype(str) + " – " + comps["competition_name"]  
    )  
    return comps[  
        ["competition_id", "season_id", "competition_name", "season_label"]  
    ]  
  
def get_statsbomb_player_season_stats():  
    frames = []  
    for _, row in _competition_table().iterrows():  
        try:  
            df = sb.player_season_stats(row.competition_id, row.season_id)  
        except Exception:  
            continue  
  
        df = df.rename(columns=lambda c: c.replace("player_season_", ""))  
        df = df[statbomb_metrics_needed]  
        df["League"] = row.competition_name          # <── ensures dropdown key  
        frames.append(df)  
  
    if not frames:  
        return pd.DataFrame()  
  
    return pd.concat(frames, ignore_index=True)  
  
&nbsp;  
 # ── smoke-test when executed directly ──────────────────────────────  
if __name__ == "__main__":  
    sample = get_statsbomb_player_season_stats().head()  
    st.write(sample)           # works in Streamlit, no-op otherwise  
