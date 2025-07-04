from data.retrieve_statbomb_data import get_statsbomb_player_season_stats  
statsbomb_data = get_statsbomb_player_season_stats()  
print(statsbomb_data.columns.tolist())     # should include 'League'  
print(statsbomb_data.head())               # preview rows  """  
retrieve_statbomb_data.py  
Pull StatsBomb season-level player data, map raw positions to custom  
position groups, and expose helper functions for the Streamlit app.  
  
– Includes 600-minute filter.  
– Adds a “League” column (copy of competition_name).  
– Safe to import even if Streamlit isn’t installed.  

from datetime import datetime  
import numpy as np  
import pandas as pd  
from statsbombpy import sb  
  
# ---------------------------------------------------------------------  
# Streamlit is optional ─ fall back to a stub if it’s not available  
# ---------------------------------------------------------------------  
try:  
    import streamlit as st  
except ModuleNotFoundError:  
    class _Stub:  
        def __getattr__(self, _):  
            # decorator form (e.g. @st.cache_data)  
            def _dec(*args, **kwargs):  
                def _wrap(func):  
                    return func  
                return _wrap  
            return _dec  
        # no-ops for common UI calls  
        def write(self, *_, **__):        ...  
        def dataframe(self, *_, **__):    ...  
        def button(self, *_, **__):       return False  
        def spinner(self, *_, **__):  
            from contextlib import contextmanager  
            @contextmanager  
            def cm(): yield  
            return cm()  
        def title(self, *_):              ...  
        def error(self, *_):              ...  
        def success(self, *_):            ...  
    st = _Stub()  
  
# ---------------------------------------------------------------------  
# Position remap (example – adjust as needed)  
# ---------------------------------------------------------------------  
position_mapping = {  
    "Centre Back"        : "Centre Back",  
    "Left Back"          : "Full Back",  
    "Right Back"         : "Full Back",  
    "Defensive Midfield" : "Number 6",  
    "Central Midfield"   : "Number 8",  
    "Attacking Midfield" : "Number 10",  
    "Left Wing"          : "Winger",  
    "Right Wing"         : "Winger",  
    "Centre Forward"     : "Centre Forward A",  
}  
  
# All columns we plan to keep (trim raw SB output)  
statbomb_metrics_needed = [  
    "player_name", "team_name", "season_name", "competition_name", "Age",  
    "minutes", "primary_position",  
    # ↓ add any extra StatsBomb player_season_ columns you need  
    "aerial_ratio", "ball_recoveries_90", "blocks_per_shot",  
    "carries_90", "crossing_ratio", "deep_progressions_90",  
    "defensive_action_regains_90", "defensive_actions_90",  
    "dribble_faced_ratio", "dribbles_90", "interceptions_padj",  
    "obv", "passes_into_box", "pressures",  
    "xg", "xg_assisted",  
]  
  
# ---------------------------------------------------------------------  
# Utility – cached list of competitions & seasons  
# ---------------------------------------------------------------------  
@st.cache_data(show_spinner=False)  
def _comp_season_table():  
    comps = sb.competitions()  
    comps["season_label"] = (  
        comps["season_name"].astype(str) + " – " + comps["competition_name"]  
    )  
    return comps[["competition_id", "season_id", "competition_name", "season_label"]]  
  
# ---------------------------------------------------------------------  
# Main retrieval routine  
# ---------------------------------------------------------------------  
def retrieve_player_season_stats() -> pd.DataFrame:  
    """Return a dataframe of player-season stats (≥ 600 mins)."""  
    frames = []  
  
    for _, row in _comp_season_table().iterrows():  
        try:  
            df = sb.player_season_stats(row.competition_id, row.season_id)  
        except Exception:  
            # quietly skip broken seasons  
            continue  
  
        # keep only defined metrics  
        df = df.rename(columns=lambda c: c.replace("player_season_", ""))  
        df = df[statbomb_metrics_needed].copy()  
  
        # rename / map  
        df = df.rename(columns={  
            "minutes"          : "Minutes",  
            "primary_position" : "Position",  
            "age"              : "Age",  
        })  
        df["Position"] = df["Position"].map(position_mapping)  
        df = df.dropna(subset=["Position"])  
  
        # minutes filter  ≥ 600  
        df = df[df["Minutes"] >= 600]  
        df["Minutes"] = df["Minutes"].astype(int)  
  
        # extra columns for the app  
        df["League"]       = row.competition_name  
        df["season_comp"]  = row.season_label  
        frames.append(df)  
  
    if not frames:  
        return pd.DataFrame()  
  
    combined = pd.concat(frames, ignore_index=True)  
    # drop duplicates player+team+season  
    return combined.drop_duplicates(  
        subset=["player_name", "team_name", "season_comp"]  
    )  
  
# ---------------------------------------------------------------------  
# Back-compat alias expected by legacy code  
# ---------------------------------------------------------------------  
def get_statsbomb_player_season_stats() -> pd.DataFrame:  # alias  
    return retrieve_player_season_stats()  
  
# ---------------------------------------------------------------------  
# Quick Streamlit demo (ignored when imported elsewhere)  
# ---------------------------------------------------------------------  
def main():  
    st.title("StatsBomb Player-Season Data")  
    st.write("Click the button to pull fresh data (600-minute cutoff).")  
  
    if st.button("Fetch / Refresh data"):  
        with st.spinner("Querying StatsBomb…"):  
            data = retrieve_player_season_stats()  
  
        if data.empty:  
            st.error("No rows returned.")  
        else:  
            st.success(f"Retrieved {len(data):,} rows.")  
            st.dataframe(data.head())  
  
if __name__ == "__main__":  
    main()  
