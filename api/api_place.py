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

# Función para encontrar una ciudad por su ID
def find_city(city_id):
    city_data = data_manager.get(city_id, 'City')
    if city_data:
        return City(city_data['name'], city_data['population'], city_data['country_code'])
    return None

# Función para encontrar amenidades por sus IDs
def find_amenities(amenity_ids):
    amenities = []
    for amenity_id in amenity_ids:
        amenity_data = data_manager.get(amenity_id, 'Amenities')
        if amenity_data:
            amenities.append(Amenities(name=amenity_data['name']))
    return amenities

# Función para validar coordenadas
def validate_coordinates(latitude, longitude):
    if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
        abort(400, description="Invalid geographical coordinates")

# Función para validar que un valor sea un entero no negativo
def validate_non_negative_integer(value, field_name):
    if not isinstance(value, int) or value < 0:
        abort(400, description=f"{field_name} must be a non-negative integer")

# Función para validar el precio
def validate_price(price):
    if not isinstance(price, (int, float)) or price < 0:
        abort(400, description="Price per night must be a valid non-negative numerical value")
