from flask_restful import Resource
from flask import request

"""
API should respond to GET requests like http://localhost:8080/forecasts&city=Berlin with a valid JSON
object that includes the fields min_temp, max_temp, rain_sum, wind_speed and a classification (i.e. sunny,
rainy, windy, or stormy) based on rain_sum and wind_speed with self-chosen thresholds.
"""


class GetWeather(Resource):
    """
    GET request for weather data with GET parameter city
    example: http://localhost:8080/forecasts&city=Berlin
    :param: city: str
    :return: weather_data: dict with {"min_temp": float,
                                      "max_temp": float,
                                      "rain_sum": float,
                                      "wind_speed": float,
                                      "classification": str
                                      }
    """

    def get(self):

        # check if city parameter is present
        # wäre auch einfacher umzusetzten, ist aber so besser erweiterbar falls noch mehr parameter hinzukommen
        obligatory_fields = ["city"]
        for field in obligatory_fields:
            if field not in request.args:
                return {"message": f"{field} not found"}, 400

        # get city from request
        city = request.args["city"]


