from flask import Blueprint, jsonify
from app.functions import my_function

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/')
def hello_world():
    result = my_function()
    return jsonify(result)
