from datetime import datetime
from typing import Dict, List
from constants.match import MATCH_GQL_QUERY, MATCH_OPERATION_NAME
from domain.league import Designation, Game, League, Opponent
from domain.sport import Sport, SportMap
from infrastructure.graphql import GQLQueryBuilder
from utils.exception import print_exception

class LeagueService:

    def __init__(self, sports: List[Sport]) -> None:
        try:
            self.reverse_sports_map = SportMap(sports)
        except Exception as e:
            print_exception(e)
            raise Exception(f"Error initializing LeagueService: {str(e)}")

    def fetch_games(self) -> List[League]:
        try:
            gql_query_builder = GQLQueryBuilder(MATCH_OPERATION_NAME)

            gql_query_builder.set_query(MATCH_GQL_QUERY)

            data: Dict = gql_query_builder.build_and_execute()

            games: List[Dict] = data.get("games",[])

            id_to_league_map: Dict[str, League] = {}

            for game in games:
                league_data : Dict = game["league"]

                sport = self.reverse_sports_map._id_to_sport_map.get(league_data["sportId"])

                if not sport:
                    continue

                league = id_to_league_map.get(league_data["id"])

                if not league:
                    league = League(
                        id=league_data["id"],
                        name=league_data["name"],
                        sport=sport
                    )

                    id_to_league_map[league.id] = league

                opponent_list: List[Dict] = game["opponents"]

                home_away_map: Dict[Designation, Opponent] = {}

                for i in range(2):
                    opponent_data = opponent_list[i]
                    home_away_map[Designation(opponent_data["designation"])]=Opponent(
                        id=opponent_data['id'],
                        designation=Designation(opponent_data["designation"]),
                        abbreviation=opponent_data["team"]["abbreviation"],
                        name=opponent_data["team"]["name"],
                        sport_name=sport.name
                    )


                league.games.append(Game(
                    id=game["id"],
                    start_time=datetime.strptime(game.get("scheduledAt",""), "%Y-%m-%dT%H:%M:%SZ"),
                    home=home_away_map[Designation.Home],
                    away=home_away_map[Designation.Away],
                ))

            return list(id_to_league_map.values())
        except Exception as e:
            print_exception(e)
            raise Exception(f"Error fetching games: {str(e)}")