#!/usr/bin/python3
"""create user view"""

from flask import jsonify, abort, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', strict_slashes=False)
def get_users():
    """get all users"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id):
    """get a user"""
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """delete a user"""
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """create a user"""
    if request.content_type != 'application/json':
        return abort(404, "Not a JSON")
    data = request.get_json()
    if data is None:
        return abort(400, "Not a JSON")
    if "email" not in data:
        return abort(400, "Missing email")
    if "password" not in data:
        return abort(400, "Missing password")
    user = User(**data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """update a user"""
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    if request.content_type != 'application/json':
        return abort(404, "Not a JSON")
    data = request.get_json()
    if data is None:
        return abort(400, "Not a JSON")
    for k, v in data.items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, k, v)
    storage.save()
    return jsonify(user.to_dict()), 200


