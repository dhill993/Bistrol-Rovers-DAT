import streamlit as st
import pandas as pd
import statsbombpy as sb
from mplsoccer import PyPizza
from matplotlib.patches import Patch,Circle
import matplotlib.pyplot as plt
from utilities.utils import get_metrics_by_position
from utilities.utils import get_player_metrics_percentile_ranks
from utilities.utils import custom_fontt

def create_pizza_chart(complete_data,league_name,season, player_name, position, api="statbomb"):
    position_specific_metric = get_metrics_by_position(position, api)

    if position == 'Number 6' and api=='statbomb':
        position = 'Number 8'

    if (position == 'Number 8' or position == 'Number 10') and api=='wyscout':
        position = 'Number 6'

    if league_name not in ['All', '']:
        complete_data = complete_data[complete_data['League'] == league_name]    
    if season!='':
        complete_data = complete_data[complete_data['Season']==season]

    player_df_before = complete_data[complete_data['Player Name'] == player_name]    

    player_df = get_player_metrics_percentile_ranks(complete_data, player_name, position, position_specific_metric)
    if player_df is None or player_df.empty:
        st.error(f'Player {player_name} not found.')
        return None

    params = position_specific_metric
    values = []
    for param in params:
        if param in player_df.columns:
            values.append(player_df[param].iloc[0])
        else:
            values.append(0)

    slice_colors = ["#1A78CF"] * len(params)
    text_colors = ["#000000"] * len(params)

    baker = PyPizza(
        params=params,
        background_color="#F2F2F2",
        straight_line_color="#EBEBE9",
        straight_line_lw=1,
        last_circle_color="#EBEBE9",
        last_circle_lw=1,
        other_circle_lw=0,
        inner_circle_size=20
    )

    font_size = 12 if api == "statbomb" else 8

    fig, ax = baker.make_pizza(
        values,
        figsize=(8, 8.5),
        color_blank_space="same",
        slice_colors=slice_colors,
        value_colors=text_colors,
        value_bck_colors=slice_colors,
        blank_alpha=0.4,
        kwargs_slices=dict(edgecolor="#F2F2F2", linewidth=1),
        kwargs_params=dict(color="#000000", fontsize=font_size, fontproperties=custom_fontt.prop, va="center"),
        kwargs_values=dict(color="#000000", fontsize=font_size, fontproperties=custom_fontt.prop, zorder=3,
                          bbox=dict(edgecolor="#000000", facecolor="cornflowerblue", boxstyle="round,pad=0.2", lw=1))
    )

    fig.text(0.515, 0.975, f"{player_name} - {position}", size=16, fontproperties=custom_fontt.prop, ha="center", color="#000000")
    fig.text(0.515, 0.953, "Percentile Rank vs. Positional Peers", size=13, fontproperties=custom_fontt.prop, ha="center", color="#000000")
    
    CREDIT_1 = f"data: {api}"
    CREDIT_2 = "inspired by: @Worville, @FootballSlices, @somazerofc & @Soumyaj15209314"
    fig.text(0.99, 0.02, f"{CREDIT_1}\n{CREDIT_2}", size=9, fontproperties=custom_fontt.prop, color="#000000", ha="right")

    return fig
@st.cache_data
def get_statsbomb_data():
    try:
        creds = {"user": st.secrets["SB_USERNAME"], "passwd": st.secrets["SB_PASSWORD"]}
        competitions = sb.competitions(creds=creds)
        dataframes = []
        
        for _, comp in competitions.iterrows():
            comp_id = comp['competition_id']
            season_id = comp['season_id']
            
            try:
                df = sb.player_season_stats(comp_id, season_id, creds=creds)
                df['League'] = comp['competition_name']
                df['Season'] = comp['season_name']
                dataframes.append(df)
            except Exception as e:
                st.warning(f"Could not load data for {comp['competition_name']} {comp['season_name']}: {str(e)}")
                continue
        
        return pd.concat(dataframes, ignore_index=True) if dataframes else pd.DataFrame()
    
    except Exception as e:
        st.error(f"Error loading StatsBomb data: {str(e)}")
        return pd.DataFrame()

def process_wyscout_files(uploaded_files):
    dataframes = []
    for file in uploaded_files:
        df = pd.read_excel(file)
        df.columns = df.columns.str.strip()
        dataframes.append(df)
    return pd.concat(dataframes, ignore_index=True) if dataframes else pd.DataFrame()

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()

st.title("Player Profile Dashboard")

# Data source selection
data_source = st.selectbox("Select Data Source", ["StatsBomb", "Upload Wyscout Files"])

if data_source == "StatsBomb":
    if st.button("Load StatsBomb Data"):
        with st.spinner("Loading StatsBomb data..."):
            df = get_statsbomb_data()
            st.session_state.df = df
            if not df.empty:
                st.success(f"Loaded {len(df)} player records")
    df = st.session_state.df

elif data_source == "Upload Wyscout Files":
    uploaded_files = st.file_uploader("Upload Wyscout Excel files", type=['xlsx'], accept_multiple_files=True)
    if uploaded_files:
        with st.spinner("Processing uploaded files..."):
            df = process_wyscout_files(uploaded_files)
            st.session_state.df = df
            if not df.empty:
                st.success(f"Loaded {len(df)} player records")
    df = st.session_state.df
