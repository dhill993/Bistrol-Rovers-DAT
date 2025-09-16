import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from statsbombpy import sb

# ------------------- CONFIG -------------------
st.set_page_config(page_title='Football Z-Score Profiles', layout='wide')
st.title('Football Z-Score Profiles')

# ------------------- STATSBOMB CREDENTIALS -------------------
STATSBOMB_USER = "dhillon.gil@bristolrovers.co.uk"
STATSBOMB_PASS = "004laVPb"

# ------------------- METRIC MAPPING -------------------
metric_map = {
    "player_season_aerial_ratio": "Aerial Win %",
    "player_season_ball_recoveries_90": "Ball Recoveries",
    "player_season_blocks_per_shot": "Blocks/Shots",
    "player_season_carries_90": "Carries",
    "player_season_crossing_ratio": "Successful Crosses",
    "player_season_deep_progressions_90": "Deep Progressions",
    "player_season_defensive_action_regains_90": "Defensive Regains",
    "player_season_defensive_actions_90": "Defensive Actions",
    "player_season_dribble_faced_ratio": "Dribbles Stopped %",
    "player_season_dribble_ratio": "Successful Dribbles",
    "player_season_dribbles_90": "Dribbles",
    "player_season_np_shots_90": "Shots",
    "player_season_np_xg_90": "xG",
    "player_season_np_xg_per_shot": "xG/Shot",
    "player_season_npg_90": "NP Goals",
    "player_season_npxgxa_90": "xG Assisted",
    "player_season_obv_90": "OBV",
    "player_season_obv_defensive_action_90": "DA OBV",
    "player_season_obv_dribble_carry_90": "OBV D&C",
    "player_season_obv_pass_90": "Pass OBV",
    "player_season_obv_shot_90": "Shot OBV",
    "player_season_op_f3_passes_90": "OP F3 Passes",
    "player_season_op_key_passes_90": "OP Key Passes",
    "player_season_op_passes_into_and_touches_inside_box_90": "PINTIN",
    "player_season_op_passes_into_box_90": "OP Passes Into Box",
    "player_season_padj_clearances_90": "PADJ Clearances",
    "player_season_padj_interceptions_90": "PADJ Interceptions",
    "player_season_padj_pressures_90": "PADJ Pressures",
    "player_season_padj_tackles_90": "PADJ Tackles",
    "player_season_passing_ratio": "Passing %",
    "player_season_shot_on_target_ratio": "Shooting %",
    "player_season_shot_touch_ratio": "Shot Touch %",
    "player_season_touches_inside_box_90": "Touches in Box",
    "player_season_xgbuildup_90": "xG Buildup",
    "player_season_op_xa_90": "OP XG ASSISTED",
    "player_season_pressured_passing_ratio": "PR. Pass %",
    "player_season_da_aggressive_distance": "GK AGGRESSIVE DIST",
    "player_season_clcaa": "CLAIMS %",
    "player_season_gsaa_ratio": "SHOT STOPPING %",
    "player_season_gsaa_90": "GSAA",
    "player_season_save_ratio": "SAVE %",
    "player_season_xs_ratio": "XSV %",
    "player_season_positive_outcome_score": "POSITIVE OUTCOME",
    "player_season_obv_gk_90": "GOALKEEPER OBV",
    "player_season_forward_pass_ratio": "Pass Forward %",
    "player_season_forward_pass_proportion": "Pass Forward %",
    "player_season_scoring_contribution_90": "Scoring Contribution",
    "player_season_fouls_won_90": "Fouls Won",
    "player_season_pressures_90": "Pressures",
    "player_season_counterpressures_90": "Counterpressures",
    "player_season_aggressive_actions_90": "Aggressive Actions"
}

