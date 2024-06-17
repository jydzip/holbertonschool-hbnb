from typing import List
from .DataManager import DataManager
from..Models.Reviews import Reviews


class ReviewsManager(DataManager):
    """
        Reviews Manager.
    """
    _TABLE_DB = "Reviews",
    _TABLE_CLASS = Reviews
    _TABLE_KEY_ID = "id"

    def getReviews(self) -> List[Reviews]:
        return self._all()

    def getReview(self, id:int) -> (Reviews | None):
        return self._get(id)