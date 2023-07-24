from flask import Blueprint

bp = Blueprint('find', __name__, url_prefix='/find')

from . import routes