################################################################################
# pages/Player Profile.py
#
# One–page interactive player profile:
# – Sidebar: pick the data source + player
# – Header: player photo & bio details
# – Column 1: radar + stat bars
# – Column 2: four‑quadrant scatter matrix (benchmark vs league peers)
################################################################################
import streamlit as st
import pandas as pd
import plotly.express as px
from mplsoccer import Radar, FontManager
from PIL import Image
import io, requests, textwrap
from utils import (
    get_metrics_by_position,                     # ← you already have these
    get_player_metrics_percentile_ranks,
    get_avg_metrics_percentile_ranks,
)

# ------------------------------------------------------------------#
# 1.  DATA SOURCES  ──────────────────────────────────────────────── #
# ------------------------------------------------------------------#
# NB: we import lazily so the API call runs only when the page is open
@st.cache_data(ttl=14_400, show_spinner=False)
def load_statbomb_df():
    from data.retrieve_statbomb_data import get_statsbomb_player_season_stats
    return get_statsbomb_player_season_stats()

@st.cache_data(ttl=14_400, show_spinner=False)
def load_wyscout_df():
    from data.retrieve_wyscout_data import get_wyscout_player_season_stats
    return get_wyscout_player_season_stats()

def get_df(api_name):
    return load_statbomb_df() if api_name == "Statbomb" else load_wyscout_df()

# ------------------------------------------------------------------#
# 2.  SIDEBAR CONTROLS  ──────────────────────────────────────────── #
# ------------------------------------------------------------------#
st.set_page_config(page_title="Player Profile", layout="wide")

with st.sidebar:
    api_name = st.selectbox("Data source", ["Statbomb", "Wyscout"])
    df = get_df(api_name)

    # Dynamic filters: League ▸ Season ▸ Position ▸ Player
    league  = st.selectbox("League",   ["All", *sorted(df["League"].unique())])
    season  = st.selectbox("Season",   ["", *sorted(df["Season"].unique(), reverse=True)])
    pos_raw = st.selectbox("Position", sorted(df["Position"].unique()))

    # Get the list of players after filters via your helper
    from utils import get_players_by_position
    plyr_list = get_players_by_position(df, league, season, pos_raw)
    player = st.selectbox("Player", plyr_list)

# Slice the DataFrame for convenience
player_row = df[df["Player Name"] == player].iloc[0]  # Series
pos_df     = df[df["Position"] == pos_raw]            # peer group

# ------------------------------------------------------------------#
# 3.  HEADER  ────────────────────────────────────────────────────── #
# ------------------------------------------------------------------#
st.markdown("## {}  ({})".format(player_row["Player Name"], pos_raw))

col_img, col_meta = st.columns([1, 3], gap="medium")

with col_img:
    # If you don’t have portraits locally, you can hit an external URL.
    # Placeholder fallback: club badge or silhouette.
    try:
        img_url = f"https://media.api-sports.io/football/players/{player_row['Player Name']}.png"
        img     = Image.open(requests.get(img_url, stream=True).raw)
    except Exception:
        img     = Image.open("data/bristol-rovers.svg")   # fallback
    st.image(img, width=180)

with col_meta:
    contract = player_row.get("Contract", "N/A")
    value    = player_row.get("xTV", "N/A")
    mins     = player_row["Minutes"]
    age      = int(player_row["Age"])
    club     = player_row["Team"]
    st.write(f"**Club:** {club}")
    st.write(f"**Age:** {age}")
    st.write(f"**Contract exp.:** {contract}")
    st.write(f"**Transfer value (xTV):** {value}")
    st.write(f"**2024‑25 minutes played:** {mins:,}")

# ------------------------------------------------------------------#
# 4.  LAYOUT = 2 COLUMNS  ────────────────────────────────────────── #
# ------------------------------------------------------------------#
left, right = st.columns([1.1, 1], gap="large")

