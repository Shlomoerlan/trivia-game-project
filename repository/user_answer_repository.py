import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List
from datetime import timedelta
from config.sql_config import SQL_URL
from models.UserAnswerModel import UserAnswer


def get_db_connection():
    return psycopg2.connect(SQL_URL, cursor_factory=RealDictCursor)


def create_user_answers_table():
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS user_answers (
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL,
            question_id INT NOT NULL,
            answer_text TEXT NOT NULL,
            is_correct BOOLEAN NOT NULL,
            time_taken INTERVAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
        );
        """)
        conn.commit()
    conn.close()


def find_all_user_answers() -> List[UserAnswer]:
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM user_answers;")
        user_answers = cur.fetchall()

    user_answers_objects = [
        UserAnswer(
            id=ua['id'],
            user_id=ua['user_id'],
            question_id=ua['question_id'],
            answer_text=ua['answer_text'],
            is_correct=ua['is_correct'],
            time_taken=timedelta(seconds=ua['time_taken'].total_seconds())
        )
        for ua in user_answers
    ]

    conn.close()
    return user_answers_objects


def create_user_answer_by_params(user_id: int, question_id: int, answer_text: str, is_correct: bool,
                                 time_taken: timedelta) -> None:
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO user_answers (user_id, question_id, answer_text, is_correct, time_taken) 
            VALUES (%s, %s, %s, %s, %s);
        """, (user_id, question_id, answer_text, is_correct, time_taken))
        conn.commit()
    conn.close()


