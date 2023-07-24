from flask import Blueprint

bp = Blueprint('fight', __name__, url_prefix='/fight')

from . import routes