"""  
retrieve_statbomb_data.py  
Build a season-level player dataframe from StatsBomb that’s safe to  
import whether or not Streamlit is installed.  
  
Key features  
– Safe Streamlit stub (top of file)    
– Minutes ≥ 600 filter    
– “League” column derived from competition_name    
– Legacy alias get_statsbomb_player_season_stats()  
"""  
  
# ------------------------------------------------------------------  
# Safe Streamlit import ─ works even if streamlit isn’t installed  
# ------------------------------------------------------------------  
try:  
    import streamlit as st  
except ModuleNotFoundError:  
    class _Stub:  
        def __getattr__(self, _):  
            def _dec(*a, **kw):  
                def _wrap(f): return f  
                return _wrap  
            return _dec  
        def write(*_, **__):          ...  
        def dataframe(*_, **__):      ...  
        def button(*_, **__):         return False  
        def spinner(*_, **__):  
            from contextlib import contextmanager  
            @contextmanager  
            def cm(): yield  
            return cm()  
        def title(*_, **__):          ...  
        def error(*_, **__):          ...  
        def success(*_, **__):        ...  
    st = _Stub()  
  
# ------------------------------------------------------------------  
# Standard imports  
# ------------------------------------------------------------------  
from datetime import datetime  
import pandas as pd  
import numpy as np  
from statsbombpy import sb  
  
# ------------------------------------------------------------------  
# Position mapping (edit to taste)  
# ------------------------------------------------------------------  
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
  
# Minimal set of columns to keep (add more if desired)  
statbomb_metrics_needed = [  
    "player_name",  
    "team_name",  
    "season_name",  
    "competition_name",  
    "Age",  
    "minutes",  
    "primary_position",  
]  
  
# ------------------------------------------------------------------  
# Cached table of competitions & seasons  
# ------------------------------------------------------------------  
@st.cache_data(show_spinner=False)  
def _competition_table():  
    comps = sb.competitions()  
    comps["season_label"] = (  
        comps["season_name"].astype(str) + " – " + comps["competition_name"]  
    )  
    return comps[["competition_id", "season_id", "competition_name", "season_label"]]  
  
# ------------------------------------------------------------------  
# Core retrieval  
# ------------------------------------------------------------------  
def retrieve_player_season_stats() -> pd.DataFrame:  
    """  
    Return combined player-season dataframe with:  
    – Minutes ≥ 600  
    – Position mapping  
    – League & season_comp helper cols  
    """  
    frames = []  
  
    for _, row in _competition_table().iterrows():  
        try:  
            df = sb.player_season_stats(row.competition_id, row.season_id)  
        except Exception:  
            continue  # skip bad seasons  
  
        # Trim & rename  
        df = df.rename(columns=lambda c: c.replace("player_season_", ""))  
        df = df[statbomb_metrics_needed].copy()  
        df = df.rename(columns={"minutes": "Minutes", "primary_position": "Position"})  
        df["Position"] = df["Position"].map(position_mapping)  
        df = df.dropna(subset=["Position"])  
  
        # Minutes filter  
        df = df[df["Minutes"] >= 600]  
        df["Minutes"] = df["Minutes"].astype(int)  
  
        # Extra columns  
        df["League"]      = row.competition_name  
        df["season_comp"] = row.season_label  
  
        frames.append(df)  
  
    if not frames:  
        return pd.DataFrame()  
  
    combined = pd.concat(frames, ignore_index=True)  
    return combined.drop_duplicates(subset=["player_name", "team_name", "season_comp"])  
  
# ------------------------------------------------------------------  
# Legacy alias for main.py  
# ------------------------------------------------------------------  
def get_statsbomb_player_season_stats() -> pd.DataFrame:  
    return retrieve_player_season_stats()  
  
# ------------------------------------------------------------------  
# Manual test  
# ------------------------------------------------------------------  
if __name__ == "__main__":  
    print(retrieve_player_season_stats().head())  
