from flask import Blueprint

auth = Blueprint('auth', __name__)

from app.view.auth import routes
