import pandas as pd
import numpy as np
from datetime import datetime
from statsbombpy import sb
import streamlit as st

# --- Position mapping: raw position to mapped position ---
position_mapping = {
    "Full Back": ["Full Back", "Left Back", "Right Back", "Left Wing Back", "Right Wing Back"],
    "Centre Back": ["Centre Back", "Left Centre Back", "Right Centre Back"],
    "Outside Centre Back": ["Outside Centre Back", "Left Centre Back", "Right Centre Back"],
    "Number 6": [
        "Number 6", "Left Defensive Midfielder", "Right Defensive Midfielder",
        "Defensive Midfielder", "Centre Defensive Midfielder", "Left Centre Midfield",
        "Left Centre Midfielder", "Right Centre Midfield", "Right Centre Midfielder", "Centre Midfield"
    ],
    "Number 8": [
        "Number 8", "Left Defensive Midfielder", "Right Defensive Midfielder",
        "Defensive Midfielder", "Centre Defensive Midfielder", "Left Centre Midfield",
        "Left Centre Midfielder", "Right Centre Midfield", "Right Centre Midfielder", "Centre Midfield"
    ],
    "Number 10": [
        "Secondary Striker", "Centre Attacking Midfielder", "Left Attacking Midfielder",
        "Left Centre Midfield", "Left Centre Midfielder", "Right Centre Midfield",
        "Right Centre Midfielder", "Centre Midfield"
    ],
    "Winger": ["Winger", "Right Midfielder", "Left Midfielder", "Left Wing", "Right Wing"],
    "Centre Forward A": ["Centre Forward A", "Left Centre Forward", "Right Centre Forward"],
    "Centre Forward B": ["Centre Forward B", "Left Centre Forward", "Right Centre Forward"],
    "Goalkeeper": ["Goalkeeper"]
}

def map_position(raw_pos):
    for mapped_pos, raw_pos_list in position_mapping.items():
        if raw_pos in raw_pos_list:
            return mapped_pos
    return None


# --- Metrics Needed ---
statbomb_metrics_needed = [
    "minutes_90s",
    "dribbles_stopped_pct",
    "carries",
    "op_xg_assisted",
    "successful_dribbles",
    "successful_crosses",
    "ball_recoveries",
    "op_passes_into_box",
    "pr_pass_pct",
    "padj_interceptions",
    "aerial_win_pct",
    "padj_tackles",
    "padj_clearances",
    "defensive_regains",
    "da_obv",
    "pass_forward_pct",
    "op_f3_passes",
    "deep_progressions",
    "passes_obv",
    "shots",
    "xg",
    "scoring_contributon",
    "np_goals",
    "shooting_pct",
    "xg_per_shot",
    "shot_touch_pct",
    "touches_in_box",
    "shot_obv",
    "fouls_won",
    "pressures",
    "counterpressures",
    "aggressive_actions",
    "pintin",
    "xg_assisted",
    "op_key_passes",
    "obv",
    "obv_d_c",
    "gk_aggressive_dist",
    "claims_pct",
    "shot_stopping_pct",
    "gsaa",
    "save_pct",
    "xsv_pct",
    "positive_outcome",
    "goalkeeper_obv",
]

