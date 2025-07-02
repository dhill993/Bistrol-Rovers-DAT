import pandas as pd  
from datetime import datetime  
import numpy as np  
from statsbombpy import sb  
import streamlit as st  
  
# --- Position Mapping (FIXED) ---  
position_mapping = {  
    # Full Backs  
    "Full Back": "Full Back", "Left Back": "Full Back", "Right Back": "Full Back",  
    "Left Wing Back": "Full Back", "Right Wing Back": "Full Back",  
  
    # Centre Backs (FIXED - both map to Centre Back)  
    "Centre Back": "Centre Back", "Left Centre Back": "Centre Back", "Right Centre Back": "Centre Back",  
    "Outside Centre Back": "Centre Back",  
  
    # Number 6s  
    "Number 6": "Number 6", "Left Defensive Midfielder": "Number 6", "Right Defensive Midfielder": "Number 6",  
    "Defensive Midfielder": "Number 6", "Centre Defensive Midfielder": "Number 6",  
    "Left Centre Midfield": "Number 6", "Left Centre Midfielder": "Number 6",  
    "Right Centre Midfield": "Number 6", "Right Centre Midfielder": "Number 6", "Centre Midfield": "Number 6",  
  
    # Number 8s (FIXED - removed duplicates)  
    "Number 8": "Number 8",  
    "Left Attacking Midfield": "Number 8", "Right Attacking Midfield": "Number 8",  
    "Right Attacking Midfielder": "Number 8", "Attacking Midfield": "Number 8",  
  
    # Number 10s  
    "Secondary Striker": "Number 10", "Centre Attacking Midfielder": "Number 10", "Left Attacking Midfielder": "Number 10",  
  
    # Wingers  
    "Winger": "Winger", "Right Midfielder": "Winger", "Left Midfielder": "Winger",  
    "Left Wing": "Winger", "Right Wing": "Winger",  
  
    # Centre Forward A (FIXED - separate mapping)  
    "Centre Forward": "Centre Forward A",  
    "Left Centre Forward": "Centre Forward A",  
    "Right Centre Forward": "Centre Forward A",  
      
    # Goalkeeper  
    "Goalkeeper": "Goal Keeper"  
}  
  
# --- Statbomb Metrics Required (COMPLETE LIST) ---  
statbomb_metrics_needed = [  
    'player_name', 'team_name', 'season_name', 'competition_name', 'Age',  
    'player_season_minutes', 'primary_position', "player_season_aerial_ratio",  
    "player_season_ball_recoveries_90", "player_season_blocks_per_shot", "player_season_carries_90",  
    "player_season_counterpressures_90", "player_season_crosses_90", "player_season_dribbles_90",  
    "player_season_fouls_won_90", "player_season_goals_90", "player_season_np_goals_90",  
    "player_season_op_passes_into_box_90", "player_season_padj_clearances_90", "player_season_padj_interceptions_90",  
    "player_season_padj_pressures_90", "player_season_padj_tackles_90", "player_season_passing_ratio",  
    "player_season_shot_on_target_ratio", "player_season_shot_touch_ratio", "player_season_touches_inside_box_90",  
    "player_season_xgbuildup_90", "player_season_op_xa_90", "player_season_pressured_passing_ratio",  
    'player_season_da_aggressive_distance', 'player_season_clcaa', 'player_season_gsaa_ratio',  
    'player_season_gsaa_90', 'player_season_save_ratio', 'player_season_xs_ratio',  
    'player_season_positive_outcome_score', 'player_season_obv_gk_90', 'player_season_pressures_90',  
    'player_season_aggressive_actions_90'  
]  
  
