#!/usr/bin/python3
""""""
from api.v1.views import app_views
from flask import make_response, jsonify, abort, request
from models import storage
from os import environ
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

storage_t = environ.get('HBNB_TYPE_STORAGE')

@app_views.route(
        '/places/<place_id>/amenities',
        methods=["GET"],
        strict_slashes=False
        )
def get_place_amenities(place_id):
    """get amenities of a place"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    place_amenity = []
    for amenity in place.amenities():
            place_amenity.append(amenity.to_dict())

    return make_response(jsonify(place_amenity), 200)

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

    if storage_t == "db":
        if amenity in place.amenities:
            place.amenities.remove(amenity)
    else:
        if amenity.id in place.amenity_ids:
            place.amenity_ids.remove(amenity.id)

    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=["POST"],
        strict_slashes=False)
def create_place_amenity(place_id):
    """create a place amenity"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None:
        abort(404)

    if amenity is None:
        abort(404)

    if storage_t == "db":
        if amenity not in place.amenities:
            place.amenities.append(amenity)
        else:
            return make_response(jsonify(amenity.to_dict())), 200
    else:
        if amenity.id not in place.amenity_ids:
            place.amenity_ids.append(amenity.id)
        else:
            return make_response(jsonify(amenity.to_dict())), 200


    storage.save()
    return jsonify(amenity.to_dict()), 201
