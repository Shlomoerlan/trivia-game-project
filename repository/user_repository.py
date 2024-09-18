from typing import List, Optional
from psycopg2.extras import RealDictCursor
import psycopg2
from models.UserModel import User
from config.sql_config import SQL_URL


def get_db_connection():
    return psycopg2.connect(SQL_URL, cursor_factory=RealDictCursor)


def create_users_table():
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            email VARCHAR(100) UNIQUE
        );
        """)
        conn.commit()
    conn.close()


def find_all_users() -> List[User]:
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users;")
        users = cur.fetchall()
    conn.close()
    return [User(**user) for user in users]


def find_user_by_id(user_id: int) -> Optional[User]:
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
        user = cur.fetchone()
    conn.close()
    return User(**user) if user else None


def create_user(user: User) -> int:
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO users (first_name, last_name, email) 
            VALUES (%s, %s, %s) RETURNING id;
        """, (user.first_name, user.last_name, user.email))
        user_id = cur.fetchone()['id']
        conn.commit()
    conn.close()
    return user_id


def update_user(user_id: int, user: User) -> None:
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE users SET first_name = %s, last_name = %s, email = %s
            WHERE id = %s;
        """, (user.first_name, user.last_name, user.email, user_id))
        conn.commit()
    conn.close()


def delete_user(user_id: int) -> None:
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
        conn.commit()
    conn.close()
