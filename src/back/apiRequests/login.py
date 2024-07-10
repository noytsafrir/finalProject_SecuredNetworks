from flask import request, jsonify
from flask_login import login_user
from ..models import User

def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found.', 'status': 401})

    if user.check_password(password):
        # login_user(user)
        return jsonify({'message': 'Login successful!', 'status': 200})
    else:
        return jsonify({'message': 'Invalid password.', 'status': 401})
    