import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';
import styles from "@/styles/CustomerList.module.css";

const CustomerList = () => {
    const [customers, setCustomers] = useState([]);
    const [filteredCustomers, setFilteredCustomers] = useState([]);
    const [searchField, setSearchField] = useState('customer_name');
    const [searchType, setSearchType] = useState('contains');
    const [searchData, setSearchData] = useState('');
    const [message, setMessage] = useState('');
    const [messageColor, setMessageColor] = useState('');
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [userEmail, setUserEmail] = useState('');
    const router = useRouter();

    useEffect(() => {
        const checkLoggedInStatus = () => {
            const loggedInUserEmail = localStorage.getItem('loggedInUserEmail');
            setIsLoggedIn(!!loggedInUserEmail); // !! converts to boolean
            if (loggedInUserEmail) {
                setUserEmail(loggedInUserEmail);
            }
        };

        if (typeof window !== 'undefined') {
            // Check if the window object is defined (i.e., running on the client side)
            checkLoggedInStatus();
        }
    }, []);

    useEffect(() => {
        if (!isLoggedIn) {
            // setMessage('Please log in to view customers.');
            // setMessageColor('red');
            return;
        } else {
            fetchCustomers();
        }
    }, [isLoggedIn]);

    const fetchCustomers = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:5000/get_customers');
            setCustomers(response.data);
            setFilteredCustomers(response.data);
        } catch (error) {
            console.error('Error fetching customers:', error);
            setMessage('Error fetching customers. Please try again.');
            setMessageColor('red');
        }
    };

    const handleSearch = () => {
        let filtered = customers;
        if (searchType === 'contains') {
            filtered = customers.filter(customer =>
                customer[searchField].includes(searchData)
            );
        } else if (searchType === 'equals') {
            filtered = customers.filter(customer =>
                customer[searchField] === searchData
            );
        }
        setFilteredCustomers(filtered);
    };

    const handleClear = () => {
        setSearchData('');
        setFilteredCustomers(customers);
    };

    return (
        <div className={styles.container}>
            <h1 className={styles.title}>Customer View</h1>
            <br></br>
            {message && <p style={{ color: messageColor }}>{message}</p>}
            {isLoggedIn ? (
                <>
                    <div className={styles.searchContainer}>
                        <h2 className={styles.secondTitle}> Search by:</h2>
                        <select
                            value={searchField}
                            onChange={(e) => setSearchField(e.target.value)}
                            className={styles.searchInput}
                        >
                            <option value="customer_name">Customer Name</option>
                            <option value="company_name">Company Name</option>
                            <option value="address">Address</option>
                        </select>
                        <select
                            value={searchType}
                            onChange={(e) => setSearchType(e.target.value)}
                            className={styles.searchInput}
                        >
                            <option value="contains">Contains</option>
                            <option value="equals">Equals</option>
                        </select>
                        <input
                            type="text"
                            value={searchData}
                            onChange={(e) => setSearchData(e.target.value)}
                            placeholder="Enter search data"
                            className={styles.searchInput}
                        />
                        <button onClick={handleSearch} className={styles.searchButton}>Search</button>
                        <button onClick={handleClear} className={styles.searchButton}>Clear</button>
                    </div>
                    <table className={styles.table}>
                        <thead>
                            <tr>
                                <th className={styles.tableHeader}>Customer Name</th>
                                <th className={styles.tableHeader}>Company Name</th>
                                <th className={styles.tableHeader}>Address</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filteredCustomers.map((customer, index) => (
                                <tr key={index}>
                                    <td className={styles.tableContent}>{customer.customer_name}</td>
                                    <td className={styles.tableContent}>{customer.company_name}</td>
                                    <td className={styles.tableContent}>{customer.address}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </>
            ) : (
                <h1 className={styles.title}>Please log in to view customers.</h1>
            )}
        </div>
    );
};

export default CustomerList;
