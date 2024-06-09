from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# A simple dictionary to act as a mock database for users
mock_users_db = {
    'user@example.com': 'password123',
    'admin@example.com': 'adminpass'
}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    print(f"Login attempt with email: {email}, password: {password}")

    if not email or not password:
        print("Both email and password are required.")
        return jsonify({'message': 'Both email and password are required.', 'status': 'fail'}), 400

    if email in mock_users_db and mock_users_db[email] == password:
        print("Login successful!")
        return jsonify({'message': 'Login successful!', 'status': 'success'}), 200
    else:
        print("Invalid email or password.")
        return jsonify({'message': 'Invalid email or password.', 'status': 'fail'}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    repeat_password = data.get('repeat_password')

    print(f"Register attempt with email: {email}, password: {password}, repeat_password: {repeat_password}")

    if not email or not password or not repeat_password:
        print("All fields are required.")
        return jsonify({'message': 'All fields are required.', 'status': 'fail'}), 400

    email_pattern = r'^[^\s@]+@[^\s@]+\.(com|org)$'
    if not re.match(email_pattern, email):
        print("Invalid email format.")
        return jsonify({'message': 'Invalid email format. Please use a valid email ending with .com or .org.', 'status': 'fail'}), 400

    if password != repeat_password:
        print("Passwords do not match.")
        return jsonify({'message': 'Passwords do not match.', 'status': 'fail'}), 400

    if email in mock_users_db:
        print("Email already registered.")
        return jsonify({'message': 'Email already registered.', 'status': 'fail'}), 400

    # Add the new user to the mock database
    mock_users_db[email] = password
    print("Registration successful!")
    return jsonify({'message': 'Registration successful!', 'status': 'success'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)