import React, { useState } from 'react';
import styles from "@/styles/RequestForm.module.css";

const AddCustomerForm = () => {
  const [email, setEmail] = useState('');
  const [customerName, setCustomerName] = useState('');
  const [password, setPassword] = useState('');
  const [repeatPassword, setRepeatPassword] = useState('');
  const [message, setMessage] = useState('');
  const [messageColor, setMessageColor] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    // Validate email
    if (!email || !/^\S+@\S+\.(com|org)$/.test(email)) {
      setMessage('Email is required and must be in a valid format (ending with .com or .org).');
      setMessageColor('red');
      return;
    }

    // Validate customer name
    if (!customerName) {
      setMessage('Customer name is required.');
      setMessageColor('red');
      return;
    }

    // Validate passwords
    if (!password || !repeatPassword) {
      setMessage('Both password fields are required.');
      setMessageColor('red');
      return;
    }

    if (password !== repeatPassword || password.length < 6 || password.length > 10) {
      setMessage('Passwords must match and be between 6 and 10 characters.');
      setMessageColor('red');
      return;
    }

    // Success message
    setMessage(`Customer added successfully with Email: ${email}, Name: ${customerName}`);
    setMessageColor('green');

    // Clear form fields
    setEmail('');
    setCustomerName('');
    setPassword('');
    setRepeatPassword('');
  };

  return (
    <div className={styles.footer}>
      <h1 className={styles.title}>Add a New Customer!</h1>
      <form className={styles.form} onSubmit={handleSubmit}>
        <h2>Email:</h2>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className={styles.input}
        />
        <br />
        <h2>Customer Name:</h2>
        <input
          type="text"
          placeholder="Customer Name"
          value={customerName}
          onChange={(e) => setCustomerName(e.target.value)}
          className={styles.input}
        />
        <br />
        <h2>Customer Password:</h2>
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className={styles.input}
        />
        <br />
        <h2>Repeat Password:</h2>
        <input
          type="password"
          placeholder="Repeat Password"
          value={repeatPassword}
          onChange={(e) => setRepeatPassword(e.target.value)}
          className={styles.input}
        />
        <br />
        <button type="submit" className={styles.button}>Add a Customer</button>
        <br></br><br></br>
        {message && <p style={{ color: messageColor }}>{message}</p>}
      </form>
    </div>
  );
};

export default AddCustomerForm;
