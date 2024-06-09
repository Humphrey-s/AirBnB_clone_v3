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
        '/users',
        methods=["GET"],
        strict_slashes=False
        )
def get_users():
    """get users"""
    users = storage.all(User)

    lst = [m.to_dict() for m in users.values()]
    return make_response(jsonify(lst), 200)


@app_views.route(
        '/users/<user_id>',
        methods=["GET"],
        strict_slashes=False)
def get_user(user_id):
    """get a specific user"""
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    return make_response(jsonify(user.to_dict()), 200)


@app_views.route(
        '/users/<user_id>',
        methods=["DELETE"],
        strict_slashes=False)
def delete_user(user_id):
    """deletes a user"""
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/users',
        methods=["POST"],
        strict_slashes=False)
def create_user():
    """create a amenity"""

    if not request.get_json(force=True):
        abort(400, description="Not a JSON")

    if "name" not in request.get_json(force=True):
        abort(400, description="Missing name")

    if "email" not in request.get_json(force=True):
        abort(400, description="Missing email")

    if "password" not in request.get_json(force=True):
        abort(400, description="Missing password")

    dct = request.get_json()
    instance = User(**dct)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route(
        '/users/<user_id>',
        methods=["PUT"],
        strict_slashes=False)
def update_user(user_id):
    """update a user"""
    user = storage.get(User, user_id)

    if not request.get_json(force=True):
        abort(400, description="Not a JSON")

    if user is None:
        abort(404)

    ignore = ["id", "created_at", "updated_at", "email"]
    data = request.get_json()

    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)

    user.save()
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
