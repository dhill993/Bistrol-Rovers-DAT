import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from statsbombpy import sb

# Corrected position mapping - fixes "Number 3" and adds missing positions
position_mapping = {
    # Centre Backs
    "Centre Back": "Centre Back", 
    "Left Centre Back": "Centre Back", 
    "Right Centre Back": "Centre Back",
    "Outside Centre Back": "Outside Centre Back",  # Added missing position
    
    # Full Backs - Fixed "Number 3" mapping
    "Left Back": "Full Back", 
    "Right Back": "Full Back", 
    "Number 3": "Full Back",  # Fixed: Number 3 should be Full Back
    "Left Wing Back": "Wing Back", 
    "Right Wing Back": "Wing Back",
    
    # Defensive Midfielders
    "Defensive Midfielder": "Defensive Midfielder", 
    "Left Defensive Midfielder": "Defensive Midfielder", 
    "Right Defensive Midfielder": "Defensive Midfielder", 
    "Centre Defensive Midfielder": "Defensive Midfielder",
    
    # Central Midfielders
    "Left Centre Midfield": "Central Midfielder", 
    "Left Centre Midfielder": "Central Midfielder", 
    "Right Centre Midfield": "Central Midfielder", 
    "Right Centre Midfielder": "Central Midfielder", 
    "Centre Midfield": "Central Midfielder",
    
    # Attacking Midfielders
    "Left Attacking Midfield": "Attacking Midfielder", 
    "Right Attacking Midfield": "Attacking Midfielder", 
    "Right Attacking Midfielder": "Attacking Midfielder", 
    "Attacking Midfield": "Attacking Midfielder",
    "Centre Attacking Midfielder": "Attacking Midfielder",
    "Left Attacking Midfielder": "Attacking Midfielder",
    
    # Strikers
    "Secondary Striker": "Striker",
    "Centre Forward": "Striker", 
    "Left Centre Forward": "Striker", 
    "Right Centre Forward": "Striker",
    
    # Wingers
    "Winger": "Winger", 
    "Right Midfielder": "Winger", 
    "Left Midfielder": "Winger", 
    "Left Wing": "Winger", 
    "Right Wing": "Winger",
    
    # Goalkeeper
    "Goalkeeper": "Goalkeeper"
}

