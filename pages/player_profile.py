import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from statsbombpy import sb
import warnings

# Suppress all warnings to prevent crashes
warnings.filterwarnings("ignore")
pd.options.mode.chained_assignment = None

# Corrected position mapping
position_mapping = {
    "Centre Back": "Centre Back", "Left Centre Back": "Centre Back", "Right Centre Back": "Centre Back",
    "Outside Centre Back": "Outside Centre Back", "Left Back": "Full Back", "Right Back": "Full Back", 
    "Number 3": "Full Back", "Left Wing Back": "Wing Back", "Right Wing Back": "Wing Back",
    "Defensive Midfielder": "Defensive Midfielder", "Left Defensive Midfielder": "Defensive Midfielder", 
    "Right Defensive Midfielder": "Defensive Midfielder", "Centre Defensive Midfielder": "Defensive Midfielder",
    "Left Centre Midfield": "Central Midfielder", "Left Centre Midfielder": "Central Midfielder", 
    "Right Centre Midfield": "Central Midfielder", "Right Centre Midfielder": "Central Midfielder", 
    "Centre Midfield": "Central Midfielder", "Left Attacking Midfield": "Attacking Midfielder", 
    "Right Attacking Midfield": "Attacking Midfielder", "Right Attacking Midfielder": "Attacking Midfielder", 
    "Attacking Midfield": "Attacking Midfielder", "Centre Attacking Midfielder": "Attacking Midfielder",
    "Left Attacking Midfielder": "Attacking Midfielder", "Secondary Striker": "Striker",
    "Centre Forward": "Striker", "Left Centre Forward": "Striker", "Right Centre Forward": "Striker",
    "Winger": "Winger", "Right Midfielder": "Winger", "Left Midfielder": "Winger", 
    "Left Wing": "Winger", "Right Wing": "Winger", "Goalkeeper": "Goalkeeper"
}

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
    .logo-container { text-align: center; margin: 20px 0; }
