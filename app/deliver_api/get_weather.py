from flask_restful import Resource
from flask import request
#import helper file:
from ..helper import openmeteo_helper as omh
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

    functionality:
    - get geocode for city
    - get weather data for geocode
    - parse weather data
    - return weather data
    """

    def get(self, city):

        # check if city parameter is present and a string
        if not city:
            return {"message": "no city parameter given"}, 400
        if not isinstance(city, str):
            return {"message": "city parameter must be a string"}, 400

        weather_api = omh.OpenMeteoWeather()

        # get geocode for city
        try:
            openmeteo_json = weather_api.get_geocode(city)
        except Exception as e:
            return {"message": f"could not get geocode for city: {city}"}, 500
        # print(f"openmeteo_json: {openmeteo_json}")


        # get geocodes for first city in json
        try:
            latitude, longitude = weather_api.get_first_city_coords(openmeteo_json)
        except Exception as e:
            return {"message": f"could not get geocode for city: {city}"}, 500
        # print(f"latitude: {latitude}, longitude: {longitude}")

        # get weather data for geocode
        try:
            weather_json = weather_api.get_weather(latitude, longitude)
        except Exception as e:
            return {"message": f"could not get weather for lat: {latitude}, lon: {longitude}"}, 500
        # print(f"weather_json: {weather_json}")

        # parse weather data
        try:
            weather_data = weather_api.parse_weather_response(weather_json)
        except Exception as e:
            return {"message": "could not parse weather data"}, 500
        print(f"weather_data: {weather_data}")

        # return weather data
        return weather_data, 200





