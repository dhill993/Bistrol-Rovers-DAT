import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# -----------------------
# Compare Players Function
# -----------------------
def compare_players(filtered_df, available_metrics, metric_display_names):
    st.markdown("## 📊 Compare Players")

    # Player multi-select
    players = sorted(filtered_df['player_name'].unique().tolist())
    selected_players = st.multiselect("Select up to 3 players to compare", players, max_selections=3)

    if not selected_players or len(selected_players) < 2:
        st.info("Please select at least 2 players to compare.")
        return

    # Metric multi-select
    selected_metrics = st.multiselect(
        "Choose metrics to compare (up to 10):",
        options=available_metrics,
        default=available_metrics[:10],
        format_func=lambda x: metric_display_names.get(x, x)
    )

    if not selected_metrics:
        st.warning("Please select at least one metric.")
        return

    # Filter selected players
    comparison_data = filtered_df[filtered_df['player_name'].isin(selected_players)]

    # Display player cards side-by-side
    cols = st.columns(len(selected_players))

    for i, player in enumerate(selected_players):
        with cols[i]:
            player_row = comparison_data[comparison_data['player_name'] == player].iloc[0]

            st.markdown(f"### {player}")
            st.markdown(f"**Club:** {player_row['team_name']}")
            st.markdown(f"**Age:** {player_row['player_age']}")
            st.markdown(f"**Minutes:** {int(player_row['player_season_minutes']):,}")

            for metric in selected_metrics:
                value = player_row.get(metric, None)

                try:
                    val_display = f"{value:.2f}" if isinstance(value, float) else str(value)
                    bg_color = "#16a34a" if isinstance(value, (int, float)) and value >= 1 else "#1e3a8a"
                except:
                    val_display = "N/A"
                    bg_color = "#6b7280"

                st.markdown(f"""
                    <div style="background-color:{bg_color};padding:6px;border-radius:6px;
                                margin-bottom:6px;color:white;text-align:center;">
                        <strong>{metric_display_names.get(metric, metric)}</strong><br>{val_display}
                    </div>
                """, unsafe_allow_html=True)


# -----------------------
# Streamlit App Layout
# -----------------------
st.set_page_config(layout="wide")

st.title("⚽ Player Performance Dashboard")

# Sample Data Load (Replace with your own DataFrame loading logic)
@st.cache_data
def load_data():
    return pd.read_csv("your_cleaned_stats_data.csv")

df = load_data()

if not df.empty:
    # Filtering example
    selected_league = st.selectbox("League", sorted(df['league'].unique()))
    selected_season = st.selectbox("Season", sorted(df['season'].unique(), reverse=True))
    filtered_df = df[(df['league'] == selected_league) & (df['season'] == selected_season)]

    available_metrics = [col for col in df.columns if col.startswith('player_season_') and df[col].dtype in [np.float64, np.int64]]
    metric_display_names = {
        metric: metric.replace('player_season_', '').replace('_', ' ').title()
        for metric in available_metrics
    }

    tab1, tab2 = st.tabs(["📋 Player Profile", "📊 Compare Players"])

    with tab1:
        players = ['Select a player'] + sorted(filtered_df['player_name'].unique().tolist())
        selected_player = st.selectbox("Select Player", players)

        if selected_player != "Select a player":
            player_data = filtered_df[filtered_df['player_name'] == selected_player].iloc[0]
            player_position = player_data.get('mapped_position', 'Unknown')

            st.markdown("### Select Metrics (Min: 10, Max: 15)")
            selected_metrics = st.multiselect(
                "Choose metrics to analyze:",
                options=available_metrics,
                format_func=lambda x: metric_display_names[x],
                help="Select between 10 and 15 metrics for analysis"
            )

            if len(selected_metrics) < 10:
                st.warning(f"Please select at least 10 metrics. Currently selected: {len(selected_metrics)}")
            elif len(selected_metrics) > 15:
                st.warning(f"Please select maximum 15 metrics. Currently selected: {len(selected_metrics)}")
            else:
                st.success(f"✅ {len(selected_metrics)} metrics selected")

                position_df = filtered_df[filtered_df['mapped_position'] == player_position]

                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.subheader(f"Player Profile: {selected_player} - {player_position}")

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

                    st.info(f"Percentiles calculated against {len(position_df)} players in {player_position} position")

                else:
                    st.warning("No valid data for selected metrics")

                st.markdown("</div>", unsafe_allow_html=True)

                # KPI Cards
                col1, col2, col3, col4 = st.columns(4)

                overall_rank = np.mean(values) if values else 0
                minutes_played = int(player_data.get('player_season_minutes', 0))
                metrics_above_70 = sum(1 for v in values if v >= 70)

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
                        <div class="metric-title">Elite Metrics</div>
                        <div class="metric-value">{metrics_above_70}</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col4:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Minutes</div>
                        <div class="metric-value">{minutes_played:,}</div>
                    </div>
                    """, unsafe_allow_html=True)

    with tab2:
        compare_players(filtered_df, available_metrics, metric_display_names)
