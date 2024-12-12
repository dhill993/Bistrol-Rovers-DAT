from scipy.stats import zscore
from utilities.statbomb_default_metrics import profiles_zcore as statbomb_profiles
from utilities.wyscout_default_metrics import profiles_zcore as wyscout_zcore

def top_10_players_by_profile(league_name, season, position, profile_name, df, api='statbomb'):

    if api == 'statbomb' :
        profiles_zcore = statbomb_profiles
    else:
        profiles_zcore = wyscout_zcore

    profile = next(
        (p for p in profiles_zcore.get(position, []) if p["Profile Name"] == profile_name), None
    )
    if not profile:
        raise ValueError(f"Profile '{profile_name}' for position '{position}' not found.")


    if position == 'Number 6' and api=='statbomb':
        position = 'Number 8'

    if (position == 'Number 8' or position == 'Number 10') and api=='wyscout':
        position = 'Number 6'

    if league_name not in ['All', '']:
        df = df[df['League'] == league_name]    
    if season!='':
        df = df[df['Season']==season]

    df = df[df['Position'] == position]

    # Find the selected profile for the given position
    # Extract metrics and weighted metrics
    metrics = profile["Using Metrics"]
    weighted_metrics = profile["Weighted Metrics"]
    z_score_name = profile["Z Score Name"]

    all_metrics = metrics + weighted_metrics
    # Fill missing values with the mean of each column in the selected metrics
    df[all_metrics] = df[all_metrics].apply(lambda x: x.fillna(x.mean()))
    
    # Calculate z-scores for each metric
    for metric in all_metrics:
        df[metric + '_z'] = zscore(df[metric])
    
    # Define weights for each metric z-score
    weights = {metric + '_z': 2 if metric in weighted_metrics else 1 for metric in all_metrics}

    # Initialize the profile score column to 0
    df[z_score_name] = 0
    
    # Calculate the profile score based on weighted z-scores
    for metric in all_metrics:
        df[z_score_name] += df[metric + '_z'] * weights[metric + '_z']

    df[z_score_name] = df[z_score_name].round(2)

    # Sort the dataframe by the calculated profile score in descending order and get the top 10
    top_10_players = df.sort_values(by=z_score_name, ascending=False).head(10).reset_index(drop=True)
    return top_10_players[['Player Name', 'Team', 'League', 'Minutes', 'Position', 'Age' ,z_score_name]]