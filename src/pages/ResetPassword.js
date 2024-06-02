// pages/ResetPassword.js
import React, { useState } from 'react';
import { useRouter } from 'next/router';
import styles from "@/styles/RequestForm.module.css";

const ResetPassword = () => {
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');
  const [messageColor, setMessageColor] = useState('');
  const router = useRouter();

  const handleResetPassword = () => {
    if (newPassword.length < 8) {
      setMessage('Password should be at least 8 characters long.');
      setMessageColor('red');
      return;
    }
    if (newPassword !== confirmPassword) {
      setMessage('Passwords do not match. Please try again.');
      setMessageColor('red');
      return;
    }
    
    // If passwords match and meet the length criteria, navigate to login page
    setMessage('Password reset successful. Redirecting to login...');
    setMessageColor('green');
    setTimeout(() => {
      router.push('/login');
    }, 2000);
  };

  return (
    <div className={styles.footer}>
      <div className={styles.loginContainer}>
        <h2 className={styles.center}>Reset Your Password</h2>
        <br />
        <input
          type="password"
          placeholder="Enter new password..."
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          className={styles.input}
        />
        <input
          type="password"
          placeholder="Confirm new password..."
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          className={styles.input}
        />
        <br />
        <div className={`${styles['button-container']}`} style={{ marginLeft: '550px' }}>
          <button
            type="button"
            className={styles.button}
            onClick={handleResetPassword}
          >
            Reset Password
          </button>
        </div>
        <br />
        {message && <p style={{ color: messageColor }}>{message}</p>}
      </div>
    </div>
  );
};

export default ResetPassword;
