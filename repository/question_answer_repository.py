from typing import List
from api.question_answer_api import fetch_question_answers_from_api
from config.sql_config import SQL_URL
import psycopg2
from psycopg2.extras import RealDictCursor
from models.QuestionModel import Question

def get_db_connection():
    return psycopg2.connect(SQL_URL, cursor_factory=RealDictCursor)

def create_answers_table():
    print("Creating answers table if not exists...")
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS answers (
                id SERIAL PRIMARY KEY,
                question_id INT REFERENCES questions(id) ON DELETE CASCADE,
                incorrect_answer VARCHAR(255) NOT NULL
            );
        """)
        conn.commit()
    conn.close()

def insert_question(conn, question: Question) -> int:
    try:
        print(f"Inserting question: {question.question_text}")
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO questions (question_text, correct_answer)
                VALUES (%s, %s) RETURNING id;
            """, (question.question_text, question.correct_answer))
            question_id = cur.fetchone()['id']
            print(f"Inserted question with ID: {question_id}")
            conn.commit()
        return question_id
    except Exception as e:
        print(f"Error inserting question: {e}")
        conn.rollback()

def insert_answers(conn, question_id: int, incorrect_answers: List[str]):
    try:
        print(f"Inserting answers for question ID {question_id}: {incorrect_answers}")
        with conn.cursor() as cur:
            for incorrect_answer in incorrect_answers:
                cur.execute("""
                    INSERT INTO answers (question_id, incorrect_answer)
                    VALUES (%s, %s);
                """, (question_id, incorrect_answer))
            conn.commit()
    except Exception as e:
        print(f"Error inserting answers: {e}")
        conn.rollback()

def process_questions_and_answers():
    questions_data = fetch_question_answers_from_api("https://opentdb.com/api.php?amount=20")
    conn = get_db_connection()
    for qa in questions_data:
        question = Question(
            question_text=qa.question_text,
            correct_answer=qa.correct_answer
        )

        question_id = insert_question(conn, question)

        if question_id:
            insert_answers(conn, question_id, qa.incorrect_answers)

    conn.close()