# --- Metrics Mapping (COMPLETE WITH LEAGUE FIX) ---  
metrics_mapping = {  
    'player_name': 'Player', 'team_name': 'Team', 'season_name': 'Season',  
    'competition_name': 'League', 'player_season_minutes': 'Minutes',  
    'primary_position': 'Position', 'player_season_aerial_ratio': 'Aerial %',  
    'player_season_ball_recoveries_90': 'Ball Recoveries', 'player_season_blocks_per_shot': 'Blocks per Shot',  
    'player_season_carries_90': 'Carries', 'player_season_counterpressures_90': 'Counterpressures',  
    'player_season_crosses_90': 'Crosses', 'player_season_dribbles_90': 'Dribbles',  
    'player_season_fouls_won_90': 'Fouls Won', 'player_season_goals_90': 'Goals',  
    'player_season_np_goals_90': 'NP Goals', 'player_season_op_passes_into_box_90': 'OP Passes Into Box',  
    'player_season_padj_clearances_90': 'PADJ Clearances', 'player_season_padj_interceptions_90': 'PADJ Interceptions',  
    'player_season_padj_pressures_90': 'PADJ Pressures', 'player_season_padj_tackles_90': 'PADJ Tackles',  
    'player_season_passing_ratio': 'Passing %', 'player_season_shot_on_target_ratio': 'Shooting %',  
    'player_season_shot_touch_ratio': 'Shot Touch %', 'player_season_touches_inside_box_90': 'Touches in Box',  
    'player_season_xgbuildup_90': 'xG Buildup', 'player_season_op_xa_90': 'OP XG ASSISTED',  
    'player_season_pressured_passing_ratio': 'PR. Pass %', 'player_season_da_aggressive_distance': 'GK AGGRESSIVE DIST',  
    'player_season_clcaa': 'CLAIMS %', 'player_season_gsaa_ratio': 'SHOT STOPPING %',  
    'player_season_gsaa_90': 'GSAA', 'player_season_save_ratio': 'SAVE %',  
    'player_season_xs_ratio': 'XSV %', 'player_season_positive_outcome_score': 'POSITIVE OUTCOME',  
    'player_season_obv_gk_90': 'GOALKEEPER OBV', 'player_season_pressures_90': 'Pressures',  
    'player_season_aggressive_actions_90': 'Aggressive Actions'  
}  
  
# --- Data Load Function (FIXED WITH LEAGUE) ---  
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
  
            # Subset only available cols  
            available_cols = [col for col in statbomb_metrics_needed if col in df.columns]  
            df = df[available_cols]  
  
            df = df.replace([np., '', 'None', '', '', 'null'], 0)  
            df = df.apply(pd.to_numeric, errors='ignore')  
  
            # Rename columns using metrics mapping  
            df.rename(columns={k: v for k, v in metrics_mapping.items() if k in df.columns}, inplace=True)  
  
            # Apply position mapping  
            if 'Position' in df.columns:  
                df['Position'] = df['Position'].map(position_mapping)  
  
            # Remove rows with unmapped positions  
            df = df.dropna(subset=['Position'])  
            df = df[df['Minutes'] >= 600]  
            df['Minutes'] = df['Minutes'].astype(int)  
  
            # FIXED: Handle missing columns gracefully  
            if 'NP Goals' in df.columns and 'OP XG ASSISTED' in df.columns:  
                df['Scoring Contribution'] = df['NP Goals'] + df['OP XG ASSISTED']  
            elif 'NP Goals' in df.columns:  
                df['Scoring Contribution'] = df['NP Goals']  
            else:  
                df['Scoring Contribution'] = 0  
  
            if 'Passing %' in df.columns:  
                df['Pass Forward %'] = df['Passing %'] * 0.6  
  
            # FIXED: Add missing columns with default values if they don't exist  
            required_display_cols = ['Fouls Won', 'Pressures', 'Counterpressures', 'Aggressive Actions']  
            for col in required_display_cols:  
                if col not in df.columns:  
                    df[col] = 0  
  
            dataframes.append(df)  
  
        except Exception as e:  
            print(f"Error processing competition {row.get('competition_name', 'Unknown')}: {e}")  
  
    final_df = pd.concat(dataframes, ignore_index=True)  
      
    # FIXED: Create Centre Forward B as a copy of Centre Forward A data  
    cf_a_data = final_df[final_df['Position'] == 'Centre Forward A'].copy()  
    if not cf_a_data.empty:  
        cf_b_data = cf_a_data.copy()  
        cf_b_data['Position'] = 'Centre Forward B'  
        final_df = pd.concat([final_df, cf_b_data], ignore_index=True)  
      
    return final_df  
  
# Load the data  
statsbomb_data = get_statsbomb_player_season_stats()  
  
# Now you can access the League column  
leagues = list(statsbomb_data['League'].unique())  
