#!usr/bin/python3
from flask import Flask, jsonify, request, abort
from model.place import Place
from model.city import City
from model.amenities import Amenities
from model.users import User  # Asegúrate de tener la clase User importada
from persistence.data_manager import DataManager
from datetime import datetime

app = Flask(__name__)
data_manager = DataManager()

# Function to meet a city by your ID
def find_city(city_id):
    city_data = data_manager.get(city_id, 'City')
    if city_data:
        return City(city_data['name'], city_data['population'], city_data['country_code'])
    return None

# Function to find updates for your ID
    amenities = []
    for amenity_id in amenity_ids:
        amenity_data = data_manager.get(amenity_id, 'Amenities')
        if amenity_data:
            amenities.append(Amenities(name=amenity_data['name']))
    return amenities

# Function to validate coordinates
def validate_coordinates(latitude, longitude):
    if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
        abort(400, description="Invalid geographical coordinates")

# Function to validate that a value is a non-negative entry
def validate_non_negative_integer(value, field_name):
    if not isinstance(value, int) or value < 0:
        abort(400, description=f"{field_name} must be a non-negative integer")

# Function to validate the price
def validate_price(price):
    if not isinstance(price, (int, float)) or price < 0:
        abort(400, description="Price per night must be a valid non-negative numerical value")

def validate_city_id(city_id):
    if not find_city(city_id):
        abort(400, description="Invalid city_id, city does not exist")

def validate_amenity_ids(amenity_ids):
    for amenity_id in amenity_ids:
        if not data_manager.get(amenity_id, 'Amenities'):
            abort(400, description=f"Invalid amenity_id {amenity_id}, amenity does not exist")

@app.route('/places', methods=['POST'])
def create_place():
    data = request.get_json()
    if not data:
        abort(400, description="Invalid input")

    # Validate inputs
    validate_coordinates(data.get('latitude'), data.get('longitude'))
    validate_non_negative_integer(data.get('number_of_rooms'), 'number_of_rooms')
    validate_non_negative_integer(data.get('number_of_bathrooms'), 'number_of_bathrooms')
    validate_non_negative_integer(data.get('max_guests'), 'max_guests')
    validate_price(data.get('price_per_night'))
    validate_city_id(data.get('city_id'))
    validate_amenity_ids(data.get('amenity_ids', []))

    new_place = Place(
        name=data.get('name'),
        description=data.get('description'),
        address=data.get('address'),
        city=find_city(data.get('city_id')),
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        host_id=data.get('host_id'),
        number_of_rooms=data.get('number_of_rooms'),
        number_of_bathrooms=data.get('number_of_bathrooms'),
        price_per_night=data.get('price_per_night'),
        max_guests=data.get('max_guests'),
        amenities=find_amenities(data.get('amenity_ids', []))
    )

    data_manager.save(new_place)

    return jsonify(new_place.to_dict()), 201
@app.route('/places', methods=['GET'])
def get_places():
    places = list(data_manager.storage.get('Place', {}).values())
    return jsonify(places), 200


@app.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    place_data = data_manager.get(place_id, 'Place')
    if not place_data:
        abort(404, description="Place not found")

    place = Place(**place_data)
    detailed_place = add_detailed_info(place.to_dict())
    return jsonify(detailed_place), 200

@app.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    data = request.json
    place_data = data_manager.get(place_id, 'Place')
    if not place_data:
        abort(404, description="Place not found")

    place = Place(**place_data)