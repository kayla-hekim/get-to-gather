import uuid
from datetime import datetime

class Event:
    def __init__(self, summary: str, start_time: datetime, end_time: datetime, notes: str, location: str = "", calendar_id: str = None, event_id: str = None):
        self.id = event_id or str(uuid.uuid4())
        self.summary = summary
        self.start_time = start_time
        self.end_time = end_time
        self.notes = notes
        self.location = location
        self.calendar_id = calendar_id

    
    def get_event_id(self):
        return self.id

    
    def set_summary(self, new_summary:str):
        if not isinstance(new_summary, str) or not new_summary.strip():
            raise ValueError("Event Summary must be included.")
        if len(new_summary) > 100:
            raise ValueError("Event Summary is too long.")
        self.summary = new_summary.strip()

    def get_summary(self):
        return self.summary
    
    def get_duration(self):
        return self.end_time - self.start_time
        

    def set_start_time(self, new_time:datetime):
        if new_time >= self.end_time:
            raise ValueError("Start time must be before end time.")
        self.start_time = new_time
    
    def get_start_time(self):
        return self.start_time
    

    def set_end_time(self, new_time:datetime):
        if new_time <= self.start_time:
            raise ValueError("End time must be after start time.")
        self.end_time = new_time
    
    def get_end_time(self):
        return self.end_time
    

    def set_notes(self, new_notes: str):
        if not isinstance(new_notes, str):
            raise TypeError("Notes must be a string.")
        if len(new_notes) > 200:
            raise ValueError("Notes are too long.")
        self.notes = new_notes.strip()

    def get_notes(self):
        return self.notes
    

    def set_location(self, new_loc:str):
        if not isinstance(new_loc, str):
            raise TypeError("Location must be a string.")
        if len(new_loc) > 200:
            raise ValueError("Location is too long.")
        self.location = new_loc.strip()

    def get_location(self):
        return self.location
    

    def get_calendar_id(self):
        return self.calendar_id


    def to_dict(self):
        return {
            "id": self.id,
            "summary": self.summary,
            "start": self.start_time,
            "end": self.end_time,
            "notes": self.notes,
            "location": self.location,
            "calendar_id": self.calendar_id
        }
    

    def __repr__(self):
        return f"Event({self.summary}, {self.start_time}–{self.end_time})"