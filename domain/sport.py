from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class Category:
    id: str
    name: str

@dataclass
class Sport:
    id: str
    name: str
    categories: List[Category] = field(default_factory=list)


class CategoryMap:

    _id_to_category_map: Dict[str, Category] = {}
    category_id_to_sports_map: Dict[str, Sport] = {}

    def __init__(self, sports: List[Sport]) -> None:
        for sport in sports:
            self._id_to_category_map.update({
                category.id : category
                for category in sport.categories
            })

            self.category_id_to_sports_map.update({
                category.id : sport
                for category in sport.categories
            })

class SportMap:
    _id_to_sport_map : Dict[str, Sport] = {}

    def __init__(self, sports: List[Sport]):
        for sport in sports:
            self._id_to_sport_map[sport.id] = sport