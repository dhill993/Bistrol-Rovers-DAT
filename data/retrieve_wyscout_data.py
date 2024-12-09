import pandas as pd
import numpy as np
import streamlit as st
import os

data_path = './data/wyscout_data/'
position_mapping = {
    "RWB": "Full Back",
    "RB": "Full Back",
    "LWB": "Full Back",
    "LB": "Full Back",
    "LCB": "Centre Back",
    "RCB": "Centre Back",
    "RCMF": "Number 6",
    "LCMF": "Number 6",
    "LDMF": "Number 6",
    "RDFM": "Number 6",
    "DMF": "Number 6",
    "AMF": "Number 8",
    "RAMF": "Number 8",
    "LAMF": "Number 8",
    "LW": "Winger",
    "RW": "Winger",
    "RWF": "Winger",
    "LWF": "Winger",
    "CF": "Centre Forward",
    "RAMF": "Winger",
    "LAFM": "Winger"
}


# Original column names
original_columns = [
    "Player",
    "Team within selected timeframe",
    "Position",
    "Age",
    "Market value",
    "Contract expires",
    "Matches played",
    "Minutes played",
    "Goals",
    "xG",
    "Assists",
    "xA",
    "Duels per 90",
    "Duels won, %",
    "Birth country",
    "Passport country",
    "Foot",
    "Height",
    "Weight",
    "On loan",
    "Successful defensive actions per 90",
    "Defensive duels per 90",
    "Defensive duels won, %",
    "Aerial duels per 90",
    "Aerial duels won, %",
    "Sliding tackles per 90",
    "PAdj Sliding tackles",
    "Shots blocked per 90",
    "Interceptions per 90",
    "PAdj Interceptions",
    "Fouls per 90",
    "Yellow cards",
    "Yellow cards per 90",
    "Red cards",
    "Red cards per 90",
    "Successful attacking actions per 90",
    "Goals per 90",
    "Non-penalty goals",
    "Non-penalty goals per 90",
    "xG per 90",
    "Head goals",
    "Head goals per 90",
    "Shots",
    "Shots per 90",
    "Shots on target, %",
    "Goal conversion, %",
    "Assists per 90",
    "Crosses per 90",
    "Accurate crosses, %",
    "Dribbles per 90",
    "Successful dribbles, %",
    "Offensive duels per 90",
    "Offensive duels won, %",
    "Touches in box per 90",
    "Progressive runs per 90",
    "Accelerations per 90",
    "Passes per 90",
    "Accurate passes, %",
    "Forward passes per 90",
    "Accurate forward passes, %",
    "Back passes per 90",
    "Accurate back passes, %",
    "Lateral passes per 90",
    "Accurate lateral passes, %",
    "Long passes per 90",
    "Accurate long passes, %",
    "Average pass length, m",
    "Average long pass length, m",
    "xA per 90",
    "Shot assists per 90",
    "Second assists per 90",
    "Third assists per 90",
    "Smart passes per 90",
    "Accurate smart passes, %",
    "Key passes per 90",
    "Passes to final third per 90",
    "Accurate passes to final third, %",
    "Passes to penalty area per 90",
    "Accurate passes to penalty area, %",
    "Through passes per 90",
    "Accurate through passes, %",
    "Deep completions per 90",
    "Deep completed crosses per 90",
    "Progressive passes per 90",
    "Accurate progressive passes, %"
]

