# Create friendly names for metrics
available_metrics = get_available_metrics(filtered_df)
metric_display_names = {
    metric: metric.replace('player_season_', '').replace('_', ' ').title()
    for metric in available_metrics
}

tab1, tab2 = st.tabs(["📋 Player Profile", "📊 Compare Players"])

with tab1:
    # Player selection
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

                st.info(f"Percentiles calculated against {len(position_df)} players in {player_position} position")

            else:
                st.warning("No valid data for selected metrics")

            st.markdown("</div>", unsafe_allow_html=True)

            # KPI cards
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
