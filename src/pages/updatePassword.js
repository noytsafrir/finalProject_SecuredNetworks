import React, { useState, useEffect } from 'react';
import styles from "@/styles/RequestForm.module.css";
import axios from 'axios';

const UpdatePassword = () => {
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [repeatNewPassword, setRepeatNewPassword] = useState('');
  const [message, setMessage] = useState('');
  const [messageColor, setMessageColor] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const checkLoggedInStatus = () => {
      const loggedInUserEmail = localStorage.getItem('loggedInUserEmail');
      setIsLoggedIn(!!loggedInUserEmail); // !! converts to boolean
    };

    if (typeof window !== 'undefined') {
      checkLoggedInStatus();
    }
  }, []);

  const handleUpdatePassword = async () => {
    if (!isLoggedIn) {
      setMessage('Please log in to update your password.');
      setMessageColor('red');
      return;
    }

    if (!oldPassword || !newPassword || !repeatNewPassword) {
      setMessage('All fields are required.');
      setMessageColor('red');
      return;
    }

    if (newPassword !== repeatNewPassword) {
      setMessage('New passwords do not match.');
      setMessageColor('red');
      return;
    }

    axios.post('http://127.0.0.1:5000/update_password', { oldPassword, newPassword })
    .then(response => {
      const { message, status } = response.data;
      setMessage(message);
      setMessageColor(status === 200 ? 'green' : 'red');
      if (status === 200) {
        setOldPassword('');
        setNewPassword('');
        setRepeatNewPassword('');
      }
    })
    
    
    
    // const email = localStorage.getItem('loggedInUserEmail');

    // try {
    //   const response = await fetch('http://localhost:5000/update_password', {
    //     method: 'POST',
    //     headers: {
    //       'Content-Type': 'application/json',
    //     },
    //     body: JSON.stringify({ email, oldPassword, newPassword }),
    //   });

    //   const data = await response.json();

    //   if (data.status === 200) {
    //     setMessage('Password updated successfully.');
    //     setMessageColor('green');

    //     // Clear form fields
    //     setOldPassword('');
    //     setNewPassword('');
    //     setRepeatNewPassword('');
    //   } else {
    //     setMessage(data.message);
    //     setMessageColor('red');
    //   }
    // } catch (error) {
    //   console.error('An error occurred while updating the password', error);
    //   setMessage('An error occurred. Please try again.');
    //   setMessageColor('red');
    // }
  };

  return (
    <div className={styles.footer}>
      {isLoggedIn ? (
        <div>
          <div className={styles.inputContainer}>
            <h1>Update Password</h1>
            <br></br>
            <h3>Old Password</h3>
            <input
              type="password"
              id="oldPassword"
              placeholder="Enter your old password"
              value={oldPassword}
              onChange={(e) => setOldPassword(e.target.value)}
              className={styles.input}
            />
          </div>
          <div className={styles.inputContainer}>
            <h3>New Password</h3>
            <input
              type="password"
              id="newPassword"
              placeholder="Enter your new password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              className={styles.input}
            />
          </div>
          <br />
          <div className={styles.inputContainer}>
            <h3>Repeat New Password</h3>
            <input
              type="password"
              id="repeatNewPassword"
              placeholder="Repeat your new password"
              value={repeatNewPassword}
              onChange={(e) => setRepeatNewPassword(e.target.value)}
              className={styles.input}
            />
          </div>

          <div className={`${styles['button-container']}`} style={{ marginLeft: '400px' }}>
            <button
              type="button"
              className={styles.button}
              onClick={handleUpdatePassword}
            >
              Update Password
            </button>
          </div>
          {message && <p style={{ color: messageColor, textAlign: 'center' }}>{message}</p>}
        </div>
      ) : (
        <h1 className={styles.title}>Please log in to update the password.</h1>
      )}
    </div>
  );
};

export default UpdatePassword;