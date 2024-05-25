#!/usr/bin/python3
"""create place view"""

from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places(city_id):
    """get all places"""
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """get a place"""
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """delete a place"""
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """create a place"""
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    if request.content_type != 'application/json':
        return abort(404, "Not a JSON")
    data = request.get_json()
    if data is None:
        return abort(400, "Not a JSON")
    if "user_id" not in data:
        return abort(400, "Missing user_id")
    user = storage.get(User, data['user_id'])
    if user is None:
        return abort(404)
    if "name" not in data:
        return abort(400, "Missing name")
    place = Place(city_id=city_id, **data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """update a place"""
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    if request.content_type != 'application/json':
        return abort(404, "Not a JSON")
    data = request.get_json()
    if data is None:
        return abort(400, "Not a JSON")
    for k, v in data.items():
        if k not in ['id', 'user_id', 'city_id', 'created]at', 'updated_at']:
            setattr(place, k, v)
    storage.save()
    return jsonify(place.to_dict()), 200