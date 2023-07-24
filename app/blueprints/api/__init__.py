from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/api')

from . import poke_api_routes, my_poke_routes