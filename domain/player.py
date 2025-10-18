from dataclasses import dataclass, field
from typing import Dict, List

from domain.league import Opponent
from domain.sport import Category


@dataclass
class Probability:
    line : float
    over: float
    under: float

@dataclass
class Market:
    id: str
    category: Category
    probabilities: List[Probability] = field(default_factory=list)


@dataclass
class Player:
    opponent: Opponent
    full_name: str
    markets: List[Market] = field(default_factory=list)

class PlayerMap:

    _id_to_player_map: Dict[str, Player] = {}
    _opponent_id_to_player_list_map: Dict[str, List[Player]] = {}

    def __init__(self, players: List[Player]):
        for player in players:
            self._id_to_player_map[player.opponent.id] = player
            self._opponent_id_to_player_list_map.setdefault(player.opponent.id, []).append(player)
            
