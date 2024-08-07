#!usr/bin/python3
from flask import Blueprint, jsonify, request, abort
from model.place import Place
from model.city import City
from model.amenities import Amenities
from model.users import User
from persistence.data_manager import DataManager
from persistence.database import db

app = Flask(__name__)
data_manager = DataManager()

# Function to meet a city by your ID
def find_city(city_id):
    return data_manager.get(City, city_id)

# Function to find updates for your IDs
def find_amenities(amenity_ids):
    return data_manager.query_all_by_filter(Amenities, Amenities.id.in_(amenity_ids))

# Function to validate coordinates
def validate_coordinates(latitude, longitude):
    if latitude is None or longitude is None:
        abort(400, description="Latitude and longitude are required")
    if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
        abort(400, description="Invalid geographical coordinates")

# Function to validate that a value is a non-negative entry
def validate_non_negative_integer(value, field_name):
    if value is None:
        abort(400, description=f"{field_name} is required")
    if not isinstance(value, int) or value < 0:
        abort(400, description=f"{field_name} must be a non-negative integer")

# Function to validate the price
def validate_price(price):
    if price is None:
        abort(400, description="Price per night is required")
    if not isinstance(price, (int, float)) or price < 0:
        abort(400, description="Price per night must be a valid non-negative numerical value")

def validate_city_id(city_id):
    if not city_id or not find_city(city_id):
        abort(400, description="Invalid city_id, city does not exist")

def validate_amenity_ids(amenity_ids):
    if not isinstance(amenity_ids, list):
        abort(400, description="Amenity_ids must be a list")
    if not data_manager.query_all_by_filter(Amenities, Amenities.id.in_(amenity_ids)).count() == len(amenity_ids):
        abort(400, description="One or more amenity_ids are invalid")
        
@api.route('/places', methods=['POST'])
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
        max_guests=data.get('max_guests')
    )

    new_place.amenities = find_amenities(data.get('amenity_ids', []))

    data_manager.save(new_place)

    return jsonify(new_place.to_dict()), 201

@api_.route('/places', methods=['GET'])
def get_places():
    places = data_manager.query_all(Place)
    return jsonify(places), 200

@api.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    place_data = data_manager.get(place_id, 'Place')
    if not place:
        abort(404, description="Place not found")

    return jsonify(detailed_place), 200

@api.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    place = data_manager.get(place_id, 'Place')
    if not place:
        abort(404, description="Place not found")

    data = request.get_json()
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
    place.city_id = data.get('city_id', place.city_id)
    place.latitude = data.get('latitude', place.latitude)
    place.longitude = data.get('longitude', place.longitude)
    place.host_id = data.get('host_id', place.host_id)
    place.number_of_rooms = data.get('number_of_rooms', place.number_of_rooms)
    place.number_of_bathrooms = data.get('number_of_bathrooms', place.number_of_bathrooms)
    place.price_per_night = data.get('price_per_night', place.price_per_night)
    place.max_guests = data.get('max_guests', place.max_guests)
    place.amenities = find_amenities(data.get('amenity_ids', []))

    data_manager.update(place)
    return jsonify(place.to_dict()), 200

@app.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = data_manager.get(Place, place_id)
    if not place:
        abort(404, description="Place not found")

    data_manager.delete(place)

    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
