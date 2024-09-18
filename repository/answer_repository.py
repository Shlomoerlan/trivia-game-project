import psycopg2
from psycopg2.extras import RealDictCursor
from config.sql_config import SQL_URL
from typing import List, Optional
from models.AnswerModel import Answer


def get_db_connection():
    return psycopg2.connect(SQL_URL, cursor_factory=RealDictCursor)


def create_answers_table():
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


def insert_answers(answers: List[Answer]):
    conn = get_db_connection()
    with conn.cursor() as cur:
        for answer in answers:
            cur.execute("""
            INSERT INTO answers (question_id, incorrect_answer) 
            VALUES (%s, %s);
            """, (answer.question_id, answer.incorrect_answer))
        conn.commit()
    conn.close()


def find_all_answers() -> List[dict]:
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM answers;")
        answers = cur.fetchall()
    conn.close()
    return answers



def find_answers_by_question_id(question_id: int) -> List[Answer]:
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM answers WHERE question_id = %s;", (question_id,))
        answers = cur.fetchall()
    conn.close()
    return [Answer(**answer) for answer in answers]


def create_answer(answer: Answer) -> None:
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO answers (question_id, incorrect_answer) 
            VALUES (%s, %s);
        """, (answer.question_id, answer.incorrect_answer))
        conn.commit()
    conn.close()


def update_answer(answer_id: int, answer: Answer) -> None:
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE answers SET question_id = %s, incorrect_answer = %s
            WHERE id = %s;
        """, (answer.question_id, answer.incorrect_answer, answer_id))
        conn.commit()
    conn.close()


def delete_answer(answer_id: int) -> None:
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM answers WHERE id = %s;", (answer_id,))
        conn.commit()
    conn.close()
