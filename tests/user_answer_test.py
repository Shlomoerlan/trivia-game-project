import pytest
from repository.user_answer_repository import (
    create_user_answers_table,
    find_all_user_answers,
)


@pytest.fixture(scope="module")
def setup_database():
    create_user_answers_table()
    yield


def test_create_and_find_all_user_answers(setup_database):
    user_answers = find_all_user_answers()
    assert len(user_answers) > 0
