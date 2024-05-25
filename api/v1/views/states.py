#!/usr/bin/python3
"""create state view"""

from flask import jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views

@app_views.route('/states', strict_slashes=False)
def get_states():
    """get all states"""
    states = storage.all("State") # in vid: states = storage.all(State).values()
    states = [state.to_dict() for state in states.values()] # in vid: state_list = [state.to_dict() for state in states]
    return jsonify(states) # in vid: return jsonify(state_list)

@app_views.route('/states/<state_id>', strict_slashes=False)
def get_state(state_id):
    """get a state"""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """delete a state"""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """create a state"""
    if request.content_type != 'application/json':
        return abort(404, "Not a JSON")
    data = request.get_json()
    if data is None:
        return abort(400, "Not a JSON")
    if "name" not in data:
        return abort(400, "Missing name")
    state = State(**data)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """update a state"""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    if request.content_type != 'application/json':
        return abort(404, "Not a JSON")
    data = request.get_json()
    if data is None:
        return abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200