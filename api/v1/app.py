#!/usr/bin/python3
"""api app"""
from flask import Flask
from models import storage
import app_views from api.v1.views
from os import environ
from flask_cors import CORS

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def close(self):
    """calls storage.close()"""
    storage.close()

app.config['SWAGGER'] = {
    'title': 'AirBnB clone Restful API',
    'uiversion': 3
}

if __name__ == "__main__":
    """ runs the flask app """
    host = environ.get("HBNB_API_HOST")
    port = environ.get("HBNB_API_PORT")

    if host is None:
        host = "0.0.0.0"
    if not port:
        port = "5000"

    app.run(host=host, port=port, threaded=True)
