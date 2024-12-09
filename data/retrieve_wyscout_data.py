import pandas as pd
import numpy as np
import streamlit as st

data_path = './data/wyscout_data.csv'

@st.cache_data(ttl=86400,show_spinner=False)
def get_wyscout_player_season_stats():
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
    }

    data = pd.read_csv(data_path)
    data["Position"] = data["Position"].str.split(", ").str[0]
    data['Position'] = data['Position'].map(position_mapping)
    data = data.dropna(subset=['Position'])
    data = data.replace([np.nan, 'NaN', 'None', '', 'nan', 'null'], 0)
    data = data.apply(pd.to_numeric, errors='ignore')

    data = data.rename(columns={"Player":"Player Name", "Minutes played":"Minutes", "Team within selected timeframe":"Team"})
    return data
