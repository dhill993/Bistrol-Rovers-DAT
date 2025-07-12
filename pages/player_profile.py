import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from statsbombpy import sb

# Position mapping
position_mapping = {
    "Centre Back": "Centre Back", 
    "Left Centre Back": "Centre Back", 
    "Right Centre Back": "Centre Back",
    "Outside Centre Back": "Outside Centre Back",
    "Left Back": "Full Back", 
    "Right Back": "Full Back", 
    "Number 3": "Full Back",
    "Left Wing Back": "Wing Back", 
    "Right Wing Back": "Wing Back",
    "Defensive Midfielder": "Defensive Midfielder", 
    "Left Defensive Midfielder": "Defensive Midfielder", 
    "Right Defensive Midfielder": "Defensive Midfielder", 
    "Centre Defensive Midfielder": "Defensive Midfielder",
    "Left Centre Midfield": "Central Midfielder", 
    "Left Centre Midfielder": "Central Midfielder", 
    "Right Centre Midfield": "Central Midfielder", 
    "Right Centre Midfielder": "Central Midfielder", 
    "Centre Midfield": "Central Midfielder",
    "Left Attacking Midfield": "Attacking Midfielder", 
    "Right Attacking Midfield": "Attacking Midfielder", 
    "Right Attacking Midfielder": "Attacking Midfielder", 
    "Attacking Midfield": "Attacking Midfielder",
    "Centre Attacking Midfielder": "Attacking Midfielder",
    "Left Attacking Midfielder": "Attacking Midfielder",
    "Secondary Striker": "Striker",
    "Centre Forward": "Striker", 
    "Left Centre Forward": "Striker", 
    "Right Centre Forward": "Striker",
    "Winger": "Winger", 
    "Right Midfielder": "Winger", 
    "Left Midfielder": "Winger", 
    "Left Wing": "Winger", 
    "Right Wing": "Winger",
    "Goalkeeper": "Goalkeeper"
}

ALL_METRICS = [
    'player_season_aerial_ratio', 'player_season_ball_recoveries_90', 'player_season_blocks_per_shot',
    'player_season_carries_90', 'player_season_crossing_ratio', 'player_season_deep_progressions_90',
    'player_season_defensive_action_regains_90', 'player_season_defensive_actions_90',
    'player_season_dribble_faced_ratio', 'player_season_dribble_ratio', 'player_season_dribbles_90',
    'player_season_np_shots_90', 'player_season_np_xg_90', 'player_season_np_xg_per_shot',
    'player_season_npg_90', 'player_season_passes_90', 'player_season_passes_into_box_90',
    'player_season_passes_ratio', 'player_season_passes_received_90', 'player_season_pressure_regains_90',
    'player_season_pressures_90', 'player_season_primary_assists_90', 'player_season_progressive_passes_90',
    'player_season_progressive_passes_ratio', 'player_season_shots_on_target_90',
    'player_season_shots_on_target_ratio', 'player_season_tackles_90', 'player_season_touches_90',
    'player_season_touches_def_pen_90', 'player_season_touches_in_box_90', 'player_season_turnovers_90',
    'player_season_xa_90', 'player_season_xg_90', 'player_season_xg_assisted_90',
    'player_season_xg_per_shot', 'player_season_xpass_90'
]

def get_default_metrics(position):
    defaults = {
        'Striker': ['player_season_npg_90', 'player_season_np_xg_90', 'player_season_np_shots_90', 'player_season_touches_in_box_90', 'player_season_primary_assists_90'],
        'Winger': ['player_season_npg_90', 'player_season_xa_90', 'player_season_dribbles_90', 'player_season_crossing_ratio', 'player_season_progressive_passes_90'],
        'Attacking Midfielder': ['player_season_xa_90', 'player_season_progressive_passes_90', 'player_season_passes_into_box_90', 'player_season_primary_assists_90', 'player_season_npg_90'],
        'Central Midfielder': ['player_season_progressive_passes_90', 'player_season_passes_90', 'player_season_defensive_actions_90', 'player_season_ball_recoveries_90', 'player_season_passes_ratio'],
        'Defensive Midfielder': ['player_season_defensive_actions_90', 'player_season_ball_recoveries_90', 'player_season_tackles_90', 'player_season_pressures_90', 'player_season_passes_ratio'],
        'Full Back': ['player_season_defensive_actions_90', 'player_season_xa_90', 'player_season_progressive_passes_90', 'player_season_crosses_90', 'player_season_dribbles_90'],
        'Wing Back': ['player_season_xa_90', 'player_season_defensive_actions_90', 'player_season_progressive_passes_90', 'player_season_crosses_90', 'player_season_dribbles_90'],
        'Centre Back': ['player_season_defensive_actions_90', 'player_season_aerial_ratio', 'player_season_progressive_passes_90', 'player_season_passes_ratio', 'player_season_ball_recoveries_90'],
        'Outside Centre Back': ['player_season_defensive_actions_90', 'player_season_aerial_ratio', 'player_season_progressive_passes_90', 'player_season_passes_ratio', 'player_season_ball_recoveries_90'],
        'Goalkeeper': ['player_season_saves_90', 'player_season_save_ratio', 'player_season_clean_sheet_ratio', 'player_season_passes_ratio', 'player_season_long_passes_90']
    }
    return defaults.get(position, ALL_METRICS[:5])

