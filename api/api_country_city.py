#!/usr/bin/python3
from flask import Flask, jsonify, request, abort
from model.city import City
import uuid
import pycountry
from persistence.data_manager import DataManager

app = Flask(__name__)
data_manager = DataManager()


def find_country_by_code(country_code):
    try:
        country = pycountry.countries.get(alpha_2=country_code.upper())
        if country:
            return {
                "id": str(uuid.uuid4()),
                "name": country.name,
                "iso_3166_1_alpha_2": country.alpha_2
            }
    except KeyError:
        return None


def validate_city_data(data, is_update=False):
    if 'name' not in data or 'population' not in data or 'country_code' not in data:
        abort(400, description="Missing required fields: name, population, country_code")
    if not find_country_by_code(data['country_code']):
        abort(404, description=f"Country with code '{data['country_code']}' not found")
    if not is_update:
        if any(city['name'] == data['name'] and city['country_code'] == data['country_code'] for city in data_manager.get_all('City')):
            abort(409, description=f"City '{data['name']}' already exists in country '{data['country_code']}'")


@app.route('/countries', methods=['GET'])
def get_countries():
    countries = [
        {
            "name": country.name,
            "iso_3166_1_alpha_2": country.alpha_2
        } for country in pycountry.countries
    ]
    return jsonify(countries), 200
