import time
import random
from datetime import timedelta
from toolz import pipe
from toolz.curried import partial
from models.UserModel import User
from models.UserAnswerModel import UserAnswer
from repository.user_repository import create_user, find_user_by_id
from repository.question_repository import find_all_questions
from repository.answer_repository import find_answers_by_question_id
from repository.user_answer_repository import create_user_answer_by_params
import psycopg2
from config.sql_config import SQL_URL


def drop_all_tables():
    conn = psycopg2.connect(SQL_URL)
    with conn.cursor() as cur:
        cur.execute("""
            DROP TABLE IF EXISTS user_answers CASCADE;
            DROP TABLE IF EXISTS answers CASCADE;
            DROP TABLE IF EXISTS questions CASCADE;
            DROP TABLE IF EXISTS users CASCADE;
        """)
        conn.commit()
    conn.close()
    print("All tables dropped successfully.")


menu_options = {
    '1': ('Create new user', 'create_new_user'),
    '2': ('Start the game', 'start_game'),
    '3': ('Exit', 'exit')
}


def create_new_user():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    email = input("Enter email: ")
    user = User(first_name=first_name, last_name=last_name, email=email)
    user_id = create_user(user)
    print(f"User created with ID: {user_id}")
    return user_id


def ask_question(user_id: int, question):
    print(f"\nQuestion: {question['question_text']}")
    correct_answer = question['correct_answer']
    incorrect_answers = find_answers_by_question_id(question['id'])
    all_answers = [correct_answer] + [answer.incorrect_answer for answer in incorrect_answers]
    random.shuffle(all_answers)

    for idx, answer in enumerate(all_answers, start=1):
        print(f"{idx}. {answer}")

    start_time = time.time()
    user_answer_index = int(input("\nYour answer (enter the number): ")) - 1
    end_time = time.time()

    time_taken = end_time - start_time
    user_answer_text = all_answers[user_answer_index]
    is_correct = user_answer_text == correct_answer

    user_answer = UserAnswer(
        user_id=user_id,
        question_id=question['id'],
        answer_text=user_answer_text,
        is_correct=is_correct,
        time_taken=timedelta(seconds=time_taken)
    )

    create_user_answer_by_params(
        user_answer.user_id, user_answer.question_id, user_answer.answer_text,
        user_answer.is_correct, user_answer.time_taken
    )

    if is_correct:
        print("Correct!")
    else:
        print(f"Wrong! The correct answer was: {correct_answer}")

    return is_correct


def start_game():
    user_id = int(input("Enter your user ID: "))
    user = find_user_by_id(user_id)
    if user is None:
        print("User not found. Please create a new user first.")
        return

    questions = find_all_questions()
    if not questions:
        print("No questions found. Exiting the game.")
        return

    print(f"\nWelcome, {user.first_name} {user.last_name}!")
    print("Let's start the game. You'll answer all questions in order.")

    correct_answers = 0
    total_questions = len(questions)

    for question in questions:
        if ask_question(user_id, question):
            correct_answers += 1

    print(f"\nGame Over! You got {correct_answers} out of {total_questions} questions correct.")


def display_menu():
    print("\n--- Welcome to the best trivia game ever ---")
    pipe(
        menu_options.items(),
        partial(map, lambda item: f"{item[0]}. {item[1][0]}"),
        lambda lines: '\n'.join(lines),
        print
    )


def handle_menu_choice(choice):
    if choice == '1':
        create_new_user()
    elif choice == '2':
        start_game()
    elif choice == '3':
        print("Exiting the game.")
        drop_all_tables()
        exit()
    else:
        print("Invalid option. Please try again.")


if __name__ == '__main__':
    while True:
        display_menu()
        user_choice = input("Choose an option: ")
        handle_menu_choice(user_choice)
