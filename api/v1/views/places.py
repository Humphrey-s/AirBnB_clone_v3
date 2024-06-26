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
        '/cities/<city_id>/places',
        methods=["GET"],
        strict_slashes=False
        )
def get_places(city_id):
    """get cities of a state"""
    city = storage.get(City, city_id)
    places = storage.all(Place)

    if city is None:
        abort(404)

    city_place = []
    for place in places.values():
        if place.city_id == city_id:
            city_place.append(place.to_dict())

    return make_response(jsonify(city_place), 200)


@app_views.route(
        'places/<place_id>',
        methods=["GET"],
        strict_slashes=False)
def get_place(place_id):
    """get a specific place"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    return make_response(jsonify(place.to_dict()), 200)


@app_views.route(
        '/places/<place_id>',
        methods=["DELETE"],
        strict_slashes=False)
def delete_place(place_id):
    """deletes a place"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/cities/<city_id>/places',
        methods=["POST"],
        strict_slashes=False)
def create_place(city_id):
    """create a place"""
    city = storage.get(City, city_id)
    user_id = request.get_json(force=True).get("user_id")
    user = storage.get(User, user_id)

    if city is None:
        abort(404)

    if not request.get_json(force=True):
        abort(400, description="Not a JSON")

    if "user_id" not in request.get_json(force=True):
        abort(400, description="Missing user_id")

    if user is None:
        abort(404)

    if "name" not in request.get_json(force=True):
        abort(400, description="Missing name")

    dct = request.get_json()
    dct["city_id"] = city.id
    instance = Place(**dct)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route(
        '/places/<place_id>',
        methods=["PUT"],
        strict_slashes=False)
def update_place(place_id):
    """update a place"""
    place = storage.get(Place, place_id)

    if not request.get_json(force=True):
        abort(400, description="Not a JSON")

    if place is None:
        abort(404)

    ignore = ["id", "user_id", "created_at", "updated_at", "city_id"]
    data = request.get_json()

    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)

    place.save()
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route(
        '/places_search',
        methods=["POST"],
        strict_slashes=False)
def place_search():
    """retrieves all Place objects depending of the JSON"""

    if not request.get_json(force=True):
        abort(400, description="Not a JSON")

    data = request.get_json(force=True)

    if not data or not len(data):
        lst = [p.to_dict() for p in storage.all(Place).values()]
        return jsonify(lst), 200

    results = []
    cities = storage.all(City).values()
    places = storage.all(Place).values()
    amenities = storage.all(Amenity).values()
    s_cities = []

    if "states" in data.keys():
        for state in data["states"]:
            obj = storage.get(State, state)
            if obj is not None:
                s_cities = [city for city in cities if city.state_id == obj.id]

    if "cities" in data.keys():
        for city_id in data["cities"]:
            city = storage.get(City, city_id)
            if city not in s_cities:
                s_cities.append(city)

    pre_places = []
    for city in s_cities:
        for place in places:
            if place.city_id == city.id:
                pre_places.append(place)

    results = pre_places[:]

    if "amenities" in data.keys():
        for amenity_id in data["amenities"]:
            amenity = storage.get(Amenity, amenity_id)
            for p in pre_places:
                if storage_t == "db":
                    if amenity in p.amenities:
                        if p not in results:
                            results.append(p)
                    else:
                        if p in results:
                            results.remove(p)
                else:
                    if amenity.id in p.amenity_ids:
                        if amenity not in results:
                            results.append(p)
                    else:
                        if p in results:
                            results.remove(p)

    results = [r.to_dict() for r in results]
    return jsonify(results), 201
