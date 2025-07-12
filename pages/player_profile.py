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
st.set_page_config(page_title="Player Performance Dashboard", layout="wide", page_icon="📊")

# Enhanced styling with dynamic KPI card colors
st.markdown("""
<style>
    .main { background-color: #1e3a8a; color: white; }
    .metric-card-neutral {
        background-color: #1e40af; padding: 20px; border-radius: 10px;
        text-align: center; color: white; margin: 5px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3); border: 2px solid #3b82f6;
    }
    .metric-card-red {
        background-color: #dc2626; padding: 20px; border-radius: 10px;
        text-align: center; color: white; margin: 5px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3); border: 2px solid #ef4444;
    }
    .metric-card-amber {
        background-color: #d97706; padding: 20px; border-radius: 10px;
        text-align: center; color: white; margin: 5px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3); border: 2px solid #f59e0b;
    }
    .metric-card-green {
        background-color: #16a34a; padding: 20px; border-radius: 10px;
        text-align: center; color: white; margin: 5px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3); border: 2px solid #22c55e;
    }
    .metric-title { font-size: 12px; font-weight: bold; margin-bottom: 5px; text-transform: uppercase; }
    .metric-value { font-size: 36px; font-weight: bold; }
    .chart-container { background-color: #1e40af; padding: 15px; border-radius: 8px; }
    .stMultiSelect > div > div > div { background-color: #1e40af; }
    .logo-container { text-align: center; margin: 20px 0; }
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

def get_player_age(player_data):
    """Get player age with multiple fallback methods"""
    # Try multiple age columns
    age_columns = ['age', 'player_age', 'player_season_age']
    
    for col in age_columns:
        if col in player_data.index and pd.notna(player_data.get(col)):
            age_val = player_data.get(col)
            if isinstance(age_val, (int, float)) and age_val > 0:
                return int(age_val)
    
    # Try to calculate from birth_date
    if 'birth_date' in player_data.index and pd.notna(player_data.get('birth_date')):
        try:
            birth_date = pd.to_datetime(player_data.get('birth_date'))
            current_date = datetime.now()
            age = current_date.year - birth_date.year
            if current_date.month < birth_date.month or (current_date.month == birth_date.month and current_date.day < birth_date.day):
                age -= 1
            return age if age > 0 else None
        except:
            pass
    
    return None

def get_transfermarkt_url(player_name):
    """Generate Transfermarkt URL for player"""
    # Clean player name for URL
    clean_name = player_name.lower().replace(' ', '-').replace('.', '').replace("'", '')
    return f"https://www.transfermarkt.com/{clean_name}/profil/spieler"

def get_kpi_card_class(percentage):
    """Get CSS class for KPI card based on percentage"""
    if percentage < 49:
        return "metric-card-red"
    elif percentage >= 70:
        return "metric-card-green"
    else:
        return "metric-card-amber"

# Main app with data icon instead of trophy
st.title("📊 Player Performance Dashboard")

# Bristol Rovers Logo placeholder - you'll need to replace with actual logo
st.markdown("""
<div class="logo-container">
    <img src="data:image/png;base64,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" 
         alt="Bristol Rovers Logo" style="max-height: 100px; margin: 10px;">
</div>
""", unsafe_allow_html=True)



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
        
        # Show original position and Transfermarkt link
        original_position = player_data.get('primary_position', 'Unknown')
        transfermarkt_url = get_transfermarkt_url(selected_player)
        
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.info(f"Original Position: {original_position} → Mapped to: {player_position}")
        with col_info2:
            st.markdown(f"🔗 [View {selected_player} on Transfermarkt]({transfermarkt_url})")
        
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
            
            # Calculate percentiles for selected metrics with 95% cap like pizza chart
            values = []
            labels = []
            
            for metric in selected_metrics:
                if metric in position_df.columns and pd.notna(player_data.get(metric)):
                    percentile = position_df[metric].rank(pct=True).loc[player_data.name] * 100
                    # Cap at 95% like pizza chart
                    percentile = min(percentile, 95)
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
                st.info(f"Percentiles calculated against {len(position_df)} players in {player_position} position (capped at 95%)")
                
            else:
                st.warning("No valid data for selected metrics")
            
            st.markdown("</div>", unsafe_allow_html=True)
            # Enhanced KPI cards with dynamic colors based on overall rank
            col1, col2, col3, col4 = st.columns(4)
            
            overall_rank = np.mean(values) if values else 0
            minutes_played = int(player_data.get('player_season_minutes', 0))
            team_name = player_data.get('team_name', 'Unknown')
            
            # Use the same age detection method as pizza chart
            player_age = get_player_age(player_data)
            age_display = str(player_age) if player_age else "N/A"
            
            # Dynamic color for overall rank card
            overall_rank_class = get_kpi_card_class(overall_rank)
            
            with col1:
                st.markdown(f'''
                <div class="{overall_rank_class}">
                    <div class="metric-title">Overall Rank</div>
                    <div class="metric-value">{overall_rank:.0f}%</div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col2:
                st.markdown(f'''
                <div class="metric-card-neutral">
                    <div class="metric-title">Age</div>
                    <div class="metric-value">{age_display}</div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col3:
                st.markdown(f'''
                <div class="metric-card-neutral">
                    <div class="metric-title">Minutes Played</div>
                    <div class="metric-value">{minutes_played:,}</div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col4:
                st.markdown(f'''
                <div class="metric-card-neutral">
                    <div class="metric-title">Team</div>
                    <div class="metric-value" style="font-size: 18px;">{team_name}</div>
                </div>
                ''', unsafe_allow_html=True)

else:
    st.error("No data available. Please check your StatsBomb API credentials.")
