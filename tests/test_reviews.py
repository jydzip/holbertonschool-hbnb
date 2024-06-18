import unittest
from classes.TestCase import TestCase


class TestReviews(TestCase):
    def test_manager__update_review__rating(self):
        self.assertEqual(self.review1.rating, 4)

        self.review1 = self.review_manager.updateReview({
            "id": self.review1.id,
            "rating": 5
        })
        self.assertEqual(self.review1.rating, 5)

    def test_manager__delete_review(self):
        review1_before = self.review_manager.getReview(self.review1.id)
        self.assertIsNotNone(review1_before)

        self.review_manager.deleteReview(self.review1.id)

        review1_after = self.review_manager.getReview(self.review1.id)
        self.assertIsNone(review1_after)

        self.review1 = self.create_review_test(self.data_review1)
    
    def test_manager__create_review__validate_data(self):
        # rating: range of 1 to 5
        with self.assertRaises(ValueError) as context:
            data_review_copy = self.data_review1.copy()
            data_review_copy['rating'] = 6
            self.create_review_test(data_review_copy)
        self.assertEqual("rating: need to be within the range of 1 to 5.", str(context.exception))

        with self.assertRaises(ValueError) as context:
            data_review_copy = self.data_review1.copy()
            data_review_copy['rating'] = 0
            self.create_review_test(data_review_copy)
        self.assertEqual("rating: need to be within the range of 1 to 5.", str(context.exception))

        # Valid user_id
        with self.assertRaises(ValueError) as context:
            data_review_copy = self.data_review1.copy()
            data_review_copy['user_id'] = "000"
            self.create_review_test(data_review_copy)
        self.assertEqual("user_id: is not a valid user.", str(context.exception))

        # Valid place_id
        with self.assertRaises(ValueError) as context:
            data_review_copy = self.data_review1.copy()
            data_review_copy['place_id'] = "000"
            self.create_review_test(data_review_copy)
        self.assertEqual("place_id: is not a valid place.", str(context.exception))

    def test_api__get_reviews(self):
        reviews = [
            self.review1,
            self.review2
        ]

        response = self.client.get("/reviews/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        i = 0
        for review in reviews:
            for key in [
                'id',
                'place_id',
                'user_id',
                'rating',
                'comment',
            ]:
                self.assertEqual(
                    getattr(review, key), data[i][key]
                )
            i += 1

    def test_api__retrieve_review(self):
        response = self.client.get(f"/reviews/{self.review1.id}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        for key in [
            'id',
            'place_id',
            'user_id',
            'rating',
            'comment',
        ]:
            self.assertEqual(
                getattr(self.review1, key), data[key]
            )
    
    def test_api__get_reviews_by_user(self):
        response = self.client.get(f"/users/{self.user2.id}/reviews")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        i = 0
        for review in [self.review1, self.review2]:
            for key in [
                'id',
                'place_id',
                'user_id',
                'rating',
                'comment',
            ]:
                self.assertEqual(
                    getattr(review, key), data[i][key]
                )
            i += 1
        
        response = self.client.get(f"/users/{self.user1.id}/reviews")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual([], data)

    def test_api__create_review(self):
        data_review3 = {
            "user_id": self.user3.id,
            "rating": 3,
            "comment": "It's good, but not recommanded.",
        }
        response = self.client.post(f"/places/{self.place2.id}/reviews", json=data_review3)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()

        review = self.review_manager.getReview(data["data"]["id"])
        self.assertEqual(review.place_id, self.place2.id)
        for key in [
            'id',
            'user_id',
            'rating',
            'comment',
        ]:
            self.assertEqual(
                getattr(review, key), data["data"][key]
            )

    def test_api__update_review(self):
        data = {
            "rating": 3,
            "comment": "Excellent appartment but finally no-"
        }
        response = self.client.put(f"/reviews/{self.review1.id}", json=data)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()

        review = self.review_manager.getReview(data["data"]["id"])
        for key in [
            'rating',
            'comment',
        ]:
            self.assertEqual(
                getattr(review, key), data["data"][key]
            )

    def test_api__delete_review(self):
        response = self.client.delete(f"/reviews/{self.review1.id}")
        self.assertEqual(response.status_code, 204)

        response = self.client.get(f"/reviews/{self.review1.id}")
        self.assertEqual(response.status_code, 404)

        self.review1 = self.create_review_test(self.data_review1)
    
    def test_api__review_not_exist(self):
        response = self.client.get(f"/reviews/000")
        self.assertEqual(response.status_code, 404)

        response = self.client.put(f"/reviews/000", json=self.data_review1)
        self.assertEqual(response.status_code, 404)

        response = self.client.delete(f"/reviews/000")
        self.assertEqual(response.status_code, 404)
    
    def test_api__create_review_himself(self):
        data_review4 = {
            "user_id": self.user1.id,
            "rating": 5,
            "comment": "BEAUTIFUL! Best ever appartment!",
        }
        response = self.client.post(f"/places/{self.place1.id}/reviews", json=data_review4)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.get_json()["message"], "The host cannot review himself.")

    def test_api__create_review_multiple_same_place(self):
        data_review5 = {
            "user_id": self.user2.id,
            "rating": 1,
            "comment": "No. Not good.",
        }
        response = self.client.post(f"/places/{self.place2.id}/reviews", json=data_review5)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.get_json()["message"], "Only one review by user can be submitted for a place.")

if __name__ == '__main__':
    unittest.main()