import streamlit as st
import pandas as pd

# Replace this with loading your real processed dataframe:
# Example placeholder: df = pd.read_csv("path/to/your_bristol_rovers_data.csv")
# The dataframe should contain columns like 'player_name', 'club', 'season', 'position', and the metrics.

# Placeholder for demonstration:
# Remove this block when you load your real data
data = {
    "player_name": ["Player A", "Player B"],
    "club": ["Bristol Rovers", "Bristol Rovers"],
    "season": ["2025/26", "2025/26"],
    "position": ["Wing Back", "No10"],
    "CARRIES": [12.5, 8.3],
    "DRIBBLES STOPPED %": [65, 50],
    "OP XG ASSISTED": [0.1, 0.05],
    "SUCCESSFUL DRIBBLES": [4, 2],
    "SUCCESSFUL CROSSES": [1, 0],
    "BALL RECOVERIES": [8, 5],
    "OP PASSES INTO BOX": [3, 1],
    "PR PASS %": [72, 68],
    "PADJ INTERCEPTIONS": [1.5, 0.7],
    "AERIAL WIN %": [55, 40],
    "SHOTS": [1.2, 2.5],
    "xG": [0.15, 0.35],
    "SCORING CONTRIBUTION": [0.05, 0.2],
}
df = pd.DataFrame(data)

# Your full position metrics dictionary (truncated here for brevity)
position_metrics = {
    "Wing Back": [
        "DRIBBLES STOPPED %", "CARRIES", "OP XG ASSISTED", "SUCCESSFUL DRIBBLES",
        "SUCCESSFUL CROSSES", "BALL RECOVERIES", "OP PASSES INTO BOX", "PR PASS %",
        "PADJ INTERCEPTIONS", "AERIAL WIN %"
    ],
    "No10": [
        "SHOTS", "xG", "SCORING CONTRIBUTION", "PR PASS%", "OP KEY PASSES",
        "SUCCESSFUL DRIBBLES", "PINTIN", "xG ASSISTED", "CARRIES", "SHOOTING %"
    ],
    # Add the rest of your positions...
}

st.title("Bristol Rovers Player Benchmark (2025/26)")

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
    
    # Compute league averages for the selected position
    league_avg_df = df[
        (df["position"] == selected_position) &
        (df["season"] == "2025/26")
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
        better = player_value > league_value
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
