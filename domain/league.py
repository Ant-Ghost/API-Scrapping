from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Tuple

from domain.sport import Sport

class Designation(Enum):
    Home = "home"
    Away = "away"

@dataclass
class Opponent:
    id: str
    designation: Designation
    abbreviation: str
    sport_name: str
    name: str

@dataclass
class Game:
    id: str
    start_time: datetime
    home: Opponent
    away: Opponent

@dataclass
class League:
    id: str
    name: str
    sport: Sport
    games: List[Game] = field(default_factory=list)

class GameMap:
    _id_to_game_map: Dict[str, Game] = {}
    _game_id_to_league_map: Dict[str, League] = {}

    def __init__(self, leagues: List[League]) -> None:
        
        for league in leagues:
            for game in league.games:
                self._id_to_game_map.update({
                    game.id: game,
                    game.id: game
                })

                self._game_id_to_league_map.update({
                    game.id: league,
                    game.id: league
                })


class OpponentMap:

    _id_to_opponent_map: Dict[str, Opponent] = {}
    _opponent_id_to_league_map: Dict[str, League] = {}
    _opponent_id_to_game_map: Dict[str, Game] = {}

    def __init__(self, leagues: List[League]) -> None:
        
        for league in leagues:
            for game in league.games:
                self._id_to_opponent_map.update({
                    game.home.id: game.home,
                    game.away.id: game.away
                })

                self._opponent_id_to_league_map.update({
                    game.home.id: league,
                    game.away.id: league
                })

                self._opponent_id_to_game_map.update({
                    game.home.id: game,
                    game.away.id: game
                })
        