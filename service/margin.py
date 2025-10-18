from typing import Dict, List, Literal, Optional

from constants.margin import MLB_DATA, NCAA_DATA, NFL_DATA, LeagueNames
from utils.exception import print_exception



class DynamicMargin:

    CATEGORIES_NAME_MAP = {
        "strikeouts": "Strikeouts",
        "win_probability": "Win probability",
        "singles": "Singles",
        "doubles": "Doubles",
        "triples": "Triples",
        "home_runs": "Home runs",
        "total_bases": "Total bases",
        "hits": "Hits",
        "hits_allowed": "Hits allowed",
        "earned_runs": "Earned runs",
        "hits_runs_rbis": "Hits runs rbis",
        "outs": "Outs",
        "runs": "Runs",
        "rbis": "Rbis",
        "stolen_bases": "Stolen bases",
        "walks": "Walks",
        "batter_strikeouts": "Batter strikeouts",
        "batter_walks": "Batter walks",
        "first_home_run": "First home run",
        "passing_yards": "Passing yards",
        "passing_tds": "Passing tds",
        "receiving_yards": "Receiving yards",
        "receiving_tds": "Receiving tds",
        "rushing_yards": "Rushing yards",
        "rushing_tds": "Rushing tds",
        "interceptions_thrown": "Interceptions thrown",
        "passing_attempts": "Passing attempts",
        "rushing_attempts": "Rushing attempts",
        "receptions": "Receptions",
        "receiving_rushing_yards": "Receiving rushing yards",
        "passing_completions": "Passing completions",
        "first_td_scorer": "First td scorer",
        "anytime_td_scorer": "Anytime td scorer",
        "kicking_points": "Kicking points",
        "longest_completion": "Longest completion",
        "longest_reception": "Longest reception",
        "longest_rush": "Longest rush",
        "passing_rushing_yards": "Passing rushing yards",
        "tackles": "Tackles",
        "last_td_scorer": "Last td scorer",
        "defensive_assists": "Defensive assists",
        "defensive_tackles_assists": "Defensive tackles assists",
        "field_goal_made": "Field goal made",
        "extra_point_made": "Extra point made",
        "sacks": "Sacks",
        "fumbles": "Fumbles"
    }

    def __init__(self) -> None:
        try:
            self.league_to_margin_map = {
                LeagueNames.NCAA: {},
                LeagueNames.MLB: {},
                LeagueNames.NFL: {}
            }
            self.set_margins(LeagueNames.NCAA, NCAA_DATA)
            self.set_margins(LeagueNames.MLB, MLB_DATA)
            self.set_margins(LeagueNames.NFL, NFL_DATA)
        except Exception as e:
            print_exception(e)
            raise Exception(f"Error initializing DynamicMargin: {str(e)}")
    
    def calc_margin(self, historical_data):
        try:
            if not historical_data:
                return 0
            return 0.15 - 0.5 * min(max(historical_data, -0.1), 0.1)
        except Exception as e:
            print_exception(e)
            raise Exception(f"Error calculating margin: {str(e)}")
    
    def set_margins(self, league_name: LeagueNames, data_list: List[Dict]):
        try:
            for data in data_list:
                if not data.get("category_key"):
                    continue

                category_name = self.CATEGORIES_NAME_MAP[data["category_key"]]

                self.league_to_margin_map[league_name][category_name] = {
                    "inPlayMargin": self.calc_margin(data.get("historical_inplay_margin")),
                    "preGameMargin":self.calc_margin(data.get("historical_pregame_margin"))
                }
        except Exception as e:
            print_exception(e)
            raise Exception(f"Error setting margins: {str(e)}")

    def get_dynamic_margin(
        self,
        league_name: LeagueNames,
        category_name: str,
        is_live: bool
    ):
        try:
            margins: Optional[Dict[str, float]] = self.league_to_margin_map[league_name].get(category_name)
            if not margins:
                print("Margin not found", league_name, category_name, is_live)
                return 0.0

            return margins["inPlayMargin"] if is_live else margins["preGameMargin"]
        except Exception as e:
            print_exception(e)
            raise Exception(f"Error getting dynamic margin: {str(e)}")




