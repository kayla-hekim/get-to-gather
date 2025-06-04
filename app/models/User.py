from app.models.Calendar import Calendar

class User:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.calendar_id = Calendar(user_id)

    