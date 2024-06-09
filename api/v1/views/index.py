#!/usr/bin/python3
""""""
from api.v1.views import app_views
from flask import jsonify
from models.engine.file_storage import classes
from models import storage


@app_views.route('/status', methods=["GET"], strict_slashes=False)
def status():
    """returns a JSON"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=["GET"], strict_slashes=False)
def stats():
    """retrieves the number of each objects by type"""
    new_dict = {}
    for cls in classes:
        if cls != "BaseModel":
            new_dict[cls] = storage.count(cls)

    return jsonify(new_dict)
