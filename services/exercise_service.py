from functools import partial
from statistics import mean, median
from toolz import pipe, groupby, concat
import csv
from repository.user_answer_repository import find_all_user_answers
from repository.question_repository import find_all_questions

# Exercise 1
# Description: Find the user with the highest score (most correctly answered questions)


def find_user_with_highest_score():
    user_answers = find_all_user_answers()
    grouped_by_user = groupby(lambda ua: ua.user_id, user_answers)
    user_scores = [(user_id, len(list(filter(lambda x: x.is_correct, answers))))
                   for user_id, answers in grouped_by_user.items()]
    return max(user_scores, key=lambda x: x[1], default=None)


# Exercise 2
# Description: Find the question that was answered correctly the fastest

def find_fastest_correct_question():
    user_answers = find_all_user_answers()
    correct_answers = filter(lambda ua: ua.is_correct, user_answers)
    return min(correct_answers, key=lambda x: x.time_taken, default=None)


# Exercise 3
# Description: Find the second-place user and their fastest answer time


def find_second_place_user():
    user_answers = find_all_user_answers()
    grouped_by_user = groupby(lambda ua: ua.user_id, user_answers)
    sorted_users = sorted([(user_id, len(list(filter(lambda x: x.is_correct, answers))),
                            min(answers, key=lambda x: x.time_taken).time_taken)
                           for user_id, answers in grouped_by_user.items()],
                          key=lambda x: (-x[1], x[2]))
    return sorted_users[1] if len(sorted_users) > 1 else None


# Exercise 4
# Description: Calculate the average time taken to answer each question

def calculate_avg_time_per_question():
    user_answers = find_all_user_answers()
    grouped_by_question = groupby(lambda ua: ua.question_id, user_answers)
    avg_times = [(question_id, mean([ua.time_taken.total_seconds() for ua in answers]))
                 for question_id, answers in grouped_by_question.items()]
    return avg_times


# Exercise 5
# Description: Calculate the success rate for each question

def calculate_success_rate():
    user_answers = find_all_user_answers()
    grouped_by_question = groupby(lambda ua: ua.question_id, user_answers)
    success_rates = [(question_id,
                      len(list(filter(lambda x: x.is_correct, answers))) / len(answers) * 100)
                     for question_id, answers in grouped_by_question.items()]
    return success_rates


# Exercise 6
# Description: Find users who have answered all questions

def find_users_answered_all_questions():
    all_questions = set(map(lambda q: q['id'], find_all_questions()))
    user_answers = find_all_user_answers()

    user_answers_grouped = pipe(
        user_answers,
        partial(groupby, lambda ua: ua.user_id)  # Using attribute access for UserAnswer objects
    )

    users_answered_all = filter(
        lambda user_data: all_questions.issubset(set(map(lambda ans: ans.question_id, user_data[1]))),
        user_answers_grouped.items()
    )

    return list(users_answered_all)


# Exercise 7
# Description: Calculate the median time taken for correct answers vs incorrect answers

def calculate_median_time_for_answers():
    user_answers = find_all_user_answers()
    correct_times = list(map(lambda x: x.time_taken.total_seconds(),
                             filter(lambda ua: ua.is_correct, user_answers)))
    incorrect_times = list(map(lambda x: x.time_taken.total_seconds(),
                               filter(lambda ua: not ua.is_correct, user_answers)))
    return {
        "median_correct": median(correct_times) if correct_times else None,
        "median_incorrect": median(incorrect_times) if incorrect_times else None
    }


# Exercise 8
# Description: Generate a comprehensive report for each user
# containing total_questions, answered_questions
# , correct_answers, avg_time, fastest_answer, slowest_answer
# , unanswered_questions. Export result to csv.
def generate_user_report():
    user_answers = find_all_user_answers()
    grouped_by_user = groupby(lambda ua: ua.user_id, user_answers)
    total_questions = len(find_all_questions())

    user_report = [(user_id,
                    len(answers),
                    len(list(filter(lambda x: x.is_correct, answers))),
                    mean([ua.time_taken.total_seconds() for ua in answers]),
                    min(answers, key=lambda x: x.time_taken).time_taken.total_seconds(),
                    max(answers, key=lambda x: x.time_taken).time_taken.total_seconds(),
                    total_questions - len(answers))
                   for user_id, answers in grouped_by_user.items()]

    with open("user_report.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["User ID", "Answered Questions", "Correct Answers", "Avg Time",
                         "Fastest Answer", "Slowest Answer", "Unanswered Questions"])
        for row in user_report:
            writer.writerow(row)
    return "user_report.csv"
