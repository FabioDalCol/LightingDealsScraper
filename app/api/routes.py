from flask import Blueprint
from app.services.database import test_db_connection

default_routes = Blueprint('deal_blueprint', __name__)

@default_routes.route('/')
def index():
    return "LightingDealsScraper!"

@default_routes.route('/db_test')
def db_test():
    return test_db_connection()