# ------------------- Z-SCORE PROFILES -------------------
PROFILES = {
    # --- Centre Forward ---
    "Target Man": {
        "raw_positions": ["Centre Forward", "Right Centre Forward", "Left Centre Forward"],
        "statsbomb_metrics": ["player_season_aerial_ratio", "player_season_touches_inside_box_90"],
        "wyscout_metrics": ["Aerial duels per 90", "Aerial duels won, %", "Touches in box per 90"]
    },
    "Pressing Forward": {
        "raw_positions": ["Centre Forward", "Right Centre Forward", "Left Centre Forward"],
        "statsbomb_metrics": ["player_season_padj_pressures_90", "player_season_counterpressures_90"],
        "wyscout_metrics": ["Dribbles per 90", "Accelerations per 90", "Progressive runs per 90", "Duels per 90"]
    },
    "Poacher": {
        "raw_positions": ["Centre Forward", "Right Centre Forward", "Left Centre Forward"],
        "statsbomb_metrics": ["player_season_np_xg_per_shot", "player_season_shot_touch_ratio",
                              "player_season_shot_on_target_ratio", "player_season_touches_inside_box_90"],
        "wyscout_metrics": ["Shots on target, %", "xG per 90", "Touches in box per 90"]
    },
    # --- Centre Back ---
    "No Nonsense CB": {
        "raw_positions": ["Centre Back", "Right Centre Back", "Left Centre Back"],
        "statsbomb_metrics": ["player_season_aerial_ratio", "player_season_padj_clearances_90",
                              "player_season_blocks_per_shot", "player_season_obv_defensive_action_90",
                              "player_season_defensive_action_regains_90"],
        "wyscout_metrics": ["Defensive duels per 90", "Defensive duels won %", "Aerial duels per 90", "Aerial duels won %"]
    },
    "Outside CB": {
        "raw_positions": ["Centre Back", "Right Centre Back", "Left Centre Back"],
        "statsbomb_metrics": ["player_season_dribbles_90", "player_season_carries_90", "player_season_op_passes_into_box_90"],
        "wyscout_metrics": ["Dribbles per 90", "Progressive runs per 90", "Passes to final third per 90"]
    },
    "Ball Playing CB": {
        "raw_positions": ["Centre Back", "Right Centre Back", "Left Centre Back"],
        "statsbomb_metrics": ["player_season_op_passes_into_box_90", "player_season_pressured_passing_ratio",
                              "player_season_obv_pass_90", "player_season_passing_ratio"],
        "wyscout_metrics": ["Passes per 90", "Progressive passes per 90", "Accurate passes %", "Received passes per 90"]
    },
    # --- Full Back ---
    "Defensive FB": {
        "raw_positions": ["Left Back", "Left Wing Back", "Right Back", "Right Wing Back"],
        "statsbomb_metrics": ["player_season_aerial_ratio", "player_season_obv_defensive_action_90",
                              "player_season_ball_recoveries_90", "player_season_defensive_action_regains_90"],
        "wyscout_metrics": ["Aerial duels won %", "Defensive duels won %", "Duels won %"]
    },
    "Progressive WB": {
        "raw_positions": ["Left Back", "Left Wing Back", "Right Back", "Right Wing Back"],
        "statsbomb_metrics": ["player_season_carries_90", "player_season_dribbles_90",
                              "player_season_op_xa_90", "player_season_crossing_ratio"],
        "wyscout_metrics": ["Progressive passes per 90", "Crosses per 90", "xA per 90", "Passes to penalty area per 90",
                            "Dribbles per 90", "Progressive runs per 90"]
    },
    # --- Centre Midfield ---
    "Ball Playing 6": {
        "raw_positions": ["Left Defensive Midfielder", "Centre Defensive Midfielder", "Right Defensive Midfielder",
                          "Left Centre Midfielder", "Centre Midfielder", "Right Centre Midfielder"],
        "statsbomb_metrics": ["player_season_op_passes_into_box_90", "player_season_pressured_passing_ratio",
                              "player_season_obv_pass_90", "player_season_passing_ratio", "player_season_xgbuildup_90"],
        "wyscout_metrics": ["Progressive passes per 90", "Received passes per 90", "Passes per 90"]
    },
    "Destroyer 6": {
        "raw_positions": ["Left Defensive Midfielder", "Centre Defensive Midfielder", "Right Defensive Midfielder",
                          "Left Centre Midfielder", "Centre Midfielder", "Right Centre Midfielder"],
        "statsbomb_metrics": ["player_season_aerial_ratio", "player_season_obv_defensive_action_90",
                              "player_season_defensive_action_regains_90", "player_season_padj_interceptions_90",
                              "player_season_padj_tackles_90", "player_season_ball_recoveries_90"],
        "wyscout_metrics": ["Interceptions per 90", "Duels won %", "Defensive duels won", "Aerial duels won %"]
    },
    "Box to Box 8": {
        "raw_positions": ["Left Defensive Midfielder", "Centre Defensive Midfielder", "Right Defensive Midfielder",
                          "Left Centre Midfielder", "Centre Midfielder", "Right Centre Midfielder"],
        "statsbomb_metrics": ["player_season_padj_interceptions_90", "player_season_touches_inside_box_90",
                              "player_season_deep_progressions_90", "player_season_dribble_faced_ratio"],
        "wyscout_metrics": ["Touches in box per 90", "Duels per 90", "Interceptions per 90", "Passes to final third per 90"]
    },
    "Creative 8": {
        "raw_positions": ["Left Defensive Midfielder", "Centre Defensive Midfielder", "Right Defensive Midfielder",
                          "Left Centre Midfielder", "Centre Midfielder", "Right Centre Midfielder"],
        "statsbomb_metrics": ["player_season_op_key_passes_90", "player_season_op_xa_90", "player_season_carries_90"],
        "wyscout_metrics": ["Progressive runs per 90", "Key passes per 90", "Progressive passes per 90"]
    },
    "Aerial 8": {
        "raw_positions": ["Left Defensive Midfielder", "Centre Defensive Midfielder", "Right Defensive Midfielder",
                          "Left Centre Midfielder", "Centre Midfielder", "Right Centre Midfielder"],
        "statsbomb_metrics": ["player_season_aerial_ratio", "player_season_carries_90"],
        "wyscout_metrics": ["Aerial duels won %", "Progressive runs per 90"]
    },
    "Creative 10": {
        "raw_positions": ["Left Centre Midfielder", "Centre Midfielder", "Right Centre Midfielder",
                          "Left Attacking Midfielder", "Centre Attacking Midfielder", "Right Attacking Midfielder"],
        "statsbomb_metrics": ["player_season_op_key_passes_90", "player_season_op_xa_90", "player_season_obv_dribble_carry_90"],
        "wyscout_metrics": ["Key passes per 90", "xA per 90", "Progressive passes per 90"]
    },
    "Goal Threat 10": {
        "raw_positions": ["Left Centre Midfielder", "Centre Midfielder", "Right Centre Midfielder",
                          "Left Attacking Midfielder", "Centre Attacking Midfielder", "Right Attacking Midfielder"],
        "statsbomb_metrics": ["player_season_np_xg_90", "player_season_np_shots_90",
                              "player_season_scoring_contribution_90", "player_season_obv_shot_90"],
        "wyscout_metrics": ["Shots per 90", "Touches in box per 90", "Shots on target %", "xG per 90"]
    },
    # --- Wingers ---
    "Direct Winger": {
        "raw_positions": ["Left Midfielder", "Left Winger", "Right Midfielder", "Right Wing"],
        "statsbomb_metrics": ["player_season_dribbles_90", "player_season_dribble_ratio",
                              "player_season_carries_90", "player_season_carries_90", "player_season_crossing_ratio"],
        "wyscout_metrics": ["Dribbles per 90", "Accelerations per 90", "Crosses per 90", "Successful dribbles %"]
    },
    "Goal Threat Winger": {
        "raw_positions": ["Left Midfielder", "Left Winger", "Right Midfielder", "Right Wing"],
        "statsbomb_metrics": ["player_season_np_xg_90", "player_season_np_shots_90",
                              "player_season_scoring_contribution_90", "player_season_obv_shot_90"],
        "wyscout_metrics": ["Shots per 90", "Dribbles per 90", "xG per 90"]
    }
}

