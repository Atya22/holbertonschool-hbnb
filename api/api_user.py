#!/usr/bin/python3
from flask import Blueprint, jsonify, request
from model.users import User
from persistence.data_manager import DataManager
import re
from uuid import UUID

api_user = Blueprint('api_user', __name__)
data_manager = DataManager()


def validate_email(email):
    email_regex = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_regex, email)


def validate_name(name):
    return isinstance(name, str) and name.strip() != ""


def validate_user_data(data):
    if not validate_email(data.get("email", "")):
        return False, "Invalid email format."
    if not validate_name(data.get("first_name", "")):
        return False, "First name cannot be empty."
    if not validate_name(data.get("last_name", "")):
        return False, "Last name cannot be empty."
    return True, ""


def is_valid_uuid(val):
    try:
        UUID(str(val))
        return True
    except ValueError:
        return False


@api_user.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    valid, message = validate_user_data(data)

    if not valid:
        return jsonify({"error": message}), 400

    if any(
        user["email"] == data["email"]
        for user in data_manager.storage.get("User", {}).values()
    ):
        return jsonify({"error": "Email already exists"}), 409

    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        password=data.get("password", ""),
    )
    data_manager.save(user)
    return jsonify(user.to_dict()), 201


@api_user.route("/users", methods=["GET"])
def get_users():
    users = list(data_manager.storage.get("User", {}).values())
    return jsonify(users), 200


@api_user.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    if not is_valid_uuid(user_id):
        return jsonify({"error": "Invalid user ID"}), 400
    user = data_manager.get(user_id, "User")
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200


@api_user.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()

    if not is_valid_uuid(user_id):
        return jsonify({"error": "Invalid user ID"}), 400

    user = data_manager.get(user_id, "User")

    if user is None:
        return jsonify({"error": "User not found"}), 404

    valid, message = validate_user_data(data)

    if not valid:
        return jsonify({"error": message}), 400

    if any(
        user["email"] == data["email"] and user["id"] != user_id
        for user in data_manager.storage.get("User", {}).values()
    ):

        return jsonify({"error": "Email already exists"}), 409

    updated_user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        password=data.get("password", user["password"]),
    )
    updated_user.id = user_id
    data_manager.update(updated_user)
    return jsonify(updated_user.to_dict()), 200


@api_user.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    if not is_valid_uuid(user_id):
        return jsonify({"error": "Invalid user ID"}), 400

    user = data_manager.get(user_id, "User")
    if user is None:
        return jsonify({"error": "User not found"}), 404

    data_manager.delete(user_id, "User")
    return jsonify({}), 204