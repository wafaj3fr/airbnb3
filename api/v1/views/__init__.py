#!/usr/bin/python3
"""Flask app blueprint"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *

""""
task 6
"""

from api.v1.views.states import *

"""
task 7
"""

from api.v1.views.cities import *

"""
task 8
"""

from api.v1.views.amenities import *

"""
task 9
"""

from api.v1.views.users import *

"""
task 10
"""

from api.v1.views.places import *

"""
task 11
"""

from api.v1.views.places_reviews import *