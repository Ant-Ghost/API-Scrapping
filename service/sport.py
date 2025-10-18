from typing import Dict, List
from constants.sport import SPORTS_GQL_QUERY, SPORTS_OPERATION_NAME
from domain.sport import Category, CategoryMap, Sport
from infrastructure.graphql import GQLQueryBuilder

class SportService:

    category_map: CategoryMap

    def __init__(self, allowed_sports: List[str] = []) -> None:
        try:
            self.is_all_games = not(bool(allowed_sports)) # if empty, allow all
            self.allowed_sports = allowed_sports
            self.name_to_sport_map = {}
        except Exception as e:
            raise Exception(f"Error initializing SportService: {str(e)}")

    def fetch_sport(self):
        try:
            gql_query_builder = GQLQueryBuilder(SPORTS_OPERATION_NAME)

            gql_query_builder.set_query(SPORTS_GQL_QUERY)
            gql_query_builder.set_variables()

            data = gql_query_builder.build_and_execute()

            sports_list: List[Dict] = data["system"]["sports"]

            sports: List[Sport] = []

            for sport_data in sports_list:

                current_sport = Sport(id=sport_data["id"], name=sport_data["name"])

                category_list: List[Dict] = sport_data.get("categories", [])

                for category_data in category_list:
                    current_sport.categories.append(
                        Category(
                            id=category_data.get("id",""),
                            name=category_data.get("name","")
                        )
                    )

                sports.append(current_sport)

                if not self.is_all_games and current_sport.name.lower() in self.allowed_sports:
                    self.name_to_sport_map[current_sport.name.lower()] = current_sport

            self.category_map = CategoryMap(sports)

            return sports
        except Exception as e:
            raise Exception(f"Error fetching sports: {str(e)}")

    def get_allowed_sports(self) -> List[Sport]:
        try:
            return list(self.name_to_sport_map.values())
        except Exception as e:
            raise Exception(f"Error getting allowed sports: {str(e)}")




