import React, { useState } from 'react';
import styles from "@/styles/RequestForm.module.css";

const AddCustomerForm = () => {
  const [customerName, setCustomerName] = useState('');
  const [companyName, setCompanyName] = useState('');
  const [customerAddress, setCustomerAddress] = useState('');
  const [message, setMessage] = useState('');
  const [messageColor, setMessageColor] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    // Validate customer name
    if (!customerName) {
      setMessage('Customer name is required.');
      setMessageColor('red');
      return;
    }

    // Validate company name
    if (!companyName) {
      setMessage('Company name is required.');
      setMessageColor('red');
      return;
    }

    // Validate customer address
    if (!customerAddress) {
      setMessage('Customer address is required.');
      setMessageColor('red');
      return;
    }

    // Success message
    setMessage(`Customer added successfully with Name: ${customerName}, Company: ${companyName}, Address: ${customerAddress}`);
    setMessageColor('green');

    // Clear form fields
    setCustomerName('');
    setCompanyName('');
    setCustomerAddress('');
  };

  return (
    <div className={styles.footer}>
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
        <br></br><br></br>
        {message && <p style={{ color: messageColor }}>{message}</p>}
      </form>
    </div>
  );
};

export default AddCustomerForm;
