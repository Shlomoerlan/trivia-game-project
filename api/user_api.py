import requests
from typing import List
from models.UserModel import User



def fetch_users() -> List[User]:
    response = requests.get("https://randomuser.me/api?results=4")

    if response.status_code == 200:
        data = response.json()["results"]
        users = [
            User(first_name=user_data["name"]["first"], last_name=user_data["name"]["last"], email=user_data["email"])
            for idx, user_data in enumerate(data)
        ]
        return users
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return []


