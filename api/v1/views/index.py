#!/usr/bin/python3
""""""
from api.v1.views import app_views
from flask import jsonify
from models.engine.file_storage import classes
from models import storage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


@app_views.route('/status', methods=["GET"], strict_slashes=False)
def status():
    """returns a JSON"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=["GET"], strict_slashes=False)
def stats():
    """retrieves the number of each objects by type"""

    classes = {
            "Amenity": "amenities",
            "Place": "places",
            "State": "states",
            "User": "users",
            "City": "cities",
            "Review": "reviews"}

    new_dict = {}
    for cls in classes:
        if cls != "BaseModel":
            new_dict[classes[cls]] = storage.count(cls)

    return jsonify(new_dict)