def load_data():
    try:
        df = sb.player_season_stats(
            leagues={'A-League Men': [2023]},
            split_by_teams=True,
            creds={'user': st.secrets['sb_user'], 'passwd': st.secrets['sb_password']}
        )
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def calculate_percentiles(df, player_data, position, metrics):
    position_df = df[df['primary_position_group'] == position]
    percentiles = {}
    
    for metric in metrics:
        if metric in position_df.columns:
            values = position_df[metric].dropna()
            if len(values) > 0:
                player_value = player_data.get(metric, 0)
                percentile = (values < player_value).sum() / len(values) * 100
                percentiles[metric] = percentile
    
    return percentiles

st.set_page_config(page_title="Player Performance Dashboard", layout="wide")

st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-title {
        font-size: 12px;
        font-weight: bold;
        margin-bottom: 8px;
        text-transform: uppercase;
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("Player Performance Dashboard")

df = load_data()

if df is not None:
    df['primary_position_group'] = df['primary_position'].map(position_mapping)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_league = st.selectbox("Select League", ["A-League Men"])
    
    with col2:
        selected_season = st.selectbox("Select Season", [2023])
    
    with col3:
        available_positions = sorted(df['primary_position_group'].dropna().unique())
        selected_position = st.selectbox("Select Position", available_positions)
    
    position_df = df[df['primary_position_group'] == selected_position]
    
    if not position_df.empty:
        player_names = sorted(position_df['player_name'].unique())
        selected_player = st.selectbox("Select Player", player_names)
        
        if selected_player:
            player_data = position_df[position_df['player_name'] == selected_player].iloc[0]
            
            default_metrics = get_default_metrics(selected_position)
            available_metrics = [m for m in ALL_METRICS if m in df.columns]
            
            selected_metrics = st.multiselect(
                "Select Metrics for Analysis",
                available_metrics,
                default=default_metrics
            )
            
            if selected_metrics:
                percentiles = calculate_percentiles(df, player_data, selected_position, selected_metrics)
                
                if percentiles:
                    st.markdown(f"<div style='background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%); padding: 20px; border-radius: 10px; margin: 20px 0;'>", unsafe_allow_html=True)
                    
                    labels = [metric.replace('player_season_', '').replace('_', ' ').title() for metric in selected_metrics]
                    values = [percentiles.get(metric, 0) for metric in selected_metrics]
                    
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        y=labels,
                        x=values,
                        orientation='h',
                        marker=dict(color=values, colorscale='RdYlGn', cmin=0, cmax=100),
                        text=[f"{v:.1f}%" for v in values],
                        textposition='auto'
                    ))
                    
                    fig.update_layout(
                        title=dict(text=f"Custom Metrics Analysis - {selected_player} ({selected_position})",
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
                    st.info(f"Percentiles calculated against {len(position_df)} players in {selected_position} position")
                else:
                    st.warning("No valid data for selected metrics")
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # KPI cards with FIXED age detection
                col1, col2, col3, col4 = st.columns(4)
                
                overall_rank = np.mean(values) if values else 0
                minutes_played = int(player_data.get('player_season_minutes', 0))
                team_name = player_data.get('team_name', 'Unknown')
                
                # FIXED: Try multiple age column names like your pizza chart does
                age = 0
                age_columns = ['age', 'player_age', 'player_season_age', 'birth_date']
                for age_col in age_columns:
                    if age_col in player_data.index and pd.notna(player_data.get(age_col)):
                        if age_col == 'birth_date':
                            # Calculate age from birth date
                            birth_date = pd.to_datetime(player_data.get(age_col))
                            age = (datetime.now() - birth_date).days // 365
                        else:
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
