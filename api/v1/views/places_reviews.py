#!/usr/bin/python3
""""""
from api.v1.views import app_views
from flask import make_response, jsonify, abort, request
from models import storage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {
            "Amenity": Amenity,
            "Place": Place,
            "State": State,
            "User": User,
            "City": City,
            "Review": Review
            }


@app_views.route(
        '/places/<place_id>/reviews',
        methods=["GET"],
        strict_slashes=False
        )
def get_reviews(place_id):
    """get reviews of a place"""
    place = storage.get(Place, place_id)
    reviews = storage.all(Review)

    if place is None:
        abort(404)

    place_review = []
    for review in reviews.values():
        if review.place_id == place_id:
            place_review.append(review.to_dict())

    return make_response(jsonify(place_review), 200)


@app_views.route(
        '/reviews/<review_id>',
        methods=["GET"],
        strict_slashes=False)
def get_review(review_id):
    """get a specific review of a place"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    return make_response(jsonify(review.to_dict()), 200)


@app_views.route(
        '/reviews/<review_id>',
        methods=["DELETE"],
        strict_slashes=False)
def delete_review(review_id):
    """deletes a review"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/places/<place_id>/reviews',
        methods=["POST"],
        strict_slashes=False)
def create_review(place_id):
    """create a place review"""
    place = storage.get(Place, place_id)
    user_id = request.get_json(force=True).get("user_id")
    user = storage.get(User, user_id)

    if place is None:
        abort(404)

    if not request.get_json(force=True):
        abort(400, description="Not a JSON")

    if "user_id" not in request.get_json(force=True):
        abort(400, description="Missing user_id")

    if user is None:
        abort(404)

    if "text" not in request.get_json(force=True):
        abort(400, description="Missing text")

    dct = request.get_json()
    dct["place_id"] = place.id
    instance = Review(**dct)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route(
        '/reviews/<review_id>',
        methods=["PUT"],
        strict_slashes=False)
def update_review(review_id):
    """update a place review"""
    review = storage.get(Review, review_id)

    if not request.get_json(force=True):
        abort(400, description="Not a JSON")

    if review is None:
        abort(404)

    ignore = ["id", "user_id", "created_at", "updated_at", "place_id"]
    data = request.get_json()

    for key, value in data.items():
        if key not in ignore:
            setattr(review, key, value)

    review.save()
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
