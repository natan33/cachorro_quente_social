from flask import Blueprint

main = Blueprint('main', __name__)

from app.view.main import routes
