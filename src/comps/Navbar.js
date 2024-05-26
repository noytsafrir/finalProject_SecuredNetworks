import styles from "@/styles/Navbar.module.css"

// Navbar.js

const Navbar = () => {
  return (
    <ul className={styles.navbar}>
      <li><a href="login">Login</a></li>
      <li><a href="register">Register</a></li>
      <li><a href="addCustomerForm">Add a customer!</a></li>
      <li><a href="updatePassword">Update password</a></li>
      <li><a href="about">About</a></li>
    </ul>
  );
};
export default Navbar;

