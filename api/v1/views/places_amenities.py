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
        '/places/<place_id>/amenities',
        methods=["GET"],
        strict_slashes=False
        )
def get_place_amenities(place_id):
    """get amenities of a place"""
    place = storage.get(Place, place_id)
    amenities = storage.all(Amenity)

    if place is None:
        abort(404)

    place_amenity = []
    for amenity in amenities.values():
        if amenity.place_id == place_id:
            place_amenity.append(review.to_dict())

    return make_response(jsonify(place_amenity), 200)


@app_views.route(
        '/amenities/<amenity_id>',
        methods=["GET"],
        strict_slashes=False)
def get_place_amenity(amenity_id):
    """get a specific amenity of a place"""
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    return make_response(jsonify(amenity.to_dict()), 200)


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=["DELETE"],
        strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """deletes a amenity"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=["POST"],
        strict_slashes=False)
def create_place_amenity(place_id):
    """create a place review"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None:
        abort(404)

    if amenity is None:
        abort(404)

    if not request.get_json(force=True):
        abort(400, description="Not a JSON")

    data = request.get_json()
    data["place_id"] = place.id
    ignore = ["id", "created_at", "updated_at"]

    for key, value in data.items():
        if key not in ignore:
            setattr(amenity, key, value)

    amenity.save()
    storage.save()
    return jsonify(amenity.to_dict()), 201