# All available metrics for selection
ALL_METRICS = [
    'player_season_aerial_ratio', 'player_season_ball_recoveries_90', 'player_season_blocks_per_shot',
    'player_season_carries_90', 'player_season_crossing_ratio', 'player_season_deep_progressions_90',
    'player_season_defensive_action_regains_90', 'player_season_defensive_actions_90',
    'player_season_dribble_faced_ratio', 'player_season_dribble_ratio', 'player_season_dribbles_90',
    'player_season_np_shots_90', 'player_season_np_xg_90', 'player_season_np_xg_per_shot',
    'player_season_npg_90', 'player_season_npxgxa_90', 'player_season_obv_90',
    'player_season_obv_defensive_action_90', 'player_season_obv_dribble_carry_90',
    'player_season_obv_pass_90', 'player_season_obv_shot_90', 'player_season_op_f3_passes_90',
    'player_season_op_key_passes_90', 'player_season_op_passes_into_and_touches_inside_box_90',
    'player_season_op_passes_into_box_90', 'player_season_padj_clearances_90',
    'player_season_padj_interceptions_90', 'player_season_padj_pressures_90', 'player_season_padj_tackles_90',
    'player_season_passing_ratio', 'player_season_shot_on_target_ratio', 'player_season_shot_touch_ratio',
    'player_season_touches_inside_box_90', 'player_season_xgbuildup_90', 'player_season_op_xa_90',
    'player_season_pressured_passing_ratio', 'player_season_da_aggressive_distance',
    'player_season_clcaa', 'player_season_gsaa_ratio', 'player_season_gsaa_90',
    'player_season_save_ratio', 'player_season_xs_ratio', 'player_season_positive_outcome_score',
    'player_season_obv_gk_90', 'player_season_forward_pass_ratio',
    'player_season_forward_pass_proportion', 'player_season_scoring_contribution_90',
    'player_season_fouls_won_90', 'player_season_pressures_90', 'player_season_counterpressures_90',
    'player_season_aggressive_actions_90'
]

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
    .stMultiSelect > div > div > div { background-color: #1e40af; }
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
                
                # Apply position mapping
                df['mapped_position'] = df['primary_position'].map(position_mapping)
                df = df.dropna(subset=['mapped_position'])
                
                dataframes.append(df)
            except:
                continue
                
        return pd.concat(dataframes, ignore_index=True) if dataframes else pd.DataFrame()
    except Exception as e:
        st.error(f"StatsBomb API error: {e}")
        return pd.DataFrame()

def get_available_metrics(df):
    """Get metrics that are available in the dataframe"""
    return [metric for metric in ALL_METRICS if metric in df.columns]

# Main app
st.title("🏆 Player Performance Dashboard")

# Load StatsBomb data
with st.spinner("Loading StatsBomb data..."):
    df = get_statsbomb_data()

if not df.empty:
    # Filters - removed sidebar, now in main area
    col1, col2, col3 = st.columns(3)
    
    with col1:
        leagues = ['All'] + sorted(df['League'].unique().tolist())
        selected_league = st.selectbox("League", leagues)
    
    with col2:
        seasons = ['All'] + sorted(df['Season'].unique().tolist())
        selected_season = st.selectbox("Season", seasons)
    
    with col3:
        positions = ['All'] + sorted(df['mapped_position'].dropna().unique().tolist())
        selected_position = st.selectbox("Position", positions)
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_league != 'All':
        filtered_df = filtered_df[filtered_df['League'] == selected_league]
    
    if selected_season != 'All':
        filtered_df = filtered_df[filtered_df['Season'] == selected_season]
    
    if selected_position != 'All':
        filtered_df = filtered_df[filtered_df['mapped_position'] == selected_position]
    
    # Player selection
    players = ['Select a player'] + sorted(filtered_df['player_name'].unique().tolist())
    selected_player = st.selectbox("Select Player", players)

    
    if selected_player != "Select a player":
        player_data = filtered_df[filtered_df['player_name'] == selected_player].iloc[0]
        player_position = player_data.get('mapped_position', 'Unknown')
        
        # Show original position too
        original_position = player_data.get('primary_position', 'Unknown')
        st.info(f"Original Position: {original_position} → Mapped to: {player_position}")
        
        # Get available metrics for this dataset
        available_metrics = get_available_metrics(filtered_df)
        
        # Metric selection with validation
        st.markdown("### Select Metrics (Min: 10, Max: 15)")
        
        # Create friendly names for metrics
        metric_display_names = {
            metric: metric.replace('player_season_', '').replace('_', ' ').title()
            for metric in available_metrics
        }
        
        selected_metrics = st.multiselect(
            "Choose metrics to analyze:",
            options=available_metrics,
            format_func=lambda x: metric_display_names[x],
            help="Select between 10 and 15 metrics for analysis"
        )
        
        # Validation
        if len(selected_metrics) < 10:
            st.warning(f"Please select at least 10 metrics. Currently selected: {len(selected_metrics)}")
        elif len(selected_metrics) > 15:
            st.warning(f"Please select maximum 15 metrics. Currently selected: {len(selected_metrics)}")
        else:
            st.success(f"✅ {len(selected_metrics)} metrics selected")
            
            # Filter data by position for percentile calculation
            position_df = filtered_df[filtered_df['mapped_position'] == player_position]
            
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader(f"Player Profile: {selected_player} - {player_position}")
            
            # Calculate percentiles for selected metrics
            values = []
            labels = []
            
            for metric in selected_metrics:
                if metric in position_df.columns and pd.notna(player_data.get(metric)):
                    percentile = position_df[metric].rank(pct=True).loc[player_data.name] * 100
                    values.append(percentile)
                    labels.append(metric_display_names[metric])
            
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
                    title=dict(text=f"Custom Metrics Analysis - {selected_player} ({player_position})",
                              font=dict(color='white', size=16), x=0.5),
                    plot_bgcolor='#1e40af', paper_bgcolor='#1e40af',
                    font=dict(color='white'), height=max(400, len(values) * 30),
                    xaxis=dict(range=[0, 100], showgrid=True, gridcolor='rgba(255,255,255,0.2)',
                              title="Percentile Ranking vs Same Position", tickfont=dict(color='white')),
                    yaxis=dict(tickfont=dict(color='white'), categoryorder='array',
                              categoryarray=labels[::-1]),
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Show comparison info
                st.info(f"Percentiles calculated against {len(position_df)} players in {player_position} position")
                
            else:
                st.warning("No valid data for selected metrics")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # KPI cards
            col1, col2, col3, col4 = st.columns(4)
            
            overall_rank = np.mean(values) if values else 0
            minutes_played = int(player_data.get('player_season_minutes', 0))
            team_name = player_data.get('team_name', 'Unknown')
            # Try multiple possible age column names
            age_columns = ['age', 'player_age', 'player_season_age']
            age = 0
            for age_col in age_columns:
                if age_col in player_data.index and pd.notna(player_data.get(age_col)):
                    age = int(player_data.get(age_col, 0))
                    break
            
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
                    <div class="metric-title">Minutes Played</div>
                    <div class="metric-value">{minutes_played:,}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Team</div>
                    <div class="metric-value" style="font-size: 20px;">{team_name}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Age</div>
                    <div class="metric-value">{age}</div>
                </div>
                """, unsafe_allow_html=True)
else:
    st.error("No data available. Please check your StatsBomb API credentials.")
