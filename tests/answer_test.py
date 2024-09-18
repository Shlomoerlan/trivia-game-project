import pytest
from repository.answer_repository import (
    create_answers_table,
    insert_answers,
    find_all_answers,
    find_answer_by_id,
    create_answer,
    update_answer,
    delete_answer
)
from repository.question_repository import create_question
from models.AnswerModel import Answer
from models.QuestionModel import Question


@pytest.fixture(scope="module")
def setup_database():
    create_answers_table()
    yield


def insert_dummy_question():
    question = Question(question_text="Dummy Question", correct_answer="Dummy Answer")
    create_question(question)
    return question


def test_insert_and_find_all_answers(setup_database):
    dummy_question = insert_dummy_question()
    answer1 = Answer(question_id=dummy_question.id, incorrect_answer="Incorrect Answer 1")
    answer2 = Answer(question_id=dummy_question.id, incorrect_answer="Incorrect Answer 2")
    insert_answers([answer1, answer2])

    answers = find_all_answers()
    assert len(answers) > 1


def test_find_answer_by_id(setup_database):
    dummy_question = insert_dummy_question()
    answer = Answer(question_id=dummy_question.id, incorrect_answer="New Incorrect Answer")
    create_answer(answer)

    inserted_answer = find_all_answers()[0]
    fetched_answer = find_answer_by_id(inserted_answer['id'])
    assert fetched_answer['incorrect_answer']


def test_update_answer(setup_database):
    dummy_question = insert_dummy_question()
    answer = Answer(question_id=dummy_question.id, incorrect_answer="Original Answer")
    create_answer(answer)

    inserted_answer = find_all_answers()[0]
    updated_answer = Answer(question_id=dummy_question.id, incorrect_answer="Updated Answer")
    update_answer(inserted_answer['id'], updated_answer)

    fetched_answer = find_answer_by_id(inserted_answer['id'])
    assert fetched_answer['incorrect_answer'] == "Updated Answer"


def test_delete_answer(setup_database):
    dummy_question = insert_dummy_question()
    answer = Answer(question_id=dummy_question.id, incorrect_answer="Answer to be deleted")
    create_answer(answer)

    inserted_answer = find_all_answers()[0]
    delete_answer(inserted_answer['id'])

    assert find_answer_by_id(inserted_answer['id']) is None
