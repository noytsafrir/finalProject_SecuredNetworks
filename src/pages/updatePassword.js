import React, { useState, useEffect } from 'react';
<<<<<<< HEAD
=======
import axios from 'axios';
>>>>>>> main
import styles from "@/styles/RequestForm.module.css";

const UpdatePassword = () => {
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [repeatNewPassword, setRepeatNewPassword] = useState('');
  const [message, setMessage] = useState('');
  const [messageColor, setMessageColor] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
<<<<<<< HEAD
=======
  const [userEmail, setUserEmail] = useState('');
>>>>>>> main

  useEffect(() => {
    const checkLoggedInStatus = () => {
      const loggedInUserEmail = localStorage.getItem('loggedInUserEmail');
      setIsLoggedIn(!!loggedInUserEmail); // !! converts to boolean
<<<<<<< HEAD
=======
      if (loggedInUserEmail) {
        setUserEmail(loggedInUserEmail);
      }
>>>>>>> main
    };

    if (typeof window !== 'undefined') {
      // Check if the window object is defined (i.e., running on the client side)
      checkLoggedInStatus();
    }
  }, []);
<<<<<<< HEAD

  const handleUpdatePassword = () => {
    if (!isLoggedIn) {
      setMessage('Please log in to update your password.');
      setMessageColor('red');
      return;
    }

=======

  const handleUpdatePassword = async () => {
    if (!isLoggedIn) {
      setMessage('Please log in to update your password.');
      setMessageColor('red');
      return;
    }

>>>>>>> main
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

    let response='';
    try {
      response = await axios.post('http://127.0.0.1:5000/update_password', {
        email: userEmail,
        old_password: oldPassword,
        new_password: newPassword
      });

      if (response.data.status === 200) {
        setMessage('Password updated successfully.');
        setMessageColor('green');

        // Clear form fields
        setOldPassword('');
        setNewPassword('');
        setRepeatNewPassword('');
      } else {
        setMessage(response.data.message);
        setMessageColor('red');
      }
    } catch (error) {
      setMessage(response.data.message);
      setMessageColor('red');    }
  };

  return (
    <div className={styles.footer}>
      {isLoggedIn ? (
        <div>
          <div className={styles.inputContainer}>
<<<<<<< HEAD
          <h1>Update Password</h1>
          <br></br>
=======
            <h1>Update Password</h1>
            <br />
>>>>>>> main
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