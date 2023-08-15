import requests
from datetime import datetime, timedelta

from marshmallow import ValidationError

#import openmeteo_schema
from app.schemas.openmeteo_schemas import ResponseSchema, LocationSchema

class OpenMeteoWeather:
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"    #forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m
        self.geocode_base_url = "https://geocoding-api.open-meteo.com/v1/"  #search?name=Berlin&count=10&language=en&format=json


   # get geocode for city
    def get_geocode(self, city):
        """
        #gets the geocode for citys with the given name
        :param city:
        :return: json with geocodes and additional information for all cities with the given name
        example:    {'results':
                        [
                        {'id': 2950159,
                        'name': 'Berlin',
                        'latitude': 52.52437,
                        'longitude': 13.41053,
                        'elevation': 74.0,
                        'feature_code': 'PPLC',
                        'country_code': 'DE',
                        'admin1_id': 2950157,
                        'admin3_id': 6547383,
                        'admin4_id': 6547539,
                        'timezone': 'Europe/Berlin',
                        'population': 3426354,
                        'postcodes': ['10967', '13347'],
                        'country_id': 2921044,
                        'country': 'Germany',
                        'admin1': 'Land Berlin',
                        'admin3': 'Berlin, Stadt',
                        'admin4': 'Berlin'},

                        {'id': 5083330,
                        'name': 'Berlin',
                        'latitude': 44.46867,
                        'longitude': -71.18508,
                        'elevation': 311.0,
                        'feature_code': 'PPL',
                        'country_code': 'US',
                        'admin1_id': 5090174,
                        'admin2_id': 5084973,
                        'admin3_id': 5083340,
                        'timezone': 'America/New_York',
                        'population': 9367,
                        'postcodes': ['03570'],
                        'country_id': 6252001,
                        'country': 'United States',
                        'admin1': 'New Hampshire',
                        'admin2': 'Coos', 'admin3':
                        'City of Berlin'},
                        {'id': 4500771, 'name': 'Berlin', ...}
                        ],
                    'generationtime_ms': 1.0390282}

        """
        url = self.geocode_base_url + "search?name=" + city + "&count=10&language=en&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            response_json = response.json()
            return response_json
        else:
            return {"error": response.status_code, "message": f"could not get geocode for city: {city}"}, 500

    def get_first_city_coords(self, openmeteo_json):
        """
        :param openmeteo_json: json with geocodes and additional information for all cities with the given name
        :return: latitude and longitude of first city in json
        """
        #check if given json is valid:
        response_schema = ResponseSchema()
        data = openmeteo_json
        print(f"data: {data}")
        try:
            result = response_schema.load(data)
        except ValidationError as err:
            print("Validation errors:", err.messages)
        else:
            print("Validation successful")

        # get latitude and longitude of first city in json
        # the keys must be there because we checked the json with the schema.
        # Look at the schema for more information in "schema/openmeteo_schema.py"
        latitude = openmeteo_json["results"][0]["latitude"]
        longitude = openmeteo_json["results"][0]["longitude"]
        return latitude, longitude


    def get_weather(self, latitude, longitude, hourly="temperature_2m"):
        """

        :param latitude: float
        :param latitude:
        :param longitude:
        :param hourly:
        :return:

        https://open-meteo.com/en/docs
        """


# test:
city = "Berlin"

weather_client = OpenMeteoWeather()
geocode = weather_client.get_geocode(city)
print(f"geocode: {geocode}")

latitude, longitude = weather_client.get_first_city_coords(geocode)
print(f"latitude: {latitude}, longitude: {longitude}")
