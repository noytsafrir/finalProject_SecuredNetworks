import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import styles from "@/styles/RequestForm.module.css";
import axios from 'axios';

const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [messageColor, setMessageColor] = useState('');
  const [showCodeInput, setShowCodeInput] = useState(false);
  const [code, setCode] = useState('');
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

  // const sendCode = async (email, code) => {
  //   try {
  //     const response = await fetch('/api/send-code', {
  //       method: 'POST',
  //       headers: {
  //         'Content-Type': 'application/json',
  //       },
  //       body: JSON.stringify({ email, code }),
  //     });

  //     const data = await response.json();
  //     if (data.success) {
  //       console.log('Reset code sent');
  //     } else {
  //       console.error('Failed to send reset code');
  //     }
  //   } catch (error) {
  //     console.error('An error occurred while sending the reset code', error);
  //   }
  // };

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

    axios.post('http://127.0.0.1:5000/forgot_password', { email })
    .then(respone => {
      const { message, status } = response.data;
      console.log("message is: " + message);
      console.log("status is: " + status);
      setMessage(message);
      setMessageColor(status === 200 ? 'green' : 'red');
      if (status === 200) {
          // Optionally clear form fields on successful request
          setEmail('');
          setTimeout(() => {
              setMessage('');
              setMessageColor('');
          }, 5000);
      }
  })
  .catch(error => {
    if (error.response) {
        // The request was made and the server responded with a status code
        const { data, status } = error.response;
        setMessage(data.message || 'Request failed. Please try again.');
        setMessageColor(status === 200 || status === 201 ? 'green' : 'red');
        setTimeout(() => {
            setMessage('');
            setMessageColor('');
        }, 5000);
    } else if (error.request) {
        // The request was made but no response was received
        setMessage('No response received from the server. Please try again later.');
        setMessageColor('red');
        setTimeout(() => {
            setMessage('');
            setMessageColor('');
        }, 5000);
    } else {
        // Something happened in setting up the request that triggered an Error
        // setMessage('An unexpected error occurred. Please try again.');
        // setMessageColor('red');
        setTimeout(() => {
            setMessage('');
            setMessageColor('');
        }, 5000);
    }
  });
    // await sendCode(email);
    setMessage(`A message to reset your password was sent to: ${email}`);
    setMessageColor('green');
    setShowCodeInput(true);
    setTimeRemaining(300); // Reset timer to 5 minutes
  };

  const handleCodeSubmit = async () => {
    try {
      const response = await fetch('http://localhost:5000/verify_reset_code', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, code }),
      });

      const data = await response.json();
      if (data.status === 200) {
        localStorage.setItem('forgotUserEmail', email);
        router.push('/ResetPassword');
      } else {
        setMessage('Invalid code or time expired. Please try again.');
        setMessageColor('red');
      }
    } catch (error) {
      console.error('An error occurred while verifying the code', error);
      setMessage('An error occurred. Please try again.');
      setMessageColor('red');
    }
  };

  const handleResendCode = async () => {
    await sendCode(email);
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
