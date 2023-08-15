import enum
import unittest
from main import app
from flask import current_app
from app import create_app
from ..helper import openmeteo_helper
from app.schemas.openmeteo_schemas import ResponseSchema, WeatherAPISchema
# unittest for helper functions

class TestOpenMeteoHelper(unittest.TestCase):
    def setUp(self):
        self.app = create_app('unit')
        self.app_context = self.app.app_context()
        self.app_context.push()
    def tearDown(self):
        self.app_context.pop()

    def test_get_geo_code(self):
        openmeteo_instance = openmeteo_helper.OpenMeteoWeather()

        # test for valid city
        city = "Berlin"
        try:
            openmeteo_json = openmeteo_instance.get_geocode(city)
        except Exception as e:
            self.fail(f"could not get geocode for city: {city}")
        print(f"openmeteo_json: {openmeteo_json}")
        #check if response is a dict and has results
        self.assertIsInstance(openmeteo_json, dict)
        self.assertTrue(openmeteo_json["results"])

        # test for invalid city
        city = "DOES_NOT_EXIST"
        try:
            openmeteo_json = openmeteo_instance.get_geocode(city)
        except Exception as e:
            self.fail(f"could not get geocode for city: {city}")
        print(f"openmeteo_json: {openmeteo_json}")
        #check if response is a dict and has no results
        self.assertIsInstance(openmeteo_json, dict)
        self.assertFalse("results" in openmeteo_json)

    def test_get_weather(self):
        openmeteo_instance = openmeteo_helper.OpenMeteoWeather()

        # test for valid coordinates
        latitude = 52.520008
        longitude = 13.404954
        try:
            weather_json = openmeteo_instance.get_weather(latitude, longitude)
        except Exception as e:
            self.fail(f"could not get weather for lat: {latitude}, lon: {longitude}")
        print(f"weather_json: {weather_json}")
        #check if response is a dict and has all requested fields with schema
        self.assertIsInstance(weather_json, dict)
        schema = WeatherAPISchema()
        validate = schema.validate(weather_json) # returns None if valid and list of errors if not
        print(f"validate: {validate}")
        self.assertEqual(validate, {})

        # test for invalid coordinates
        latitude = -99
        longitude = 90
        try:
            weather_json = openmeteo_instance.get_weather(latitude, longitude)
        except Exception as e:
            self.fail(f"could not get weather for lat: {latitude}, lon: {longitude}")
        print(f"weather_json: {weather_json}")
        ##check if response is a dict and has all requested fields with schema. Must fail
        self.assertIsInstance(weather_json, dict)
        schema = WeatherAPISchema()
        validate = schema.validate(weather_json)  # returns None if valid and list of errors if not
        print(f"validate2: {validate}")
        self.assertTrue("error" in validate)








