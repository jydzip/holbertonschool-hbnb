from flask import request
from flask_restx import Namespace, Resource, fields, marshal

from classes.Persistences.ReviewsManager import ReviewsManager
from utils.api import make_error

api = Namespace("reviews", description="Reviews related operations")

reviews_model = api.model(
    "Reviews", 
    {
        "id": fields.String(required=True, description="The review id"),
        "user_id": fields.String(required=True, description="The review user_id"),
        "place_id": fields.String(required=True, description="The review place_id"),
        "rating": fields.Integer(required=True, description="The review rating"),
        "comment": fields.String(required=True, description="The review comment"),
        "created_at": fields.String(required=True, description="The review created_at"),
        "updated_at": fields.String(required=True, description="The review updated_at"),
    },
)

reviews_model_entry = api.model(
    "ReviewsEntry",
    {
        "user_id": fields.String(required=True, description="The amenity user_id"),
        "rating": fields.Integer(required=True, description="The amenity rating"),
        "comment": fields.String(required=True, description="The amenity comment")
    }
)
reviews_model_response = api.model(
    "ReviewsResponse", 
    {
        "message": fields.String(required=True, description="Message Response"),
        "data": fields.Nested(reviews_model),
    },
)

@api.route("/")
@api.response(400, "Bad Request")
@api.response(409, "Conflict")
class ReviewsList(Resource):
    @api.doc("list_reviews")
    @api.response(200, "List all reviews", reviews_model)
    def get(self):
        """List all reviews"""
        reviews = ReviewsManager().getReviews()
        if not reviews:
            return marshal([], reviews_model)
        return marshal([review.toJSON() for review in reviews], reviews_model)

@api.route("/<id>")
@api.param("id", "The reviews identifier")
@api.response(404, "Review not found")
@api.response(400, "Bad Request")
@api.response(409, "Conflict")
class ReviewsRetrieve(Resource):
    @api.doc("get_reviews")
    @api.response(200, "Get a review", reviews_model)
    def get(self, id):
        review = ReviewsManager().getReview(id)
        if review:
            return marshal(review.toJSON(), reviews_model)
        make_error(api, 404, "Review {} doesn't exist".format(id))
    
    @api.doc('update_reviews')
    @api.expect(reviews_model_entry)
    @api.response(201, "Update a review", reviews_model_response)
    def put(self, id):
        """Update a review"""
        if not request.is_json:
            make_error(api, 400, "Missing JSON in request.")

        review = ReviewsManager().getReview(id)
        if not review:
            make_error(api, 404, "Review {} doesn't exist".format(id))

        data: dict = request.json
        data['id'] = id

        try:
            updated_review = ReviewsManager().updateReview(data)
            return marshal({
                "message": "Review updated.",
                "data": updated_review.toJSON()
            }, reviews_model_response), 201
        except ValueError as e:
            make_error(api, 400, e)
        except TypeError as e:
            make_error(api, 409, e)

    @api.doc('delete_reviews')
    @api.response(204, "Delete a user", reviews_model_response)
    def delete(self, id):
        """Delete a review"""
        review = ReviewsManager().getReview(id)
        if not review:
            make_error(api, 404, "Review {} doesn't exist".format(id))

        ReviewsManager().deleteReview(id)

        return marshal({
            "message": "Review deleted.",
            "data": review.toJSON()
        }, reviews_model_response), 204