</style>
""", unsafe_allow_html=True)

def safe_numeric_convert(df):
    """Safely convert numeric columns without warnings"""
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                converted = pd.to_numeric(df[col], errors='coerce')
                if not converted.isna().all():
                    df[col] = converted
            except:
                continue
    return df

@st.cache_data(ttl=3600)
def get_statsbomb_data():
    """Fetch StatsBomb data with crash protection"""
    try:
        user = st.secrets["user"]
        passwd = st.secrets["passwd"]
        creds = {"user": user, "passwd": passwd}
        
        all_comps = sb.competitions(creds=creds)
        dataframes = []
        
        progress_bar = st.progress(0)
        total_comps = len(all_comps)
        
        for idx, (_, row) in enumerate(all_comps.iterrows()):
            try:
                comp_id, season_id = row["competition_id"], row["season_id"]
                df = sb.player_season_stats(comp_id, season_id, creds=creds)
                
                if df.empty:
                    continue
                
                # Safe numeric conversion
                df = safe_numeric_convert(df)
                
                df['League'] = row['competition_name']
                df['Season'] = row['season_name']
                df['mapped_position'] = df['primary_position'].map(position_mapping)
                df = df.dropna(subset=['mapped_position'])
                
                if not df.empty:
                    dataframes.append(df)
                    
                progress_bar.progress((idx + 1) / total_comps)
                
            except Exception:
                continue
                
        progress_bar.empty()
        
        if dataframes:
            combined_df = pd.concat(dataframes, ignore_index=True, sort=False)
            return combined_df
        else:
            return pd.DataFrame()
            
    except Exception as e:
        st.error(f"Data loading error: {str(e)}")
        return pd.DataFrame()

def get_available_metrics(df):
    return [metric for metric in ALL_METRICS if metric in df.columns]

def get_player_age(player_data):
    age_columns = ['age', 'player_age', 'player_season_age']
    for col in age_columns:
        if col in player_data.index and pd.notna(player_data.get(col)):
            age_val = player_data.get(col)
            if isinstance(age_val, (int, float)) and age_val > 0:
                return int(age_val)
    return None

def get_transfermarkt_url(player_name):
    clean_name = player_name.lower().replace(' ', '-').replace('.', '').replace("'", '')
    return f"https://www.transfermarkt.com/{clean_name}/profil/spieler"

def get_kpi_card_class(percentage):
    if percentage < 49:
        return "metric-card-red"
    elif percentage >= 70:
        return "metric-card-green"
    else:
        return "metric-card-amber"

# Main app
st.title("📊 Player Performance Dashboard")

# Bristol Rovers Logo
st.markdown("""
<div class="logo-container">
    <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAABlVBMVEX///8AAAA8ZZbl5eXk5OTm5ubj4+Pn5+fi4uLo6Ojh4eHp6enq6urg4ODr6+vf39/s7Ozt7e3e3t7u7u7d3d3v7+/c3Nzw8PDx8fHb29vy8vLz8/Pa2trY2Nj09PT19fXX19fW1tb29vb39/fV1dXU1NT4+PjT09P5+fn6+vrS0tL7+/vR0dH8/PzQ0ND9/f3Pz8/+/v7Ozs7//v7Nzc3Ly8vMzMzKysrJycnIyMjHx8fGxsbFxcXExMTDw8PCwsLBwcHAwMC/v7++vr69vb28vLy7u7u6urq5ubm4uLi3t7e2tra1tbW0tLS0s7OysrKxsbGwsLCvr6+urq6tra2srKyrq6uqqqqpqamop6eoqKinp6empqalpaWkpKSjo6OioqKhoaGgoKCfn5+enp6dnZ2cnJybm5uampqZmZmYmJiXl5eWlpaVlZWUlJSTk5OSkpKRkZGQkJCPj4+Ojo6NjY2MjIyLi4uKioqJiYmIiIiHh4eGhoaFhYWEhISCgoKBgYGAgIB/f39+fn59fX18fHx7e3t6enp5eXl4eHh3d3d2dnZ1dXV0dHRzc3NycnJxcXFwcHBvb29ubm5tbW1sbGxra2tqamppaWloaGhnZ2dmZmZlZWVkZGRjY2NiYmJhYWFgYGBfX19eXl5dXV1cXFxbW1taWlpZWVlYWFhXV1dWVlZVVVVUVFRTU1NSUlJRUVFQUFBPT09OTk5NTU1MTExLS0tKSkpJSUlISEhHR0dGRkZFRUVERERDQ0NCQkJBQUFAQEA/Pz8+Pj49PT08PDw7Ozs6Ojo5OTk4ODg3Nzc2NjY1NTU0NDQzMzMyMjIxMTEwMDAvLy8uLi4tLS0sLCwrKysqKioqKSkoKCgnJyckJCQjIyMiIiIhISEgICAeHh4dHR0cHBwbGxsaGhoZGRkYGBgXFxcWFhYVFRUUFBQTExMSEhIREREQEBAPDw8ODg4NDQ0MDAwLCwsKCgoJCQkICAgHBwcGBgYFBQUEBAQDAwMCAgIBAQEAAAD///8=" width="100" alt="Bristol Rovers Logo">
