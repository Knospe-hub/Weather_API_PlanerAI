from marshmallow import Schema, fields, validate, pre_load, post_load, post_dump, validates_schema
from marshmallow.validate import ValidationError
import re

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
