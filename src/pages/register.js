import React, { useState } from 'react';
import styles from "@/styles/RequestForm.module.css";
import axios from 'axios';

const Register = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [repeatPassword, setRepeatPassword] = useState('');
    const [message, setMessage] = useState('');
    const [messageColor, setMessageColor] = useState('');

    const handleRegister = () => {
        if (!email || !password || !repeatPassword) {
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

        axios.post('http://127.0.0.1:5000/register', { email, password, repeat_password: repeatPassword })
        .then(response => {
            const { message, status } = response.data;
            setMessage(message);
            setMessageColor(status === 'success' ? 'green' : 'red');
            if (status === 'success') {
                // Clear form fields on successful registration
                setEmail('');
                setPassword('');
                setRepeatPassword('');
            }
        })
        .catch(error => {
            if (error.response) {
                // The request was made and the server responded with a status code
                const { data, status } = error.response;
                setMessage(data.message || 'Registration failed. Please try again.');
                setMessageColor(status === 200 || status === 201 ? 'green' : 'red');
            } else if (error.request) {
                // The request was made but no response was received
                setMessage('No response received from the server. Please try again later.');
                setMessageColor('red');
            } else {
                // Something happened in setting up the request that triggered an Error
                setMessage('An unexpected error occurred. Please try again.');
                setMessageColor('red');
            }
        });
    
    };

    return (
        <div className={styles.footer}>
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
    );
};

export default Register;
