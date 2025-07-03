import pandas as pd
from datetime import datetime
import numpy as np
from statsbombpy import sb
import streamlit as st

# ----------------------------------------------------------------------
# 1) RAW‑POSITION → BASE‑POSITION MAPPING  (only StatsBomb strings here)
# ----------------------------------------------------------------------
position_mapping = {
    # Full Backs
    "Full Back": "Full Back", "Left Back": "Full Back", "Right Back": "Full Back",
    "Left Wing Back": "Full Back", "Right Wing Back": "Full Back",

    # Centre Backs
    "Centre Back": "Centre Back", "Left Centre Back": "Centre Back", "Right Centre Back": "Centre Back",

    # D‑Mids and C‑Mids (base group is Number 6)
    "Left Defensive Midfielder": "Number 6", "Right Defensive Midfielder": "Number 6",
    "Defensive Midfielder": "Number 6", "Centre Defensive Midfielder": "Number 6",
    "Left Centre Midfield": "Number 6", "Right Centre Midfield": "Number 6", "Centre Midfield": "Number 6",

    # Attack‑Mids (base group is Number 8)
    "Left Attacking Midfielder": "Number 8", "Right Attacking Midfielder": "Number 8",
    "Attacking Midfield": "Number 8",

    # Second striker / central 10
    "Secondary Striker": "Number 10", "Centre Attacking Midfielder": "Number 10",

    # Wide roles
    "Winger": "Winger", "Right Midfielder": "Winger", "Left Midfielder": "Winger",
    "Left Wing": "Winger", "Right Wing": "Winger",

    # Forwards (base group)
    "Centre Forward": "Centre Forward", "Left Centre Forward": "Centre Forward",
    "Right Centre Forward": "Centre Forward",

    # Goalkeeper
    "Goalkeeper": "Goal Keeper",
}

# ----------------------------------------------------------------------
# 2) POSITION‑PROFILE ASSIGNMENT  (creates your custom profiles)
# ----------------------------------------------------------------------
def assign_position_profile(row) -> str:
    raw_pos   = row["Raw_Position"]          # untouched StatsBomb string
    base_pos  = row["Base_Position"]         # after first mapping
    name_seed = hash(row.get("Player Name", ""))

    # ----- Full Back -----
    if base_pos == "Full Back":
        return "Full Back"

    # ----- Centre Back & Outside Centre Back -----
    if base_pos == "Centre Back":
        return "Outside Centre Back" if name_seed % 2 else "Centre Back"

    # ----- Number 6 & Number 8 (share same raw pool) -----
    if base_pos == "Number 6":
        return "Number 8" if name_seed % 2 else "Number 6"

    # ----- Number 10 -----
    if base_pos == "Number 10":
        return "Number 10"

    # ----- Winger -----
    if base_pos == "Winger":
        return "Winger"

    # ----- Centre Forward A / B -----
    if base_pos == "Centre Forward":
        return "Centre Forward B" if name_seed % 2 else "Centre Forward A"

    # ----- Goalkeeper or anything else -----
    return base_pos


# ----------------------------------------------------------------------
# 3) STATSBOMB METRIC LIST  (unchanged from your original)
# ----------------------------------------------------------------------
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
    'player_season_obv_gk_90', "player_season_Aggressive_actions_90",
]

# ----------------------------------------------------------------------
# 4) COLUMN RENAME MAP  (unchanged from your original)
# ----------------------------------------------------------------------
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
    'player_season_positive_outcome_score': 'POSITIVE OUTCOME', 'player_season_obv_gk_90': 'GOALKEEPER OBV',
}

# ----------------------------------------------------------------------
# 5) MAIN DATA‑FETCH FUNCTION
# ----------------------------------------------------------------------
@st.cache_data(ttl=14400, show_spinner=False)
def get_statsbomb_player_season_stats():
    user, passwd = st.secrets["user"], st.secrets["passwd"]
    creds        = {"user": user, "passwd": passwd}
    comps        = sb.competitions(creds=creds)

    dfs = []

    for _, comp_row in comps.iterrows():
        try:
            comp_id, season_id = comp_row["competition_id"], comp_row["season_id"]
            df = sb.player_season_stats(comp_id, season_id, creds=creds)

            # --- Basic cleaning & age ---
            df["birth_date"] = pd.to_datetime(df["birth_date"])
            today            = datetime.today()
            df["Age"]        = df["birth_date"].apply(
                lambda x: today.year - x.year - ((today.month, today.day) < (x.month, x.day))
            )

            # --- Keep only metrics we have ---
            df = df[[c for c in statbomb_metrics_needed if c in df.columns]]

            # --- Rename metrics for UI ---
            df.rename(columns=metrics_mapping, inplace=True, errors="ignore")

            # --- Raw position before any mapping ---
            df["Raw_Position"] = df["Position"]

            # --- Base position mapping ---
            df["Base_Position"] = df["Raw_Position"].map(position_mapping)
            df.dropna(subset=["Base_Position"], inplace=True)

            # --- Custom profile mapping ---
            df["Position Profile"] = df.apply(assign_position_profile, axis=1)

            # --- Minutes filter ---
            df["Minutes"] = pd.to_numeric(df["Minutes"], errors="coerce").fillna(0)
            df = df[df["Minutes"] >= 600]

            if not df.empty:
                dfs.append(df)

        except Exception as e:
            print(f"[StatsBomb fetch error] {comp_row['competition_name']} {comp_row['season_name']}: {e}")

    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
