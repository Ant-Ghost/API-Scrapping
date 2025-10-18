from dataclasses import dataclass, field
from datetime import datetime
from typing import List

@dataclass
class Odd:
    id: str
    market: str
    player_name: str
    decimal_odds: float

    def to_dict(self):
        return {
            "id": self.id,
            "market": self.market,
            "player_name": self.player_name,
            "decimal_odds": self.decimal_odds
        }

@dataclass
class Match:
    id: str
    home_team: str
    away_team: str
    start_time: datetime
    league: str
    odds: List[Odd] = field(default_factory=list)

    def to_dict(self):
        return {
            "id": self.id,
            "home_team": self.home_team,
            "away_team": self.away_team,
            "start_time": self.start_time,
            "league": self.league,
            "odds": [odd.to_dict() for odd in self.odds]
        }