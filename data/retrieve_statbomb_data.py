# data/retrieve_statbomb_data.py
import pandas as pd
import numpy as np
from datetime import datetime
from statsbombpy import sb
import streamlit as st

# ────────────────────────────────────────────────────────────────────────────────
# 0.  metrics_per_position  (unchanged – copied from your message)               │
# ────────────────────────────────────────────────────────────────────────────────
metrics_per_position = {  # ←‑‑‑ full dict exactly as you provided
    "Full Back": [
        "Dribbles Stopped %", "Carries", "OP XG ASSISTED", "Successful Dribbles",
        "Successful Crosses", "Ball Recoveries", "OP Passes Into Box",
        "PR. Pass %", "PADJ Interceptions", "Aerial Win %"
    ],
    # … << entire dict preserved >> …
    "Goal Keeper": [
        "GK AGGRESSIVE DIST", "CLAIMS %", "PR. Pass %", "SHOT STOPPING %",
        "OP F3 Passes", "GSAA", "SAVE %", "XSV %", "POSITIVE OUTCOME",
        "GOALKEEPER OBV"
    ]
}

# ────────────────────────────────────────────────────────────────────────────────
# 1.  mapping helpers                                                             │
# ────────────────────────────────────────────────────────────────────────────────
base_position_map = {
    # full backs
    "Full Back": "Full Back", "Left Back": "Full Back", "Right Back": "Full Back",
    "Left Wing Back": "Full Back", "Right Wing Back": "Full Back",
    # centre‑back variants → single base
    "Centre Back": "CB BASE", "Left Centre Back": "CB BASE", "Right Centre Back": "CB BASE",
    "Outside Centre Back": "CB BASE",
    # CF variants → single base
    "Centre Forward": "CF BASE", "Left Centre Forward": "CF BASE", "Right Centre Forward": "CF BASE",
    # DM/CM/AM mapping (6 / 8 / 10)
    "Number 6": "Number 6", "Defensive Midfielder": "Number 6", "Centre Defensive Midfielder": "Number 6",
    "Left Defensive Midfielder": "Number 6", "Right Defensive Midfielder": "Number 6",
    "Centre Midfield": "Number 8", "Left Centre Midfield": "Number 8", "Right Centre Midfield": "Number 8",
    "Left Centre Midfielder": "Number 8", "Right Centre Midfielder": "Number 8",
    "Number 8": "Number 8",
    "Attacking Midfield": "Number 8", "Left Attacking Midfield": "Number 8", "Right Attacking Midfield": "Number 8",
    "Right Attacking Midfielder": "Number 8",
    "Secondary Striker": "Number 10", "Centre Attacking Midfielder": "Number 10", "Left Attacking Midfielder": "Number 10",
    # wingers
    "Winger": "Winger", "Right Midfielder": "Winger", "Left Midfielder": "Winger",
    "Left Wing": "Winger", "Right Wing": "Winger",
    # gk
    "Goalkeeper": "Goal Keeper",
}

# StatsBomb → friendly names
metrics_mapping = {
    "player_name": "Player Name", "team_name": "Team", "season_name": "Season",
    "competition_name": "League", "player_season_minutes": "Minutes",
    "primary_position": "Position",

    # <‑‑‑ rest identical to the mapping you provided (omitted here for brevity) ─>
    "player_season_foul_won": "Fouls Won",
    "player_season_Pressures_90": "Pressures",
    "player_season_Counter_Pressures_90": "Counterpressures",
    "player_season_Aggressive_actions_90": "Aggressive Actions",
    "player_season_Scoring_Contribution_90": "Scoring Contribution",
}

statbomb_metrics_needed = list(metrics_mapping.keys())

# ────────────────────────────────────────────────────────────────────────────────
# 2.  loader (cached)                                                             │
# ────────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=14_400, show_spinner=False)
def _load_raw_statsbomb() -> pd.DataFrame:
    creds = {"user": st.secrets["user"], "passwd": st.secrets["passwd"]}
    comps = sb.competitions(creds=creds)
    frames = []
    for _, r in comps.iterrows():
        try:
            frames.append(
                sb.player_season_stats(r["competition_id"], r["season_id"], creds=creds)
            )
        except Exception as e:
            print("Skip comp", r["competition_id"], r["season_id"], ":", e)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

# ────────────────────────────────────────────────────────────────────────────────
# 3.  post‑process helpers                                                        │
# ────────────────────────────────────────────────────────────────────────────────
def _calculate_age(series):
    today = datetime.today()
    return series.apply(
        lambda d: today.year - d.year - ((today.month, today.day) < (d.month, d.day))
        if not pd.isna(d) else 0
    )

def _duplicate_positions(df: pd.DataFrame) -> pd.DataFrame:
    """make CF A/B duplicates & Centre‑Back / Outside‑CB duplicates."""
    cf = df[df["Position"] == "CF BASE"]
    cb = df[df["Position"] == "CB BASE"]

    cf_a = cf.copy(); cf_a["Position"] = "Centre Forward A"
    cf_b = cf.copy(); cf_b["Position"] = "Centre Forward B"

    cb_core = cb.copy();   cb_core["Position"] = "Centre Back"
    cb_out  = cb.copy();   cb_out["Position"] = "Outside Centre Back"

    others = df[~df["Position"].isin(["CF BASE", "CB BASE"])]

    return pd.concat([others, cf_a, cf_b, cb_core, cb_out], ignore_index=True)

def _ensure_metric_columns(df: pd.DataFrame) -> pd.DataFrame:
    needed = {m for lst in metrics_per_position.values() for m in lst}
    needed.add("Scoring Contribution")          # derived
    for col in needed:
        if col not in df.columns:
            df[col] = 0
    return df

# ────────────────────────────────────────────────────────────────────────────────
# 4.  main callable                                                               │
# ────────────────────────────────────────────────────────────────────────────────
def get_statsbomb_player_season_stats() -> pd.DataFrame:
    raw = _load_raw_statsbomb()
    if raw.empty:
        return raw

    # keep + rename
    keep = [c for c in statbomb_metrics_needed if c in raw.columns]
    df = raw[keep].copy().rename(columns=metrics_mapping)

    # age
    if "birth_date" in raw.columns:
        df["Age"] = _calculate_age(pd.to_datetime(raw["birth_date"], errors="coerce"))

    # map to base positions
    df["Position"] = raw["primary_position"].map(base_position_map)
    df = df.dropna(subset=["Position"])

    # derived metrics
    if {"NP Goals", "OP XG ASSISTED"}.issubset(df.columns):
        df["Scoring Contribution"] = df["NP Goals"] + df["OP XG ASSISTED"]

    # minutes filter
    df = df[df["Minutes"] >= 600].copy()

    # produce duplicates
    df = _duplicate_positions(df)

    # guarantee all metric columns exist
    df = _ensure_metric_columns(df)

    # numeric clean
    df.replace([np.nan, "NaN", "", "None", "null"], 0, inplace=True)
    df = df.apply(pd.to_numeric, errors="ignore")

    return df.reset_index(drop=True)

# ────────────────────────────────────────────────────────────────────────────────
# 5. quick manual test when run standalone                                        │
# ────────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test = get_statsbomb_player_season_stats()
    print("rows:", len(test))
    print(test["Position"].value_counts().head())
