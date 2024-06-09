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


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    states = storage.all(State)
    new_list = [state.to_dict() for state in states.values()]
    return jsonify(new_list)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """Retrieve particular state"""
    states = storage.all(State)
    for state in states.values():
        if state.id == state_id:
            return jsonify(state.to_dict()), 200
    else:
        abort(404)


@app_views.route(
        "/states/<state_id>",
        methods=["DELETE"],
        strict_slashes=False)
def delete_state(state_id):
    """delete a state"""
    states = storage.all(State)
    for state in states.values():
        if state.id == state_id:
            storage.delete(state)
            storage.save()
            return make_response(jsonify("[]"), 200)
    else:
        abort(404)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """creates a state instance"""
    dct = request.get_json()
    instance = State(**dct)

    instance.save()
    storage.save()
    return make_response(jsonify(instance.to_dict()), 200)


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Updates a state"""
    states = storage.all(State)
    dct = request.get_json()
    ignore = ["id", "created_at", "updated_at"]
    instance = storage.get(State, state_id)

    if instance is None:
        abort(404)

    if dct is None:
        abort(404, "Not a JSON")

    for key, value in dct.items():
        if key not in ignore:
            setattr(instance, key, value)
    else:
        instance.save()
        storage.save()
        return jsonify(instance.to_dict()), 200
