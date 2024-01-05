#!/usr/bin/python3
"""Contains the places_amenities view for the API."""
from flask import jsonify, abort

import models
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route(
    "/places/<place_id>/amenities", methods=["GET"], strict_slashes=False
)
def retrieve_place_amenity(place_id):
    """Retrieves list of amenities of a particular place"""
    # grab place from storage
    place = storage.get(Place, place_id)

    # abort if place can't be found in storage
    if place is None:
        abort(404)

    # get the list of amenities of the place
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>", methods=["DELETE"]
)
def delete_place_amenity(place_id, amenity_id):
    """Deletes as specific amenity of a place"""
    # grab the place from storage
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    # grab the specific amenity of that place
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if models.storage_t == "db":
        # ForDBStorage, remove amenity instance from amenities relationship
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        # For FileStorage, remove amenity ID from place.amenity_ids
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
        storage.save()
        return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"])
def create_place_amenity(place_id, amenity_id):
    """Creates or links an amenity to a place if not so already"""
    # grab the place from storage
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    # grab the specific amenity of that place
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if models.storage_t == "db":
        # ForDBStorage, link amenity instance to the place if not already
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        # For FileStorage, link amenity_id to place.amenity_ids if not already
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)

    storage.save()
    return jsonify(amenity.to_dict()), 201
