#!/usr/bin/python3
"""Flask app_view"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def api_status():
    """status"""
    response = {'status': "OK"}
    return jsonify(response)