import math
from typing import List, Optional
from constants.margin import LeagueNames
from domain.league import Game, GameMap, OpponentMap
from domain.match_odds import Match, Odd
from domain.player import Market, Player, PlayerMap, Probability
from domain.sport import CategoryMap
from service.margin import DynamicMargin
from utils.exception import print_exception


class MatchOddsService:

    def __init__(
        self,
        player_map: PlayerMap,
        opponent_map: OpponentMap,
        game_map: GameMap,
        dynamic_margin: DynamicMargin
    ) -> None:
        try:
            self.player_map = player_map
            self.opponent_map = opponent_map
            self.game_map = game_map
            self.dynamic_margin = dynamic_margin
        except Exception as e:
            print_exception(e)
            raise Exception(f"Error initializing MatchOddsService: {str(e)}")

    def perform_match_odds(self):
        try:
            required_match_list: List[Match] = []

            for game in self.game_map._id_to_game_map.values():

                league = self.game_map._game_id_to_league_map.get(game.id)
                if not league:
                    continue

                players = self.player_map._opponent_id_to_player_list_map.get(game.home.id)
                if not players:
                    continue

                required_match_list.append(Match(
                    id=game.id,
                    home_team=game.home.name,
                    away_team=game.away.name,
                    start_time=game.start_time,
                    league=league.name,
                    odds=self.process_players_for_odds(players,game)
                ))

            return required_match_list
        except Exception as e:
            print_exception(e)
            raise Exception(f"Error performing match odds: {str(e)}")

    def process_players_for_odds(self, players: List[Player], game: Game):
        try:
            required_odds: List[Odd] = []
            for player in players:


                for market in player.markets:
                    decimal_odds = self.perform_odds(market, game)

                    required_odds.extend([
                        Odd(
                            id=market.id,
                            market=market.category.name,
                            player_name=player.full_name,
                            decimal_odds=decimal_odds[0]
                        ),
                        Odd(
                            id=market.id,
                            market=market.category.name,
                            player_name=player.full_name,
                            decimal_odds=decimal_odds[1]
                        )
                    ])

            return required_odds
        except Exception as e:
            print_exception(e)
            raise Exception(f"Error processing players for odds: {str(e)}")

    def isLive(self, market_id: str):
        try:
            return '1' == market_id.split(':')[2]
        except Exception as e:
            print_exception(e)
            raise Exception(f"Error checking if market is live: {str(e)}")

    def perform_odds(self, market: Market, game: Game):
        try:
            league_name = LeagueNames(self.game_map._game_id_to_league_map[game.id].name)

            margin = self.dynamic_margin.get_dynamic_margin(
                league_name=league_name,
                category_name=market.category.name,
                is_live=self.isLive(market.id)
            )

            median_probability = self.get_median_probability(market.probabilities)

            decimal_odd_over, decimal_odd_under = 0.0, 0.0

            if median_probability:
                decimal_odd_over = self.formatOdds(
                    raw_probability=median_probability.over,
                    format_type='decimal',
                    custom_margin=margin
                )
                decimal_odd_under = self.formatOdds(
                    raw_probability=median_probability.under,
                    format_type='decimal',
                    custom_margin=margin
                )

            return (decimal_odd_over, decimal_odd_under)
        except Exception as e:
            print_exception(e)
            raise Exception(f"Error performing odds calculation: {str(e)}")
        


    def get_median_probability(self, probabilities: List[Probability]) -> Optional[Probability]:
        """
        Replicates the medianProbability logic: finds the probability object
        where the absolute difference between over and under raw probabilities is minimized.
        """
        try:
            # Filter out invalid probabilities (void 0 in JS means None in Protobuf)
            valid_probabilities = [
                p for p in probabilities
                if bool(p.over) or bool(p.under)
            ]

            if not valid_probabilities:
                return None

            # Sort based on the absolute difference between over and under
            # The first element is the median probability (minimum difference)
            valid_probabilities.sort(key=lambda p: abs(p.over - p.under))

            return valid_probabilities[0]
        except Exception as e:
            print_exception(e)
            raise Exception(f"Error getting median probability: {str(e)}")
    
    def apply_margin_to_probability(self, raw_probability: float, margin: float, n = 10):
        try:
            if raw_probability == 0 or margin == 0:
                return raw_probability

            # Formula 1: f = u * (1 + ((1 - u) / u - 0.2) * Math.exp(-n * t))
            term_b = ((1 - margin) / margin) - 0.2
            term_c = math.exp(-n * raw_probability)
            f = margin * (1 + term_b * term_c)

            if f >= 1.0:
                # Avoid division by zero in the next step
                return raw_probability # Return unadjusted value as a fallback

            # Formula 2: o = (1 + f / (1 - f)) * t
            adjusted_probability = (1 + f / (1 - f)) * raw_probability

            return adjusted_probability
        except Exception as e:
            print_exception(e)
            raise Exception(f"Error applying margin to probability: {str(e)}")

    def formatOdds(
        self,
        raw_probability: float,
        format_type: str,
        # apply_margin: bool,
        custom_margin: float
    ):
        try:
            if not raw_probability:
                return 0.0

            # System Margin is confirmed to be 0.13
            default_system_margin = 0.13
            required_margin = custom_margin if custom_margin is not None else default_system_margin

            # Calculate Adjusted Probability (o)
            adjusted_probability = self.apply_margin_to_probability(raw_probability, required_margin)

            # Calculate Decimal Odds (l = 1 / o)
            if adjusted_probability == 0:
                return 0.0
            l = 1 / adjusted_probability

            # For 'decimal' type, the JS formats and rounds to 2 decimal places.
            if format_type == 'decimal':
                # We round to match the UI's display precision before returning the float.
                return round(l, 2)

            # Add other formats here if needed, but 'decimal' is the target for Odd.decimal_odds
            return round(l, 2)
        except Exception as e:
            print_exception(e)
            raise Exception(f"Error formatting odds: {str(e)}")