</div>
""", unsafe_allow_html=True)

# Load data
with st.spinner("Loading player data..."):
    df = get_statsbomb_data()

if df.empty:
    st.error("No data available. Please check your connection and try again.")
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")

# League filter
leagues = sorted(df['League'].unique())
selected_leagues = st.sidebar.multiselect("Select Leagues", leagues, default=leagues[:3] if len(leagues) >= 3 else leagues)

# Position filter
positions = sorted(df['mapped_position'].unique())
selected_positions = st.sidebar.multiselect("Select Positions", positions, default=positions)

# Filter data
filtered_df = df[
    (df['League'].isin(selected_leagues)) & 
    (df['mapped_position'].isin(selected_positions))
]

if filtered_df.empty:
    st.warning("No players match the selected filters.")
    st.stop()

# Player selection
players = sorted(filtered_df['player_name'].unique())
selected_player = st.selectbox("Select Player", players)

if not selected_player:
    st.warning("Please select a player.")
    st.stop()

# Get player data
player_data = filtered_df[filtered_df['player_name'] == selected_player].iloc[0]

# Metrics selection
available_metrics = get_available_metrics(filtered_df)
if not available_metrics:
    st.error("No metrics available for analysis.")
    st.stop()

default_metrics = available_metrics[:6] if len(available_metrics) >= 6 else available_metrics
selected_metrics = st.multiselect("Select Metrics for Analysis", available_metrics, default=default_metrics)

if not selected_metrics:
    st.warning("Please select at least one metric.")
    st.stop()

# Player Information Section
st.header(f"Player Profile: {selected_player}")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"**Team:** {player_data.get('team_name', 'N/A')}")
    
with col2:
    st.markdown(f"**Position:** {player_data.get('mapped_position', 'N/A')}")
    
with col3:
    age = get_player_age(player_data)
    st.markdown(f"**Age:** {age if age else 'N/A'}")
    
with col4:
    transfermarkt_url = get_transfermarkt_url(selected_player)
    st.markdown(f"[📊 Transfermarkt Profile]({transfermarkt_url})")

# KPI Cards Section
st.header("Performance Metrics")

# Calculate percentiles for selected metrics
position_peers = filtered_df[filtered_df['mapped_position'] == player_data['mapped_position']]

kpi_cols = st.columns(min(len(selected_metrics), 4))

for i, metric in enumerate(selected_metrics[:4]):
    col_idx = i % 4
    with kpi_cols[col_idx]:
        if metric in player_data.index and pd.notna(player_data[metric]):
            player_value = player_data[metric]
            
            # Calculate percentile (capped at 99th percentile)
            valid_values = position_peers[metric].dropna()
            if len(valid_values) > 1:
                percentile = min(99, (valid_values < player_value).mean() * 100)
            else:
                percentile = 50
            
            # Get appropriate card class
            card_class = get_kpi_card_class(percentile)
            
            # Format metric name
            metric_display = metric.replace('player_season_', '').replace('_', ' ').title()
            
            st.markdown(f"""
            <div class="{card_class}">
                <div class="metric-title">{metric_display}</div>
                <div class="metric-value">{player_value:.2f}</div>
                <div style="font-size: 14px; margin-top: 5px;">{percentile:.0f}th percentile</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card-neutral">
                <div class="metric-title">{metric.replace('player_season_', '').replace('_', ' ').title()}</div>
                <div class="metric-value">N/A</div>
                <div style="font-size: 14px; margin-top: 5px;">No data</div>
            </div>
            """, unsafe_allow_html=True)

# Additional KPI cards if more than 4 metrics selected
if len(selected_metrics) > 4:
    st.markdown("<br>", unsafe_allow_html=True)
    remaining_metrics = selected_metrics[4:]
    additional_cols = st.columns(min(len(remaining_metrics), 4))
    
    for i, metric in enumerate(remaining_metrics[:4]):
        col_idx = i % 4
        with additional_cols[col_idx]:
            if metric in player_data.index and pd.notna(player_data[metric]):
                player_value = player_data[metric]
                
                valid_values = position_peers[metric].dropna()
                if len(valid_values) > 1:
                    percentile = min(99, (valid_values < player_value).mean() * 100)
                else:
                    percentile = 50
                
                card_class = get_kpi_card_class(percentile)
                metric_display = metric.replace('player_season_', '').replace('_', ' ').title()
                
                st.markdown(f"""
                <div class="{card_class}">
                    <div class="metric-title">{metric_display}</div>
                    <div class="metric-value">{player_value:.2f}</div>
                    <div style="font-size: 14px; margin-top: 5px;">{percentile:.0f}th percentile</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="metric-card-neutral">
                    <div class="metric-title">{metric.replace('player_season_', '').replace('_', ' ').title()}</div>
                    <div class="metric-value">N/A</div>
                    <div style="font-size: 14px; margin-top: 5px;">No data</div>
                </div>
                """, unsafe_allow_html=True)

# Radar Chart Section
st.header("Performance Radar Chart")

if len(selected_metrics) >= 3:
    # Prepare radar chart data
    radar_metrics = selected_metrics[:8]  # Limit to 8 metrics for readability
    radar_values = []
    radar_labels = []
    
    for metric in radar_metrics:
        if metric in player_data.index and pd.notna(player_data[metric]):
            valid_values = position_peers[metric].dropna()
            if len(valid_values) > 1:
                percentile = min(99, (valid_values < player_data[metric]).mean() * 100)
                radar_values.append(percentile)
                radar_labels.append(metric.replace('player_season_', '').replace('_', ' ').title())
            
    if radar_values:
        # Close the radar chart
        radar_values.append(radar_values[0])
        radar_labels.append(radar_labels[0])
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=radar_values,
            theta=radar_labels,
            fill='toself',
            name=selected_player,
            line_color='#22c55e',
            fillcolor='rgba(34, 197, 94, 0.3)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(color='white'),
                    gridcolor='rgba(255,255,255,0.3)'
                ),
                angularaxis=dict(
                    tickfont=dict(color='white', size=10),
                    gridcolor='rgba(255,255,255,0.3)'
                ),
                bgcolor='rgba(30, 64, 175, 0.8)'
            ),
            showlegend=True,
            title=dict(
                text=f"{selected_player} - Performance Percentiles",
                font=dict(color='white', size=16),
                x=0.5
            ),
            paper_bgcolor='rgba(30, 58, 138, 0.9)',
            plot_bgcolor='rgba(30, 64, 175, 0.8)',
            font=dict(color='white'),
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Not enough valid data to create radar chart.")
else:
    st.info("Select at least 3 metrics to display radar chart.")

# Position Comparison Section
st.header("Position Comparison")

comparison_col1, comparison_col2 = st.columns(2)

with comparison_col1:
    if selected_metrics:
        comparison_metric = st.selectbox("Select metric for comparison", selected_metrics)
        
        if comparison_metric in position_peers.columns:
            # Create histogram
            valid_data = position_peers[comparison_metric].dropna()
            
            if len(valid_data) > 1:
                fig_hist = go.Figure()
                
                fig_hist.add_trace(go.Histogram(
                    x=valid_data,
                    nbinsx=20,
                    name='Position Peers',
                    marker_color='rgba(59, 130, 246, 0.7)',
                    opacity=0.7
                ))
                
                # Add player marker
                if comparison_metric in player_data.index and pd.notna(player_data[comparison_metric]):
                    player_value = player_data[comparison_metric]
                    fig_hist.add_vline(
                        x=player_value,
                        line_dash="dash",
                        line_color="#22c55e",
                        line_width=3,
                        annotation_text=f"{selected_player}: {player_value:.2f}",
                        annotation_position="top"
                    )
                
                fig_hist.update_layout(
                    title=f"{comparison_metric.replace('player_season_', '').replace('_', ' ').title()} Distribution",
                    xaxis_title="Value",
                    yaxis_title="Frequency",
                    paper_bgcolor='rgba(30, 58, 138, 0.9)',
                    plot_bgcolor='rgba(30, 64, 175, 0.8)',
                    font=dict(color='white'),
                    height=400
                )
                
                st.plotly_chart(fig_hist, use_container_width=True)
            else:
                st.warning("Not enough data for comparison.")

with comparison_col2:
    # Top performers in position
    if selected_metrics:
        top_metric = st.selectbox("Show top performers by", selected_metrics, key="top_performers")
        
        if top_metric in position_peers.columns:
            top_performers = position_peers.nlargest(10, top_metric)[['player_name', 'team_name', top_metric]]
            
            if not top_performers.empty:
                st.subheader(f"Top 10 - {top_metric.replace('player_season_', '').replace('_', ' ').title()}")
                
                for idx, (_, row) in enumerate(top_performers.iterrows(), 1):
                    player_name = row['player_name']
                    team_name = row.get('team_name', 'N/A')
                    value = row[top_metric]
                    
                    # Highlight selected player
                    if player_name == selected_player:
                        st.markdown(f"**{idx}. {player_name}** ({team_name}) - **{value:.2f}** ⭐")
                    else:
                        st.markdown(f"{idx}. {player_name} ({team_name}) - {value:.2f}")

# Footer
st.markdown("---")
st.markdown("**Data Source:** StatsBomb | **Dashboard:** Bristol Rovers Analytics")
