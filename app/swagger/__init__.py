from flask import Blueprint

swagger_bp = Blueprint('swagger_bp', __name__)

from . import swagger_ui
