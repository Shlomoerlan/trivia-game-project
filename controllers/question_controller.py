from flask import Blueprint, jsonify, request
from repository.question_repository import (
    find_all_questions,
    find_question_by_id,
    create_question,
    update_question,
    delete_question
)
from models.QuestionModel import Question
from dto.ErrorDto import QuestionErrorDto

question_blueprint = Blueprint("question", __name__)


@question_blueprint.route("/", methods=["GET"])
def get_all_questions():
    try:
        questions = find_all_questions()
        return jsonify(questions), 200
    except Exception as e:
        return jsonify(QuestionErrorDto(error=f"An error occurred: {str(e)}")), 500


@question_blueprint.route("/question/<int:question_id>", methods=["GET"])
def get_question_by_id(question_id):
    try:
        question = find_question_by_id(question_id)
        if question:
            return jsonify(question), 200
        else:
            return jsonify(QuestionErrorDto(error="Question not found")), 404
    except Exception as e:
        return jsonify(QuestionErrorDto(error=f"An error occurred: {str(e)}")), 500


@question_blueprint.route("/create", methods=["POST"])
def create_new_question():
    try:
        data = request.get_json()
        if not data or not all(key in data for key in ("question_text", "correct_answer")):
            return jsonify(QuestionErrorDto(error="Missing question data")), 400

        new_question = Question(
            question_text=data["question_text"],
            correct_answer=data["correct_answer"]
        )
        create_question(new_question)
        return jsonify(QuestionErrorDto(message="Question created successfully", body=new_question)), 201
    except Exception as e:
        return jsonify(QuestionErrorDto(error=f"An error occurred: {str(e)}")), 500


@question_blueprint.route("/update/<int:question_id>", methods=["PUT"])
def update_existing_question(question_id):
    try:
        question_data = request.get_json()
        if not question_data or not all(key in question_data for key in ("question_text", "correct_answer")):
            return jsonify(QuestionErrorDto(error="Missing question data")), 400

        existing_question = find_question_by_id(question_id)
        if not existing_question:
            return jsonify(QuestionErrorDto(error="Question not found")), 404

        updated_question = Question(
            question_text=question_data["question_text"],
            correct_answer=question_data["correct_answer"]
        )
        update_question(question_id, updated_question)
        return jsonify(QuestionErrorDto(message="Question updated successfully", body=updated_question)), 200
    except Exception as e:
        return jsonify(QuestionErrorDto(error=f"An error occurred: {str(e)}")), 500


@question_blueprint.route("/delete/<int:question_id>", methods=["DELETE"])
def delete_existing_question(question_id):
    try:
        existing_question = find_question_by_id(question_id)
        if not existing_question:
            return jsonify(QuestionErrorDto(error="Question not found")), 404

        delete_question(question_id)
        return jsonify(QuestionErrorDto(message="Question deleted successfully")), 200
    except Exception as e:
        return jsonify(QuestionErrorDto(error=f"An error occurred: {str(e)}")), 500
