from typing import List
from .DataManager import DataManager
from..Models.Reviews import Reviews


class ReviewsManager(DataManager):
    """
        Reviews Manager.
    """
    _TABLE_DB = "reviews"
    _TABLE_CLASS = Reviews
    _TABLE_KEY_ID = "id"

    def getReviews(self) -> List[Reviews]:
        """
            Retrieves the list of all reviews.
            Returns:
                List[Places]: The list of reviews.
        """
        return self._all()

    def getReviewsByUser(self, user_id: str) -> List[Reviews]:
        """
            Retrieves the list of reviews by their user.
            Args:
                user_id (str): The review place.
            Returns:
                List[Reviews]: The list of reviews.
        """
        reviews = self.getReviews()
        reviews_result = []
        for review in reviews:
            if review.user_id == user_id:
                reviews_result.append(review)
        return reviews_result

    def getReviewsByPlace(self, place_id: str) -> List[Reviews]:
        """
            Retrieves the list of reviews by their place.
            Args:
                place_id (str): The review place.
            Returns:
                List[Reviews]: The list of reviews.
        """
        reviews = self.getReviews()
        reviews_result = []
        for review in reviews:
            if review.place_id == place_id:
                reviews_result.append(review)
        return reviews_result

    def getReview(self, review_id: str) -> (Reviews | None):
        """
            Retrieves a review by its identifier.
            Args:
                review_id (str): The review identifier.
            Returns:
                Reviews | None: The review or None if no review is found.
        """
        return self._get(review_id)

    def deleteReview(self, review_id: str) -> None:
        """
            Deletes a review by its identifier.
            Args:
                review_id (str): The review identifier.
        """
        return self._delete(review_id)

    def updateReview(self, review_data: dict) -> Reviews:
        """
            Updates a review with new data (partial or not).
            Args:
                review_data (dict): The review new data.
            Returns:
                Reviews: The review updated.
        """
        Reviews.validate_request_data(review_data, True)
        if review_data.get("user_id"):
            Reviews.validate_exist_user(review_data['user_id'])
        if review_data.get("place_id"):
            Reviews.validate_exist_place(review_data['place_id'])

        return self._update(review_data)
    
    def createReview(self, review_data: dict) -> Reviews:
        """
            Creates a review.
            Args:
                review_data (dict): The review data.
            Returns:
                Reviews: The review created.
        """
        Reviews.validate_request_data(review_data)
        Reviews.validate_exist_user(review_data['user_id'])
        Reviews.validate_exist_place(review_data['place_id'], review_data['user_id'])

        Reviews.validate_can_review(review_data['user_id'], review_data['place_id'])

        return self._save(review_data)