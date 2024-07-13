1. **Prerequisites**:
    - **Node.js**: https://nodejs.org/en/download/package-manager
    - **Python**: https://www.python.org/downloads/
    - **MySQLServer**: https://dev.mysql.com/downloads/mysql/
  
2. **RUN MySQL Server**:
    - **Download project zip & extract all code**
    - **On visual studio code - click file -> open folder -> select root directory of the project**
    - **Open cmd on windows - run the commands**:
      - ```mysql -u root -p```
      - Insert your root password
      - ```CREATE DATABASE store;```

3. **Install needed dependencies**:
    - On new terminal run the following commands:
      - ``` npm install``` - to install every nodejs dependency
      - ``` pip install -r requirements.txt``` - to install every python dependency

4. **Update MySql password if needed**:
    - Open file src/back/config.py and replace ```A123456``` with your root password on MySQL.

5. **SETTING .env variables as wanted**:
    - **GMAIL_USER & GMAIL_PASS** are needed in order to send OTP messages on email
    - **SAFE_MODE (true/false)** - true = safe from sqli attacks, false = not safe from sqli attacks
    - **NEXT_PUBLIC_SAFE_MODE (true/false)** - true = safe from xss stored attacks, false = not safe from xss stored attacks 

6. **Running the project**:
    - Split the terminal to 2 terminals
    - On the first terminal - run the command: ```python src/back/main.py``` and verify the server is running as expected
    - On the second terminal - run the command: ```npm run dev``` and verify the frontend is running as expected
    - Press ctrl + click on the URL: ```http://localhost:3000```

7. **XSS stored attack demonstartion**:
    - Navigate to .env and verify **NEXT_PUBLIC_SAFE_MODE=false**
    - Log in to an existing user
    - Navigate to add new customer page
    - Insert as a new customer name: ```<img src=x onerror='alert("HACKED!")'>```
    - Insert other needed inputs and click submit
