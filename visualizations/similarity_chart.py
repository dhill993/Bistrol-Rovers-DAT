from utilities.utils import get_metrics_by_position


def filter_similar_players(df, player_name, league_name, season, position, similarity_threshold, max_age, api="statbomb"):
    """
    Filters players based on similarity to a selected player's metrics and age limit.

    Parameters:
        df (pd.DataFrame): DataFrame containing player data with metrics.
        player_name (str): Name of the selected player to compare others against.
        position (str): The position of the player.
        similarity_threshold (float): The initial similarity threshold (e.g., 0.9 for 90%).
        max_age (int): The maximum age limit for players to be considered in the filtered results.

    Returns:
        pd.DataFrame: DataFrame with players that match the similarity criteria.
    """
    # Extract the selected player's metrics as reference

    num_columns = get_metrics_by_position(position, api)

    if position == 'Number 6' and api=='statbomb':
        position = 'Number 8'

    if league_name not in ['All', '']:
        df = df[df['League'] == league_name]    
    if season!='':
        df = df[df['Season']==season]
    df = df[df['Position'] == position]

    columns = ['Player Name', 'Team', 'League', 'Minutes', 'Age', 'Position'] + num_columns

    df = df[columns]

    selected_player = df.loc[df['Player Name'] == player_name].iloc[0]
    df = df[df['Player Name']!= player_name]

    # List to hold indices of rows that match the similarity conditions
    matching_indices = []

    # Iterate through each player in the DataFrame
    for idx, row in df.iterrows():
        if row['Age'] >= max_age:
            continue  # Skip this player if the age is equal to or above max_age
        
        match_count = 1  # Counter for satisfied metric conditions
        
        for metric in num_columns:
            threshold_value = selected_player[metric] * similarity_threshold
            if row[metric] >= threshold_value:
                match_count += 1
    
        # Match if enough conditions are met
        if match_count >= 10:  # Can adjust this threshold based on your needs
            matching_indices.append(idx)

    # Final result with matching players and their similarity score
    df = df[['Player Name', 'Team', 'League', 'Minutes', 'Age', 'Position',]]
    return df.loc[matching_indices].reset_index(drop=True)
