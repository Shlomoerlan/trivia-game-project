import psycopg2
from repository.question_repository import create_questions_table, create_question
from repository.answer_repository import create_answers_table, create_answer
from repository.user_repository import create_users_table, create_user
from repository.user_answer_repository import create_user_answers_table
from models.QuestionModel import Question
from models.AnswerModel import Answer
from models.UserModel import User
from api.question_answer_api import fetch_question_answers_from_api
from config.sql_config import SQL_URL


def table_exists(table_name: str) -> bool:
    conn = psycopg2.connect(SQL_URL)
    with conn.cursor() as cur:
        cur.execute(f"""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = '{table_name}'
            );
        """)
        result = cur.fetchone()[0]
    conn.close()
    return result


def seed():
    if not table_exists('users'):
        print("Creating 'users' table...")
        create_users_table()
        users = [
            User(first_name="John", last_name="Doe", email="john.doe@example.com"),
            User(first_name="Jane", last_name="Doe", email="jane.doe@example.com")
        ]
        map(lambda u: create_user(u), users)
        print("Inserted sample users.")

    if not table_exists('questions'):
        print("Creating 'questions' table...")
        create_questions_table()
        question_answer_pairs = fetch_question_answers_from_api("https://opentdb.com/api.php?amount=20")
        for qa in question_answer_pairs:
            question = Question(question_text=qa.question_text, correct_answer=qa.correct_answer)
            question_id = create_question(question)

            for incorrect in qa.incorrect_answers:
                answer = Answer(question_id=question_id, incorrect_answer=incorrect)
                create_answer(answer)
        print("Inserted questions and answers.")

    if not table_exists('answers'):
        print("Creating 'answers' table...")
        create_answers_table()
        print("'answers' table created successfully.")

    if not table_exists('user_answers'):
        print("Creating 'user_answers' table...")
        create_user_answers_table()
        print("'user_answers' table created successfully.")

    print("Database seeding completed.")


