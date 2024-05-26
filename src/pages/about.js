import Navbar from "../comps/Navbar";
import { Inter } from "next/font/google";
import styles from "@/styles/RequestForm.module.css";

const inter = Inter({ subsets: ["latin"] });

export default function About() {
    return (
      <div className={styles.footer}>
        <h1>Welcome to Final project secured networks!</h1>
        <br></br><br></br>
        <h3>Yarden Krispel</h3>
        <br></br><br></br>
        <h3>Ben Shervi</h3>
        <br></br><br></br>
        <h3>Noy Tsafrir</h3>
        <br></br><br></br>
        <h3>Shir Falach</h3>
        <br></br><br></br>
        <h3>Saar Gamzo</h3>
            
     </div>
    );
}
