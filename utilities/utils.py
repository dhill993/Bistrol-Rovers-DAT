import pandas as pd
import matplotlib.font_manager as fm
import numpy as np
from .statbomb_default_metrics import metrics_per_position
from .wyscout_default_metrics import metrics_per_position as metrics_per_position_1

custom_fontt = fm.FontProperties(fname="fonts/Alexandria-Regular.ttf")

# Helper function to get players by position
def get_metrics_by_position(position, api='statbomb'):
    if api=='statbomb':
        return metrics_per_position[position]
    elif api=='wyscout':
        return metrics_per_position_1[position]

def get_players_by_position(df, league, season, position):
    if league not in ['All', '']:
        df = df[df['League'] == league]    
    if season!='':  
        df = df[df['Season'] == season]    
    return df[df['Position'] == position]['Player Name'].tolist()

def get_player_metrics_percentile_ranks(df, player_name, position, all_metric):
    position_specific_data = df[df['Position'] == position]
    numeric_columns = position_specific_data[all_metric]
    non_numeric_columns = position_specific_data.drop(columns=all_metric)

    # Perform percentile ranking (only for numeric columns)
    positional_percentile_data = numeric_columns.rank(pct=True, axis=0) * 100

    # Combine the ranked numeric data with the non-numeric columns
    result = pd.concat([non_numeric_columns.reset_index(drop=True), positional_percentile_data.reset_index(drop=True)], axis=1)

    player_data = result[result['Player Name'] == player_name]

    if not player_data.empty:
        return player_data
    return None

def get_avg_metrics_percentile_ranks(df, position):
    position_specific_data = df[df['Position'] == position]
    numeric_columns = position_specific_data.select_dtypes(include=np.number)

    # Step 2: Calculate mean of each column
    column_means = numeric_columns.mean()

    # Step 3: Create a new row for the average values
    avg_row = {col: column_means[col] for col in numeric_columns.columns}
    avg_row['Player Name'] = 'AVG'
    avg_row['Position'] = None  # Non-numeric fields set to None

    # Create a DataFrame for the average row
    avg_df = pd.DataFrame([avg_row], columns=df.columns)

    # Step 4: Combine the original DataFrame with the average row
    df_with_avg = pd.concat([df, avg_df], ignore_index=True)

    # Calculate percentile ranks including the average row
    positional_percentile_data = df_with_avg[numeric_columns.columns].rank(pct=True, axis=0) * 100

    # Prepare the average metrics DataFrame
    avg_data = avg_df.copy()
    avg_data[numeric_columns.columns] = positional_percentile_data.loc[df_with_avg['Player Name'] == 'AVG'].values.flatten()
    
    return avg_data

def get_player_and_avg_metrics(df, player_name, position, all_metrics):
    # Get player metrics
    player_metrics = get_player_metrics_percentile_ranks(df, player_name, position, all_metrics)
    # Get average metrics
    avg_metrics = get_avg_metrics_percentile_ranks(df, position)

    return player_metrics, avg_metrics

def get_stat_values(all_metrics, player_metrics_df, positional_means_df):
    stat1 = []
    stat2 = []

    for metric in all_metrics:
        # Append value from player_metrics_df or None if metric doesn't exist
        if metric in player_metrics_df.columns:
            stat1.append(player_metrics_df[metric].values[0])  # Get value from player_metrics_df
        else:
            stat1.append(None)  # Or handle as needed

        # Append value from positional_means_df or None if metric doesn't exist
        if metric in positional_means_df.columns:
            stat2.append(positional_means_df[metric].values[0])  # Get value from positional_means_df
        else:
            stat2.append(None)  # Or handle as needed
            
    return stat1, stat2

def get_weighted_score(league_name):
    league_rankings = {
        "Premier League": 0.95,
        "Spain 1": 0.9,
        "Italy 1": 0.89,
        "Germany 1": 0.89,
        "France 1": 0.87,
        "Netherlands 1": 0.83,
        "Portugal 1": 0.83,
        "Belgium 1": 0.82,
        "Championship": 0.80,
        "MLS": 0.79,
        "Japan 1": 0.78,
        "Turkey 1": 0.78,
        "Norway 1": 0.77,
        "Denmark 1": 0.77,
        "Bundesliga": 0.77,
        "Italy 2": 0.76,
        "Croatia 1": 0.76,
        "Premiership": 0.76,
        "Poland 1": 0.76,
        "Allsvenskan": 0.76,
        "NB I": 0.75,
        "Czech 1": 0.75,
        "Germany 2": 0.75,
        "Greece 1": 0.75,
        "Romania 1": 0.75,
        "Spain 2": 0.75,
        "K League 1": 0.74,
        "Swiss 1": 0.75,
        "Serbia 1": 0.73,
        "France 2": 0.73,
        "League One": 0.72,
        "Slovakia 1": 0.70,
        "Bulgaria 1": 0.70,
        "1. SNL": 0.69,
        "Belgium 2": 0.69,
        "Portugal 2": 0.69,
        "Netherlands 2": 0.69,
        "A-League": 0.67,
        "Germany 3": 0.68,
        "France 3": 0.68,
        "Japan 2": 0.65,
        "Iceland 1": 0.52,
        "Veikkausliiga": 0.63,
        "Latvia 1": 0.64,
        "Norway 2": 0.62,
        "Sweden 2": 0.62,
        "Swizz 2": 0.63,
        "Moldova 1": 0.60,
        "K League 2": 0.59,
        "League Two": 0.60,
        "Austria 2": 0.63,
        "Denmark 2": 0.58,
        "Scotland 2": 0.55,
        "Canada 1": 0.59,
        "Hungary 2": 0.60,
        "Ireland 1": 0.52,
        "Germany 4": 0.57,
        "Turkey 2": 0.56,
        "National League": 0.50,
        "Wales 1": 0.42,
        "NIreland1": 0.43,
        "Ireland 2": 0.41,
        "Scotland 3": 0.41,
        "VNL 2": 0.40
    }

    return league_rankings[league_name]