# --- Metric Rename Mapping ---
metric_rename_mapping = {
    "minutes_90s": "Minutes",
    "dribbles_stopped_pct": "Dribbles Stopped %",
    "carries": "Carries",
    "op_xg_assisted": "OP XG ASSISTED",
    "successful_dribbles": "Successful Dribbles",
    "successful_crosses": "Successful Crosses",
    "ball_recoveries": "Ball Recoveries",
    "op_passes_into_box": "OP Passes Into Box",
    "pr_pass_pct": "PR. Pass %",
    "padj_interceptions": "PADJ Interceptions",
    "aerial_win_pct": "Aerial Win %",
    "padj_tackles": "PADJ Tackles",
    "padj_clearances": "PADJ Clearances",
    "defensive_regains": "Defensive Regains",
    "da_obv": "DA OBV",
    "pass_forward_pct": "Pass Forward %",
    "op_f3_passes": "OP F3 Passes",
    "deep_progressions": "Deep Progressions",
    "passes_obv": "Pass OBV",
    "shots": "Shots",
    "xg": "xG",
    "scoring_contributon": "Scoring Contributon",
    "np_goals": "NP Goals",
    "shooting_pct": "Shooting %",
    "xg_per_shot": "xG/Shot",
    "shot_touch_pct": "Shot Touch %",
    "touches_in_box": "Touches in Box",
    "shot_obv": "Shot OBV",
    "fouls_won": "Fouls Won",
    "pressures": "Pressures",
    "counterpressures": "Counterpressures",
    "aggressive_actions": "Aggressive Actions",
    "pintin": "PINTIN",
    "xg_assisted": "xG Assisted",
    "op_key_passes": "OP Key Passes",
    "obv": "OBV",
    "obv_d_c": "OBV D&C",
    "gk_aggressive_dist": "GK AGGRESSIVE DIST",
    "claims_pct": "CLAIMS %",
    "shot_stopping_pct": "SHOT STOPPING %",
    "gsaa": "GSAA",
    "save_pct": "SAVE %",
    "xsv_pct": "XSV %",
    "positive_outcome": "POSITIVE OUTCOME",
    "goalkeeper_obv": "GOALKEEPER OBV",
}


# List of desired columns: player info + metrics needed
desired_columns = [
    "player_id", "player_name", "birth_date", "primary_position",
    "team_name", "competition_name", "season_name"
] + statbomb_metrics_needed


@st.cache_data(ttl=14400, show_spinner=False)
def get_statsbomb_player_season_stats():
    user = st.secrets["user"]
    passwd = st.secrets["passwd"]
    creds = {"user": user, "passwd": passwd}

    all_comps = sb.competitions(creds=creds)
    dfs = []

    def calculate_age(birth_date):
        today = datetime.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    for _, row in all_comps.iterrows():
        try:
            comp_id = row["competition_id"]
            season_id = row["season_id"]

            df = sb.player_season_stats(comp_id, season_id, creds=creds)

            if df.empty:
                continue

            # Filter columns to only desired ones that exist
            available_cols = [col for col in desired_columns if col in df.columns]
            df = df[available_cols]

            # Clean and convert data
            df = df.replace([np.nan, "NaN", "None", "", "nan", "null"], 0)

            for col in df.columns:
                if col not in ["player_name", "team_name", "competition_name", "season_name", "birth_date", "primary_position"]:
                    try:
                        df[col] = pd.to_numeric(df[col])
                    except Exception:
                        pass  # Ignore non-numeric columns

            # Calculate age
            if "birth_date" in df.columns:
                df["birth_date"] = pd.to_datetime(df["birth_date"], errors='coerce')
                df["Age"] = df["birth_date"].apply(lambda x: calculate_age(x) if pd.notnull(x) else np.nan)

            # Rename metrics columns to your standard names
            df.rename(columns=metric_rename_mapping, inplace=True)

            # Map positions
            if "primary_position" in df.columns:
                df["Mapped Position"] = df["primary_position"].apply(map_position)
                df = df.dropna(subset=["Mapped Position"])  # Keep only rows with mapped positions
            else:
                df["Mapped Position"] = None

            # Filter by minimum minutes played (600)
            if "Minutes" in df.columns:
                df = df[df["Minutes"] >= 600]
                df["Minutes"] = df["Minutes"].astype(int)

            dfs.append(df)

        except Exception as e:
            print(f"Error fetching stats for {row['competition_name']} {row['season_name']}: {e}")

    if len(dfs) == 0:
        return pd.DataFrame()

    combined_df = pd.concat(dfs, ignore_index=True)
    return combined_df
