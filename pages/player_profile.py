import sys
import os

# Add the parent directory to sys.path to allow importing from 'utilities'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utilities.utils import get_metrics_by_position, get_weighted_rank, get_player_metrics_percentile_ranks

# Your existing code continues here...
# For example:
# import streamlit as st
# ... rest of your player profile logic

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import numpy as np
from utilities.utils import get_metrics_by_position, get_weighted_rank, get_player_metrics_percentile_ranks
from PIL import Image
import requests
from io import BytesIO

def create_profile_summary_card(data, player_name, league_name, season, position, api="statbomb"):
    # Get weighted rank data including overall scores
    weighted_data = get_weighted_rank(data, player_name, league_name, season, position, api)
    if weighted_data.empty:
        print(f"No weighted rank data for {player_name}")
        return None

    # Get positional percentile ranks for metrics
    position_metrics = get_metrics_by_position(position, api)
    player_percentiles = get_player_metrics_percentile_ranks(data, player_name, position, position_metrics)
    if player_percentiles is None or player_percentiles.empty:
        print(f"No percentile rank data for {player_name}")
        return None

    # Extract main info
    player_info = weighted_data.iloc[0]
    percentile_values = player_percentiles[position_metrics].iloc[0].values
    metrics_labels = position_metrics

    # Basic figure setup
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_facecolor("#121212")
    plt.axis('off')

    # Background box
    ax.add_patch(Rectangle((0, 0), 1, 1, color="#222222", zorder=0))

    # Title and player info
    ax.text(0.05, 0.9, player_info['Player Name'], fontsize=22, fontweight='bold', color='white')
    ax.text(0.05, 0.85, f"Club: {player_info['Team']}", fontsize=12, color='lightgray')
    ax.text(0.05, 0.82, f"Position: {position}", fontsize=12, color='lightgray')
    ax.text(0.05, 0.78, f"Age: {int(player_info['Age'])}  |  Minutes: {int(player_info['Minutes'])}", fontsize=12, color='lightgray')

    # Show overall score and weighted score as bars
    overall_score = player_info['Overall Score']
    weighted_score = player_info['Score weighted aganist League One']

    max_score = 100  # assuming percentile scale max 100
    bar_width = 0.8

    # Bar background
    ax.barh(0.6, max_score, color="#333333", height=0.06)
    # Overall score bar
    ax.barh(0.6, overall_score, color="#1A78CF", height=0.06)
    ax.text(overall_score + 2, 0.6, f"Overall Score: {overall_score:.1f}", va='center', color='white', fontsize=11)

    # Weighted score bar
    ax.barh(0.5, max_score, color="#333333", height=0.06)
    ax.barh(0.5, weighted_score, color="#58AC4E", height=0.06)
    ax.text(weighted_score + 2, 0.5, f"Weighted Score: {weighted_score:.1f}", va='center', color='white', fontsize=11)

    # Draw percentile metric bars
    start_y = 0.3
    bar_height = 0.04
    gap = 0.05

    colors = []
    for v in percentile_values:
        if v >= 70:
            colors.append("#58AC4E")  # green
        elif v >= 50:
            colors.append("#1A78CF")  # blue
        else:
            colors.append("#aa42af")  # purple

    for i, (metric, val) in enumerate(zip(metrics_labels, percentile_values)):
        y = start_y - i * gap
        ax.text(0.05, y + bar_height/2, metric, color='white', fontsize=9, va='center')
        ax.barh(y, val, color=colors[i], height=bar_height)
        ax.barh(y, 100, color="#333333", height=bar_height, alpha=0.3)  # background bar for scale
        ax.text(val + 2, y + bar_height/2, f"{val:.0f}%", color='white', fontsize=9, va='center')

    # Legend for percentile colors
    legend_labels = [">= 70%", "50-69%", "< 50%"]
    legend_colors = ["#58AC4E", "#1A78CF", "#aa42af"]
    legend_x = 0.6
    legend_y = 0.9
    for c, label in zip(legend_colors, legend_labels):
        ax.add_patch(Rectangle((legend_x, legend_y), 0.04, 0.04, color=c))
        ax.text(legend_x + 0.05, legend_y + 0.02, label, fontsize=10, color='white', va='center')
        legend_y -= 0.06

    # Optional: Load player image or club badge (requires URL or local path)
    # Example placeholder (you can replace with actual image fetch logic)
    # img_url = "https://path.to/player_image.jpg"
    # response = requests.get(img_url)
    # img = Image.open(BytesIO(response.content))
    # ax.imshow(img, extent=[0.7, 0.95, 0.65, 0.9], aspect='auto')

    plt.tight_layout()
    return fig

