import React, { useState, useEffect } from 'react';
import styles from "@/styles/RequestForm.module.css";
import axios from 'axios';
import { useRouter } from 'next/router';

const AddCustomerForm = () => {
  const [customerName, setCustomerName] = useState('');
  const [companyName, setCompanyName] = useState('');
  const [customerAddress, setCustomerAddress] = useState('');
  const [message, setMessage] = useState('');
  const [messageColor, setMessageColor] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [newCustomerName, setNewCustomerName] = useState('');
  // Read SAFE_MODE from environment variable
  const safeModeEnv = process.env.NEXT_PUBLIC_SAFE_MODE === 'true';
  const [SAFE_MODE, setSafeMode] = useState(safeModeEnv);


  useEffect(() => {
    const loggedInUserEmail = localStorage.getItem('loggedInUserEmail');
    setIsLoggedIn(!!loggedInUserEmail); // !! converts to boolean
  }, []);

  useEffect(() => {
    let timer;
    if (message) {
      timer = setTimeout(() => {
        setMessage('');
        setMessageColor('');
      }, 5000);
    }
    return () => clearTimeout(timer);
  }, [message]);

  useEffect(() => {
    let timer;
    if (newCustomerName) {
      timer = setTimeout(() => {
        setNewCustomerName('');
      }, 5000);
    }
    return () => clearTimeout(timer);
  }, [newCustomerName]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!isLoggedIn) {
      setMessage('Please log in to add a customer.');
      setMessageColor('red');
      return;
    }

    if (!validateInputs()) return;

    try {
      const response = await axios.post('http://127.0.0.1:5000/add_customer', {
        customer_name: customerName,
        company_name: companyName,
        address: customerAddress
      });
      const { message, status } = response.data;
      setMessage(message);
      setMessageColor(status === 200 ? 'green' : 'red');
      if (status === 200) {
        setNewCustomerName(customerName);
        setCustomerName('');
        setCompanyName('');
        setCustomerAddress('');
      }
    } catch (error) {
      console.error('Error adding customer:', error);
      setMessage('An error occurred. Please try again.');
      setMessageColor('red');
    }
  };

  const validateInputs = () => {
    if (!customerName || !companyName || !customerAddress) {
      setMessage('All fields are required.');
      setMessageColor('red');
      return false;
    }

    if (customerName.length < 5 || companyName.length < 5 || customerAddress.length < 5) {
      setMessage('All fields must be at least 5 characters long.');
      setMessageColor('red');
      return false;
    }

    if (SAFE_MODE) {
      // Basic SQL injection prevention
      const regex = /^[a-zA-Z0-9\s,.']+$/;
      if (!regex.test(customerName) || !regex.test(companyName) || !regex.test(customerAddress)) {
        setMessage('Invalid characters in input fields.');
        setMessageColor('red');
        return false;
      }
    }
    return true;
  };

  return (
    <div className={styles.footer}>
      {isLoggedIn ? (
        <>
          <h1 className={styles.title}>Add a New Customer!</h1>
          <form className={styles.form} onSubmit={handleSubmit}>
            <h2>Customer Name:</h2>
            <input
              type="text"
              placeholder="Customer Name"
              value={customerName}
              onChange={(e) => setCustomerName(e.target.value)}
              className={styles.input}
            />
            <br />
            <h2>Company Name:</h2>
            <input
              type="text"
              placeholder="Company Name"
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
              className={styles.input}
            />
            <br />
            <h2>Customer Address:</h2>
            <input
              type="text"
              placeholder="Customer Address"
              value={customerAddress}
              onChange={(e) => setCustomerAddress(e.target.value)}
              className={styles.input}
            />
            <br />
            <button type="submit" className={styles.button}>Add a Customer</button>
            <br /><br />
            {message && <p style={{ color: messageColor }}>{message}</p>}
            {newCustomerName && (
              SAFE_MODE ? (
                <p style={{ color: "green"}}>{newCustomerName}</p>
              ) : (
                <div dangerouslySetInnerHTML={{ __html: newCustomerName }} />
              )
            )}
          </form>
        </>
      ) : (
        <h1 className={styles.title}>Please log in to add a customer.</h1>
      )}
    </div>
  );
};

export default AddCustomerForm;