# Desired column names
desired_columns = [
    "Player Name",
    "Team",
    "Position",
    "Age",
    "Market value",
    "Contract expires",
    "Matches played",
    "Minutes",
    "GOALS",
    "xG",
    "ASSISTS",
    "xA",
    "DUELS PER 90",
    "DUELS WON %",
    "Birth country",
    "Passport country",
    "Foot",
    "Height",
    "Weight",
    "On loan",
    "SUCCESSFUL DEFENSIVE ACTIONS PER 90",
    "DEFENSIVE DUELS PER 90",
    "DEFENSIVE DUELS WON %",
    "AERIAL DUELS PER 90",
    "AERIAL DUELS WON %",
    "SLIDING TACKLES PER 90",
    "PADJ SLIDING TACKLES",
    "SHOTS BLOCKED PER 90",
    "INTERCEPTIONS PER 90",
    "PADJ INTERCEPTIONS",
    "FOULS PER 90",
    "Yellow cards",
    "Yellow cards per 90",
    "Red cards",
    "Red cards per 90",
    "SUCCESSFUL ATTACKING ACTIONS PER 90",
    "GOALS PER 90",
    "Non-penalty goals",
    "NON PENALTY GOALS PER 90",
    "xG PER 90",
    "Head goals",
    "Head goals per 90",
    "SHOTS",
    "SHOTS PER 90",
    "SHOTS ON TARGET %",
    "GOAL CONVERSION %",
    "ASSISTS PER 90",
    "CROSSES PER 90",
    "ACCURATE CROSSES %",
    "DRIBBLES PER 90",
    "SUCCESSFUL DRIBBLES %",
    "OFFENSIVE DUELS PER 90",
    "OFFENSIVE DUELS WON %",
    "TOUCHES IN BOX PER 90",
    "PROGRESSIVE RUNS PER 90",
    "ACCELERATIONS PER 90",
    "PASSES PER 90",
    "ACCURATE PASSES %",
    "FORWARD PASSES PER 90",
    "ACCURATE FORWARD PASSES %",
    "BACK PASSES PER 90",
    "ACCURATE BACK PASSES %",
    "LATERAL PASSES PER 90",
    "ACCURATE LATERAL PASSES %",
    "LONG PASSES PER 90",
    "ACCURATE LONG PASSES %",
    "AVERAGE PASS LENGTH",
    "AVERAGE LONG PASS LENGTH",
    "xA PER 90",
    "SHOT ASSISTS PER 90",
    "SECOND ASSISTS PER 90",
    "THIRD ASSISTS PER 90",
    "SMART PASSES PER 90",
    "ACCURATE SMART PASSES %",
    "KEY PASSES PER 90",
    "PASSES TO FINAL THIRD PER 90",
    "ACCURATE PASSES TO FINAL THIRD %",
    "PASSES TO PENALTY AREA PER 90",
    "ACCURATE PASSES TO PENALTY AREA %",
    "THROUGH PASSES PER 90",
    "ACCURATE THROUGH PASSES %",
    "DEEP COMPLETIONS PER 90",
    "DEEP COMPLETED CROSSES per 90",
    "PROGRESSIVE PASSES PER 90",
    "ACCURATE PROGRESSIVE PASSES %"
]

# Create the mapping
df_mapping = dict(zip(original_columns, desired_columns))

@st.cache_data(ttl=86400,show_spinner=False)
def get_wyscout_player_season_stats(folder_path=data_path):
    all_data = []
    
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.xlsx'):  # Check if it's an .xlsx file
            # Extract league and season from the filename
            parts = filename.split(' ', 2)  # Split from the left into at most 3 parts
            league = parts[0] + " " + parts[1]  # Combine the first two parts for the league name
            season = parts[2].split('.')[0]  # Take the third part and remove the extension
            # Read the file into a DataFrame
            file_path = os.path.join(folder_path, filename)
            df = read_transform_individual_files(file_path)
            
            # Add league and season columns
            df['League'] = league
            df['Season'] = season
            
            # Append the DataFrame to the list
            all_data.append(df)
    
    # Concatenate all DataFrames
    combined_df = pd.concat(all_data, ignore_index=True)
    return combined_df

def read_transform_individual_files(file_path):
    data = pd.read_excel(file_path)
    data["Position"] = data["Position"].str.split(", ").str[0]
    data['Position'] = data['Position'].map(position_mapping)
    data = data.dropna(subset=['Position'])
    data = data.replace([np.nan, 'NaN', 'None', '', 'nan', 'null'], 0)
    data = data.apply(pd.to_numeric, errors='ignore')

    data.rename(columns=df_mapping, inplace=True)
    return data
