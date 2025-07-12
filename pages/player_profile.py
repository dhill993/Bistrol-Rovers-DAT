import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from statsbombpy import sb

# Position-based metrics (same as pizza chart logic)
POSITION_METRICS = {
    'Goalkeeper': [
        'goalkeeper_saves', 'goalkeeper_save_percentage', 'goalkeeper_goals_conceded',
        'goalkeeper_clean_sheets', 'passes', 'pass_accuracy'
    ],
    'Centre Back': [
        'passes', 'pass_accuracy', 'defensive_actions', 'aerial_wins',
        'clearances', 'interceptions'
    ],
    'Full Back': [
        'passes', 'pass_accuracy', 'crosses', 'defensive_actions',
        'dribbles', 'assists'
    ],
    'Wing Back': [
        'passes', 'pass_accuracy', 'crosses', 'assists',
        'dribbles', 'defensive_actions'
    ],
    'Defensive Midfield': [
        'passes', 'pass_accuracy', 'defensive_actions', 'interceptions',
        'tackles', 'aerial_wins'
    ],
    'Central Midfield': [
        'passes', 'pass_accuracy', 'assists', 'key_passes',
        'dribbles', 'defensive_actions'
    ],
    'Attacking Midfield': [
        'assists', 'key_passes', 'goals', 'shots',
        'dribbles', 'pass_accuracy'
    ],
    'Winger': [
        'goals', 'assists', 'dribbles', 'crosses',
        'shots', 'key_passes'
    ],
    'Striker': [
        'goals', 'shots', 'shots_on_target', 'assists',
        'aerial_wins', 'key_passes'
    ]
}

st.set_page_config(page_title="Player Performance Dashboard", layout="wide")

# Styling
st.markdown("""
<style>
    .main { background-color: #1e3a8a; color: white; }
    .metric-card {
        background-color: #16a34a; padding: 20px; border-radius: 10px;
        text-align: center; color: white; margin: 5px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3); border: 2px solid #22c55e;
    }
    .metric-title { font-size: 12px; font-weight: bold; margin-bottom: 5px; text-transform: uppercase; }
    .metric-value { font-size: 36px; font-weight: bold; }
    .chart-container { background-color: #1e40af; padding: 15px; border-radius: 8px; }
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
        
        for _, row in all_comps.iterrows():
            try:
                comp_id, season_id = row["competition_id"], row["season_id"]
                df = sb.player_season_stats(comp_id, season_id, creds=creds)
                
                df['League'] = row['competition_name']
                df['Season'] = row['season_name']
                dataframes.append(df)
            except:
                continue
                
        return pd.concat(dataframes, ignore_index=True) if dataframes else pd.DataFrame()
    except Exception as e:
        st.error(f"StatsBomb API error: {e}")
        return pd.DataFrame()

def get_position_metrics(position):
    """Get metrics for a specific position"""
    # Map common position variations
    position_map = {
        'CB': 'Centre Back', 'LB': 'Full Back', 'RB': 'Full Back',
        'LWB': 'Wing Back', 'RWB': 'Wing Back', 'CDM': 'Defensive Midfield',
        'CM': 'Central Midfield', 'CAM': 'Attacking Midfield', 'AM': 'Attacking Midfield',
        'LW': 'Winger', 'RW': 'Winger', 'LM': 'Winger', 'RM': 'Winger',
        'ST': 'Striker', 'CF': 'Striker', 'GK': 'Goalkeeper'
    }
    
    mapped_position = position_map.get(position, position)
    return POSITION_METRICS.get(mapped_position, POSITION_METRICS['Central Midfield'])

# Main app
st.title("🏆 Player Performance Dashboard")

# Load StatsBomb data
with st.spinner("Loading StatsBomb data..."):
    df = get_statsbomb_data()
    if not df.empty:
        st.success(f"Loaded {len(df)} player records")

if not df.empty:
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        leagues = ['All'] + sorted(df['League'].unique().tolist())
        selected_league = st.selectbox("League", leagues)
    
    with col2:
        seasons = ['All'] + sorted(df['Season'].unique().tolist())
        selected_season = st.selectbox("Season", seasons)
    
    with col3:
        positions = ['All'] + sorted(df['primary_position'].dropna().unique().tolist())
        selected_position = st.selectbox("Position", positions)
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_league != 'All':
        filtered_df = filtered_df[filtered_df['League'] == selected_league]
    
    if selected_season != 'All':
        filtered_df = filtered_df[filtered_df['Season'] == selected_season]
    
    if selected_position != 'All':
        filtered_df = filtered_df[filtered_df['primary_position'] == selected_position]
    
    # Player selection
    players = ['Select a player'] + sorted(filtered_df['player_name'].unique().tolist())
    selected_player = st.selectbox("Select Player", players)
    
    if selected_player != "Select a player":
        player_data = filtered_df[filtered_df['player_name'] == selected_player].iloc[0]
        player_position = player_data.get('primary_position', 'Unknown')
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader(f"Player Profile: {selected_player} - {player_position}")
        
        # Get position-specific metrics
        position_metrics = get_position_metrics(player_position)
        
        # Create bar chart with position-based metrics
        values = []
        labels = []
        
        for metric in position_metrics:
            if metric in filtered_df.columns and pd.notna(player_data.get(metric)):
                percentile = filtered_df[metric].rank(pct=True).loc[player_data.name] * 100
                values.append(percentile)
                labels.append(metric.replace('_', ' ').title())
        
        if values:
            colors = ['#16a34a' if v >= 70 else '#eab308' if v >= 50 else '#ef4444' for v in values]
            
            fig = go.Figure(go.Bar(
                y=labels, x=values, orientation='h',
                marker_color=colors,
                text=[f'{v:.0f}%' for v in values],
                textposition='outside',
                textfont=dict(color='white', size=12, family='Arial Black')
            ))
            
            fig.update_layout(
                title=dict(text=f"Performance Metrics - {selected_player} ({player_position})", 
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
        else:
            st.warning(f"No metrics available for {player_position}")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # KPI cards
        col1, col2, col3 = st.columns(3)
        
        overall_rank = np.mean(values) if values else 0
        minutes_played = int(player_data.get('minutes_played', 0))
        
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
                <div class="metric-title">Position</div>
                <div class="metric-value">{player_position}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Minutes</div>
                <div class="metric-value">{minutes_played:,}</div>
            </div>
            """, unsafe_allow_html=True)
