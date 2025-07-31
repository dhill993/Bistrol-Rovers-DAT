import streamlit as st
from mplsoccer import PyPizza
from matplotlib.patches import Patch, Circle
import matplotlib.pyplot as plt
from utilities.utils import get_metrics_by_position
from utilities.utils import get_player_metrics_percentile_ranks
from utilities.utils import custom_fontt

def create_pizza_chart(complete_data, league_name, season, player_name, position, api="statbomb"):

    # Save original for display if needed
    shown_position = position

    # Handle StatBomb/Wyscout fallback cases
    if api == 'statbomb':
        if position == 'Number 6':
            position = 'Number 8'
        elif position == 'Centre Back':
            position = 'Outside Centre Back'
        elif position == 'Runner':
            position = 'Centre Forward A'
        elif position == 'box to box 8':
            position = 'Number 8'

    elif api == 'wyscout':
        if position in ['Number 8', 'Number 10']:
            position = 'Number 6'
        elif position == 'Outside Centre Back':
            position = 'Centre Back'
        elif position == 'Centre Forward A':
            position = 'Runner'
        elif position == 'Number 8':
            position = 'box to box 8'

    position_specific_metric = get_metrics_by_position(position, api)

    if league_name not in ['All', '']:
        complete_data = complete_data[complete_data['League'] == league_name]
    if season != '':
        complete_data = complete_data[complete_data['Season'] == season]

    player_df_before = complete_data[complete_data['Player Name'] == player_name]

    player_df = get_player_metrics_percentile_ranks(complete_data, player_name, position, position_specific_metric)
    if player_df is None or player_df.empty:
        st.error(f'Player {player_name} not found.')
        return None

    available_metrics = position_specific_metric
    metric_values = player_df[available_metrics].iloc[0].values.tolist()
    if len(available_metrics) != len(metric_values):
        st.error("Metric mismatch error.")
        return None

    slice_colors = []
    for metric in metric_values:
        if metric >= 70:
            slice_colors.append("#58AC4E")
        elif metric >= 50:
            slice_colors.append("#1A78CF")
        else:
            slice_colors.append("#aa42af")

    baker = PyPizza(
        params=available_metrics,
        background_color="#222222",
        straight_line_color="#000000",
        straight_line_lw=1,
        last_circle_color="#000000",
        last_circle_lw=4,
        other_circle_lw=0,
        inner_circle_size=20
    )

    font_size = 12 if api == "statbomb" else 8

    fig, ax = baker.make_pizza(
        metric_values,
        figsize=(9.5, 11),
        color_blank_space="same",
        blank_alpha=0.1,
        slice_colors=slice_colors,
        kwargs_slices=dict(edgecolor="#000000", zorder=2, linewidth=2),
        kwargs_params=dict(color="#F2F2F2", fontsize=font_size, fontproperties=custom_fontt, va="center"),
        kwargs_values=dict(color="#F2F2F2", fontsize=0, alpha=0, fontproperties=custom_fontt, zorder=-5)
    )

    fig.text(
        0.08, 0.94, f"{player_name}", size=25,
        ha="left", fontproperties=custom_fontt, color="#F2F2F2"
    )

    fig.text(
        0.08, 0.92, f"Club: {str(player_df.iloc[0]['Team'])}",
        size=10, ha="left", fontproperties=custom_fontt, color="#F2F2F2", alpha=0.8
    )

    fig.text(
        0.08, 0.90,
        "Percentile Rank vs. Positional Peers",
        size=10, ha="left", fontproperties=custom_fontt, color="#F2F2F2", alpha=0.8
    )

    fig.text(
        0.08, 0.88,
        f"Minutes Played: {int(player_df_before['Minutes'])}  |  Age: {int(player_df_before['Age'])}",
        size=10, ha="left", fontproperties=custom_fontt, color="#F2F2F2", alpha=0.8
    )

    legend_elements = [
        Patch(facecolor="#58AC4E", edgecolor='white', label='>=70%'),
        Patch(facecolor="#1A78CF", edgecolor='white', label='50 - 69%'),
        Patch(facecolor="#aa42af", edgecolor='white', label='<50%')
    ]
    ax.legend(handles=legend_elements, loc='lower right', bbox_to_anchor=(1.25, 0), fontsize=12, frameon=False, labelcolor='white')

    fig.add_artist(plt.Line2D((0, 1.2), (0.87, 0.87), color='white', linewidth=2, alpha=0.8, transform=fig.transFigure))

    circle_params = [
        (0.415, 0.5, 0.5),
        (0.330, 0.5, 0.5),
        (0.245, 0.5, 0.5),
        (0.160, 0.5, 0.5)
    ]
    for radius, x, y in circle_params:
        circle = Circle((x, y), radius, color='black', alpha=0.25, fill=False, zorder=50, linewidth=1.75, transform=ax.transAxes)
        ax.add_patch(circle)

    ax.text(0.5, 0.5 + 0.395, '80', ha='center', va='center', fontsize=13, color='white', alpha=0.325, fontproperties=custom_fontt, transform=ax.transAxes)
    ax.text(0.5, 0.5 + 0.31, '60', ha='center', va='center', fontsize=13, color='white', alpha=0.325, fontproperties=custom_fontt, transform=ax.transAxes)
    ax.text(0.5, 0.5 + 0.225, '40', ha='center', va='center', fontsize=13, color='white', alpha=0.325, fontproperties=custom_fontt, transform=ax.transAxes)
    ax.text(0.5, 0.5 + 0.14, '20', ha='center', va='center', fontsize=13, color='white', alpha=0.325, fontproperties=custom_fontt, transform=ax.transAxes)

    return fig

# ✅ NEW: Helper function to populate the dropdown
def get_all_position_options(complete_data):
    custom_roles = [
        "Winger", "Full Back", "Centre Forward A", "Centre Back", "Number 6",
        "Number 8", "Number 10", "Goal Keeper",
        "Runner", "box to box 8", "Outside Centre Back"
    ]
    existing_positions = list(complete_data['Position'].dropna().unique())
    return sorted(set(custom_roles + existing_positions))
