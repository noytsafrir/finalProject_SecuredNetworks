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

7. **Screens**:
   ![login](https://github.com/user-attachments/assets/230992ff-0c25-422d-9940-69c993b730d3)
   ![register](https://github.com/user-attachments/assets/222ee516-f445-470f-947c-ba6530625db3)
   ![forgotPassword](https://github.com/user-attachments/assets/b3a39365-c680-4492-b64b-72f9941ee7b6)
   ![resetPassword](https://github.com/user-attachments/assets/63399c0b-2aad-461d-bcd4-554bfb17cb41)
   ![addCustomer](https://github.com/user-attachments/assets/d727e61d-e17d-476a-9d76-2ae65f45bf3f)
   ![customerView](https://github.com/user-attachments/assets/c14be13e-a3d3-44dd-ab87-00b5f0645aac)
   ![updatePassword](https://github.com/user-attachments/assets/e0e3d1ea-a04f-4467-83f0-37fa8d3131fd)




