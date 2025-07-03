import pandas as pd
import numpy as np
from datetime import datetime
from statsbombpy import sb
import streamlit as st

# List of metrics you want to retrieve — make sure to include all needed stats, including new ones
statbomb_metrics_needed = [
    # Add all your metrics here — example:
    'Player',
    'Position',
    'Minutes',
    'birth_date',
    'NP Goals',
    'Shots',
    'Shooting %',
    'xG',
    'xG/Shot',
    'Shot Touch %',
    'Touches in Box',
    'Carries',
    'Shot OBV',
    'Fouls Won',
    'Pressures',
    'Counterpressures',
    'Aggressive Actions',
    'Aerial Win %',
    'Dribbles Stopped %',
    'PADJ Tackles',
    'PADJ Interceptions',
    'PR. Pass %',
    'Successful Crosses',
    'OP Passes Into Box',
    'OP F3 Passes',
    # Add any others you need here...
]

# Mapping raw API column names to friendly names (adjust as needed)
metrics_mapping = {
    # Example mappings - update as per your metric keys
    'player_season_np_goals': 'NP Goals',
    'player_season_shots': 'Shots',
    'player_season_shooting_percentage': 'Shooting %',
    'player_season_xg': 'xG',
    'player_season_xg_per_shot': 'xG/Shot',
    'player_season_shot_touch_percentage': 'Shot Touch %',
    'player_season_touches_in_box': 'Touches in Box',
    'player_season_carries': 'Carries',
    'player_season_shot_obv': 'Shot OBV',
    'player_season_fouls_won': 'Fouls Won',
    'player_season_pressures': 'Pressures',
    'player_season_counterpressures': 'Counterpressures',
    'player_season_aggressive_actions': 'Aggressive Actions',
    'player_season_aerial_win_percentage': 'Aerial Win %',
    'player_season_dribbles_stopped_percentage': 'Dribbles Stopped %',
    'player_season_padjtackles': 'PADJ Tackles',
    'player_season_padjinterceptions': 'PADJ Interceptions',
    'player_season_pr_pass_percentage': 'PR. Pass %',
    'player_season_successful_crosses': 'Successful Crosses',
    'player_season_op_passes_into_box': 'OP Passes Into Box',
    'player_season_op_f3_passes': 'OP F3 Passes',
    # Add others accordingly...
}

# Mapping raw positions to generic categories (will override CF and CB later)
position_mapping = {
    "Full Back": "Full Back", "Left Back": "Full Back", "Right Back": "Full Back",
    "Left Wing Back": "Full Back", "Right Wing Back": "Full Back",

    "Centre Back": "Centre Back", "Left Centre Back": "Centre Back", "Right Centre Back": "Centre Back",

    "Number 6": "Number 6", "Left Defensive Midfielder": "Number 6", "Right Defensive Midfielder": "Number 6",
    "Defensive Midfielder": "Number 6", "Centre Defensive Midfielder": "Number 6",
    "Left Centre Midfield": "Number 6", "Left Centre Midfielder": "Number 6",
    "Right Centre Midfield": "Number 6", "Right Centre Midfielder": "Number 6", "Centre Midfield": "Number 6",

    "Number 8": "Number 8", "Left Attacking Midfielder": "Number 8", "Right Attacking Midfielder": "Number 8",
    "Attacking Midfield": "Number 8",

    "Secondary Striker": "Number 10", "Centre Attacking Midfielder": "Number 10",

    "Winger": "Winger", "Right Midfielder": "Winger", "Left Midfielder": "Winger",
    "Left Wing": "Winger", "Right Wing": "Winger",

    "Goalkeeper": "Goal Keeper"
}


@st.cache_data(ttl=14400, show_spinner=False)
def get_statsbomb_player_season_stats():
    creds = {"user": st.secrets["user"], "passwd": st.secrets["passwd"]}
    all_comps = sb.competitions(creds=creds)
    dataframes = []

    def calculate_age(birth_date):
        today = datetime.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    for _, row in all_comps.iterrows():
        try:
            comp_id, season_id = row["competition_id"], row["season_id"]
            df = sb.player_season_stats(comp_id, season_id, creds=creds)

            # Calculate age
            df['birth_date'] = pd.to_datetime(df['birth_date'])
            df['Age'] = df['birth_date'].apply(calculate_age)

            # Filter to needed metrics + essential cols
            available_cols = [col for col in statbomb_metrics_needed if col in df.columns]
            df = df[available_cols + ['Player', 'Position', 'Minutes', 'birth_date']]

            # Clean and convert numeric
            df = df.replace([np.nan, 'NaN', 'None', '', 'nan', 'null'], 0)
            df = df.apply(pd.to_numeric, errors='ignore')

            # Rename columns to friendly names
            rename_map = {k: v for k, v in metrics_mapping.items() if k in df.columns}
            df.rename(columns=rename_map, inplace=True)

            # Positions to handle separately
            cf_positions = ["Centre Forward", "Left Centre Forward", "Right Centre Forward"]
            cb_positions = ["Centre Back", "Left Centre Back", "Right Centre Back"]

            # Split dataframe by positions
            df_cf = df[df['Position'].isin(cf_positions)].copy()
            df_cb = df[df['Position'].isin(cb_positions)].copy()
            df_other = df[~df['Position'].isin(cf_positions + cb_positions)].copy()

            # Duplicate CF for A and B profiles
            df_cf_a = df_cf.copy()
            df_cf_a['MappedPosition'] = 'Centre Forward A'

            df_cf_b = df_cf.copy()
            df_cf_b['MappedPosition'] = 'Centre Forward B'

            # Map CB rows to Outside Centre Back profile
            df_cb['MappedPosition'] = 'Outside Centre Back'

            # Map others normally via mapping dict
            df_other['MappedPosition'] = df_other['Position'].map(position_mapping)
            df_other = df_other.dropna(subset=['MappedPosition'])

            # Combine all processed dataframes
            combined_df = pd.concat([df_cf_a, df_cf_b, df_cb, df_other], ignore_index=True)

            # Filter players with >= 600 minutes
            combined_df = combined_df[combined_df['Minutes'] >= 600]
            combined_df['Minutes'] = combined_df['Minutes'].astype(int)

            dataframes.append(combined_df)

        except Exception as e:
            print(f"Error processing {row['competition_name']} {row['season_name']}: {e}")

    if not dataframes:
        return pd.DataFrame()

    return pd.concat(dataframes, ignore_index=True)
