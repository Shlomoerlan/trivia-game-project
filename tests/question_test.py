import pytest
from repository.question_repository import (
    create_questions_table,
    insert_questions,
    find_all_questions,
    find_question_by_id,
    create_question,
    update_question,
    delete_question
)
from models.QuestionModel import Question


@pytest.fixture(scope="module")
def setup_database():
    create_questions_table()
    yield


def test_insert_and_find_all_questions(setup_database):
    question1 = Question(question_text="Question 1", correct_answer="Answer 1")
    question2 = Question(question_text="Question 2", correct_answer="Answer 2")
    insert_questions([question1, question2])

    questions = find_all_questions()
    assert len(questions) > 1


def test_find_question_by_id(setup_database):
    question = Question(question_text="Find Me", correct_answer="Correct Answer")
    create_question(question)

    inserted_question = find_all_questions()[0]
    fetched_question = find_question_by_id(inserted_question['id'])
    assert fetched_question['correct_answer']


def test_update_question(setup_database):
    question = Question(question_text="Original Question", correct_answer="Original Answer")
    create_question(question)

    inserted_question = find_all_questions()[0]
    updated_question = Question(question_text="Updated Question", correct_answer="Updated Answer")
    update_question(inserted_question['id'], updated_question)

    fetched_question = find_question_by_id(inserted_question['id'])
    assert fetched_question['correct_answer'] == "Updated Answer"


def test_delete_question(setup_database):
    question = Question(question_text="Delete Me", correct_answer="Correct Answer")
    create_question(question)

    inserted_question = find_all_questions()[0]
    delete_question(inserted_question['id'])

    assert find_question_by_id(inserted_question['id']) is None
