from flask import Blueprint
from flask_bootstrap import Bootstrap5

auth = Blueprint('auth', __name__)

from . import views