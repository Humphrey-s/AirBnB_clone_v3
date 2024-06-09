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
        '/states/<state_id>/cities',
        methods=["GET"],
        strict_slashes=False
        )
def get_cities(state_id):
    """get cities of a state"""
    state = storage.get(State, state_id)
    cities = storage.all(City)

    if state is None:
        abort(404)

    state_cities = []
    for city in cities.values():
        if city.state_id == state_id:
            state_cities.append(city.to_dict())

    return make_response(jsonify(state_cities), 200)


@app_views.route(
        'cities/<city_id>',
        methods=["GET"],
        strict_slashes=False)
def get_city(city_id):
    """get a specific city"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    return make_response(jsonify(city.to_dict()), 200)


@app_views.route(
        '/cities/<city_id>',
        methods=["DELETE"],
        strict_slashes=False)
def delete_city(city_id):
    """deletes a city"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/states/<state_id>/cities',
        methods=["POST"],
        strict_slashes=False)
def create_city(state_id):
    """create a city"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    if not request.get_json(force=True):
        abort(400, description="Not a JSON")

    if "name" not in request.get_json(force=True):
        abort(400, description="Missing name")

    dct = request.get_json()
    dct["state_id"] = state.id
    instance = City(**dct)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route(
        '/cities/<city_id>',
        methods=["PUT"],
        strict_slashes=False)
def update_city(city_id):
    """update a city"""
    city = storage.get(City, city_id)

    if not request.get_json(force=True):
        abort(400, description="Not a JSON")

    if city is None:
        abort(404)

    ignore = ["id", "created_at", "updated_at", "state_id"]
    data = request.get_json()

    for key, value in data.items():
        if key not in ignore:
            setattr(city, key, value)

    city.save()
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
