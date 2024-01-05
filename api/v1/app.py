#!/usr/bin/python3
""" The app file """
from os import getenv

from flask import Flask, jsonify
from flask_cors import CORS

from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, origins="0.0.0.0")


@app.teardown_appcontext
def teardown_flask(exception):
    """The Flask app/request context end event listener."""
    # print(exception)
    storage.close()


@app.errorhandler(404)
def handle_404(err):
    """Handles the 404 HTTP error code."""
    return jsonify(error="Not found"), 404


@app.errorhandler(400)
def handle_400(err):
    """Handles the 400 HTTP error code."""
    if err.description:
        return jsonify(error=err.description), 400
    return jsonify(error="Bad Request"), 400


if __name__ == "__main__":
    env_host = getenv("HBNB_API_HOST", "0.0.0.0")
    env_port = getenv("HBNB_API_PORT", "5000")
    app.run(host=env_host, port=env_port, threaded=True)
