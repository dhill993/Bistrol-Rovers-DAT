import streamlit as st
from st_pages import show_pages_from_config
from data.retrieve_statbomb_data import get_statsbomb_player_season_stats

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
with st.spinner("Retrieving data from statsbomb api"):
    statsbomb_data = get_statsbomb_player_season_stats()
    statsbomb_data["Minutes"] = statsbomb_data['Minutes'].astype(int)
st.dataframe(statsbomb_data, height=600, use_container_width=True)
