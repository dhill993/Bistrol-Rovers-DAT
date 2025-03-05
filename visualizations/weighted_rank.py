from visualizations.overall_rank import get_overall_rank
from utilities.utils import get_weighted_score

def get_weighted_rank(data, player_name, league_name, comparison_league, season, position, api='statbomb'):
    data = get_overall_rank(data, league_name, season, position, api)
    data = data[data['Player Name'] == player_name]
    points = get_weighted_score(comparison_league)
    
    data = data[['Player Name', 'Age', 'Minutes', 'Overall Score']]
    data['Weighted Score'] =  data['Overall Score']*points
    data.reset_index(drop=True, inplace=True)

    return data[['Player Name', 'Age', 'Minutes', 'Overall Score', 'Weighted Score']]
