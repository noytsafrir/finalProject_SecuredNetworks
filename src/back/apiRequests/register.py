import mysql.connector
from flask import Blueprint, request, jsonify
from models import db, User, PasswordHistory
from myfunc import *

register_bp = Blueprint('register_bp', __name__)

@register_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    # safe mode
    if safe_mode:
        if check_user(email):
            return jsonify({'message': 'User already exists', 'status' : 400})
    # unsafe mode
    else:  
        try:
            existing_user = False
            # Database connection setup
            unsecuredConnection, unsecuredCursor = set_unsecured_connection()
            # Constructing a single query that includes a potential SQL injection
            query = f"SELECT * FROM users WHERE email = '{email}';"
            # Executing the query with multi=True to allow multiple statements
            for result in unsecuredCursor.execute(query, multi=True):
                if result.with_rows:
                    res = result.fetchall()
                    if res:
                        existing_user = True
            close_unsecured_connection(unsecuredCursor, unsecuredConnection)
            if existing_user:
                return jsonify({'message': 'User already exists', 'status': 400})
        except mysql.connector.ProgrammingError as e:
            print(f"Error: {e}")
            return jsonify({'message': 'SQL error', 'status': 500})

    # safe mode    
    if not password_configuration(email,password):
        return jsonify({'message': 'Password must be at least 10 characters long and include uppercase, lowercase, digits, and special characters, cant be a dictionary word', 'status': 400})

    new_user = User(email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    new_password_history = PasswordHistory(email=email, password_hash=new_user.password_hash)
    db.session.add(new_password_history)
    db.session.commit()
    return jsonify({'message': 'User registered successfully', 'status': 200})