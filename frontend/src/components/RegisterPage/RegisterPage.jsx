import React, { useState } from "react";
import { registerUser } from "../../services/authApi";
import "./RegisterPage.css";


const RegisterPage = ({setAuthMode}) => {
const [name, setName] = useState("");
const [email, setEmail] = useState("");
const [password, setPassword] = useState("");
const [error, setError] = useState("");

async function handleSubmit(e) {
e.preventDefault();

setError("");

if (name.trim().length < 2) {
  setError("Name must be at least 2 characters long");
  return;
}

if (!email.includes("@")) {
  setError("Please enter a valid email");
  return;
}

if (password.length < 6) {
  setError("Password must be at least 6 characters long");
  return;
}


const data = await registerUser(name,email,password);

setAuthMode('login');

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

        <h2>Create Account</h2>

        {error && <p className="auth-error">{error}</p>}

        <form className="auth-form" onSubmit={handleSubmit}>

            <label htmlFor="name">Name</label>

            <input
                type="text"
                id="name"
                placeholder="Enter your name"
                value={name}
                onChange={(e) => setName(e.target.value)}
            />

            <label htmlFor="email">Email</label>

            <input
                type="email"
                id="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />

            <label htmlFor="password">Password</label>

            <input
                type="password"
                id="password"
                placeholder="Create a password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />

            <button type="submit">
                Create Account
            </button>

        </form>

        <div className="auth-footer">

            <span>Already have an account?</span>

            <button
                type="button"
                className="link-button"
                onClick={() => setAuthMode("login")}
            >
                Sign In
            </button>

        </div>

    </div>

</div>
);
};

export default RegisterPage;