# ------------------- SIDEBAR -------------------
data_source = st.sidebar.radio("Select Data Source", ["Wyscout Upload", "StatsBomb API"])

# ------------------- WYSCOOUT -------------------
if data_source == "Wyscout Upload":
    st.header("Wyscout Data Upload")
    wyscout_file = st.file_uploader("Upload Wyscout Excel file", type=['xlsx'])
    profile = st.selectbox("Select Z-Score Profile", list(PROFILES.keys()))
    min_minutes = st.slider("Minimum Minutes Played", 0, 2000, 500, 50)

    if wyscout_file and st.button("Run Z-Score Analysis (Wyscout)"):
        df = pd.read_excel(wyscout_file)
        df_filt = df[df['Minutes played'] > min_minutes]
        df_filt = df_filt[df_filt['Position'].isin(PROFILES[profile]['raw_positions'])]
        metrics = PROFILES[profile]['wyscout_metrics']

        z_df = df_filt[['Player', 'Team within selected timeframe', 'Age', 'Minutes played'] + metrics].copy()
        for m in metrics:
            if m in z_df:
                z_df[m + ' (z)'] = (z_df[m] - z_df[m].mean()) / (z_df[m].std(ddof=0) + 1e-8)

        z_cols = [m + ' (z)' for m in metrics if m + ' (z)' in z_df]
        z_df['Profile Z-Score'] = z_df[z_cols].mean(axis=1)
        z_df = z_df.sort_values('Profile Z-Score', ascending=False).head(10)

        st.dataframe(z_df[['Player', 'Team within selected timeframe', 'Age', 'Profile Z-Score']].rename(
            columns={'Team within selected timeframe': 'Team'}))
        st.caption("Top 10 players for selected profile (Z-Score based)")

