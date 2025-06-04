from typing import List
from app.models.Calendar import Calendar
from app.models.Event import Event

class User:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.calendar = Calendar(user_id)


    def get_user_id(self):
        return self.user_id
    

    def get_calendar(self):
        return self.calendar
    

    def add_event(self, event) -> None:
        self.calendar.add_event(event)

    def update_event(self, event_id, updates) -> Event:
        return self.calendar.update_event(event_id, updates)

    def delete_event(self, event_id) -> bool:
        return self.calendar.delete_event(event_id)

    def list_events(self) ->  List[Event]:
        return self.calendar.list_events()
    
    def clear_calendar(self) -> None:
        return self.calendar.clear_all_events()
    
    def get_event_by_id(self, event_id) -> Event:
        return self.calendar.get_event_by_id(event_id)


    def to_dict(self):
        return {
            "user_id": self.user_id,
            "calendar": self.calendar.to_dict()
        }