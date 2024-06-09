import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import styles from "@/styles/RequestForm.module.css";
import axios from 'axios';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [messageColor, setMessageColor] = useState('');
  const [showCodeInput, setShowCodeInput] = useState(false);
  const [code, setCode] = useState('');
  const [timeRemaining, setTimeRemaining] = useState(180); // 3 minutes in seconds

  const router = useRouter();

  useEffect(() => {
    let intervalId;
    if (showCodeInput && timeRemaining > 0) {
      intervalId = setInterval(() => {
        setTimeRemaining(prevTime => prevTime - 1);
      }, 1000);
    }

    return () => clearInterval(intervalId);
  }, [showCodeInput, timeRemaining]);

  const handleLogin = () => {
    if (!email || !password) {
      setMessage('Both email and password are required.');
      setMessageColor('red');
      return;
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.(com|org)$/;
    if (!emailPattern.test(email)) {
      setMessage('Invalid email format. Please use a valid email ending with .com or .org.');
      setMessageColor('red');
      return;
    }

    axios.post('http://localhost:5000/login', { email, password })
      .then(response => {
        const { message, status } = response.data;
        setMessage(message);
        setMessageColor(status === 'success' ? 'green' : 'red');
        if (status === 'success') {
          setShowCodeInput(true);  // Show code input if login is successful
        }
      })
      .catch(error => {
        setMessage('Login failed. Please try again.');
        setMessageColor('red');
      });
  };

  const handleCodeSubmit = () => {
    // Validate code here, for simplicity, we'll assume it's correct
    setMessage('Code submitted successfully.');
    setMessageColor('green');
    setShowCodeInput(false); // Hide the input fields after code submission
    setTimeRemaining(0); // Reset timer
  };

  const formatTime = (time) => {
    const minutes = Math.floor(time / 60);
    const seconds = time % 60;
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  };

  return (
    <div className={styles.footer}>
      <div className={styles.loginContainer}>
        <h2 className={styles.center}>Please login:</h2>
        <br />
        <br />
        <div>
          <h3>Email</h3>
          <h3>Password</h3>
        </div>
        <br />
        <input
          type="email"
          placeholder="Enter your email..."
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className={styles.input}
        />
        <input
          type="password"
          placeholder="Enter your password..."
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className={styles.input}
        />
        <br />
        <br />
        <div className={`${styles['button-container']}`} style={{ marginLeft: '550px' }}>
          <button
            type="button"
            className={styles.button}
            onClick={handleLogin}
          >
            Login
          </button>
        </div>
        <br />
        <div className={`${styles['button-container']}`} style={{ marginLeft: '550px' }}>
          <button
            type="button"
            className={styles.button}
            onClick={() => router.push('/ForgotPassword')}
          >
            Forgot your password?
          </button>
        </div>
        <br />
        {message && <p style={{ color: messageColor }}>{message}</p>}
      </div>
    </div>
  );
};

export default Login;