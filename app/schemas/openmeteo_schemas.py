from marshmallow import Schema, fields, validate, pre_load, post_load, post_dump, validates_schema
from marshmallow.validate import ValidationError
import re




# schema check for geocoding api START ---------------------------------------------------------------------------------

"""
schema that checks against the documentated json schema of the openmeteo api
see here: https://open-meteo.com/en/docs/geocoding-api
"""
class LocationSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    latitude = fields.Float()
    longitude = fields.Float()
    elevation = fields.Float()
    feature_code = fields.Str()
    country_code = fields.Str()
    admin1_id = fields.Int(missing=None)  # Making the admin fields optional
    admin2_id = fields.Int(missing=None)
    admin3_id = fields.Int(missing=None)
    admin4_id = fields.Int(missing=None)
    timezone = fields.Str()
    population = fields.Int()
    postcodes = fields.List(fields.Str())  # postcodes is a list of strings. Example: 'postcodes': ['10967', '13347']
    country_id = fields.Int()
    country = fields.Str()
    admin1 = fields.Str(missing=None)
    admin2 = fields.Str(missing=None)
    admin3 = fields.Str(missing=None)
    admin4 = fields.Str(missing=None)


class ResponseSchema(Schema):
    results = fields.List(fields.Nested(LocationSchema))
    generationtime_ms = fields.Float()


# schema check for geocoding api END -----------------------------------------------------------------------------------


# schema check for weather api START -----------------------------------------------------------------------------------

"""
schema that checks against the documentated json schema of the openmeteo api
see here: https://open-meteo.com/en/docs
schema is for checking against a repsonse with this parameters: hourly = temperature_2m&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,rain_sum,windspeed_10m_max&timezone=auto
"""
class HourlyDataSchema(Schema):
    time = fields.List(fields.String())
    temperature_2m = fields.List(fields.Float())

class DailyDataSchema(Schema):
    time = fields.List(fields.String())
    temperature_2m_max = fields.List(fields.Float(), data_key='temperature_2m_max')
    temperature_2m_min = fields.List(fields.Float(), data_key='temperature_2m_min')
    precipitation_sum = fields.List(fields.Float())
    rain_sum = fields.List(fields.Float())
    windspeed_10m_max = fields.List(fields.Float(), data_key='windspeed_10m_max')

class WeatherAPISchema(Schema):
    latitude = fields.Float()
    longitude = fields.Float()
    generationtime_ms = fields.Float()
    utc_offset_seconds = fields.Integer()
    timezone = fields.String()
    timezone_abbreviation = fields.String()
    elevation = fields.Float()
    hourly_units = fields.Dict(keys=fields.String(), values=fields.String())
    hourly = fields.Nested(HourlyDataSchema)
    daily_units = fields.Dict(keys=fields.String(), values=fields.String())
    daily = fields.Nested(DailyDataSchema)

# schema check for weather api END -------------------------------------------------------------------------------------
