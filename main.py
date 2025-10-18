from domain.league import GameMap
from domain.player import PlayerMap
from service.league import LeagueService
from service.margin import DynamicMargin
from service.match_odds import MatchOddsService
from service.player import PlayerService, create_opponent_map
from service.sport import SportService
required_sports = [
    "football", 
    "baseball", 
    # "basketball"
]

sport_service = SportService(required_sports)
sports = sport_service.fetch_sport()

game_service = LeagueService(sports)
games = game_service.fetch_games()

opponent_map = create_opponent_map(games)
game_map = GameMap(games)

player_service = PlayerService(
    opponent_map=opponent_map,
    category_map=sport_service.category_map
)
dynamic_margin = DynamicMargin()

import ipdb; ipdb.set_trace()

for sport in sport_service.get_allowed_sports():

    players = player_service.fetch_players(sport.id)
    
    match_odds_service = MatchOddsService(
        PlayerMap(players), 
        opponent_map,
        game_map,
        dynamic_margin,
    )
    match_odds_service.perform_match_odds()

    import ipdb; ipdb.set_trace()