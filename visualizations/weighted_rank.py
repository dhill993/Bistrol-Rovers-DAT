from visualizations.overall_rank import get_overall_rank
from utilities.utils import get_weighted_score

def get_weighted_rank(data, player_name, league_name, season, position, api='statbomb'):
    data = get_overall_rank(data, league_name, season, position, api)
    data = data[data['Player Name'] == player_name]
    points_of_this_league = get_weighted_score(league_name)
    points_of_league_two = get_weighted_score("League two")

    factor = points_of_this_league/points_of_league_two

    data = data[['Player Name', 'Age', 'Minutes', 'Overall Score']]
    data['Score weighted aganist League two'] =  data['Overall Score']*factor
    data.reset_index(drop=True, inplace=True)

    return data[['Player Name', 'Age', 'Minutes', 'Overall Score', 'Score weighted aganist League two']]
