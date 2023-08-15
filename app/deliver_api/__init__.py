from flask import Blueprint

delivery_api_bp = Blueprint('delivery_resources', __name__)

from . import (
    get_weather

)

"""
alle neuen endpoints hinzufügen
"""
