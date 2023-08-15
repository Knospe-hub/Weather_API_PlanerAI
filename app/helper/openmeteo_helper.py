import requests
from datetime import datetime, timedelta
from marshmallow import ValidationError
# import openmeteo_schema
from app.schemas.openmeteo_schemas import ResponseSchema, WeatherAPISchema


class OpenMeteoWeather:
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"  # forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m
        self.geocode_base_url = "https://geocoding-api.open-meteo.com/v1/"  # search?name=Berlin&count=10&language=en&format=json

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
        # check if given json is valid:
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

    def get_weather(self, latitude, longitude, days = 5, hourly="temperature_2m&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,rain_sum,windspeed_10m_max&timezone=auto"):
        """

        :param latitude: float
        :param latitude:
        :param longitude:
        :param hourly:
        :return: response_json: json with weather data

        https://open-meteo.com/en/docs
        """
        url = self.base_url + f'?latitude={latitude}&longitude={longitude}&hourly={hourly}&forecast_days={days}'


        response = requests.get(url)
        if response.status_code == 200:
            response_json = response.json()
            return response_json
        else:
            return {"error": response.status_code, "message": f"could not get weather for lat: {latitude}, lon: {longitude}"}, 500

    def parse_weather_response(self, weather_json):
        """
        :param weather_json: json with weather data
        :return: min_temp, max_temp, rain_sum, wind_speed and a classification (i.e. sunny,
                rainy, windy, or stormy) based on rain_sum and wind_speed with defined thresholds
        """
        #check json against schema
        weather_schema = WeatherAPISchema()
        data = weather_json
        print(f"data: {data}")
        try:
            result = weather_schema.load(data)
            print(f"result: {result}")
        except ValidationError as err:
            print("Validation errors:", err.messages)
        else:
            print("Validation successful")

        #result looks like this: {'latitude': 52.52, 'longitude': 13.419998, 'generationtime_ms': 0.8810758590698242, 'utc_offset_seconds': 7200, 'timezone': 'Europe/Berlin', 'timezone_abbreviation': 'CEST', 'elevation': 46.0, 'hourly_units': {'time': 'iso8601', 'temperature_2m': '°C'}, 'hourly': {'time': ['2023-08-15T00:00', '2023-08-15T01:00', '2023-08-15T02:00', '2023-08-15T03:00', '2023-08-15T04:00', '2023-08-15T05:00', '2023-08-15T06:00', '2023-08-15T07:00', '2023-08-15T08:00', '2023-08-15T09:00', '2023-08-15T10:00', '2023-08-15T11:00', '2023-08-15T12:00', '2023-08-15T13:00', '2023-08-15T14:00', '2023-08-15T15:00', '2023-08-15T16:00', '2023-08-15T17:00', '2023-08-15T18:00', '2023-08-15T19:00', '2023-08-15T20:00', '2023-08-15T21:00', '2023-08-15T22:00', '2023-08-15T23:00', '2023-08-16T00:00', '2023-08-16T01:00', '2023-08-16T02:00', '2023-08-16T03:00', '2023-08-16T04:00', '2023-08-16T05:00', '2023-08-16T06:00', '2023-08-16T07:00', '2023-08-16T08:00', '2023-08-16T09:00', '2023-08-16T10:00', '2023-08-16T11:00', '2023-08-16T12:00', '2023-08-16T13:00', '2023-08-16T14:00', '2023-08-16T15:00', '2023-08-16T16:00', '2023-08-16T17:00', '2023-08-16T18:00', '2023-08-16T19:00', '2023-08-16T20:00', '2023-08-16T21:00', '2023-08-16T22:00', '2023-08-16T23:00'], 'temperature_2m': [21.1, 20.8, 20.6, 20.0, 19.7, 19.3, 18.9, 19.3, 20.0, 21.7, 23.8, 26.0, 26.8, 27.8, 28.7, 29.8, 30.4, 30.3, 30.0, 28.7, 26.3, 24.1, 23.4, 22.9, 22.0, 21.4, 21.1, 20.8, 20.6, 20.3, 20.0, 20.0, 20.4, 21.3, 22.3, 22.8, 23.7, 25.4, 26.5, 27.0, 26.9, 27.2, 26.6, 26.0, 24.7, 23.1, 21.8, 20.9]}, 'daily_units': {'time': 'iso8601', 'temperature_2m_max': '°C', 'temperature_2m_min': '°C', 'precipitation_sum': 'mm', 'rain_sum': 'mm', 'windspeed_10m_max': 'km/h'}, 'daily': {'time': ['2023-08-15', '2023-08-16'], 'temperature_2m_max': [30.4, 27.2], 'temperature_2m_min': [18.9, 20.0], 'precipitation_sum': [5.7, 0.3], 'rain_sum': [4.9, 0.2], 'windspeed_10m_max': [12.5, 13.5]}}

        # get weather data and filter it
        # the fields must be there because we checked the json against the schema. see "schemas/openmetei_schemas.py"
        api_response = weather_json
        daily_data = api_response['daily']
        rain_sum = daily_data['rain_sum']
        wind_speed = daily_data['windspeed_10m_max']
        min_temp = daily_data['temperature_2m_min']
        max_temp = daily_data['temperature_2m_max']

        # Thresholds for classification
        rain_threshold = 1.0  # You can adjust this value
        wind_threshold = 10.0  # You can adjust this value

        # Performing classification based on rain_sum and wind_speed
        classification = []
        for rain, wind in zip(rain_sum, wind_speed):
            if rain > rain_threshold and wind > wind_threshold:
                classification.append('stormy')
            elif rain > rain_threshold:
                classification.append('rainy')
            elif wind > wind_threshold:
                classification.append('windy')
            else:
                classification.append('sunny')

        # Printing the results
        # for i in range(len(rain_sum)):
        #     print(f"Date: {daily_data['time'][i]}")
        #     print(f"Min Temp: {min_temp[i]}°C, Max Temp: {max_temp[i]}°C")
        #     print(f"Rain Sum: {rain_sum[i]} mm, Wind Speed: {wind_speed[i]} km/h")
        #     print(f"Classification: {classification[i]}\n")

        #return json with filtered data
        return {"min_temp": min_temp, "max_temp": max_temp, "rain_sum": rain_sum, "wind_speed": wind_speed, "classification": classification}




# test:
# city = "München"
#
# weather_client = OpenMeteoWeather()
# geocode = weather_client.get_geocode(city)
# print(f"geocode: {geocode}")
#
# latitude, longitude = weather_client.get_first_city_coords(geocode)
# print(f"latitude: {latitude}, longitude: {longitude}")
#
# weather = weather_client.get_weather(latitude, longitude)
# print(f"weather: {weather}")
#
# parsed_weather = weather_client.parse_weather_response(weather)
# print(f"parsed_weather: {parsed_weather}")
