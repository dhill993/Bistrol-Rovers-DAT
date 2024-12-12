import streamlit as st
from utilities.utils import get_players_by_position, get_metrics_by_position
from visualizations.radar_chart import create_radar_chart
from visualizations.pizza_chart import create_pizza_chart
from visualizations.overall_rank import create_rank_visualization
from visualizations.scatter_plot import create_scatter_chart
from visualizations.zscore_ranking import top_10_players_by_profile
from visualizations.similarity_chart import filter_similar_players
from utilities.wyscout_default_metrics import profiles_zcore as profiles
from st_pages import show_pages_from_config
from data.retrieve_wyscout_data import get_wyscout_player_season_stats

show_pages_from_config()
st.set_page_config(
    page_title='Bristol Rovers - Recruitment Data Hub',
    page_icon='💹',
    layout="wide",
    initial_sidebar_state="expanded"
)
# Define your HTML and CSS styling
st.markdown("""
    <style>
        .title-container {
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 20px;
            flex-wrap: wrap; /* Allows elements to wrap on smaller screens */
        }
        
        .logo {
            width: 60px; /* Adjust logo size */
            height: auto;
            margin-right: 12px; /* Space between logo and title */
        }
        
        .title {
            font-size: 36px;
            font-weight: bold;
            color: #014FFF; /* Custom color for the title */
            white-space: nowrap; /* Prevents the title from breaking into multiple lines */
        }

        /* Media query for small screens (mobile devices) */
        @media (max-width: 600px) {
            .title-container {
                justify-content: center;
                text-align: center; /* Centers the title and logo */
            }

            .logo {
                width: 50px; /* Adjust logo size for smaller screens */
                margin-right: 8px; /* Reduce space between logo and title */
            }

            .title {
                font-size: 18px; /* Smaller font size for mobile */
                text-align: center; /* Centers the title on smaller screens */
            }
        }
    </style>

    <div class="title-container">
        <img src="https://www.bristolrovers.co.uk/themes/custom/bristol/files/bristol-rovers.svg" class="logo" alt="Logo">
        <span class="title">Bristol Rovers - Recruitment Data Hub</span>
    </div>
""", unsafe_allow_html=True)


st.markdown("")
wyscout_data = []
with st.spinner("Retrieving data from wyscout api"):
    wyscout_data = get_wyscout_player_season_stats()
playing_positions = list(wyscout_data['Position'].unique())
playing_positions.append('Number 8')
playing_positions.append('Number 10')
leagues = list(wyscout_data['League'].unique())
leagues.append('All')
seasons = list(wyscout_data['Season'].unique())

with st.expander("Expand to view pizza chart", expanded=False):
    league = st.selectbox('Select League:',leagues[::-1], index=0, key='pizza_lague')
    season = st.selectbox('Select Season:', seasons, index=0, key='pizza_seaosn')

    position = st.selectbox('Select Playing Position:', playing_positions, index=0, key='pizza_pos')
    if position in ['Number 8', 'Number 10'] :
        player_name = st.selectbox('Select Player:', get_players_by_position(wyscout_data, league,season,'Number 6'), index=0, key='pizza_player')
    else:
        player_name = st.selectbox('Select Player:', get_players_by_position(wyscout_data, league,season,position), index=0, key='pizza_player')

    # Button to generate pizza chart
    if st.button('Generate Pizza Chart'):
        try:
            fig_pizza = create_pizza_chart(wyscout_data, league,season, player_name, position, 'wyscout')
            if fig_pizza is not None:
                st.pyplot(fig_pizza)  # Display the pizza chart
        except Exception as e:
            st.error(f"Error : {e}")

with st.expander("Expand to view player comparison radar chart", expanded=False):

    league = st.selectbox('Select League:',leagues[::-1], index=0, key='radar_lague')
    season = st.selectbox('Select Season:', seasons, index=0, key='radar_seaosn')

    position = st.selectbox('Select Playing Position:', playing_positions, index=0, key='radar_positon')
    if position in ['Number 8', 'Number 10'] :
        player_name = st.selectbox('Select Player:', get_players_by_position(wyscout_data, league,season,'Number 6'), index=0, key='radar_player')
    else:
        player_name = st.selectbox('Select Player:', get_players_by_position(wyscout_data, league,season,position), index=0, key='radar_player')


    # Button to generate pizza chart
    if st.button('Generate Radar Chart'):
        try:
            fig_radar = create_radar_chart(wyscout_data, league,player_name, position,season, "wyscout")
            if fig_radar is not None:
                st.pyplot(fig_radar)  # Display the pizza chart
        except Exception as e:
            st.error(f"Error : {e}")

