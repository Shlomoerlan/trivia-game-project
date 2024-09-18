import pytest
from services.exercise_service import (
    find_user_with_highest_score,
    find_fastest_correct_question,
    find_second_place_user,
    calculate_avg_time_per_question,
    calculate_success_rate,
    find_users_answered_all_questions,
    calculate_median_time_for_answers,
    generate_user_report
)


@pytest.fixture(scope="module")
def setup_database():
    pass


def test_find_user_with_highest_score(setup_database):
    highest_score_user = find_user_with_highest_score()
    assert highest_score_user is not None, "No user found with highest score"


def test_find_fastest_correct_question(setup_database):
    fastest_question = find_fastest_correct_question()
    assert fastest_question is not None, "No question found with fastest correct answer"


def test_find_second_place_user(setup_database):
    second_place_user = find_second_place_user()
    assert second_place_user is not None, "No second-place user found"


def test_calculate_avg_time_per_question(setup_database):
    avg_time = calculate_avg_time_per_question()
    assert avg_time is not None, "Could not calculate average time per question"


def test_calculate_success_rate(setup_database):
    success_rates = calculate_success_rate()
    assert success_rates is not None, "Could not calculate success rate"


def test_find_users_answered_all_questions(setup_database):
    users = find_users_answered_all_questions()
    assert users is not None, "Could not find users who answered all questions"


def test_calculate_median_time_for_answers(setup_database):
    median_times = calculate_median_time_for_answers()
    assert median_times is not None, "Could not calculate median time for answers"


def test_generate_user_report(setup_database):
    user_reports = generate_user_report()
    assert user_reports is not None, "Could not generate user report"
