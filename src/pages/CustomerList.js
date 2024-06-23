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
    const router = useRouter();

    useEffect(() => {
        const userLoggedIn = localStorage.getItem('loggedInUserEmail');
        if (!userLoggedIn) {
            router.push('/login');
        } else {
            fetchCustomers();
        }
    }, []);

    const fetchCustomers = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:5000/get_customers');
            setCustomers(response.data);
            setFilteredCustomers(response.data);
        } catch (error) {
            console.error('Error fetching customers:', error);
            setMessage('Error fetching customers. Please try again.');
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
            {message && <p style={{ color: 'red' }}>{message}</p>}
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
        </div>
    );
};

export default CustomerList;
