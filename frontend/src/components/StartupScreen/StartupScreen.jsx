import React, { useEffect, useState } from 'react'
import './StartupScreen.css'

const StartupScreen = () => {
  const [secondsLeft, setSecondsLeft] = useState(60);

    useEffect(() => {
        const interval = setInterval(() => {
            setSecondsLeft((prev) => {
                if (prev <= 0) {
                    clearInterval(interval);
                    return 0;
                }

                return prev - 1;
            });
        }, 1000);

        return () => clearInterval(interval);
    }, []);

    return (
      <div className="startup-screen">
    <div className="startup-card">

        <div className="startup-logo">
            AI
        </div>

        <h1>AI Knowledge Base</h1>

        <p className="startup-subtitle">
            Business Document Intelligence
        </p>

        <div className="startup-spinner"></div>

        <h2>Starting the AI service...</h2>

        <p className="startup-description">
            The application is hosted on the free tier of Render.
            The backend automatically goes to sleep after inactivity and
            usually wakes within one minute.
        </p>

        <div className="startup-timer">
            {secondsLeft}s
        </div>

    </div>
</div>
    );
}

export default StartupScreen