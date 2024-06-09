import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import styles from "@/styles/RequestForm.module.css";

const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [messageColor, setMessageColor] = useState('');
  const [showCodeInput, setShowCodeInput] = useState(false);
  const [code, setCode] = useState('');
  const [generatedCode, setGeneratedCode] = useState('');
  const [timeRemaining, setTimeRemaining] = useState(300); // 5 minutes in seconds
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

  const sendCode = async (email, code) => {
    try {
      const response = await fetch('/api/send-code', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, code }),
      });

      const data = await response.json();
      if (data.success) {
        console.log('Email sent');
      } else {
        console.error('Failed to send email');
      }
    } catch (error) {
      console.error('An error occurred while sending the email', error);
    }
  };

  const handleForgotPassword = async () => {
    if (!email) {
      setMessage('Email is required to reset your password.');
      setMessageColor('red');
      return;
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.(com|org)$/;
    if (!emailPattern.test(email)) {
      setMessage('Invalid email format. Please use a valid email ending with .com or .org.');
      setMessageColor('red');
      return;
    }

    const generatedCode = Math.random().toString(36).substring(2, 10); // Generate an 8-character random string
    setGeneratedCode(generatedCode);

    // Send the code via email
    await sendCode(email, generatedCode);
    console.log("The code is: " + generatedCode);
    setMessage(`A message to reset your password was sent to: ${email}`);
    setMessageColor('green');
    setShowCodeInput(true);
    setTimeRemaining(300); // Reset timer to 5 minutes
  };

  const handleCodeSubmit = () => {
    if (code === generatedCode && timeRemaining > 0) {
      router.push('/ResetPassword');
    } else {
      setMessage('Invalid code or time expired. Please try again.');
      setMessageColor('red');
    }
  };

  const handleResendCode = async () => {
    const newGeneratedCode = Math.random().toString(36).substring(2, 10); // Generate a new 8-character random string
    setGeneratedCode(newGeneratedCode);

    // Send the new code via email
    await sendCode(email, newGeneratedCode);

    setMessage(`A new code was sent to: ${email}`);
    setMessageColor('green');
    setTimeRemaining(300); // Reset timer to 5 minutes
  };

  const formatTime = (time) => {
    const minutes = Math.floor(time / 60);
    const seconds = time % 60;
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  };

  return (
    <div className={styles.footer}>
      <div className={styles.loginContainer}>
        <h2 className={styles.center}>Forgot Password</h2>
        <br />
        <input
          type="email"
          placeholder="Enter your email..."
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className={styles.input}
        />
        <br />
        <div className={`${styles['button-container']}`} style={{ marginLeft: '550px' }}>
          <button
            type="button"
            className={styles.button}
            onClick={handleForgotPassword}
          >
            Submit
          </button>
        </div>
        <br />
        {message && <p style={{ color: messageColor }}>{message}</p>}
        {showCodeInput && (
          <div>
            <br />
            <h3>Please enter the code sent to your email:</h3>
            <input
              type="text"
              placeholder="Enter code..."
              value={code}
              onChange={(e) => setCode(e.target.value)}
              className={styles.input}
            />
            <br />
            <div className={`${styles['button-container']}`} style={{ marginLeft: '550px' }}>
              <button
                type="button"
                className={styles.button}
                onClick={handleCodeSubmit}
                disabled={timeRemaining === 0}
                style={{ backgroundColor: timeRemaining === 0 ? 'grey' : '' }}
              >
                Submit Code
              </button>
              <button
                type="button"
                className={styles.button}
                onClick={handleResendCode}
                disabled={timeRemaining > 0}
                style={{ backgroundColor: timeRemaining > 0 ? 'grey' : '' }}
              >
                Resend Code
              </button>
            </div>
            <br />
            <p style={{ color: 'green' }}>
              Time remaining to use OTP: {formatTime(timeRemaining)}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ForgotPassword;
