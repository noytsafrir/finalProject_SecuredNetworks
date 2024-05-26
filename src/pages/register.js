import React, { useState } from 'react';
import styles from "@/styles/RequestForm.module.css";

const Register = () => {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [repeatPassword, setRepeatPassword] = useState('');
  const [message, setMessage] = useState('');
  const [messageColor, setMessageColor] = useState('');

  const handleRegister = () => {
    if (!fullName || !email || !password || !repeatPassword) {
      setMessage('All fields are required.');
      setMessageColor('red');
      return;
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.(com|org)$/;
    if (!emailPattern.test(email)) {
      setMessage('Invalid email format. Please use a valid email ending with .com or .org.');
      setMessageColor('red');
      return;
    }

    if (password !== repeatPassword) {
      setMessage('Passwords do not match.');
      setMessageColor('red');
      return;
    }

    setMessage(`Successfully registered with Full Name: ${fullName}, Email: ${email}, Password: ${password}`);
    setMessageColor('green');

    // Clear form fields
    setFullName('');
    setEmail('');
    setPassword('');
    setRepeatPassword('');
  };

  return (
    <div className={styles.footer}>
      <h1>Users Registration</h1>
      <br></br>
      <div>
        <div className={styles.inputContainer}>
          <h3>Full name</h3>
          <input
            type="text"
            id="fullName"
            placeholder="Enter your full name"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            className={styles.input}
          />
        </div>
        <br />
        <div className={styles.inputContainer} style={{ marginLeft: '24px' }}>
          <h3>Email</h3>
          <input
            type="email"
            id="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className={styles.input}
          />
        </div>
        <br />
        <div className={styles.inputContainer}>
          <h3>Password</h3>
          <input
            type="password"
            id="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className={styles.input}
          />
        </div>
        <br />
        <div className={styles.inputContainer}>
          <h3>Re-Password</h3>
          <input
            type="password"
            id="repeat_password"
            placeholder="Repeat your password"
            value={repeatPassword}
            onChange={(e) => setRepeatPassword(e.target.value)}
            className={styles.input}
          />
        </div>

        <div className={`${styles['button-container']}`} style={{ marginLeft: '400px' }}>
          <button
            type="button"
            className={styles.button}
            onClick={handleRegister}
          >
            Register
          </button>
        </div>
        {message && <p style={{ color: messageColor, textAlign: 'center' }}>{message}</p>}
      </div>
    </div>
  );
};

export default Register;
