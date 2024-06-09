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
        '/amenities',
        methods=["GET"],
        strict_slashes=False
        )
def get_amenities():
    """get amenities"""
    amenities = storage.all(Amenity)

    lst = [m.to_dict() for m in amenities.values()]
    return make_response(jsonify(lst), 200)


@app_views.route(
        '/amenities/<amenity_id>',
        methods=["GET"],
        strict_slashes=False)
def get_amenity(amenity_id):
    """get a specific amenity"""
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    return make_response(jsonify(amenity.to_dict()), 200)


@app_views.route(
        '/amenities/<amenity_id>',
        methods=["DELETE"],
        strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes an amenity"""
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/amenities',
        methods=["POST"],
        strict_slashes=False)
def create_amenity():
    """create a amenity"""

    if not request.get_json(force=True):
        abort(400, description="Not a JSON")

    if "name" not in request.get_json(force=True):
        abort(400, description="Missing name")

    dct = request.get_json()
    instance = Amenity(**dct)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route(
        '/amenities/<amenity_id>',
        methods=["PUT"],
        strict_slashes=False)
def update_amenity(amenity_id):
    """update a amenity"""
    amenity = storage.get(Amenity, amenity_id)

    if not request.get_json(force=True):
        abort(400, description="Not a JSON")

    if amenity is None:
        abort(404)

    ignore = ["id", "created_at", "updated_at"]
    data = request.get_json()

    for key, value in data.items():
        if key not in ignore:
            setattr(amenity, key, value)

    amenity.save()
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
