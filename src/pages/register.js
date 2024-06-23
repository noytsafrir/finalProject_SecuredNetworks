import React, { useState, useEffect } from 'react';
import styles from "@/styles/RequestForm.module.css";
import axios from 'axios';

const Register = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [repeatPassword, setRepeatPassword] = useState('');
    const [message, setMessage] = useState('');
    const [messageColor, setMessageColor] = useState('');
    const [isLoggedIn, setIsLoggedIn] = useState(false); // State to track login status

    useEffect(() => {
        // Check if user is already logged in
        const userLoggedIn = localStorage.getItem('loggedInUserEmail'); // Check if user email is stored
        setIsLoggedIn(!!userLoggedIn); // Set isLoggedIn based on stored email
    }, []);

    const handleRegister = () => {
        if (!email || !password || !repeatPassword) {
            setMessage('All fields are required.');
            setMessageColor('red');
            setTimeout(() => {
                setMessage('');
                setMessageColor('');
            }, 5000);
            return;
        }

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

        if (password !== repeatPassword) {
            setMessage('Passwords do not match.');
            setMessageColor('red');
            setTimeout(() => {
                setMessage('');
                setMessageColor('');
            }, 5000);
            return;
        }

        axios.post('http://127.0.0.1:5000/register', { email, password, repeat_password: repeatPassword })
        .then(response => {
            const { message, status } = response.data;
            console.log("message is: " + message);
            console.log("status is: " + status);
            setMessage(message);
            setMessageColor(status === 200 ? 'green' : 'red');
            if (status === 200) {
                // Clear form fields on successful registration
                setEmail('');
                setPassword('');
                setRepeatPassword('');
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
                setMessage(data.message || 'Registration failed. Please try again.');
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
                setMessage('An unexpected error occurred. Please try again.');
                setMessageColor('red');
                setTimeout(() => {
                    setMessage('');
                    setMessageColor('');
                }, 5000);
            }
        });
    };

    const handleLogout = () => {
        // Clear user email from localStorage upon logout
        localStorage.removeItem('loggedInUserEmail');
        setIsLoggedIn(false);
    };

    return (
        <div className={styles.footer}>
            {isLoggedIn ? (
                <div>
                    <h1>You are already logged in!</h1>
                    <br />
                    <h3>Email: {localStorage.getItem('loggedInUserEmail')}</h3>
                    <div className={`${styles['button-container']}`} style={{ marginLeft: '550px' }}>
                        <button
                            type="button"
                            className={styles.button}
                            onClick={handleLogout}
                        >
                            Logout
                        </button>
                    </div>
                </div>
            ) : (
                <div>
                    <h1>Users Registration</h1>
                    <br />
                    <div>
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
            )}
        </div>
    );
};

export default Register;
