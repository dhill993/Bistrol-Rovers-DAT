"""  
retrieve_statbomb_data.py  
Pull StatsBomb season-level player data, map raw positions to your custom  
position profiles, and expose a small Streamlit front-end for testing.  
"""  
  
import pandas as pd  
from datetime import datetime  
import numpy as np  
from statsbombpy import sb  
import streamlit as st  
  
# ------------------------------------------------------------------  
# 1.  Master list of season metrics we keep  
# ------------------------------------------------------------------  
statbomb_metrics_needed = [  
    # IDs / labels  
    "player_name", "team_name", "season_name", "competition_name", "Age",  
    # minutes & basic  
    "player_season_minutes", "primary_position",  
    # legacy metrics you already tracked  
    "player_season_aerial_ratio", "player_season_ball_recoveries_90",  
    "player_season_blocks_per_shot", "player_season_carries_90",  
    "player_season_crossing_ratio", "player_season_deep_progressions_90",  
    "player_season_defensive_action_regains_90",  
    "player_season_defensive_actions_90", "player_season_dribble_faced_ratio",  
    "player_season_dribble_ratio", "player_season_dribbles_90",  
    "player_season_np_shots_90", "player_season_np_xg_90",  
    "player_season_np_xg_per_shot", "player_season_npg_90",  
    "player_season_npxgxa_90", "player_season_obv_90",  
    "player_season_obv_defensive_action_90", "player_season_obv_possession_90",  
    "player_season_obv_shot_90", "player_season_padj_blocks_90",  
    "player_season_padj_clearances_90", "player_season_padj_interceptions_90",  
    "player_season_padj_tackles_90", "player_season_pass_accuracy",  
    "player_season_passes_90", "player_season_passes_into_box_90",  
    "player_season_pressures_90", "player_season_shots_90",  
    "player_season_xg_90",  
    # NEW metrics you asked to bolt on  
    "Carries", "Successful Crosses", "OP Passes Into Box", "OP F3 Passes",  
    "Scoring Contribution", "PR. Pass %", "Fouls Won", "Pressures",  
    "Counterpressures", "Aggressive Actions"  
]  
  
# ------------------------------------------------------------------  
# 2.  Map StatsBomb raw positions → your custom profiles  
# ------------------------------------------------------------------  
position_mapping = {  
    # FULL BACK  
    "Left Back": "Full Back", "Right Back": "Full Back",  
    "Left Wing Back": "Full Back", "Right Wing Back": "Full Back",  
  
    # CENTRE BACK  (traditional)  
    "Left Centre Back": "Centre Back",  
    "Right Centre Back": "Centre Back",  
    "Centre Back": "Centre Back",  
  
    # OUTSIDE CENTRE BACK  (progressive CB in back-three)  
    "Left Centre Back (OCB)": "Outside Centre Back",  
    "Right Centre Back (OCB)": "Outside Centre Back",  
    "Centre Back (OCB)": "Outside Centre Back",  
  
    # NUMBER 6  
    "Left Defensive Midfielder": "Number 6",  
    "Right Defensive Midfielder": "Number 6",  
    "Defensive Midfielder": "Number 6",  
    "Left Centre Midfield": "Number 6",  
    "Right Centre Midfield": "Number 6",  
    "Centre Midfield": "Number 6",  
  
    # NUMBER 8  
    "Left Defensive Midfielder (8)": "Number 8",  
    "Right Defensive Midfielder (8)": "Number 8",  
    "Defensive Midfielder (8)": "Number 8",  
    "Left Centre Midfield (8)": "Number 8",  
    "Right Centre Midfield (8)": "Number 8",  
    "Centre Midfield (8)": "Number 8",  
  
    # NUMBER 10  
    "Left Attacking Midfield": "Number 10",  
    "Right Attacking Midfield": "Number 10",  
    "Attacking Midfield": "Number 10",  
    "Left Midfielder": "Number 10",  
    "Right Midfielder": "Number 10",  
    "Left Wing": "Number 10",  
    "Right Wing": "Number 10",  
    "Secondary Striker": "Number 10",  
  
    # WINGER  
    "Left Attacking Midfield (W)": "Winger",  
    "Right Attacking Midfield (W)": "Winger",  
    "Left Midfielder (W)": "Winger",  
    "Right Midfielder (W)": "Winger",  
    "Left Wing (W)": "Winger",  
    "Right Wing (W)": "Winger",  
  
    # CENTRE FORWARD A (box striker)  
    "Centre Forward": "Centre Forward A",  
    "Left Centre Forward": "Centre Forward A",  
    "Right Centre Forward": "Centre Forward A",  
  
    # CENTRE FORWARD B (pressing / roaming striker)  
    "Centre Forward (B)": "Centre Forward B",  
    "Left Centre Forward (B)": "Centre Forward B",  
    "Right Centre Forward (B)": "Centre Forward B",  
}  
  
# ------------------------------------------------------------------  
# 3.  Helpers  
# ------------------------------------------------------------------  
@st.cache_data(show_spinner=False)  
def get_comp_season_ids():  
    """Return df of competition & season IDs."""  
    comps = sb.competitions()  
    comps["season_label"] = comps["season_name"].astype(str) + " – " + comps["competition_name"]  
    return comps[["competition_id", "season_id", "season_label"]]  
  
def retrieve_player_season_stats():  
    """Loop through every season, pull stats, map positions, concatenate."""  
    comps = get_comp_season_ids()  
    season_frames = []  
  
    for _, row in comps.iterrows():  
        try:  
            df = sb.player_season_stats(  
                competition_id=row.competition_id,  
                season_id=row.season_id  
            )  
        except Exception:  
            continue  
  
        # rename & prune  
        df = df.rename(columns={c: c.replace("player_season_", "") for c in df.columns})  
        df = df.rename(columns={"minutes": "Minutes",  
                                "primary_position": "Position",  
                                "age": "Age"})  
        df = df[[c for c in df.columns if c in statbomb_metrics_needed]]  
  
        # apply position profiles  
        df["Position"] = df["Position"].map(position_mapping)  
        df = df.dropna(subset=["Position"])  
  
        df["season_comp"] = row.season_label  
        season_frames.append(df)  
  
    if season_frames:  
        combined = pd.concat(season_frames, ignore_index=True)  
        return combined.drop_duplicates(subset=["player_name", "team_name", "season_comp"])  
    return pd.DataFrame()  
  
# ------------------------------------------------------------------  
# 4.  Streamlit UI  
# ------------------------------------------------------------------  
def main():  
    st.title("StatsBomb – Player-Season Data")  
    st.write("Pull data, map to custom positions, and preview below.")  
  
    if st.button("Fetch / Refresh data"):  
        with st.spinner("Querying StatsBomb…"):  
            data = retrieve_player_season_stats()  
  
        if data.empty:  
            st.error("No rows returned – check API / filters.")  
        else:  
            st.success(f"Retrieved {len(data):,} rows")  
            st.dataframe(data.head())  
  
if __name__ == "__main__":  
    main()  
