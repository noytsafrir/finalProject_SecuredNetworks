import Navbar from "../comps/Navbar";
import { Inter } from "next/font/google";
import styles from "@/styles/RequestForm.module.css";

export default function Home() {
  return (
    <div className={styles.footer}>
      <h1>Welcome to final secured networks home page peroject!</h1>
      <br></br>
      <h3>Please login to see your options!</h3>
    </div>
  );
}
