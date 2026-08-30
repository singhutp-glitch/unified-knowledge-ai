import React, { useState } from 'react'
import './LoginPage.css'
import { loginUser } from '../../services/authApi';

const LoginPage = ({setUser,setAuthMode}) => {

const [email, setEmail] = useState("");
const [password, setPassword] = useState("");
const [error, setError] = useState("");

async function handleSubmit(e) {
  try{

    e.preventDefault();
    
    setError("");
    
    if (!email.includes("@")) {
      setError("Please enter a valid email");
    return;
    }

    if (password.length < 6) {
    setError("Password must be at least 6 characters long");
    return;
    }


  const result = await loginUser(email,password);
  
  localStorage.setItem('token',result.token);
  setUser(result.user);
  
}catch(error){
  console.error(error);
}
}

return ( <div className="auth-page">

    <div className="auth-card">

        <div className="auth-header">

            <h1>Knowledge Workspace</h1>

            <p>
                Enterprise document intelligence with grounded answers and
                verifiable citations.
            </p>

        </div>

        <h2>Sign in</h2>

        {error && <p className="auth-error">{error}</p>}

        <form className="auth-form" onSubmit={handleSubmit}>

            <label htmlFor="email">Email</label>

            <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
            />

            <label htmlFor="password">Password</label>

            <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
            />

            <button type="submit">
                Sign In
            </button>

        </form>

        <div className="auth-footer">

            <span>Don't have an account?</span>

            <button
                type="button"
                className="link-button"
                onClick={() => setAuthMode("register")}
            >
                Register
            </button>

        </div>

    </div>

</div>

);}

export default LoginPage