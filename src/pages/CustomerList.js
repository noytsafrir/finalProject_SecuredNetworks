import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';
import styles from "@/styles/CustomerList.module.css";

const CustomerList = () => {
    const [customers, setCustomers] = useState([]);
    const [searchField, setSearchField] = useState('customer_name');
    const [searchType, setSearchType] = useState('contains');
    const [searchInput, setSearchInput] = useState(''); // State for the input field
    const [searchData, setSearchData] = useState(''); // State for the search data used in fetch
    const [message, setMessage] = useState('');
    const [messageColor, setMessageColor] = useState('');
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [userEmail, setUserEmail] = useState('');
    const router = useRouter();

    // Read SAFE_MODE from environment variable
    const safeModeEnv = process.env.NEXT_PUBLIC_SAFE_MODE === 'true';
    const [SAFE_MODE, setSafeMode] = useState(safeModeEnv);

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
        if (isLoggedIn) {
            fetchCustomers();
        }
    }, [isLoggedIn, searchData]); // Fetch customers when logged in or searchData changes

    const fetchCustomers = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:5000/get_customers', {
                params: {
                    searchField: searchField,
                    searchType: searchType,
                    searchData: searchData,
                },
            });
            setCustomers(response.data);
        } catch (error) {
            console.error('Error fetching customers:', error);
            setMessage('Error fetching customers. Please try again.');
            setMessageColor('red');
        }
    };

    const handleSearch = () => {
        if (SAFE_MODE) {
            const regex = /^[a-zA-Z0-9\s,.']+$/;
            if (!regex.test(searchInput)) {
                setMessage('Invalid characters in search data.');
                setMessageColor('red');
                return;
            }
        }
        setSearchData(searchInput); // Update the search data state
        fetchCustomers(); // Fetch customers based on the search data
    };

    const handleClear = () => {
        setSearchInput(''); // Clear the input field
        setSearchData(''); // Clear the search data state to fetch all customers
    };

    return (
        <div className={styles.container}>
            <h1 className={styles.title}>Customer View</h1>
            <br></br>
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
                            value={searchInput}
                            onChange={(e) => setSearchInput(e.target.value)}
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
                            {customers.map((customer, index) => (
                                <tr key={index}>
                                    <td className={styles.tableContent}>{customer.customer_name}</td>
                                    <td className={styles.tableContent}>{customer.company_name}</td>
                                    <td className={styles.tableContent}>{customer.address}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                    <br></br>
                    {message && <p style={{ color: messageColor }}>{message}</p>}
                    <br></br>
                    <br></br>
                    <div>
                        {SAFE_MODE ? (
                            <p style={{ color: "white" }}>{searchData}</p>
                        ) : (
                            <div style={{ color: "white" }} dangerouslySetInnerHTML={{ __html: searchData }} />
                        )}
                    </div>
                </>
            ) : (
                <h1 className={styles.title}>Please log in to view customers.</h1>
            )}
        </div>
    );
};

export default CustomerList;
