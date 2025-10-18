import json
import requests

from typing import Dict

from constants.common import BASE_GQL_URL

class GQLQueryBuilder:

    params: Dict

    def __init__(self, operation_name: str) -> None:
        self.params = {
            "operationName": operation_name
        }
    
    def set_query(self, query: str):
        self.params["query"] = query

    def set_variables(self, variables: Dict = {}):
        self.params["variables"] = json.dumps(variables)

    def build_and_execute(self) -> Dict:

        response = requests.get(
            BASE_GQL_URL, 
            params=self.params,
            headers={
                "x-hs3-version":"2"
            }
        )

        response_dict: Dict = response.json()
        return response_dict.get("data", {})

    