# Only show filters if we have data
if not df.empty:
    st.markdown("---")
    
    # League and Season filters
    col1, col2 = st.columns(2)
    
    with col1:
        available_leagues = df['League'].dropna().unique() if 'League' in df.columns else ['All Leagues']
        selected_league = st.selectbox("League", ['All'] + list(available_leagues))
        league_df = df[df['League'] == selected_league] if selected_league != 'All' and 'League' in df.columns else df
    
    with col2:
        available_seasons = league_df['Season'].dropna().unique() if 'Season' in league_df.columns else ['All Seasons']
        selected_season = st.selectbox("Season", ['All'] + list(available_seasons))
        filtered_df = league_df[league_df['Season'] == selected_season] if selected_season != 'All' and 'Season' in league_df.columns else league_df

    st.markdown("---")
    
    # Player selection and profile
    if not filtered_df.empty:
        # Determine column names - ROBUST APPROACH
        player_col = None
        team_col = None
        pos_col = None
        
        # Find player column
        player_columns = ['player_name', 'Player Name', 'Player', 'player', 'name']
        for col_name in player_columns:
            if col_name in filtered_df.columns:
                player_col = col_name
                break
        
        # Find team column
        team_columns = ['team_name', 'Team', 'team', 'Club', 'club']
        for col_name in team_columns:
            if col_name in filtered_df.columns:
                team_col = col_name
                break
        
        # Find position column
        position_columns = ['primary_position_name', 'Position', 'position', 'pos', 'Primary Position']
        for col_name in position_columns:
            if col_name in filtered_df.columns:
                pos_col = col_name
                break
        
        # Player, Team, Position filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if player_col:
                available_players = ['Select Player'] + list(filtered_df[player_col].dropna().unique())
                selected_player = st.selectbox("Player", available_players)
            else:
                st.error("No player column found in data")
                selected_player = 'Select Player'
        
        with col2:
            if team_col:
                available_clubs = filtered_df[team_col].dropna().unique()
                selected_club = st.selectbox("Club", ['All'] + list(available_clubs))
            else:
                st.warning("No team column found")
                selected_club = 'All'
        
        with col3:
            if pos_col:
                available_positions = filtered_df[pos_col].dropna().unique()
                selected_position = st.selectbox("Position", ['All'] + list(available_positions))
            else:
                st.warning("No position column found")
                selected_position = 'All'
        
        # FIXED APPROACH: Get player data first, then extract position
        if selected_player != 'Select Player' and player_col:
            # Filter by player first (robust approach from pizza chart)
            player_data_df = filtered_df[filtered_df[player_col] == selected_player]
            
            if not player_data_df.empty:
                # Get the first matching player record
                player_data = player_data_df.iloc[0]
                
                # Extract position from player record
                player_position = None
                if pos_col and pos_col in player_data.index:
                    player_position = player_data[pos_col]
                
                # Apply additional filters if specified
                display_df = player_data_df.copy()
                
                if selected_club != 'All' and team_col and team_col in display_df.columns:
                    display_df = display_df[display_df[team_col] == selected_club]
                
                if selected_position != 'All' and pos_col and pos_col in display_df.columns:
                    display_df = display_df[display_df[pos_col] == selected_position]
                
                if not display_df.empty:
                    # Display player info
                    st.markdown("### Player Profile")
                    
                    # Basic info
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Player", selected_player)
                    
                    with col2:
                        team_name = player_data.get(team_col, 'N/A') if team_col and team_col in player_data.index else 'N/A'
                        st.metric("Team", team_name)
                    
                    with col3:
                        position_display = player_position if player_position else 'N/A'
                        st.metric("Position", position_display)
                    
                    with col4:
                        minutes_cols = ['minutes_played_overall', 'Minutes played', 'minutes', 'Minutes']
                        minutes_played = 0
                        for min_col in minutes_cols:
                            if min_col in player_data.index and pd.notna(player_data[min_col]):
                                minutes_played = int(player_data[min_col])
                                break
                        st.metric("Minutes Played", minutes_played)
                    
                    # Show player stats table
                    st.markdown("### Player Statistics")
                    
                    # Create a clean display dataframe
                    display_data = display_df.copy()
                    
                    # Remove system columns and keep only relevant stats
                    cols_to_remove = ['Unnamed: 0', 'index', 'level_0']
                    for col in cols_to_remove:
                        if col in display_data.columns:
                            display_data = display_data.drop(columns=[col])
                    
                    # Display the dataframe
                    st.dataframe(display_data.T, use_container_width=True)
                    # Pizza Chart Section
                    if player_position:
                        st.markdown("### Pizza Chart")
                        
                        api_type = "statbomb" if data_source == "StatsBomb" else "wyscout"
                        
                        if st.button("Generate Pizza Chart"):
                            with st.spinner("Generating pizza chart..."):
                                try:
                                    # Use the complete dataset for percentile calculations
                                    complete_data = st.session_state.df.copy()
                                    
                                    # Ensure Player Name column exists for pizza chart
                                    if player_col != 'Player Name':
                                        complete_data['Player Name'] = complete_data[player_col]
                                    
                                    fig = create_pizza_chart(
                                        complete_data=complete_data,
                                        league_name=selected_league if selected_league != 'All' else '',
                                        season=selected_season if selected_season != 'All' else '',
                                        player_name=selected_player,
                                        position=player_position,
                                        api=api_type
                                    )
                                    
                                    if fig:
                                        st.pyplot(fig)
                                        st.success("Pizza chart generated successfully!")
                                    else:
                                        st.error("Could not generate pizza chart")
                                        
                                except Exception as e:
                                    st.error(f"Error generating pizza chart: {str(e)}")
                                    st.write("Debug info:")
                                    st.write(f"Player: {selected_player}")
                                    st.write(f"Position: {player_position}")
                                    st.write(f"API: {api_type}")
                    else:
                        st.info("Position information needed for pizza chart generation")
                else:
                    st.warning("No data found for the selected filters")
            else:
                st.warning("Player not found in filtered data")
        else:
            st.info("Please select a player to view their profile")
    else:
        st.warning("No data available after applying filters")
else:
    st.info("Please load data to begin analysis")
