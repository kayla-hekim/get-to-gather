import React from 'react';

function Login() {
  const handleLogin = () => {
    window.location.href = 'http://localhost:8000/auth/login';
  };

  return (
    <div className="login-page">
      <h2>Welcome to Get-To-Gather</h2>
      <button onClick={handleLogin}>Login with Google</button>
    </div>
  );
}

export default Login;