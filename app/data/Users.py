from app.models.User import User
from typing import Dict

user_store: Dict[str, User] = {}

def get_or_create_user(user_id: str) -> User:
    if user_id not in user_store:
        print(f"[INFO] Creating new user: {user_id}")
        user_store[user_id] = User(user_id)
    return user_store[user_id]