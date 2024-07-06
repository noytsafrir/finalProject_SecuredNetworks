import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import styles from "@/styles/RequestForm.module.css";
import axios from 'axios';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const [messageColor, setMessageColor] = useState('');
    const [isLoggedIn, setIsLoggedIn] = useState(false); // State to track login status
    const router = useRouter();

    useEffect(() => {
        // Check if user is already logged in
        const userLoggedIn = localStorage.getItem('loggedInUserEmail'); // Check if user email is stored
        setIsLoggedIn(!!userLoggedIn); // Set isLoggedIn based on stored email
    }, []);

    const handleLogin = () => {
        if (!email || !password) {
            setMessage('Both email and password are required.');
            setMessageColor('red');
            setTimeout(() => {
                setMessage('');
                setMessageColor('');
            }, 5000);
            return;
        }

        if (process.env.SAFE_MODE) {
            const emailPattern = /^[^\s@]+@[^\s@]+\.(com|org)$/;
            if (!emailPattern.test(email)) {
                setMessage('Invalid email format. Please use a valid email ending with .com or .org.');
                setMessageColor('red');
                setTimeout(() => {
                    setMessage('');
                    setMessageColor('');
                }, 5000);
                return;
            }
        }

        axios.post('http://localhost:5000/login', { email, password })
        .then(response => {
            const { message, status, user_email } = response.data;
            setMessage(message);
            setMessageColor(status === 200 ? 'green' : 'red');
            if (status === 200) {
                // Navigate to the next page upon successful login
                localStorage.setItem('loggedInUserEmail', user_email);
                setIsLoggedIn(true);
                router.push('/about');
            }
            setTimeout(() => {
                setMessage('');
                setMessageColor('');
            }, 5000);
        })
        .catch(error => {
            if (error.response) {
                // The request was made and the server responded with a status code
                // that falls out of the range of 2xx
                const { message, status } = error.response.data;
                setMessage(message || 'An error occurred.');
                setMessageColor(status === 'success' ? 'green' : 'red');
            } else if (error.request) {
                // The request was made but no response was received
                setMessage('No response received from the server. Please try again.');
                setMessageColor('red');
            } else {
                // Something happened in setting up the request that triggered an Error
                setMessage('Login failed. Please try again.');
                setMessageColor('red');
            }
            setTimeout(() => {
                setMessage('');
                setMessageColor('');
            }, 5000);
        });
    };

    const handleLogout = () => {
      // Clear user email from localStorage upon logout
      localStorage.removeItem('loggedInUserEmail');
      setIsLoggedIn(false);
  };

  return (
    <div className={styles.footer}>
        <div className={styles.loginContainer}>
            {isLoggedIn ? (
                <>
                    <h1>You are already logged in!</h1>
                    <br></br>
                    <h3>Email: {localStorage.getItem('loggedInUserEmail')}</h3>
                    <br />
                    <div className={`${styles['button-container']}`} style={{ marginLeft: '550px' }}>
                        <button
                            type="button"
                            className={styles.button}
                            onClick={handleLogout}
                        >
                            Logout
                        </button>
                    </div>
                </>
            ) : (
                <>
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
                </>
            )}
        </div>
    </div>
);
};

export default Login;