#!/usr/bin/python3
from flask import Blueprint, jsonify, request, abort
from model.amenities import Amenities
from persistence.data_manager import DataManager


api_amenities = Blueprint('api_amenities', __name__)
data_manager = DataManager()

@api_amenities.route('/amenities', methods=['POST'])
def create_amenity():
    data = request.get_json()
    amenity = Amenities(name=data['name'])
    data_manager.save(amenity)
    return jsonify(amenity.to_dict()), 201

@api_amenities.route('/amenities', methods=['GET'])
def get_amenities():
    amenities = list(data_manager.storage.get("Amenities", {}).values())
    return jsonify(amenities), 200

@api_amenities.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = data_manager.get(amenity_id, 'Amenities')
    if not amenity:
        abort(404, description="Amenity not found")
    return jsonify(amenity), 200

@api_amenities.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    data = request.get_json()
    amenity = data_manager.get(amenity_id, 'Amenities')
    if not amenity:
        abort(404, description="Amenity not found")

    amenity_instance = Amenities(name=data['name'])
    amenity_instance.id = amenity_id
    data_manager.update(amenity_instance)
    return jsonify(amenity_instance.to_dict()), 200

@api_amenities.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = data_manager.get(amenity_id, 'Amenities')
    if not amenity:
        abort(404, description="Amenity not found")
    data_manager.delete(amenity_id, 'Amenities')
    return '', 204