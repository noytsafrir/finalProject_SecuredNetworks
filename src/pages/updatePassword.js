import React, { useState } from 'react';
import styles from "@/styles/RequestForm.module.css";

const UpdatePassword = () => {
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [repeatNewPassword, setRepeatNewPassword] = useState('');
  const [message, setMessage] = useState('');
  const [messageColor, setMessageColor] = useState('');

  const handleUpdatePassword = () => {
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

    setMessage(`Password updated successfully.`);
    setMessageColor('green');

    // Clear form fields
    setOldPassword('');
    setNewPassword('');
    setRepeatNewPassword('');
  };

  return (
    <div className={styles.footer}>
      <h1>Update Password</h1>
      <br></br>
      <div>
        <div className={styles.inputContainer}>
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
    </div>
  );
};

export default UpdatePassword;
