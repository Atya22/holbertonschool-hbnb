#!usr/bin/python3
from flask import Blueprint, jsonify, request, abort
from model.place import Place
from model.city import City
from model.amenities import Amenities
from model.users import User  # Asegúrate de tener la clase User importada
from persistence.data_manager import DataManager
from datetime import datetime

api_place = Blueprint('api_place', __name__)
data_manager = DataManager()

# Function to meet a city by your ID
def find_city(city_id):
    city_data = data_manager.get(city_id, 'City')
    if city_data:
        return City(city_data['name'], city_data['population'], city_data['country_code'])
    return None

# Function to find updates for your ID
def find_amenities(amenity_ids):
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

@api_place.route('/places', methods=['POST'])
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
@api_place.route('/places', methods=['GET'])
def get_places():
    places = list(data_manager.storage.get('Place', {}).values())
    return jsonify(places), 200

# Route to get a place by your ID
@api_place.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    place_data = data_manager.get(place_id, 'Place')
    if not place_data:
        abort(404, description="Place not found")

    place = Place(**place_data)
    detailed_place = add_detailed_info(place.to_dict())
    return jsonify(detailed_place), 200

@api_place.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    data = request.json
    place_data = data_manager.get(place_id, 'Place')
    if not place_data:
        abort(404, description="Place not found")

    place = Place(**place_data)
    # Validation of entry data
    if 'latitude' in data or 'longitude' in data:
        validate_coordinates(data.get('latitude', place.latitude), data.get('longitude', place.longitude))
    if 'number_of_rooms' in data:
        validate_non_negative_integer(data.get('number_of_rooms'), 'number_of_rooms')
    if 'number_of_bathrooms' in data:
        validate_non_negative_integer(data.get('number_of_bathrooms'), 'number_of_bathrooms')
    if 'max_guests' in data:
        validate_non_negative_integer(data.get('max_guests'), 'max_guests')
    if 'price_per_night' in data:
        validate_price(data.get('price_per_night'))
    if 'city_id' in data:
        validate_city_id(data.get('city_id'))
    if 'amenity_ids' in data:
        validate_amenity_ids(data.get('amenity_ids', []))

    place.name = data.get('name', place.name)
    place.description = data.get('description', place.description)
    place.address = data.get('address', place.address)
    place.city = find_city(data.get('city_id')) if data.get('city_id') else place.city
    place.latitude = data.get('latitude', place.latitude)
    place.longitude = data.get('longitude', place.longitude)
    place.number_of_rooms = data.get('number_of_rooms', place.number_of_rooms)
    place.number_of_bathrooms = data.get('number_of_bathrooms', place.number_of_bathrooms)
    place.price_per_night = data.get('price_per_night', place.price_per_night)
    place.max_guests = data.get('max_guests', place.max_guests)
    place.amenities = find_amenities(data.get('amenity_ids', [])) if 'amenity_ids' in data else place.amenities

    data_manager.update(place)

    return jsonify(place.to_dict()), 200

@api_place.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    place_data = data_manager.get(place_id, 'Place')
    if not place_data:
        abort(404, description="Place not found")

    data_manager.delete(place_id, 'Place')

    return jsonify({"message": "Place deleted successfully"}), 204

def add_detailed_info(place):
    place["city"] = data_manager.get(place["city"]["id"], "City").to_dict() if place.get("city") else None
    place["amenities"] = [data_manager.get(amenity["id"], "Amenities").to_dict() for amenity in place.get("amenities", [])]
    place["host"] = data_manager.get(place["host_id"], "User").to_dict() if place.get("host_id") else None
    return place
