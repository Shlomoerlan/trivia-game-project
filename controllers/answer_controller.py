from flask import Blueprint, jsonify, request
from repository.answer_repository import (
    find_all_answers,
    find_answer_by_id,
    create_answer,
    update_answer,
    delete_answer
)
from models.AnswerModel import Answer
from dto.ErrorDto import AnswerErrorDto

answer_blueprint = Blueprint("answer", __name__)


@answer_blueprint.route("/", methods=["GET"])
def get_all_answers():
    try:
        answers = find_all_answers()
        return jsonify(answers), 200
    except Exception as e:
        return jsonify(AnswerErrorDto(error=f"An error occurred: {str(e)}")), 500


@answer_blueprint.route("/answer/<int:answer_id>", methods=["GET"])
def get_answer_by_id(answer_id):
    try:
        answer = find_answer_by_id(answer_id)
        if answer:
            return jsonify(answer), 200
        else:
            return jsonify(AnswerErrorDto(error="Answer not found")), 404
    except Exception as e:
        return jsonify(AnswerErrorDto(error=f"An error occurred: {str(e)}")), 500


@answer_blueprint.route("/create", methods=["POST"])
def create_new_answer():
    try:
        data = request.get_json()
        if not data or not all(key in data for key in ("question_id", "incorrect_answer")):
            return jsonify(AnswerErrorDto(error="Missing answer data")), 400

        new_answer = Answer(
            question_id=data["question_id"],
            incorrect_answer=data["incorrect_answer"]
        )
        create_answer(new_answer)
        return jsonify(AnswerErrorDto(message="Answer created successfully", body=new_answer)), 201
    except Exception as e:
        return jsonify(AnswerErrorDto(error=f"An error occurred: {str(e)}")), 500


@answer_blueprint.route("/update/<int:answer_id>", methods=["PUT"])
def update_existing_answer(answer_id):
    try:
        answer_data = request.get_json()
        if not answer_data or not all(key in answer_data for key in ("question_id", "incorrect_answer")):
            return jsonify(AnswerErrorDto(error="Missing answer data")), 400

        existing_answer = find_answer_by_id(answer_id)
        if not existing_answer:
            return jsonify(AnswerErrorDto(error="Answer not found")), 404

        updated_answer = Answer(
            question_id=answer_data["question_id"],
            incorrect_answer=answer_data["incorrect_answer"]
        )
        update_answer(answer_id, updated_answer)
        return jsonify(AnswerErrorDto(message="Answer updated successfully", body=updated_answer)), 200
    except Exception as e:
        return jsonify(AnswerErrorDto(error=f"An error occurred: {str(e)}")), 500


@answer_blueprint.route("/delete/<int:answer_id>", methods=["DELETE"])
def delete_existing_answer(answer_id):
    try:
        existing_answer = find_answer_by_id(answer_id)
        if not existing_answer:
            return jsonify(AnswerErrorDto(error="Answer not found")), 404

        delete_answer(answer_id)
        return jsonify(AnswerErrorDto(message="Answer deleted successfully")), 200
    except Exception as e:
        return jsonify(AnswerErrorDto(error=f"An error occurred: {str(e)}")), 500
