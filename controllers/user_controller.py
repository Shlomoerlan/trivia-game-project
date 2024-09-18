from flask import Blueprint, jsonify, request
from dto.ErrorDto import UserErrorDto
from repository.user_repository import (
    find_all_users,
    find_user_by_id,
    create_user,
    update_user,
    delete_user
)
from models.UserModel import User
from dataclasses import asdict


user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/users", methods=["GET"])
def get_all_users():
    users = find_all_users()
    users_list = list(map(asdict, users))
    return jsonify(users_list), 200


@user_blueprint.route("/user/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    user = find_user_by_id(user_id)
    if user:
        return jsonify(asdict(user)), 200
    else:
        return jsonify(UserErrorDto(error= "User not found")), 404


@user_blueprint.route("/create", methods=["POST"])
def create_new_user():
    data = request.get_json()
    if not data or not all(key in data for key in ("first_name", "last_name", "email")):
        return jsonify(UserErrorDto(error="Missing user data")), 400

    new_user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"]
    )
    create_user(new_user)
    return jsonify(UserErrorDto(message="User created successfully", body=new_user)), 201


@user_blueprint.route("/update/<int:user_id>", methods=["PUT"])
def update_existing_user(user_id):
    user_data = request.get_json()
    if not user_data or not all(key in user_data for key in ("first_name", "last_name", "email")):
        return jsonify(UserErrorDto(error="Missing user data")), 400

    existing_user = find_user_by_id(user_id)
    if not existing_user:
        return jsonify(UserErrorDto(error="User not found")), 404

    updated_user = User(
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
        email=user_data["email"]
    )
    update_user(user_id, updated_user)
    return jsonify(UserErrorDto(message="User updated successfully", body=updated_user)), 200


@user_blueprint.route("/delete/<int:user_id>", methods=["DELETE"])
def delete_existing_user(user_id):
    existing_user = find_user_by_id(user_id)
    if not existing_user:
        return jsonify(UserErrorDto(error="User not found")), 404

    delete_user(user_id)
    return jsonify(UserErrorDto(message="User deleted successfully")), 200
