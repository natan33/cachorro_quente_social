from flask import Blueprint

api = Blueprint('api', __name__,url_prefix='/')

from app.view.api import api_dashboard
