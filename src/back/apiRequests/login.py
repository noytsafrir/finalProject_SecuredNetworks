import mysql.connector
from flask import Blueprint, request, jsonify
from models import User
from config import Config
from myfunc import *

login_bp = Blueprint('login_bp', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = None
    if safe_mode:
        user = User.query.filter_by(email=email).first()
    else:
        try:
            # Database connection setup
            unsecuredConnection, unsecuredCursor = set_unsecured_connection()
            # Constructing a single query that includes a potential SQL injection
            query = f"SELECT * FROM users WHERE email = '{email}'"
            print(query)    # Debugging statement
            # Executing the query with multi=True to allow multiple statements
            for result in unsecuredCursor.execute(query, multi=True):
                if result.with_rows:
                    res = result.fetchone()
                    if res:
                        user = User(email=res[0], password_hash=res[1], login_attempts=res[2])
            close_unsecured_connection(unsecuredCursor, unsecuredConnection)
        except mysql.connector.ProgrammingError as e:
            print(f"Error: {e}")
            return jsonify({'message': 'SQL error', 'status': 500})
    
    if not user:
        return jsonify({'message': 'User not found.', 'status': 401})
    if user.login_attempts < Config.LOGIN_ATTEMPTS_LIMIT: 
        if user.check_password(password):
            user.reset_login_attempts()
            return jsonify({'message': 'Login successful!', 'status': 200, 'user_email': user.email})
        else:
            user.increment_login_attempts()
            return jsonify({'message': 'Invalid password.', 'status': 401})
    else:
        return jsonify({'message': 'Account locked.', 'status': 401})