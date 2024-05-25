#!/usr/bin/python3
"""create amenity view"""

from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', strict_slashes=False)
def get_amenities():
    """get all amenities"""
    amenities = storage.all(Amenity)
    amenities = [amenity.to_dict() for amenity in amenities.values()]
    return jsonify(amenities)
    # amenities = []
    # for k, v in storage.all(Amenity).items():
    #     amenities.append(v.to_dict())
    # return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity(amenity_id):
    """get an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """delete an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """create an amenity"""
    if request.content_type != 'application/json':
        return abort(404, "Not a JSON")
    data = request.get_json()
    if data is None:
        return abort(400, "Not a JSON")
    if "name" not in data:
        return abort(400, "Missing name")
    amenity = Amenity(**data)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """update an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    if request.content_type != 'application/json':
        return abort(404, "Not a JSON")
    data = request.get_json()
    if data is None:
        return abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict())