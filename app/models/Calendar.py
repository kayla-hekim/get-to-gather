from typing import List
from app.models.Event import Event
from datetime import datetime

class Calendar:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.events: List[Event] = []


    def add_event(self, new_event: Event):
        if not isinstance(new_event, Event):
            raise ValueError("Event is not an actual event.")
        if any(event.id == new_event.id for event in self.events):
            raise ValueError("An event with this ID already exists.")
        
        self.events.append(new_event)


    def delete_event(self, event_id:str):
        event = self.get_event_by_id(event_id)
        self.events.remove(event)
        return True
    

    def update_event(self, event_id: str, updates: dict):
        event = self.get_event_by_id(event_id)

        if "summary" in updates:
            event.set_summary(updates["summary"])
        if "start_time" in updates:
            event.set_start_time(updates["start_time"])
        if "end_time" in updates:
            event.set_end_time(updates["end_time"])
        if "notes" in updates:
            event.set_notes(updates["notes"])
        if "location" in updates:
            event.set_location(updates["location"])

        return event
            
    
    def get_event_by_id(self, event_id: str) -> Event:
        for event in self.events:
            if event.id == event_id:
                return event
        raise ValueError("Need Valid ID for event.")
    

    def clear_all_events(self):
        self.events.clear()


    def get_user_id(self):
        return self.user_id
    

    # Same thing tbh (2):
    def list_events(self) -> List[Event]:
        return self.events

    def list_event_dicts(self) -> List[dict]:
        return [event.to_dict() for event in self.events]


    def get_events_in_range(self, start: datetime, end: datetime) -> List[Event]:
        return [
            event for event in self.events 
            if event.start_time >= start and event.end_time <= end
        ]


    def has_conflict(self, new_event: Event) -> bool:
        return any(
            not (new_event.end_time <= event.start_time or new_event.start_time >= event.end_time)
            for event in self.events
        )
    

    def to_serializable_dict(self):
        def serialize_event(event):
            d = event.to_dict()
            d["start"] = d["start"].isoformat()
            d["end"] = d["end"].isoformat()
            return d

        return {
            "user_id": self.user_id,
            "events": [serialize_event(e) for e in self.events]
        }
    

    def to_dict(self):
        return self.to_serializable_dict()


    def sort_events(self):
        self.events.sort(key=lambda e: e.start_time)