# ------------ 4A. Radar & Stat Bars (LEFT) ------------------------ #
with left:
    st.subheader("Skill radar vs positional peers")

    # Metrics used for *this* position
    metrics = get_metrics_by_position(pos_raw, api=api_name.lower())
    player_pct = get_player_metrics_percentile_ranks(pos_df, player, pos_raw, metrics)
    avg_pct    = get_avg_metrics_percentile_ranks(pos_df, pos_raw)

    # Prepare radar values
    plyr_vals = player_pct[metrics].values.flatten().tolist()
    peer_vals = avg_pct[metrics].values.flatten().tolist()

    # Radar chart (mplsoccer)
    radar = Radar(
        metrics,
        min_range=[0]*len(metrics),
        max_range=[100]*len(metrics),
        round_int=[False]*len(metrics),
        fontfamily="Alexandria",  # your custom font if registered
    )
    fig, ax = radar.setup_radar(figsize=(6, 6))
    radar.draw_circular(ax,                fc="#0b2eca0d", ec="#0b2eca40", lw=1)
    radar.draw_radar(plyr_vals,            ax=ax, fc="#0B2ECA80", ec="#0B2ECA", lw=2, zorder=2, label=player)
    radar.draw_radar(peer_vals,            ax=ax, fc="#AAAAAA40", ec="#AAAAAA", lw=1, zorder=1, label="Pos Avg")
    ax.legend(loc="upper right", fontsize=8)
    st.pyplot(fig, use_container_width=True)

    # --- Stat bars (same 3 groups as in your example) -------------
    st.markdown("##### In‑Possession Metrics")
    cols = st.columns(3)
    for i, m in enumerate(metrics[:len(metrics)//3]):
        cols[i%3].metric(label=m, value=f"{player_row[m]:.2f}")

    st.markdown("##### Out‑Of‑Possession Metrics")
    cols2 = st.columns(3)
    for i, m in enumerate(metrics[len(metrics)//3:2*len(metrics)//3]):
        cols2[i%3].metric(label=m, value=f"{player_row[m]:.2f}")

    st.markdown("##### Defensive / Other")
    cols3 = st.columns(3)
    for i, m in enumerate(metrics[2*len(metrics)//3:]):
        cols3[i%3].metric(label=m, value=f"{player_row[m]:.2f}")

# ------------ 4B. Quadrant Scatter Matrix (RIGHT) ---------------- #
with right:
    st.subheader("Quadrant benchmarks")

    # Helper to reduce repeated code
    def quadrant(fig_title, x_col, y_col, x_label=None, y_label=None):
        fig = px.scatter(
            pos_df,
            x=x_col,
            y=y_col,
            opacity=0.6,
            height=320,
            width=320,
        )
        # highlight the chosen player
        fig.add_scatter(
            x=[player_row[x_col]], y=[player_row[y_col]],
            mode="markers+text",
            text=[player.split(" ")[-1]],  # surname as label
            textposition="top center",
            marker=dict(size=12, color="#0B2ECA"),
            showlegend=False
        )
        fig.update_layout(
            title=dict(text=fig_title, x=0.5, font=dict(size=14)),
            margin=dict(l=10, r=10, t=25, b=0),
        )
        fig.update_xaxes(title=x_label or x_col)
        fig.update_yaxes(title=y_label or y_col)
        st.plotly_chart(fig, use_container_width=True)

    # —— build the 2×2 grid of scatters
    quad1, quad2 = st.columns(2)
    with quad1:
        quadrant("Finishing", "NP Goals", "xG")
        quadrant("Progression", "Progressive Runs", "Progressive Passes")
    with quad2:
        quadrant("Creativity", "xG Assisted", "OP Key Passes")
        quadrant("Dribbling", "Successful Dribbles", "Fouls Won")

# ------------------------------------------------------------------#
# 5.  HEATMAP (Optional)  ────────────────────────────────────────── #
# ------------------------------------------------------------------#
st.divider()
st.subheader("Touch heat‑map (all comps, 2024‑25)")

# If you save heatmaps to disk, put the relative path in the dataframe (e.g. "heatmaps/rak‑sakyi.png").
heatmap_path = player_row.get("heatmap_path", None)
if heatmap_path and st.session_state.get("show_heatmaps", True):
    st.image(Image.open(heatmap_path), width=600)
else:
    st.info("No heat‑map available for this player.")