with st.expander("Expand to view scatter plot", expanded=False):


    league = st.selectbox('Select League:',leagues[::-1], index=0, key='scatter_lague')
    season = st.selectbox('Select Season:', seasons, index=0, key='scatter_seaosn')

    position = st.selectbox('Select Playing Position:', playing_positions, index=0, key='scatter_pos')
    if position in ['Number 8', 'Number 10'] :
        player_name = st.selectbox('Select Player:', get_players_by_position(wyscout_data, league,season,'Number 6'), index=0, key='scataer_player')
    else:
        player_name = st.selectbox('Select Player:', get_players_by_position(wyscout_data, league,season,position), index=0, key='scataer_player')


    # age_range = st.slider("Select Age Range", min_value=int(df['Age'].min()), max_value=int(df['Age'].max()), 
    #                       value=(int(df['Age'].min()), int(df['Age'].max())))


    age_range = st.slider("Select Age Range", min_value=int(18), max_value=int(50), 
                          value=(int(18), int(50)))

    minutes_range = st.slider("Select Minutes Played Range", min_value=150, 
                               max_value=int(wyscout_data['Minutes'].max()), 
                               value=(150, int(wyscout_data['Minutes'].max())))

    metrics = get_metrics_by_position(position, "wyscout")
    x_metric_display = st.selectbox(
        "Select Metric for X-Axis", 
        metrics,  # Use the values for the dropdown
        index=0
    )
    # Dropdown for selecting the y-axis metric, excluding the selected x_metric
    y_metric_display = st.selectbox(
        "Select Metric for Y-Axis", 
        metrics,
        index=0
    )

    # Button to generate pizza chart
    if st.button(f'Generate Scatter Plot'):
        try:
            fig_scatter = create_scatter_chart(wyscout_data, league, season, player_name, position, x_metric_display, y_metric_display, age_range[0], age_range[1], minutes_range[0], minutes_range[1], 'wyscout')
            if fig_scatter is not None:
                st.pyplot(fig_scatter)  # Display the pizza chart
        except Exception as e:
            st.error(f"Error : {e}")

with st.expander("Expand to view players overall rank score", expanded=False):

    league = st.selectbox('Select League:',leagues[::-1], index=0, key='rabk_lague')
    season = st.selectbox('Select Season:', seasons, index=0, key='rank_seaosn')

    position = st.selectbox('Select Playing Position:', playing_positions, index=0, key='rank_pos')

    # Button to generate pizza chart
    if st.button(f'Generate Overall Ranks for {position}'):
        try:
            fig_roverall = create_rank_visualization(wyscout_data, league,season, position, "wyscout")
            if fig_roverall is not None:
                with st.container():
                    st.write(
                        """
                        <style>
                        .dataframe th:nth-child(1) {{ width: 150px; }}  /* Width for Name */
                        .dataframe th:nth-child(2) {{ width: 100px; }}  /* Width for Team */
                        .dataframe th:nth-child(3) {{ width: 80px; }}   /* Width for Minutes */
                        .dataframe th:nth-child(4) {{ width: 120px; }}  /* Width for Overall Score */
                        .dataframe th:nth-child(5) {{ width: 10px; }}   /* Width for Overall Rank */
                        </style>
                        """,
                        unsafe_allow_html=True
                    )
                    st.dataframe(fig_roverall, use_container_width=True)
        except Exception as e:
            st.error(f"Error : {e}")

with st.expander("Expand to view players zscore rank score", expanded=False):

    league = st.selectbox('Select League:',leagues[::-1], index=0, key='z_lague')
    season = st.selectbox('Select Season:', seasons, index=0, key='z_seaosn')

    position = st.selectbox("Select Player Position", options=list(profiles.keys()), key='ra_prof')
    profile_options = [profile["Profile Name"] for profile in profiles[position]]
    profile_name = st.selectbox("Select Profile", options=profile_options)

    # Button to generate pizza chart
    if st.button(f'Generate Zscore Ranks'):
        try:
            top_10_players = top_10_players_by_profile(league, season, position, profile_name, wyscout_data, 'wyscout')
            st.dataframe(top_10_players, use_container_width=True)
        except Exception as e:
            st.error(f"Error : {e}")

with st.expander("Expand to view player similarity", expanded=False):

    league = st.selectbox('Select League:',leagues[::-1], index=0, key='sim_lague')
    season = st.selectbox('Select Season:', seasons, index=0, key='sim_seaosn')

    position = st.selectbox('Select Playing Position:', playing_positions, index=0, key='sim_pos')
    if position in ['Number 8', 'Number 10'] :
        player_name = st.selectbox('Select Player:', get_players_by_position(wyscout_data, league,season,'Number 6'), index=0, key='sim_player')
    else:
        player_name = st.selectbox('Select Player:', get_players_by_position(wyscout_data, league,season,position), index=0, key='sim_player')

    similarity_threshold = st.slider('Similarity Percent Threshold (%)', 50, 100, 90) / 100  # Converts slider percentage to decimal

    # Maximum age limit input
    max_age = st.number_input('Maximum Age', min_value=18, max_value=60, value=30)

    # Button to generate pizza chart
    if st.button(f'Generate similar players'):
        try:
            similar_players_df = filter_similar_players(
                wyscout_data, 
                player_name=player_name,
                league_name=league,
                position=position,
                season=season,
                similarity_threshold=similarity_threshold, 
                max_age=max_age,
                api="wyscout"
            )
            # Display similar players
            st.dataframe(similar_players_df, use_container_width=True)
        except Exception as e:
            st.error(f"Error : {e}")

