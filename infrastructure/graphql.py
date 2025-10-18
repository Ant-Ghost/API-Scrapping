import json
import requests

from typing import Dict

from constants.common import BASE_GQL_URL
from utils.exception import print_exception

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
        try:
            response = requests.get(
                BASE_GQL_URL,
                params=self.params,
                headers={
                    "x-hs3-version":"2"
                }
            )

            # Check if the response status is successful
            response.raise_for_status()

            response_dict: Dict = response.json()
            return response_dict.get("data", {})
        except requests.exceptions.ConnectionError as e:
            print_exception(e)
            raise Exception(f"Connection error while executing GraphQL query: {str(e)}")
        except requests.exceptions.Timeout as e:
            print_exception(e)
            raise Exception(f"Timeout error while executing GraphQL query: {str(e)}")
        except requests.exceptions.HTTPError as e:
            print_exception(e)
            raise Exception(f"HTTP error while executing GraphQL query: {str(e)}")
        except requests.exceptions.RequestException as e:
            print_exception(e)
            raise Exception(f"Request error while executing GraphQL query: {str(e)}")
        except json.JSONDecodeError as e:
            print_exception(e)
            raise Exception(f"JSON decode error while parsing GraphQL response: {str(e)}")
        except Exception as e:
            print_exception(e)
            raise Exception(f"Unexpected error while executing GraphQL query: {str(e)}")

    