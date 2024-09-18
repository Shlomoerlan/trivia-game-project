from psycopg2.extras import RealDictCursor
from config.sql_config import SQL_URL
import psycopg2
from typing import List, Optional
from models.QuestionModel import Question


def get_db_connection():
    return psycopg2.connect(SQL_URL, cursor_factory=RealDictCursor)


def create_questions_table():
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id SERIAL PRIMARY KEY,
            question_text TEXT,
            correct_answer VARCHAR(100)
        );
        """)
        conn.commit()
    conn.close()


def insert_questions(questions: List[Question]):
    conn = get_db_connection()
    with conn.cursor() as cur:
        for question in questions:
            cur.execute("""
            INSERT INTO questions (question_text, correct_answer) 
            VALUES (%s, %s);
            """, (question.question_text, question.correct_answer))
        conn.commit()
    conn.close()


def find_all_questions() -> List[dict]:
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM questions;")
        questions = cur.fetchall()
    conn.close()
    return questions


def find_question_by_id(question_id: int) -> Optional[dict]:
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM questions WHERE id = %s;", (question_id,))
        question = cur.fetchone()
    conn.close()
    return question


def create_question(question: Question) -> None:
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO questions (question_text, correct_answer) 
            VALUES (%s, %s);
        """, (question.question_text, question.correct_answer))
        conn.commit()
    conn.close()


def update_question(question_id: int, question: Question) -> None:
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE questions SET question_text = %s, correct_answer = %s
            WHERE id = %s;
        """, (question.question_text, question.correct_answer, question_id))
        conn.commit()
    conn.close()


def delete_question(question_id: int) -> None:
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM questions WHERE id = %s;", (question_id,))
        conn.commit()
    conn.close()
