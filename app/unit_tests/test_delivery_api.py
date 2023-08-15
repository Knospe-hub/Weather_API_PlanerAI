import unittest
from app import create_app

class TestDeliveryAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app("unit")
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_get_weather(self):

        url = "/get_weather/"
        param = "Berlin"
        response = self.app.test_client().get(url + param)
        print(f"response: {response.json}")
        self.assertEqual(200, response.status_code)

    def test_get_weather_bad_data(self):

        url = "/get_weather/"
        param = "DOES_NOT_EXIST"
        response = self.app.test_client().get(url + param)
        print(f"response: {response.json}")
        self.assertEqual(500, response.status_code)


