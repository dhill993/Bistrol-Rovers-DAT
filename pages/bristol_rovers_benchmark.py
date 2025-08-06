import streamlit as st
import pandas as pd

# Example: Load dataframe
# df = your_processed_df

st.title("Bristol Rovers Benchmark - Flexible Position & Player Selection")

# Position selector
position_types = list(position_metrics.keys())
selected_position = st.selectbox("Select Position Type", position_types)

# Filter Bristol Rovers players by selected position & season
filtered_df = df[
    (df["club"] == "Bristol Rovers") &
    (df["season"] == "2025/26") &
    (df["position"] == selected_position)
]

if filtered_df.empty:
    st.warning(f"No Bristol Rovers players found for {selected_position} in 2025/26.")
else:
    # Player selector for filtered players
    players = filtered_df["player_name"].unique()
    selected_player = st.selectbox("Select Player", players)
    
    # Retrieve player row
    player_row = filtered_df[filtered_df["player_name"] == selected_player].iloc[0]
    
    # Compute league averages for position
    league_avg_df = df[
        (df["position"] == selected_position) & (df["season"] == "2025/26")
    ]
    league_avg = league_avg_df.mean(numeric_only=True)
    
    # Metrics to compare
    metrics = position_metrics[selected_position]
    
    comparison_data = []
    for metric in metrics:
        if metric not in league_avg or metric not in player_row:
            continue  # skip metrics missing in data
        league_value = league_avg[metric]
        player_value = player_row[metric]
        better = player_value > league_value  # customize if lower is better for some
        benchmark = "✅" if better else "❌"
        comparison_data.append({
            "Metric": metric,
            "League Average": round(league_value, 2),
            selected_player: round(player_value, 2),
            "Benchmark +/-": benchmark
        })
    
    comparison_df = pd.DataFrame(comparison_data)

    def highlight_benchmark(val):
        if val == "✅":
            return "background-color: green; color: white"
        elif val == "❌":
            return "background-color: red; color: white"
        return ""

    st.dataframe(comparison_df.style.applymap(highlight_benchmark, subset=["Benchmark +/-"]))
