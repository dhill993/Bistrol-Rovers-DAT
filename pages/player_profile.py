import streamlit as st
import pandas as pd
from utilities.utils import get_players_by_position
from visualizations.pizza_chart import create_pizza_chart
from visualizations.radar_chart import create_radar_chart

st.set_page_config(
    page_title='Wyscout Player Profile',
    layout='wide',
    initial_sidebar_state='expanded'
)

st.title("Wyscout Player Profile")

# Upload CSV data
uploaded_file = st.file_uploader("Upload Wyscout Data CSV", type=['csv'])
if uploaded_file:
    wyscout_data = pd.read_csv(uploaded_file)
    st.success("Data loaded successfully!")

    # Prepare positions - example: unique values from 'Position' column + special cases
    playing_positions = list(wyscout_data['Position'].unique())
    playing_positions.extend(['Number 8', 'Number 10'])

    # Select inputs
    league = st.selectbox('Select League:', sorted(wyscout_data['Team within selected timeframe'].unique()))
    season = st.selectbox('Select Season:', sorted(wyscout_data.get('Season', ['All'])))  # If you have Season column

    position = st.selectbox('Select Playing Position:', playing_positions)

    # If special position, adjust for Number 6 as in your original script
    actual_position = 'Number 6' if position in ['Number 8', 'Number 10'] else position

    players = get_players_by_position(wyscout_data, league, season, actual_position)
    player_name = st.selectbox('Select Player:', players)

    st.markdown("---")

    # Buttons to generate charts
    if st.button('Generate Pizza Chart'):
        try:
            fig_pizza = create_pizza_chart(wyscout_data, league, season, player_name, position, api='wyscout')
            if fig_pizza:
                st.pyplot(fig_pizza)
        except Exception as e:
            st.error(f"Error generating pizza chart: {e}")

    if st.button('Generate Radar Chart'):
        try:
            fig_radar = create_radar_chart(wyscout_data, league, player_name, position, season, api='wyscout')
            if fig_radar:
                st.pyplot(fig_radar)
        except Exception as e:
            st.error(f"Error generating radar chart: {e}")

else:
    st.info("Please upload your Wyscout data CSV file to get started.")
