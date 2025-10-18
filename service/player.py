import base64
import zlib
from datetime import datetime
from typing import Dict, List, Literal

from constants.player import PLAYER_GQL_QUERY, PLAYER_OPERATION_NAME
from domain.league import League, OpponentMap
from domain.player import Market, Player, Probability
from domain.sport import CategoryMap
from infrastructure.graphql import GQLQueryBuilder
import infrastructure.protobuf.hotstreak_data_pb2 as pb
from utils.protobuf import decode_protobuf
from utils.exception import print_exception

def create_opponent_map(leagues: List[League]):
    return OpponentMap(leagues)

class PlayerService:

    def __init__(self, opponent_map: OpponentMap, category_map: CategoryMap) -> None:
        try:
            self._id_to_opponent_map = opponent_map._id_to_opponent_map
            self._id_to_category_map = category_map._id_to_category_map
        except Exception as e:
            print_exception(e)
            raise Exception(f"Error initializing PlayerService: {str(e)}")
        
    def fetch_players(self, sport_id: str) -> List[Player]:
        try:
            gql_query_builder = GQLQueryBuilder(PLAYER_OPERATION_NAME)
            gql_query_builder.set_query(PLAYER_GQL_QUERY)
            gql_query_builder.set_variables({
                "filters":{
                    "activeMarketsOnly":True,
                    "sport": sport_id
                }
            })

            data: Dict = gql_query_builder.build_and_execute()

            results: List[Dict] = data.get("search",{}).get("results", [])

            players: List[Player] = []

            for result in results:
                markets = self.get_markets(result["markets64"])
                players.append(Player(
                    opponent=self._id_to_opponent_map[result["participant"]["opponentId"]],
                    full_name=result["participant"]["player"]["fullName"],
                    markets=markets
                ))

            return players
        except Exception as e:
            print_exception(e)
            raise Exception(f"Error fetching players: {str(e)}")

    def get_markets(self, markets64_string: str):
        try:
            required_markets : List[Market] = []
            markets_message = decode_protobuf(markets64_string, pb.Markets())

            for market in markets_message.markets:
                
                market_id = market.id
                market_category = market.category

                required_probabilities : List[Probability] = []

                if market.probabilities:
                    for probability in market.probabilities:
                        required_probabilities.append(Probability(
                            probability.line,
                            probability.over,
                            probability.under
                        ))

                required_markets.append(Market(
                    id=market_id,
                    category=self._id_to_category_map[market_category],
                    probabilities=required_probabilities
                ))

            return required_markets
        except Exception as e:
            print_exception(e)
            raise Exception(f"Error getting markets: {str(e)}")