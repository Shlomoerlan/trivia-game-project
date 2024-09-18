import pytest
from repository.user_repository import (
    find_all_users,
    find_user_by_id,
    create_user,
    update_user,
    delete_user
)
from models.UserModel import User


@pytest.fixture(scope="function")
def setup_database():
    yield


def generate_unique_email(base_email: str) -> str:
    import random
    return f"{base_email.split('@')[0]}_{random.randint(1000, 9999)}@{base_email.split('@')[1]}"


def test_create_and_find_all_users(setup_database):
    user1 = User(first_name="John", last_name="Doe", email=generate_unique_email("john.doe@example.com"))
    user2 = User(first_name="Jane", last_name="Doe", email=generate_unique_email("jane.doe@example.com"))
    create_user(user1)
    create_user(user2)

    users = find_all_users()
    assert any(u.email == user1.email for u in users)
    assert any(u.email == user2.email for u in users)


def test_find_user_by_id(setup_database):
    user = User(first_name="Alice", last_name="Wonderland", email=generate_unique_email("alice@example.com"))
    create_user(user)

    inserted_user = find_all_users()[-1]
    fetched_user = find_user_by_id(inserted_user.id)
    assert fetched_user.email == user.email


def test_update_user(setup_database):

    user = User(first_name="Bob", last_name="Builder", email=generate_unique_email("bob.builder@example.com"))
    create_user(user)

    inserted_user = find_all_users()[-1]
    updated_user = User(first_name="Bobby", last_name="Builder", email=generate_unique_email("bobby.builder@example.com"))
    update_user(inserted_user.id, updated_user)

    fetched_user = find_user_by_id(inserted_user.id)
    assert fetched_user.email == updated_user.email


def test_delete_user(setup_database):
    user = User(first_name="Charlie", last_name="Chaplin", email=generate_unique_email("charlie.chaplin@example.com"))
    create_user(user)

    inserted_user = find_all_users()[-1]
    delete_user(inserted_user.id)

    assert find_user_by_id(inserted_user.id) is None