# ------------------- STATSBOMB -------------------
elif data_source == "StatsBomb API":
    st.header("StatsBomb API")
    profile = st.selectbox("Select Z-Score Profile", list(PROFILES.keys()))
    min_minutes = st.slider("Minimum Minutes Played", 0, 2000, 500, 50)

    try:
        creds = {"user": STATSBOMB_USER, "passwd": STATSBOMB_PASS}
        all_comps = sb.competitions(creds=creds)
        comp_options = all_comps[['competition_name', 'season_name', 'competition_id', 'season_id']]
        comp_options['label'] = comp_options['competition_name'] + " - " + comp_options['season_name']

        comp = st.selectbox("Select Competition/Season", comp_options['label'])
        comp_row = comp_options[comp_options['label'] == comp].iloc[0]

        if st.button("Run Z-Score Analysis (StatsBomb)"):
            player_season = sb.player_season_stats(
                competition_id=comp_row['competition_id'],
                season_id=comp_row['season_id'],
                creds=creds
            )

            # Convert age
            if 'birth_date' in player_season.columns:
                today = pd.to_datetime("today")
                player_season['Age'] = pd.to_datetime(player_season['birth_date']).apply(lambda x: today.year - x.year)
            else:
                player_season['Age'] = 0

            df_filt = player_season[
                player_season['primary_position'].isin(PROFILES[profile]['raw_positions']) &
                (player_season['player_season_minutes'] > min_minutes)
            ]
            metrics = PROFILES[profile]['statsbomb_metrics']

            z_df = df_filt[['player_name', 'team_name', 'Age', 'player_season_minutes'] + 
                            [m for m in metrics if m in df_filt.columns]].copy()
            for m in metrics:
                if m in z_df:
                    z_df[m + ' (z)'] = (z_df[m] - z_df[m].mean()) / (z_df[m].std(ddof=0) + 1e-8)

            z_cols = [m + ' (z)' for m in metrics if m + ' (z)' in z_df]
            if not z_cols:
                st.error("None of the required metrics for this profile are available in the StatsBomb data.")
            else:
                z_df['Profile Z-Score'] = z_df[z_cols].mean(axis=1)
                z_df = z_df.sort_values('Profile Z-Score', ascending=False).head(10)

                st.dataframe(z_df[['player_name', 'team_name', 'Age', 'Profile Z-Score']].rename(
                    columns={'player_name': 'Player', 'team_name': 'Team', 'player_season_minutes': 'Minutes'}
                ))
                st.caption("Top 10 players for selected profile (Z-Score based)")

            # ------------------- XG OUTPERFORMANCE -------------------
            st.subheader("Centre Forwards: xG Outperformance")
            cf_positions = ["Centre Forward", "Right Centre Forward", "Left Centre Forward"]
            cf_df = player_season[
                player_season['primary_position'].isin(cf_positions) &
                (player_season['player_season_minutes'] > min_minutes)
            ]
            if all(col in cf_df.columns for col in ["player_season_npg_90", "player_season_np_xg_90"]):
                cf_df['xG Diff'] = cf_df['player_season_npg_90'] - cf_df['player_season_np_xg_90']
                top10_xg = cf_df.sort_values('xG Diff', ascending=False).head(10)
                st.dataframe(top10_xg[['player_name', 'team_name', 'Age', 'player_season_np_xg_90', 'player_season_npg_90', 'xG Diff']].rename(
                    columns={'player_name': 'Player', 'team_name': 'Team',
                             'player_season_np_xg_90': 'xG', 'player_season_npg_90': 'NP Goals'}
                ))
            else:
                st.info("Required metrics for xG outperformance not available.")

    except Exception as e:
        st.error(f"Failed to fetch or process StatsBomb data: {e}")
