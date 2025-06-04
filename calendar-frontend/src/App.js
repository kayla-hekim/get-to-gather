import React, { useState } from 'react';
import Login from './Login';  // ./login for macs && ./Login for other OS
import CalendarView from './CalendarView';

function App() {
  const [userId, setUserId] = useState(localStorage.getItem('userId'));

  if (!userId) {
    return <Login />;
  }

  return (
    <div className="App">
      <h1>Welcome back!</h1>
      <CalendarView userId={userId} />
    </div>
  );
}

export default App;