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
    dataframes = []
    
    for uploaded_file in uploaded_files:
        try:
            df = pd.read_excel(uploaded_file)
            
            # Clean column names
            df.columns = df.columns.str.strip()
            
            # Add file info
            df['Source_File'] = uploaded_file.name
            df['League'] = uploaded_file.name.split('_')[0] if '_' in uploaded_file.name else 'Unknown'
            
            dataframes.append(df)
        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {e}")
    
    return pd.concat(dataframes, ignore_index=True) if dataframes else pd.DataFrame()

# Main app
st.title("🏆 Player Performance Dashboard")

# Data source selection
data_source = st.selectbox("Select Data Source", ["StatsBomb API", "Upload Wyscout Files"])

df = pd.DataFrame()

if data_source == "StatsBomb API":
    # Auto-load StatsBomb data if API credentials are available
    try:
        if "user" in st.secrets and "passwd" in st.secrets:
            with st.spinner("Loading StatsBomb data..."):
                df = get_statsbomb_data()
                if not df.empty:
                    st.success(f"Loaded {len(df)} player records")
                else:
                    st.error("No data loaded")
        else:
            st.error("StatsBomb API credentials not found in secrets")
    except Exception as e:
        st.error(f"Error loading StatsBomb data: {e}")

elif data_source == "Upload Wyscout Files":
    uploaded_files = st.file_uploader(
        "Upload Wyscout Excel files", 
        type=['xlsx', 'xls'], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        with st.spinner("Processing files..."):
            df = process_wyscout_files(uploaded_files)
            if not df.empty:
                st.success(f"Processed {len(uploaded_files)} files with {len(df)} player records")

if not df.empty:
    # Dynamic column detection
    player_col = None
    for col in df.columns:
        if 'player' in col.lower() and 'name' in col.lower():
            player_col = col
            break
    
    if not player_col:
        for col in df.columns:
            if 'player' in col.lower():
                player_col = col
                break
    
    if not player_col:
        st.error("Could not find player name column")
        st.stop()
    
    # Position column detection
    position_col = None
    for col in df.columns:
        if 'position' in col.lower() or 'role' in col.lower():
            position_col = col
            break
    
    # Filters
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        leagues = ['All'] + sorted(df['League'].dropna().unique().tolist())
        selected_league = st.selectbox("League", leagues)
    
    with col2:
        seasons = ['All'] + sorted(df['Season'].dropna().unique().tolist()) if 'Season' in df.columns else ['All']
        selected_season = st.selectbox("Season", seasons)
    
    with col3:
        # Position filter
        if position_col:
            positions = ['All'] + sorted(df[position_col].dropna().unique().tolist())
            selected_position = st.selectbox("Position", positions)
        else:
            selected_position = 'All'
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_league != 'All':
        filtered_df = filtered_df[filtered_df['League'] == selected_league]
    
    if selected_season != 'All' and 'Season' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Season'] == selected_season]
    
    if selected_position != 'All' and position_col:
        filtered_df = filtered_df[filtered_df[position_col] == selected_position]
    
    # Player selection
    players = ['Select a player'] + sorted(filtered_df[player_col].dropna().unique().tolist())
    selected_player = st.selectbox("Select Player", players)
    
    # Minutes played calculation
    minutes_col = None
    for col in filtered_df.columns:
        if 'minutes' in col.lower():
            minutes_col = col
            break
    
    minutes_played = 0
    if selected_player != "Select a player" and minutes_col:
        player_data = filtered_df[filtered_df[player_col] == selected_player].iloc[0]
        minutes_played = int(player_data.get(minutes_col, 0))
    
    # Display player details
    if selected_player != "Select a player":
        player_data = filtered_df[filtered_df[player_col] == selected_player].iloc[0]
        
        # Extract position from player data
        player_position = "Unknown"
        if position_col and pd.notna(player_data.get(position_col)):
            player_position = player_data[position_col]
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader(f"Player Profile: {selected_player} - {player_position}")
        
        # Performance metrics chart
        if data_source == "StatsBomb API":
            metrics = [
                'player_season_goals', 'player_season_assists', 'player_season_xg',
                'player_season_xa', 'player_season_passes', 'player_season_pass_accuracy'
            ]
        else:
            metrics = [
                'Goals per 90', 'Assists per 90', 'Key passes per 90',
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
                
                # FIXED: Use valid textposition for horizontal bar chart
                fig = go.Figure(go.Bar(
                    y=labels, x=values, orientation='h',
                    marker_color=colors,
                    text=[f'{v:.0f}%' for v in values],
                    textposition='outside',  # Changed from 'middle right' to 'outside'
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
