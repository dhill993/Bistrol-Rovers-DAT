"""  
retrieve_statbomb_data.py  ⟡  Season-level StatsBomb player data  
– Safe to import with or without Streamlit installed  
– Updated metric list           (<<<  YOUR NEW METRICS HERE  )  
– Updated position profiles     (<<<  YOUR NEW PROFILES HERE )  
– Adds a 'League' column  
"""  
  
# ------------------------------------------------------------------  
# Streamlit (optional)  
# ------------------------------------------------------------------  
try:  
    import streamlit as st  
except ModuleNotFoundError:          # running outside Streamlit  
    class _Stub:  
        def __getattr__(self, _):  
            def _dec(*a, **k):  
                def _wrap(f): return f  
                return _wrap  
            return _dec  
        def write(*a, **k):     ...  
        def dataframe(*a, **k): ...  
        def button(*a, **k):    return False  
        def spinner(*a, **k):  
            from contextlib import contextmanager  
            @contextmanager  
            def cm(): yield  
            return cm()  
        def title(*a, **k):     ...  
        def error(*a, **k):     ...  
        def success(*a, **k):   ...  
    st = _Stub()  
  
# ------------------------------------------------------------------  
# Standard imports  
# ------------------------------------------------------------------  
import pandas as pd  
from statsbombpy import sb  
  
# ------------------------------------------------------------------  
# UPDATED POSITION PROFILES  
# ------------------------------------------------------------------  
position_mapping = {  
    "Centre Back"        : "Centre Back",  
    "Left Back"          : "Full Back",  
    "Right Back"         : "Full Back",  
    "Defensive Midfield" : "6",  
    "Central Midfield"   : "8",  
    "Attacking Midfield" : "10",  
    "Left Wing"          : "Winger",  
    "Right Wing"         : "Winger",  
    "Centre Forward"     : "Striker",  
    "Second Striker"     : "Striker",  
    # add/remove as required  
}  
  
# ------------------------------------------------------------------  
# UPDATED METRIC LIST  (trim StatsBomb output to these)  
# ------------------------------------------------------------------  
statbomb_metrics_needed = [  
    "player_name", "team_name", "season_name", "competition_name", "Age",  
    "minutes", "primary_position",  
    "aerial_ratio", "ball_recoveries_90", "blocks_per_shot",  
    "carries_90", "crossing_ratio", "deep_progressions_90",  
    "defensive_action_regains_90", "defensive_actions_90",  
    "dribble_faced_ratio", "dribble_ratio", "dribbles_90",  
    "np_shots_90", "np_xg_90", "np_xg_per_shot", "npg_90",  
    "npxgxa_90", "obv_90", "obv_pass_90", "obv_shot_90",  
    "op_f3_passes_90", "op_key_passes_90",  
    "op_passes_into_and_touches_inside_box_90", "op_passes_into_box_90",  
    "padj_clearances_90", "padj_interceptions_90", "padj_pressures_90",  
    "padj_tackles_90", "passing_ratio", "shot_on_target_ratio",  
    "shot_touch_ratio", "touches_inside_box_90", "xgbuildup_90",  
    "op_xa_90", "pressured_passing_ratio", "da_aggressive_distance",  
    "clcaa", "gsaa_ratio", "gsaa_90", "save_ratio", "xs_ratio",  
    "positive_outcome_score", "obv_gk_90Carries", "Successful Crosses",  
    "OP Passes Into Box", "OP F3 Passes", "Scoring Contribution",  
    "PR. Pass %", "Fouls Won", "Pressures", "Counterpressures",  
    "Aggressive Actions",  
]  
  
# ------------------------------------------------------------------  
# Cached competitions table  
# ------------------------------------------------------------------  
@st.cache_data(show_spinner=False)  
def _comps():  
    df = sb.competitions()  
    df["season_label"] = df["season_name"].astype(str) + " – " + df["competition_name"]  
    return df[["competition_id", "season_id", "competition_name", "season_label"]]  
  
# ------------------------------------------------------------------  
# MAIN FUNCTION  
# ------------------------------------------------------------------  
def retrieve_player_season_stats():  
    frames = []  
    for _, row in _comps().iterrows():  
        try:  
            df = sb.player_season_stats(row.competition_id, row.season_id)  
        except Exception:  
            continue                                  # skip if unavailable  
  
        # keep only needed cols, rename for clarity  
        df = df.rename(columns=lambda c: c.replace("player_season_", ""))  
        df = df[statbomb_metrics_needed].copy()  
        df = df.rename(columns={"minutes": "Minutes", "primary_position": "Position"})  
  
        # map positions & drop unmapped  
        df["Position"] = df["Position"].map(position_mapping)  
        df = df.dropna(subset=["Position"])  
  
        # minutes ≥ 600  
        df = df[df["Minutes"] >= 600]  
        df["Minutes"] = df["Minutes"].astype(int)  
  
        # add helper cols  
        df["League"]      = row.competition_name  
        df["season_comp"] = row.season_label  
  
        frames.append(df)  
  
    if not frames:  
        return pd.DataFrame()  
  
    combined = pd.concat(frames, ignore_index=True)  
    return combined.drop_duplicates(subset=["player_name", "team_name", "season_comp"])  
  
# legacy wrapper  
def get_statsbomb_player_season_stats():  
    return retrieve_player_season_stats()  
  
# quick smoke-test when run directly  
if __name__ == "__main__":  
    print(retrieve_player_season_stats().head())  
