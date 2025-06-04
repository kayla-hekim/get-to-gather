import React, { useEffect, useState } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';

function CalendarView({ userId }) {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    fetch(`http://localhost:8000/calendar/${userId}`)
      .then(res => res.json())
      .then(data => {
        const formatted = data.events.map(e => ({
          title: e.summary,
          start: e.start,
          end: e.end,
        }));
        setEvents(formatted);
      });
  }, [userId]);

  return (
    <div className="calendar-container">
      <FullCalendar
        plugins={[dayGridPlugin]}
        initialView="dayGridMonth"
        events={events}
      />
    </div>
  );
}

export default CalendarView;