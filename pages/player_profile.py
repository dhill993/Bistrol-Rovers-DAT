import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import os

# App config
st.set_page_config(page_title="Player Profile View", layout="wide", initial_sidebar_state="expanded")

# Custom dark background
st.markdown("""
    <style>
    body {
        background-color: #121212;
        color: white;
    }
    .main {
        background-color: #121212;
    }
    div[data-testid="stMetricValue"] {
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- Load Wyscout data ---
@st.cache_data
def load_data():
    folder = "./data/wyscout_data"
    dfs = []
    for file in os.listdir(folder):
        if file.endswith(".xlsx"):
            df = pd.read_excel(os.path.join(folder, file))
            league = file.split("_")[0]
            df["League"] = league
            dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

df = load_data()

# --- Position mapping ---
position_mapping = {
    "RWB": "Full Back", "RB": "Full Back", "LWB": "Full Back", "LB": "Full Back",
    "LCB": "Centre Back", "RCB": "Centre Back", "CB": "Centre Back",
    "RCMF": "Number 6", "LCMF": "Number 6", "DMF": "Number 6", "LDMF": "Number 6", "RDFM": "Number 6",
    "AMF": "Attacking Midfielder", "CMF": "Number 6",
    "LW": "Winger", "RW": "Winger", "LWF": "Winger", "RWF": "Winger",
    "CF": "Centre Forward", "ST": "Centre Forward", "GK": "Goal Keeper"
}
df["Mapped Position"] = df["Position"].map(position_mapping)
df.dropna(subset=["Mapped Position"], inplace=True)

# --- Sidebar filters ---
player = st.sidebar.selectbox("Select Player", sorted(df["Player"].unique()))
player_row = df[df["Player"] == player].iloc[0]
position_group = player_row["Mapped Position"]

st.sidebar.markdown(f"**Position Group:** {position_group}")
filtered_df = df[df["Mapped Position"] == position_group]

# --- Define key metrics per position group ---
position_metrics = {
    "Centre Forward": ["Goals per 90", "xG per 90", "Shots per 90", "Touches in box per 90", "Offensive duels won %"],
    "Winger": ["Dribbles per 90", "Progressive runs per 90", "Crosses per 90", "Touches in box per 90", "Assists per 90"],
    "Number 6": ["Interceptions per 90", "Duels per 90", "Passes per 90", "Progressive passes per 90", "xA per 90"],
    "Full Back": ["Crosses per 90", "Dribbles per 90", "Defensive duels per 90", "Interceptions per 90", "Progressive runs per 90"],
    "Centre Back": ["Aerial duels won %", "Defensive duels won %", "Interceptions per 90", "Passes per 90", "Duels per 90"],
    "Goal Keeper": ["Save rate (%)", "Clean sheets", "Prevented goals per 90"]
}

metrics = [m for m in position_metrics.get(position_group, []) if m in df.columns]

# --- Calculate percentiles ---
percentile_df = filtered_df[metrics].rank(pct=True) * 100
player_percentiles = percentile_df.loc[df[df["Player"] == player].index].iloc[0]

# --- Color function ---
def color_picker(pct):
    if pct >= 70:
        return "#28a745"  # green
    elif pct >= 50:
        return "#ffc107"  # amber
    else:
        return "#dc3545"  # red

# --- Plot function ---
def draw_percentile_bars(player_name, metrics, percentiles):
    fig, ax = plt.subplots(figsize=(10, 6), facecolor="#121212")
    ax.set_facecolor("#121212")
    ax.tick_params(axis='y', colors='white')
    ax.tick_params(axis='x', colors='white')

    y_pos = np.arange(len(metrics))
    bars = ax.barh(y_pos, percentiles, color=[color_picker(p) for p in percentiles], height=0.6, edgecolor="white")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(metrics, fontsize=12, color="white")
    ax.set_xlim(0, 100)
    ax.set_xlabel("Percentile", fontsize=12, color="white")
    ax.set_title(f"{player_name} - {position_group}", fontsize=16, color="white", loc='left')

    for i, bar in enumerate(bars):
        ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2,
                f"{percentiles[i]:.0f}%", va='center', ha='left', color='white', fontsize=12)

    plt.tight_layout()
    return fig

# --- Header / Profile Info ---
col1, col2 = st.columns([1, 3])
with col1:
    st.markdown(f"### **{player_row['Player']}**")
    st.markdown(f"**Team**: {player_row.get('Team within selected timeframe', 'N/A')}")
    st.markdown(f"**League**: {player_row.get('League', '')}")
    st.markdown(f"**Position**: {position_group}")
    st.markdown(f"**Age**: {player_row.get('Age', 'N/A')}")
    st.markdown(f"**Minutes Played**: {int(player_row.get('Minutes played', 0))}")

with col2:
    fig = draw_percentile_bars(player, metrics, player_percentiles[metrics].values)
    st.pyplot(fig)
