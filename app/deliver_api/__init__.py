from flask import Blueprint

delivery_api_bp = Blueprint('delivery_resources', __name__)

from . import (
    test_endpoint,
    test_endpoint_2

)

"""
alle neuen endpoints hinzufügen
"""
