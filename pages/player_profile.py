import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os
from datetime import datetime
from statsbombpy import sb
from utilities.utils import get_player_metrics_percentile_ranks, get_weighted_score
from utilities.wyscout_default_metrics import metrics_per_position

st.set_page_config(page_title="Player Performance Dashboard", layout="wide")

# Bristol Rovers styling
st.markdown("""
<style>
    .main { background-color: #1e3a8a; color: white; }
    .stSelectbox > div > div { background-color: #3b82f6; color: white; border: 1px solid #60a5fa; }
    .stFileUploader > div { background-color: #3b82f6; border: 1px solid #60a5fa; }
    .metric-card {
        background-color: #16a34a; padding: 20px; border-radius: 10px;
        text-align: center; color: white; margin: 5px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3); border: 2px solid #22c55e;
    }
    .metric-title { font-size: 12px; font-weight: bold; margin-bottom: 5px; text-transform: uppercase; }
    .metric-value { font-size: 36px; font-weight: bold; }
    .filter-container { background-color: #1e40af; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
    .chart-container { background-color: #1e40af; padding: 15px; border-radius: 8px; }
    .league-section { background-color: #1e40af; padding: 20px; border-radius: 8px; margin: 15px 0; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_statsbomb_data():
    """Fetch StatsBomb data using API credentials"""
    try:
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
                df['League'] = row['competition_name']
                df['Season'] = row['season_name']
                
                dataframes.append(df)
            except Exception as e:
                continue
                
        return pd.concat(dataframes, ignore_index=True) if dataframes else pd.DataFrame()
    except Exception as e:
        st.error(f"StatsBomb API error: {e}")
        return pd.DataFrame()

@st.cache_data
def process_wyscout_files(uploaded_files):
    """Process uploaded Wyscout Excel files"""
    if not uploaded_files:
        return pd.DataFrame()
    
    dataframes = []
    for file in uploaded_files:
        try:
            df = pd.read_excel(file)
            # Standardize column names
            df.columns = df.columns.str.strip()
            dataframes.append(df)
        except Exception as e:
            st.error(f"Error processing {file.name}: {e}")
    
    return pd.concat(dataframes, ignore_index=True) if dataframes else pd.DataFrame()

# Data source selection
st.title("🎯 Player Performance Dashboard")

data_source = st.radio("Select Data Source:", ["StatsBomb API", "Wyscout Upload"], horizontal=True)

df = pd.DataFrame()

if data_source == "StatsBomb API":
    with st.spinner("Fetching StatsBomb data..."):
        df = get_statsbomb_data()
        
elif data_source == "Wyscout Upload":
    uploaded_files = st.file_uploader(
        "Upload Wyscout Excel files", 
        type=['xlsx', 'xls'], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        with st.spinner("Processing Wyscout files..."):
            df = process_wyscout_files(uploaded_files)

if df.empty:
    st.warning("No data available. Please select a data source and ensure proper configuration.")
    st.stop()

# League drill-down section
st.markdown("<div class='league-section'>", unsafe_allow_html=True)
st.subheader("🏆 League Analysis")

col1, col2, col3 = st.columns(3)

with col1:
    available_leagues = df['League'].dropna().unique() if 'League' in df.columns else ['All Leagues']
    selected_league = st.selectbox("Select League", ['All Leagues'] + list(available_leagues))

with col2:
    if selected_league != 'All Leagues':
        league_df = df[df['League'] == selected_league] if 'League' in df.columns else df
    else:
        league_df = df
    
    available_seasons = league_df['Season'].dropna().unique() if 'Season' in league_df.columns else ['All Seasons']
    selected_season = st.selectbox("Select Season", ['All Seasons'] + list(available_seasons))

with col3:
    if selected_season != 'All Seasons':
        filtered_df = league_df[league_df['Season'] == selected_season] if 'Season' in league_df.columns else league_df
    else:
        filtered_df = league_df
    
    st.metric("Players in Selection", len(filtered_df))

st.markdown("</div>", unsafe_allow_html=True)

# Main filters
with st.container():
    st.markdown("<div class='filter-container'>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        player_col = 'player_name' if 'player_name' in filtered_df.columns else 'Player'
        if player_col in filtered_df.columns:
            selected_player = st.selectbox("Player", filtered_df[player_col].dropna().sort_values().unique())
            player_data = filtered_df[filtered_df[player_col] == selected_player].iloc[0]
        else:
            st.error("Player column not found")
            st.stop()
    
    with col2:
        team_col = 'team_name' if 'team_name' in filtered_df.columns else 'Team'
        available_clubs = filtered_df[team_col].dropna().unique() if team_col in filtered_df.columns else ['N/A']
        selected_club = st.selectbox("Club", available_clubs)
    
with col3:
    possible_position_cols = ['primary_position_name', 'Position', 'position', 'Pos', 'Role']
    pos_col = next((col for col in possible_position_cols if col in filtered_df.columns), None)

    if not pos_col:
        st.error("No valid position column found in the dataset.")
        st.stop()

    available_positions = filtered_df[pos_col].dropna().unique()
    selected_position = st.selectbox("Position", available_positions) if len(available_positions) > 0 else "N/A"

    
    with col4:
        st.text_input("League", value=selected_league, disabled=True)
    
    with col5:
        age_val = str(player_data.get('Age', 'N/A'))
        st.text_input("Age", value=age_val, disabled=True)
    
    with col6:
        minutes_col = 'minutes_played_overall' if 'minutes_played_overall' in filtered_df.columns else 'Minutes played'
        minutes_played = int(player_data.get(minutes_col, 0)) if pd.notna(player_data.get(minutes_col, 0)) else 0
        st.text_input("Minutes", value=str(minutes_played), disabled=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Filter data based on selections
display_df = filtered_df[
    (filtered_df[player_col] == selected_player) &
    (filtered_df[team_col] == selected_club) &
    (filtered_df[pos_col] == selected_position)
]

if display_df.empty:
    display_df = filtered_df[filtered_df[player_col] == selected_player]

if not display_df.empty:
    player_data = display_df.iloc[0]

# Performance chart
with st.container():
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    
    # Define metrics based on data source
    if data_source == "StatsBomb API":
        metrics = [
            'player_season_goals', 'player_season_assists', 'player_season_xg',
            'player_season_xa', 'player_season_shots', 'player_season_key_passes',
            'player_season_dribbles_completed', 'player_season_passing_ratio'
        ]
    else:
        metrics = [
            'Goals per 90', 'Assists per 90', 'xG per 90', 'Key passes per 90',
            'Shots per 90', 'Successful dribbles per 90', 'Pass accuracy %'
        ]
    
    available_metrics = [m for m in metrics if m in filtered_df.columns]
    
    if available_metrics:
        values = []
        labels = []
        
        for metric in available_metrics:
            if pd.notna(player_data.get(metric)):
                percentile = filtered_df[metric].rank(pct=True).loc[player_data.name] * 100
                values.append(percentile)
                labels.append(metric.replace('player_season_', '').replace('_', ' ').title())
        
        if values:
            colors = ['#16a34a' if v >= 70 else '#eab308' if v >= 50 else '#ef4444' for v in values]
            
            fig = go.Figure(go.Bar(
                y=labels, x=values, orientation='h',
                marker_color=colors,
                text=[f'{v:.0f}%' for v in values],
                textposition='middle right',
                textfont=dict(color='white', size=12, family='Arial Black')
            ))
            
            fig.update_layout(
                title=dict(text=f"Performance Metrics - {selected_player}", 
                          font=dict(color='white', size=16), x=0.5),
                plot_bgcolor='#1e40af', paper_bgcolor='#1e40af',
                font=dict(color='white'), height=500,
                xaxis=dict(range=[0, 100], showgrid=True, gridcolor='rgba(255,255,255,0.2)',
                          title="Percentile Ranking", tickfont=dict(color='white')),
                yaxis=dict(tickfont=dict(color='white'), categoryorder='array', 
                          categoryarray=labels[::-1]),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# KPI cards
col1, col2, col3 = st.columns(3)

# Calculate overall rank
if 'values' in locals() and values:
    overall_rank = np.mean(values)
else:
    overall_rank = 0

# Calculate L1 weighted rank
try:
    league_weight = get_weighted_score(selected_league)
    l1_weighted_rank = overall_rank * league_weight
except:
    l1_weighted_rank = overall_rank * 0.95

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Overall Rank</div>
        <div class="metric-value">{overall_rank:.0f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">L1 Weighted Rank</div>
        <div class="metric-value">{l1_weighted_rank:.0f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Minutes Played</div>
        <div class="metric-value">{minutes_played:,}</div>
    </div>
    """, unsafe_allow_html=True)
